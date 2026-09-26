"""The four conjuncts of
hypothesis:crons-log-cap-bounds-archives-and-prunes-only-its-own-files, plus
the folded-in non-append refusal of
hypothesis:log-cap-holds-at-each-apply-and-refuses-a-non-append-writer.

(1) after ONE apply no managed file exceeds the cap -- BASE or ARCHIVE,
    including an archive that was ALREADY over the cap before the apply;
(2) the scope is the DECLARED name set, never a `*` glob: a decoy belonging to
    another service is byte-identical afterwards, size and mtime alike;
(3) `crons_live: false` (the kill switch) rotates, prunes and unlinks NOTHING;
(4) a writer holding the base open WITHOUT `O_APPEND` is refused BY NAME before
    the in-place truncate, so the NUL hole never appears.

`HOME` is redirected per test -- never the real ~/logs -- and the only writer is
a `python3 -c` stand-in.
"""
from __future__ import annotations

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

# The falsifier writer: `>` semantics, no O_APPEND. Writes `ms` of 4 KiB lines.
NON_APPEND_WRITER = """
import os, sys, time
log, ms = sys.argv[1], int(sys.argv[2])
fd = os.open(log, os.O_WRONLY | os.O_CREAT, 0o644)
blob = b"L" * 4096
end = time.time() + ms / 1000.0
while time.time() < end:
    os.write(fd, blob)
    time.sleep(0.005)
"""


@pytest.fixture(autouse=True)
def redirected_home(tmp_path, monkeypatch):
    home = tmp_path / "home"
    (home / "logs").mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    return home


def make_project(tmp_path, **cells) -> Path:
    """A project root with a crons node and a `logs` namespace. `crons_live`
    is a node key, not a cell; the cells default to copytruncate + 1 MB."""
    root = tmp_path / "proj"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / crons.CRONS_NODE_REL).write_text(
        "---\n" + yaml.safe_dump(
            {"id": "cron:crons", "type": "cron",
             "crons_live": cells.pop("crons_live", True)}) + "---\n\nB.\n")
    (root / "agi-tree.config.json").write_text(json.dumps({"logs": dict(
        {"cap_mb": CAP_MB, "rotations": KEEP, "mode": "copytruncate"},
        **cells)}))
    return root


def logs() -> Path:
    return Path(os.environ["HOME"]) / "logs"


def fingerprint(p: Path):
    st = p.stat()
    return (st.st_size, st.st_mtime_ns, p.read_bytes())


# --- (1) the cap bounds EVERY archive, including one already over ------------


def test_a_pre_existing_over_cap_archive_is_brought_under_the_cap(tmp_path):
    """The near-miss `_tail_copy` leaves: it bounds only the archive a rotation
    JUST made. An archive left at 172 MB by the previous code is `continue`d
    over forever, and the apply says nothing about it."""
    root = make_project(tmp_path)
    log = crons._log_path(root)
    log.write_bytes(OVER)
    stale = Path(f"{log}.1")          # already 1.5x the cap BEFORE the apply
    stale.write_bytes(b"z" * (CAP + 4096 + 512 * 1024))
    Path(f"{log}.3").write_bytes(b"z" * (CAP + 4096 + 1024 * 1024))
    out = crons.enforce_log_caps(root, root, dry_run=False)
    assert any("bounded to the" in line and stale.name in line for line in out), out
    assert stale.stat().st_size == CAP
    assert stale.read_bytes()[-CAP:] == stale.read_bytes()[-CAP:]
    managed = [p for p in logs().iterdir() if p.is_file()]
    assert all(p.stat().st_size <= CAP for p in managed), managed


def test_no_managed_file_is_over_the_cap_after_one_apply(tmp_path):
    """The conjunct, asserted over the whole declared set: base plus every
    archive of both declared names."""
    root = make_project(tmp_path)
    for name in (crons._log_path(root), crons.alerts_log(root)):
        name.write_bytes(b"q" * (CAP + 4096))
        Path(f"{name}.1").write_bytes(b"q" * (CAP + 4096))
        Path(f"{name}.2").write_bytes(b"q" * (CAP + 8192))
    crons.enforce_log_caps(root, root, dry_run=False)
    over = [(p.name, p.stat().st_size) for p in logs().iterdir()
            if p.is_file() and p.stat().st_size > CAP]
    assert over == [], over


# --- (2) the scope is THIS project's files -----------------------------------


def test_a_decoy_of_another_service_is_never_touched(tmp_path):
    """The falsifier: over-cap `other-service.log` and an over-cap archive
    belonging to a SIBLING project, both in the same dir, both left
    byte-identical (size AND mtime) by one apply."""
    root = make_project(tmp_path)
    crons._log_path(root).write_bytes(OVER)
    decoys = [logs() / "other-service.log", logs() / "agi-crons-other-0badf00d.log.7"]
    for d in decoys:
        d.write_bytes(b"d" * (CAP + 4096))
    before = [fingerprint(d) for d in decoys]
    out = crons.enforce_log_caps(root, root, dry_run=False)
    assert [fingerprint(d) for d in decoys] == before
    assert all(d.is_file() for d in decoys)
    assert not any("other-service" in line or "0badf00d" in line for line in out), out


