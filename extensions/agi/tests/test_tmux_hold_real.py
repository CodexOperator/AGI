"""REAL-tmux integration guard for the durable pane hold (`goal:g7.31.1.2`).

The sibling `test_tmux_hold.py` drives a FAKE tmux object, so it proves the
adapter's bookkeeping but not that a real tmux server holds a real pane across
a real process death. That gap is exactly the residue this file closes: the
falsifier is the `tmux` BINARY, invoked through the adapter's own `restart`.

Hermetic: one uniquely named session, killed in a `finally`.
"""
from __future__ import annotations

import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

from adapters import grok_bot_adapter, tmux_hold  # noqa: E402

if shutil.which("tmux") is None:  # pragma: no cover -- real binary required
    pytest.skip("tmux binary not on PATH", allow_module_level=True)

AGENT = "a00-real-hold-seat"
SEAT = tmux_hold.pane_name(AGENT)


def _tmux(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["tmux", *args], capture_output=True, text=True)


@pytest.fixture(autouse=True)
def _no_real_tmux():
    """Opt THIS file out of the project-wide tmux guard (conftest.py).

    That guard (`hypothesis:l4-conftest-tmux-guard`) answers every `tmux`
    subprocess call with rc-1 so no test can type into a LIVE session
    (`rotate.DEFAULT_TMUX_SESSION`). This file is the one that must reach a
    REAL tmux server, and it is hermetic about it: the only session it touches
    is `agi-hold-test-<pid>`, created by the test and killed in a `finally`.
    Shadowing the conftest fixture by name is the narrowest seam pytest gives
    a single file; every other test keeps the guard.
    """
    yield


@pytest.fixture
def session():
    """A unique session per run; always killed, even on failure/collection."""
    name = f"agi-hold-test-{os.getpid()}"
    _tmux("kill-session", "-t", name)
    try:
        yield name
    finally:
        _tmux("kill-session", "-t", name)


def _wait_dead(pid: int, timeout: float = 5.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if not grok_bot_adapter.is_alive(pid):
            return True
        time.sleep(0.05)
    return False


def test_restart_holds_same_real_pane(session, tmp_path, monkeypatch):
    """Kill the seat PROCESS; `restart` re-enters the SAME real tmux pane."""
    harness = {"adapter": "grok_bot", "bin": "grok-bot", "tmux": True,
               "tmux_session": session, "models": {"kid": "x"}}
    # A LONG-LIVED argv so the pane genuinely holds instead of exiting at once.
    monkeypatch.setattr(grok_bot_adapter, "build_command",
                        lambda **kw: ["/bin/sleep", "300"])
    sess_dir = tmp_path / "sess"
    sess_dir.mkdir()
    record: dict = {"worktree": str(tmp_path), "pid": 0}
    kw = dict(harness=harness, tier="kid", context_file="ctx.md",
              agent_id=AGENT, iter_n=1, sess_dir=sess_dir, agent_record=record)

    pid1 = grok_bot_adapter.restart(**kw)
    assert pid1 is not None, "restart produced no pid"
    rows = tmux_hold.panes(harness)
    assert [r[0] for r in rows] == [SEAT], f"expected one seat pane, got {rows}"
    pane_id, pane_pid = rows[0][1], int(rows[0][2])
    assert pane_pid == pid1
    assert grok_bot_adapter.is_alive(pane_pid)

    os.kill(pane_pid, signal.SIGKILL)
    assert _wait_dead(pane_pid), "seat process survived SIGKILL"
    rows = tmux_hold.panes(harness)
    assert [r[0] for r in rows] == [SEAT], "pane did not survive its process"
    assert rows[0][1] == pane_id, "pane id changed while process was dead"
    names = _tmux("list-panes", "-s", "-t", session,
                  "-F", "#{window_name}").stdout.split()
    assert names == [SEAT], f"session holds {names}, not one seat window"

    pid2 = grok_bot_adapter.restart(**kw)
    assert pid2 is not None, "restart-after-death produced no pid"
    assert pid2 != pane_pid, "restart did not produce a new process"
    assert grok_bot_adapter.is_alive(pid2)
    rows = tmux_hold.panes(harness)
    assert [r[0] for r in rows] == [SEAT], "duplicate seat window fabricated"
    assert rows[0][1] == pane_id, "restart landed in a DIFFERENT pane"
    assert int(rows[0][2]) == pid2
    assert record.get("tmux") == {"created": False, "pane_id": pane_id}, \
        f"reattach was not stamped as a hold: {record.get('tmux')}"


def test_reattach_holds_seat_when_foreign_window_is_current(
        session, tmp_path, monkeypatch):
    """`panes()` must pass `-s`: a seat whose window is NOT current is still
    the seat. Without `-s` tmux lists only the current window, `reattach`
    cannot find the seat by name, and a SECOND `seat-<hash>` window is
    fabricated -- the parent's probe-2 refutation, on a REAL server."""
    harness = {"adapter": "grok_bot", "bin": "grok-bot", "tmux": True,
               "tmux_session": session, "models": {"kid": "x"}}
    monkeypatch.setattr(grok_bot_adapter, "build_command",
                        lambda **kw: ["/bin/sleep", "300"])
    sess_dir = tmp_path / "sess"
    sess_dir.mkdir()
    record: dict = {"worktree": str(tmp_path), "pid": 0}
    kw = dict(harness=harness, tier="kid", context_file="ctx.md",
              agent_id=AGENT, iter_n=1, sess_dir=sess_dir, agent_record=record)

    pid1 = grok_bot_adapter.restart(**kw)
    assert pid1 is not None
    pane_id = tmux_hold.panes(harness)[0][1]
    os.kill(int(tmux_hold.panes(harness)[0][2]), signal.SIGKILL)
    assert _wait_dead(pid1)
    # Make a FOREIGN window current while the seat's pane is dead.
    assert _tmux("new-window", "-t", session, "-n", "other",
                 "--", "/bin/sleep", "300").returncode == 0
    assert _tmux("display-message", "-p", "-t", session,
                 "#{window_name}").stdout.strip() == "other"

    pid2 = grok_bot_adapter.restart(**kw)
    assert pid2 is not None and pid2 != pid1
    names = _tmux("list-panes", "-s", "-t", session,
                  "-F", "#{window_name}").stdout.split()
    assert names.count(SEAT) == 1, f"seat window duplicated: {names}"
    assert tmux_hold.panes(harness)[0][1] == pane_id, "seat pane id changed"
    assert record.get("tmux") == {"created": False, "pane_id": pane_id}, \
        f"a fabricated pane was passed off as held: {record.get('tmux')}"
