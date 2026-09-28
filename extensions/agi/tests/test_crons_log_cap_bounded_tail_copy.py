"""The BOUNDED tail copy (`crons._tail_copy`) behind `logs.mode: copytruncate`.

experiment:a00-fbe9eaf0-e14ad5. `shutil.copyfile` on a base a writer is still
appending to CHASES the moving EOF: on a 3 s O_APPEND writer one apply took
0.228-127.4 s, and the copy-then-truncate race window is
`writer_rate x copy duration` (experiment:a00-e4ba316a-1f6748). `_tail_copy`
snapshots the size once and reads at most `cap` bytes, so the cost follows the
CAP and the writer's rate, and the archive is never over the cap to trim.

`HOME` is redirected into a tmp dir -- never the real ~/logs.
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
OVER = b"x" * (CAP + 4096)      # a base strictly over the cap

# One 4 KiB append per loop, no sleep -- the writer that made the copy chase.
WRITER = """
import os, sys, time
log, ms = sys.argv[1], int(sys.argv[2])
fd = os.open(log, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
blob = b"U" * 4096
end = time.time() + ms / 1000.0
while time.time() < end:
    os.write(fd, blob)
"""


@pytest.fixture(autouse=True)
def redirected_home(tmp_path, monkeypatch):
    home = tmp_path / "home"
    (home / "logs").mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    return home


def make_project(tmp_path, cap_mb=CAP_MB, mode="copytruncate") -> Path:
    root = tmp_path / "proj"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / crons.CRONS_NODE_REL).write_text(
        "---\n" + yaml.safe_dump({"id": "cron:crons", "type": "cron"}) + "---\n\nB.\n")
    (root / "agi-tree.config.json").write_text(json.dumps(
        {"logs": {"cap_mb": cap_mb, "rotations": KEEP, "mode": mode}}))
    return root


def one_apply_cost(root, log, writer_ms=3000) -> float:
    """Seconds for ONE `enforce_log_caps` with `writer_ms` of a live fast writer."""
    kid = subprocess.Popen([sys.executable, "-c", WRITER, str(log), str(writer_ms)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(0.1)
        t0 = time.time()
        crons.enforce_log_caps(root, root, dry_run=False)
        return time.time() - t0
    finally:
        kid.terminate()
        kid.wait(timeout=5)


def test_apply_cost_does_not_follow_the_writer(tmp_path):
    """A 30x longer writer must not make the apply ~30x longer: the copy reads
    a snapshotted size, so cost is a function of the cap, not of the writer."""
    costs = []
    for writer_ms in (100, 3000):
        root = make_project(tmp_path / f"p{writer_ms}")
        log = crons._log_path(root)
        log.write_bytes(OVER)
        costs.append(one_apply_cost(root, log, writer_ms))
    print("\nAPPLY COST", json.dumps({"100ms_writer": costs[0],
                                     "3s_writer": costs[1]}, indent=1))
    # the old bytes blocked for 0.2-127 s on this fixture; a 1 MB bounded copy
    # is milliseconds. 10 s is slack for a loaded box, and still 1/12 of the
    # WORST old trial, so the assertion fails loudly if the chase comes back.
    assert max(costs) < 10.0, costs


def test_archive_is_the_newest_cap_bytes_and_never_over(tmp_path):
    """Bounded means the archive is exactly the base's TAIL -- the newest data,
    which is what a log rotation keeps -- and never inherits the overage the old
    full-copy-then-trim path had to trim in a second pass. No writer here: this
    asserts CONTENT, which a live writer would race."""
    root = make_project(tmp_path)
    log = crons._log_path(root)
    # 2.34 MB of numbered lines, the last 0.25 MB over the cap.
    src = b"".join(b"%08d\n" % i for i in range(260000))
    log.write_bytes(src)
    out = crons.enforce_log_caps(root, root, dry_run=False)
    arch = Path(f"{log}.1")
    print("\nARCHIVE", json.dumps({"size": arch.stat().st_size, "cap": CAP,
                                   "src": len(src), "out": out}))
    assert arch.stat().st_size == CAP
    assert arch.read_bytes() == src[-CAP:]        # the tail, byte for byte


def test_tail_copy_handles_a_base_smaller_than_the_cap(tmp_path):
    """Under-cap bases never reach the branch, but the helper is total: a short
    source must land whole, with no seek-(-cap) crash."""
    src, dst = tmp_path / "src.log", tmp_path / "dst.log.1"
    src.write_bytes(b"short\n")
    crons._tail_copy(src, dst, CAP)
    assert dst.read_bytes() == b"short\n"


def test_tail_copy_takes_the_tail_across_a_chunk_boundary(tmp_path):
    """`cap` here is NOT a multiple of the 1 MiB read chunk, so the loop is
    exercised on its second iteration."""
    src, dst = tmp_path / "src.log", tmp_path / "dst.log.1"
    src.write_bytes(bytes(range(256)) * 40_000)      # 10_240_000 B
    crons._tail_copy(src, dst, 3_000_017)            # 2 full chunks + 16_481 B
    assert dst.stat().st_size == 3_000_017
    assert dst.read_bytes() == src.read_bytes()[-3_000_017:]
