"""Falsifier 3 and falsifier 2 of
hypothesis:log-cap-holds-while-a-long-lived-writer-keeps-the-log-open, MEASURED
on the BUILT `logs.mode: copytruncate` bytes (sibling build
experiment:a00-ffbd6bc6-f2a542). Both sibling experiments asserted the
O_APPEND-only precondition in prose and never measured it; this file measures
it and pins the numbers, so the claim cannot be re-stated without them.

Never the real ~/logs: HOME is redirected per test, cap 1 MB, one apply.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import crons  # noqa: E402

CAP_MB, KEEP, CAP = 1, 3, 1024 * 1024
UNIT = b"LLLL"   # one 4 KiB line is 1024 of these

# burst lines, then idle `gap_ms` (the apply lands in the gap), then burst again.
CHILD = """
import os, sys, time
log, journal, flags, burst, gap_ms = sys.argv[1:6]
fd = os.open(log, os.O_WRONLY | os.O_CREAT | (os.O_APPEND if flags == "append" else 0), 0o644)
blob = b"L" * 4096
with open(journal, "ab") as j:
    for _ in range(int(burst)):
        os.write(fd, blob); j.write(blob)
    time.sleep(int(gap_ms) / 1000.0)     # the apply happens here
    for _ in range(int(burst)):
        os.write(fd, blob); j.write(blob)
os.close(fd)
"""


@pytest.fixture(autouse=True)
def redirected_home(tmp_path, monkeypatch):
    home = tmp_path / "home"
    (home / "logs").mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    return home


def make_project(tmp_path, mode="copytruncate") -> Path:
    root = tmp_path / "proj"
    root.mkdir()
    (root / "agi-tree.config.json").write_text(json.dumps(
        {"logs": {"cap_mb": CAP_MB, "rotations": KEEP, "mode": mode}}))
    return root


def run_one(tmp_path, flags: str, mode="copytruncate", burst=20, gap_ms=400):
    root = make_project(tmp_path, mode)
    log = crons._log_path(root)
    journal = root.parent / "home" / "writer.journal"   # OUTSIDE the capped dir
    log.write_bytes(b"H" * (CAP + 4096))                # already over the cap
    child = subprocess.Popen([sys.executable, "-c", CHILD, str(log), str(journal),
                              flags, str(burst), str(gap_ms)],
                             stdout=subprocess.DEVNULL)
    time.sleep(0.15)
    out = crons.enforce_log_caps(root, root)
    child.wait()
    base = log.read_bytes()
    arch = Path(f"{log}.1")
    arch_b = arch.read_bytes() if arch.exists() else b""
    return {
        "out": out, "base": base, "arch": arch_b, "name": log.name,
        "written_u": journal.stat().st_size // 4,
        "base_u": base.count(UNIT), "arch_u": arch_b.count(UNIT),
        "nul": base.count(b"\0"),
    }


def test_append_writer_loses_no_line_and_leaves_no_hole(tmp_path):
    """The claim's writer: every 4 KiB line the process wrote is in the base or
    the archive, and the truncated base carries no NUL hole."""
    r = run_one(tmp_path, "append")
    assert [o for o in r["out"] if "rotated" in o] == [
        f"{r['name']} rotated (cap {CAP_MB} MB, {KEEP} kept)"]
    assert r["nul"] == 0
    assert r["written_u"] <= r["base_u"] + r["arch_u"]   # nothing lost
    assert len(r["arch"]) <= CAP                         # the archive is capped too


def test_a_plain_gt_writer_is_refused_by_name_and_leaves_no_nul_hole(tmp_path):
    """Falsifier 2 of hypothesis:log-cap-holds-at-each-apply-and-refuses-a-
    non-append-writer, MEASURED: a plain `>` redirect (O_WRONLY without
    O_APPEND) would resume at its stale offset after the in-place truncate and
    leave a NUL hole. Since DH.383 the apply REFUSES that file by name before
    truncating, so the base is still whole and the refusal is reported."""
    r = run_one(tmp_path, "noappend")
    assert r["nul"] == 0, "the non-append writer was truncated anyway"
    refusals = [o for o in r["out"] if "refused" in o]
    assert len(refusals) == 1 and refusals[0].startswith(
        f"{r['name']} refused: held without O_APPEND by pid "), r["out"]
    assert r["arch"] == b""                    # no archive was made either
    assert r["base_u"] == r["written_u"]       # every line the writer wrote survived
