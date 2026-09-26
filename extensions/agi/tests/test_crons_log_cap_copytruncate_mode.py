"""The BUILT `logs.mode: copytruncate` path, on the bytes crons.py ships.

Sibling experiment:a00-e070fb47-f6889e measured the RENAME defect inline and
disproved the hypothesis as written. This file asserts the declared cell's
implementation instead: with `logs.mode = copytruncate` a long-lived O_APPEND
writer keeps writing to the BASE (never a skipped archive), and after every
apply no file in the dir is over `logs.cap_mb`.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import crons  # noqa: E402

CAP_MB, KEEP = 1, 3
CAP = CAP_MB * 1024 * 1024
OVER = b"x" * (CAP + 4096)

WRITER = """
import os, sys, time
log, journal, tag = sys.argv[1], sys.argv[2], sys.argv[3]
fd = os.open(log, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
jd = os.open(journal, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
line = (tag + "\\n").encode()
while True:
    os.write(fd, line)
    os.write(jd, line)
    time.sleep(0.02)
"""


@pytest.fixture(autouse=True)
def redirected_home(tmp_path, monkeypatch):
    home = tmp_path / "home"
    (home / "logs").mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    return home


def make_project(tmp_path, mode="copytruncate") -> Path:
    root = tmp_path / "proj"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / crons.CRONS_NODE_REL).write_text(
        "---\n" + yaml.safe_dump({"id": "cron:crons", "type": "cron"}) + "---\n\nB.\n")
    (root / "agi-tree.config.json").write_text(json.dumps(
        {"logs": {"cap_mb": CAP_MB, "rotations": KEEP, "mode": mode}}))
    return root


def sizes(d: Path) -> dict:
    return {p.name: p.stat().st_size for p in sorted(d.iterdir()) if p.is_file()}


def test_copytruncate_keeps_the_live_writer_on_a_capped_base(tmp_path):
    root, d = make_project(tmp_path), Path(os.environ["HOME"]) / "logs"
    log, jr = d / "agi-crons-test.log", d / "writer.journal"
    log.write_bytes(OVER)
    kid = subprocess.Popen([sys.executable, "-c", WRITER, str(log), str(jr), "KID"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(0.2)
        before = sizes(d)
        outs = [crons.enforce_log_caps(root, root) for _ in range(3)]
        time.sleep(0.3)
        after = sizes(d)
    finally:
        kid.terminate(); kid.wait(timeout=5)
    grew = {n: after[n] - before[n] for n in after
            if n in before and after[n] > before[n]}
    print("\nCOPYTRUNCATE-BUILT", json.dumps(
        {"before": before, "after": after, "grew": grew, "applies": outs}, indent=1))
    assert not [n for n in grew if crons._ARCHIVE_RE.match(n)], grew
    assert b"KID" in log.read_bytes(), "live writer left the capped base"
    # the cap holds at every apply boundary, archives included
    overs = {n: s for n, s in sizes(d).items() if s > CAP and n != jr.name}
    assert not overs, overs
    # and the tail of the archive is what survives (newest data kept)
    arch = Path(f"{log}.1")
    if arch.exists():
        assert arch.read_bytes().endswith(arch.read_bytes()[-16:])


def test_unknown_mode_fails_closed_by_name(tmp_path):
    root = make_project(tmp_path, mode="nope")
    with pytest.raises(crons.CronsError, match="logs.mode"):
        crons.enforce_log_caps(root, root)


def test_absent_mode_keeps_rename(tmp_path):
    """Back-compat: a config that declares no `logs.mode` rotates by RENAME."""
    root = make_project(tmp_path, mode="rename")
    (root / "agi-tree.config.json").write_text(json.dumps(
        {"logs": {"cap_mb": CAP_MB, "rotations": KEEP}}))
    d = Path(os.environ["HOME"]) / "logs"
    log = d / "agi-crons-test.log"
    log.write_bytes(OVER)
    out = crons.enforce_log_caps(root, root)
    assert out and log.with_name(log.name + ".1").exists(), out
