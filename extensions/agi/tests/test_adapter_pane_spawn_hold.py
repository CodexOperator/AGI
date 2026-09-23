"""`goal:g7.31.1.2` residual closure — the pane opt-in is reachable from a
REAL spawn, not handed in by the test.

The prior round proved `pane_hold.ensure_pane` and `restart` reuse the same
`%N`, but only in a test that injected `record = {"pane": "seatA", ...}` by
hand — nothing in production ever set the field, so there was never a pane to
reattach to. This file drives the adapter's OWN first-spawn lifecycle entry
(`grok.spawn`), which reads a generic `harness["pane"]` cell (no harness
literal) and stamps `pane`/`pane_id` onto the record itself:

  1. spawn through `grok.spawn` with `harness["pane"] = True` and a record
     that carries NO pane field,
  2. `tmux list-panes` shows the named window and `pane_hold.pane_id` is
     non-empty,
  3. SIGKILL the seat process,
  4. `grok.restart` with the SAME record,
  5. same window name, same `%N`, NEW `pane_pid`.

Half (b) is the negative control: with the opt-in OFF the ordinary Popen path
runs, no tmux call is made, and the record carries no pane.
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

import adapters  # noqa: E402
from adapters import pane_hold  # noqa: E402

grok = adapters.load("grok_bot")
REAL_TMUX = shutil.which("tmux")
_REAL_RUN = subprocess.run  # captured BEFORE conftest's autouse guard

#: A `tmux` shim: with `FAKE_TMUX_REAL` set it delegates to the real binary on
#: a throwaway `-L` socket, so no test reaches the live `agi-rc` session.
FAKE_TMUX = '''#!/bin/bash
if [ -n "$FAKE_TMUX_REAL" ]; then
  exec "$FAKE_TMUX_REAL" -L "$FAKE_TMUX_SOCKET" "$@"
fi
exit 1
'''


@pytest.fixture
def tmux_shim(tmp_path, monkeypatch):
    guard = subprocess.run  # the autouse guard, already installed

    def _run(cmd, *a, **k):
        if isinstance(cmd, list) and cmd[:1] == ["tmux"]:
            return _REAL_RUN(cmd, *a, **k)
        return guard(cmd, *a, **k)

    monkeypatch.setattr(subprocess, "run", _run)
    d = tmp_path / "shim"
    d.mkdir()
    script = d / "tmux"
    script.write_text(FAKE_TMUX)
    script.chmod(0o755)
    monkeypatch.setenv("PATH", str(d) + os.pathsep + os.environ["PATH"])
    return d


def _wait_dead(*, session: str, name: str, timeout: float = 5.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if pane_hold.pane_field(tmux_session=session, name=name,
                                field="pane_dead") == "1":
            return
        time.sleep(0.05)
    raise AssertionError(f"pane {session}:{name} never reported pane_dead=1")


# ---------------------------------------------- end-to-end: spawn -> kill -> restart


def test_spawn_creates_the_pane_and_restart_reattaches_same_id(tmp_path,
                                                               tmux_shim,
                                                               monkeypatch):
    if not REAL_TMUX:
        pytest.skip("tmux not installed")
    monkeypatch.setenv("FAKE_TMUX_REAL", REAL_TMUX)
    sock = f"agi-pane-spawn-{os.getpid()}-{os.urandom(4).hex()}"
    monkeypatch.setenv("FAKE_TMUX_SOCKET", sock)
    session = f"agi-pane-spawn-{os.getpid()}-{os.urandom(2).hex()}"

    seat_bin = tmp_path / "seat.sh"
    seat_bin.write_text("#!/bin/bash\nsleep 300\n")
    seat_bin.chmod(0o755)
    harness = {"adapter": "grok_bot", "bin": str(seat_bin),
               "models": {"kid": "grok-kid"}, "pane": True}
    sess_dir = tmp_path / "sess"
    sess_dir.mkdir()
    # NO hand-injected `pane` field -- the spawn stamps it, or the test fails.
    record = {"id": "a00-spawn-pane", "worktree": str(tmp_path),
              "pane_session": session}
    try:
        pid0 = grok.spawn(
            harness=harness, tier="kid",
            context_file=str(sess_dir / "context.md"), agent_id="a00-spawn-pane",
            iter_n=1, sess_dir=sess_dir, agent_record=record)

        name = record.get("pane")
        assert name, "the first spawn must stamp the pane name itself"
        pane0 = pane_hold.pane_id(tmux_session=session, name=name)
        assert pid0 and pane0, "spawn must leave a live pane (%N) and pid"
        assert record.get("pane_id") == pane0
        assert pane_hold.pane_pid(tmux_session=session, name=name) == pid0
        assert pane_hold.pane_field(tmux_session=session, name=name,
                                    field="window_name") == name

        os.kill(pid0, signal.SIGKILL)
        _wait_dead(session=session, name=name)
        assert pane_hold.pane_id(tmux_session=session, name=name) == pane0, (
            "the dead pane must keep its %N -- that is the hold")

        pid1 = grok.restart(
            harness=harness, tier="kid",
            context_file=str(sess_dir / "context.md"),
            agent_id="a00-spawn-pane", iter_n=1, sess_dir=sess_dir,
            agent_record=record)

        assert pid1 and pid1 != pid0, (
            f"restart must give a NEW pane pid, got {pid0} -> {pid1}")
        assert record["pane"] == name, "restart must reuse the same pane name"
        assert pane_hold.pane_id(tmux_session=session, name=name) == pane0, (
            "restart must reattach to the SAME pane id")
        assert pane_hold.pane_pid(tmux_session=session, name=name) == pid1
        assert pane_hold.pane_field(tmux_session=session, name=name,
                                    field="pane_dead") == "0", (
            "the respawned seat must be alive")
    finally:
        subprocess.run([REAL_TMUX, "-L", sock, "kill-server"], check=False)


# ------------------------------------------------------------- negative control


def test_spawn_without_the_opt_in_uses_popen_and_creates_no_pane(tmp_path,
                                                                 monkeypatch):
    captured = {}

    class FakeProc:
        pid = 4242

    def fake_popen(args, **kwargs):
        captured["args"] = args
        captured["kwargs"] = kwargs
        return FakeProc()

    def fake_run(cmd, *a, **k):
        raise AssertionError(f"tmux must not be reached without the opt-in: {cmd}")

    monkeypatch.setattr(grok.subprocess, "Popen", fake_popen)
    monkeypatch.setattr(grok.subprocess, "run", fake_run)
    sess_dir = tmp_path / "sess"
    sess_dir.mkdir()
    harness = {"adapter": "grok_bot", "bin": "grok-bot",
               "models": {"kid": "grok-kid"}}
    record = {"id": "a00-no-pane", "worktree": str(tmp_path)}

    pid = grok.spawn(harness=harness, tier="kid",
                     context_file=str(tmp_path / "context.md"),
                     agent_id="a00-no-pane", iter_n=1, sess_dir=sess_dir,
                     agent_record=record)

    assert pid == 4242
    assert captured["args"] == grok.build_command(
        harness=harness, tier="kid",
        context_file=str(tmp_path / "context.md"))
    assert captured["kwargs"]["start_new_session"] is True
    assert "pane" not in record, "no opt-in must leave the record pane-free"