def test_an_undeclared_legacy_residue_is_not_pruned(tmp_path):
    """The residue prune used to reach every `*.1.1` in the dir. It is now
    reached only for a declared base -- another service's residue is theirs."""
    root = make_project(tmp_path)
    residue = logs() / "other-service.log.1.1"
    residue.write_bytes(b"d" * (CAP + 4096))
    assert crons.enforce_log_caps(root, root, dry_run=False) == []
    assert fingerprint(residue)[2] == b"d" * (CAP + 4096)


def test_also_manage_admits_a_name_and_refuses_a_path(tmp_path):
    """config-max: the extra managed name is a declared CELL, and a path in it
    raises by name rather than reaching outside the capped dir."""
    root = make_project(tmp_path, also_manage=["agi-reaper-agi-2f118e6f.log"])
    reap = logs() / "agi-reaper-agi-2f118e6f.log"
    reap.write_bytes(OVER)
    crons.enforce_log_caps(root, root, dry_run=False)
    assert reap.stat().st_size == 0
    bad = make_project(tmp_path / "b", also_manage=["../escape.log"])
    with pytest.raises(crons.CronsError, match="logs.also_manage"):
        crons.enforce_log_caps(bad, bad, dry_run=False)


# --- (3) the kill switch stops it --------------------------------------------


def test_the_kill_switch_flag_stops_rotation_prune_and_unlink(tmp_path):
    """`enforce_log_caps` is gated HERE, at the one function that touches the
    dir; the next test drives the same gate through the real `apply`, where
    the flag comes from the node's `crons_live`."""
    root = make_project(tmp_path, crons_live=False)
    log = crons._log_path(root)
    log.write_bytes(OVER)
    Path(f"{log}.1.1").write_bytes(b"z" * (CAP + 4096))
    assert crons.enforce_log_caps(root, root, dry_run=False, live=False) == []
    assert log.stat().st_size == len(OVER)
    assert Path(f"{log}.1.1").exists()


def test_an_apply_with_the_kill_switch_through_its_own_command(tmp_path):
    """The real seam: `cli.main apply` on a `crons_live: false` node installs
    0 lines and leaves the over-cap log exactly as it found it."""
    root = make_project(tmp_path, crons_live=False)
    log = crons._log_path(root)
    log.write_bytes(OVER)
    fixture = tmp_path / "crontab.fixture"
    fixture.write_text("")
    assert crons.main(["apply", "--root", str(root),
                       "--crontab-file", str(fixture)]) == 0
    assert log.stat().st_size == len(OVER)
    assert not (logs() / f"{log.name}.1").exists()


# --- (4) a non-O_APPEND writer is refused by name ---------------------------


def _writer(log: Path, ms: int = 2500) -> subprocess.Popen:
    return subprocess.Popen(
        [sys.executable, "-c", NON_APPEND_WRITER, str(log), str(ms)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def test_a_non_append_writer_is_refused_and_never_truncated(tmp_path):
    """The folded-in falsifier: `>` semantics leaves a NUL hole at the stale
    offset. The apply must NAME the file and leave it whole."""
    root = make_project(tmp_path)
    log = crons._log_path(root)
    log.write_bytes(OVER)
    kid = _writer(log)
    try:
        time.sleep(0.2)
        out = crons.enforce_log_caps(root, root, dry_run=False)
    finally:
        kid.terminate()
        kid.wait(timeout=5)
    refusals = [o for o in out if "refused" in o]
    assert len(refusals) == 1 and refusals[0].startswith(
        f"{log.name} refused: held without O_APPEND by pid"), out
    assert not (logs() / f"{log.name}.1").exists()
    assert log.read_bytes().count(b"\0") == 0


def test_the_non_append_fallback_rename_still_bounds_the_base(tmp_path):
    """`logs.non_append: rename` is the opt-in that trades the stranded writer
    for the CAP: the base is rotated away, so nothing exceeds the cap."""
    root = make_project(tmp_path, non_append="rename")
    log = crons._log_path(root)
    log.write_bytes(OVER)
    kid = _writer(log)
    try:
        time.sleep(0.2)
        out = crons.enforce_log_caps(root, root, dry_run=False)
    finally:
        kid.terminate()
        kid.wait(timeout=5)
    assert not any("refused" in o for o in out), out
    assert any("rotated" in o for o in out), out
    assert all(p.stat().st_size <= CAP for p in logs().iterdir() if p.is_file())


def test_an_unreadable_proc_is_said_once_per_apply_never_assumed_silent(
        tmp_path, monkeypatch):
    root = make_project(tmp_path)
    log = crons._log_path(root)
    log.write_bytes(OVER)
    monkeypatch.setattr(crons, "_non_append_holders",
                        lambda p: (None, []))          # /proc not readable
    out = crons.enforce_log_caps(root, root, dry_run=False)
    unknown = [o for o in out if "UNKNOWN" in o]
    assert len(unknown) == 1 and log.name in unknown[0], out
    assert not any("refused" in o for o in out), out


def test_a_malformed_non_append_cell_raises_by_name(tmp_path):
    bad = make_project(tmp_path / "b", non_append="maybe")
    with pytest.raises(crons.CronsError, match="logs.non_append"):
        crons.enforce_log_caps(bad, bad, dry_run=False)
