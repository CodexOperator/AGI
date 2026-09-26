"""hypothesis:a00-955a27ff-64bc5a -- the seat's own child (rotate.py
`launch-wrapper`) rides the ONE memory cap, and the cap costs the wrapper
nothing because BOTH seams exec their target in place, so `child.pid` is
still the agent.

(1) unit: `spawn.seat_memory_max` wins over `spawn.memory_max`; 'none'
    leaves argv UNWRAPPED; absent -> the memory_max value rides.
(2) wire: a REAL launch-wrapper subprocess under a forced systemd scope whose
    child prints its own pid and exits 7 -- the wrapper exits 7, and the pid
    in its lifecycle log is the SAME pid the child printed (no grandchild), so
    the sigwaitinfo/waitpid/forward contract is intact under the cap.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
ROTATE = BIN / "rotate.py"
sys.path.insert(0, str(BIN))

import mem_cap  # noqa: E402
import rotate  # noqa: E402


def _root(tmp_path, spawn: dict, name: str = "a") -> Path:
    """The GRAPH root (`<repo>/.agi`) -- what `find_project_root` returns and
    what `locations.load_config` reads a config out of."""
    graph = tmp_path / f"proj-{name}" / ".agi"
    graph.mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps({"spawn": spawn}))
    return graph


def _cap_argv(argv: list) -> list:
    return [a for a in argv if a.startswith("--as=")]


def test_seat_memory_max_cell_wins_and_none_leaves_it_unwrapped(tmp_path,
                                                                monkeypatch):
    monkeypatch.setenv("AGI_MEMCAP_SYSTEMD_RUN", "0")  # prlimit seam: no bus
    child = ["claude", "-p"]
    both = _root(tmp_path, {"memory_max": "6G", "seat_memory_max": "12G"}, "1")
    assert mem_cap._as_bytes(
        _cap_argv(rotate._launch_child_argv(child, both))[0][5:]) == 12 * 1024 ** 3
    off = _root(tmp_path, {"memory_max": "6G", "seat_memory_max": "none"}, "2")
    assert rotate._launch_child_argv(child, off) == child
    plain = _root(tmp_path, {"memory_max": "6G"}, "3")
    assert mem_cap._as_bytes(
        _cap_argv(rotate._launch_child_argv(child, plain))[0][5:]) == 6 * 1024 ** 3


@pytest.mark.skipif(not os.path.exists("/run/systemd/system"),
                    reason="no systemd on this box")
def test_wrapper_keeps_the_child_pid_under_a_real_scope(tmp_path):
    """The pid contract, on the bytes: the child's printed pid IS the pid the
    wrapper waits on, so nothing downstream (the seat row's `pid`, the
    forward-to-child path) is one layer deeper under the cap."""
    graph = _root(tmp_path, {"memory_max": "6G", "seat_memory_max": "6G"})
    log = tmp_path / "seat.wrapper.log"
    inner = ("import os,sys;print(os.getpid());sys.exit(7)")
    argv = [sys.executable, str(ROTATE), "launch-wrapper", "--seat", "s1",
            "--log", str(log), "--", sys.executable, "-c", inner]
    env = {**os.environ, "AGI_MEMCAP_SYSTEMD_RUN": "1",
           "PYTHONPATH": str(BIN)}
    out = subprocess.run(argv, capture_output=True, text=True, env=env,
                         cwd=graph.parent, timeout=60)
    assert out.returncode == 7, out.stderr
    text = log.read_text()
    child_pid = out.stdout.split()[0]
    assert f"cap seam systemd-run" in text, text
    assert f"child {child_pid} exited status 7" in text, text
