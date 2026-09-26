"""Falsifiers 1-3 of hypothesis:log-cap-holds-while-a-long-lived-writer-keeps-the-log-open.

A long-lived O_APPEND writer (a `>>` redirect in the crontab) holds the base
open across a rotation. Under RENAME rotation its fd follows the renamed
inode, so every later byte lands in an ARCHIVE -- and an archive is never
capped again (crons.py `_ARCHIVE_RE`). These tests are the measurement, not a
proposal: they state what the CURRENT code does to such a writer.
"""
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import crons  # noqa: E402

import yaml  # noqa: E402

CAP_MB, KEEP = 1, 3
OVER = b"x" * (CAP_MB * 1024 * 1024 + 4096)  # a base strictly over the cap

# One append per 0.02s forever; the parent decides when it dies.
WRITER = """
import os, sys, time
log, journal, tag = sys.argv[1], sys.argv[2], sys.argv[3]
fd = os.open(log, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
jd = os.open(journal, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
line = (tag + "\\n").encode()
while True:
    os.write(fd, line)
    os.write(jd, line)          # the journal is what the process ACTUALLY wrote
    time.sleep(0.02)
"""


@pytest.fixture(autouse=True)
def redirected_home(tmp_path, monkeypatch):
    """NEVER the real ~/logs -- `enforce_log_caps` has no logs-dir seam; HOME is it."""
    home = tmp_path / "home"
    (home / "logs").mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    return home


def make_project(tmp_path) -> Path:
    root = tmp_path / "proj"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / crons.CRONS_NODE_REL).write_text(
        "---\n" + yaml.safe_dump({"id": "cron:crons", "type": "cron"}) + "---\n\nB.\n")
    (root / "agi-tree.config.json").write_text(
        json.dumps({"logs": {"cap_mb": CAP_MB, "rotations": KEEP}}))
    return root


def start_writer(log: Path, tag: str, journal: Path) -> subprocess.Popen:
    return subprocess.Popen([sys.executable, "-c", WRITER, str(log), str(journal), tag],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def lost_window(journal: Path, d: Path, tag: bytes) -> int:
    """Lines the process wrote but which are in NEITHER the base nor any archive
    -- the copy-then-truncate race window, in bytes."""
    kept = b"".join(p.read_bytes() for p in d.iterdir() if p.is_file() and p != journal)
    return journal.read_bytes().count(tag + b"\n") - kept.count(tag + b"\n")


def sizes(d: Path) -> dict:
    return {p.name: p.stat().st_size for p in sorted(d.iterdir())}


def test_f1_live_writer_keeps_appending_into_an_archive(tmp_path):
    """FALSIFIER 1: after one apply, further bytes land in an ARCHIVE."""
    root, d = make_project(tmp_path), Path(os.environ["HOME"]) / "logs"
    log = d / "agi-crons-test.log"
    jr = d / "writer.journal"
    log.write_bytes(OVER)
    kid = start_writer(log, "KID-AFTER-ROTATION", jr)
    try:
        time.sleep(0.2)
        crons.enforce_log_caps(root, root, dry_run=False)
        before = sizes(d)
        time.sleep(0.4)                      # the writer keeps writing, unrotated
        after = sizes(d)
        # 3 further applies: an ARCHIVE is skipped, so they can never cap it.
        outs = [crons.enforce_log_caps(root, root, dry_run=False) for _ in range(3)]
        recheck = sizes(d)
    finally:
        kid.terminate(); kid.wait(timeout=5)
    grew = {n: after[n] - before.get(n, 0) for n in after if after[n] > before.get(n, 0)}
    print("\nLOG DIR", json.dumps({"before": before, "after": after, "grew": grew,
                                   "3_more_applies": outs, "recheck": recheck,
                                   "cap_bytes": CAP_MB * 1024 * 1024}, indent=1))
    archives = {n for n in grew if crons._ARCHIVE_RE.match(n)}
    assert not archives, (
        f"live writer still appending to uncapped archive(s) {sorted(archives)}")
    assert not any(s > CAP_MB * 1024 * 1024 for s in sizes(d).values()), sizes(d)


def test_f4_alt_copytruncate_keeps_the_live_writer_on_a_capped_base(tmp_path):
    """The ALTERNATIVE the dispatch line names, measured the same way.

    No production edit: the copy-then-truncate MODE is emulated inline over the
    identical fixture, so the two candidates are compared on one run. For an
    O_APPEND writer (crons.py renders only `>>` redirects) the fd stays on the
    BASE inode, so later bytes re-enter the capped file, not an archive.
    """
    root, d = make_project(tmp_path), Path(os.environ["HOME"]) / "logs"
    log = d / "agi-crons-test.log"
    jr = d / "writer.journal"
    log.write_bytes(OVER)
    kid = start_writer(log, "KID", jr)
    try:
        time.sleep(0.2)
        # copytruncate: shift archives, COPY the base to .1, truncate in place
        Path(f"{log}.{KEEP}").unlink(missing_ok=True)
        for i in range(KEEP - 1, 0, -1):
            src = Path(f"{log}.{i}")
            if src.exists():
                src.replace(f"{log}.{i + 1}")
        shutil.copyfile(log, f"{log}.1")   # COPY, not rename: fd stays on the base
        log.write_bytes(b"")               # truncate the SAME inode in place
        before = sizes(d)
        time.sleep(0.4)
        after = sizes(d)
        lost = lost_window(jr, d, b"KID")
    finally:
        kid.terminate(); kid.wait(timeout=5)
    grew = {n: after[n] - before.get(n, 0) for n in after if after[n] > before.get(n, 0)}
    print("\nCOPYTRUNCATE", json.dumps({"before": before, "after": after,
                                       "grew": grew, "lost_lines": lost}, indent=1))
    assert not [n for n in grew if crons._ARCHIVE_RE.match(n)], grew
    assert b"KID" in log.read_bytes(), "live writer left the base"


def test_f2_truncated_base_has_no_nul_hole(tmp_path):
    """FALSIFIER 2: O_APPEND writes at the CURRENT end -- no sparse hole."""
    root, d = make_project(tmp_path), Path(os.environ["HOME"]) / "logs"
    log = d / "agi-crons-test.log"
    jr = d / "writer.journal"
    log.write_bytes(OVER)
    kid = start_writer(log, "KID", jr)
    try:
        time.sleep(0.2)
        crons.enforce_log_caps(root, root, dry_run=False)
        time.sleep(0.2)
        base = log.read_bytes()
    finally:
        kid.terminate(); kid.wait(timeout=5)
    print("\nBASE", len(base), "starts NUL:", base[:1] == b"\0",
          "contains NUL:", b"\0" in base)
    assert b"\0" not in base, "hole in the truncated base (writer at a stale offset)"


def test_f3_pre_rotation_bytes_survive_somewhere(tmp_path):
    """FALSIFIER 3: bytes written BEFORE the rotation are still readable."""
    root, d = make_project(tmp_path), Path(os.environ["HOME"]) / "logs"
    log = d / "agi-crons-test.log"
    jr = d / "writer.journal"
    log.write_bytes(OVER)
    kid = start_writer(log, "KID-BEFORE-ROTATION", jr)
    try:
        time.sleep(0.4)
        crons.enforce_log_caps(root, root, dry_run=False)
        after = sizes(d)
    finally:
        kid.terminate(); kid.wait(timeout=5)
    kept = b"".join(p.read_bytes() for p in d.iterdir() if p.is_file())
    print("\nAFTER", json.dumps(after), "KID bytes kept:", kept.count(b"KID-BEFORE-ROTATION"))
    assert kept.count(b"KID-BEFORE-ROTATION") >= 1, "pre-rotation bytes lost"
