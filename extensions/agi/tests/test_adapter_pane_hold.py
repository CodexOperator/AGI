"""`goal:g7.31.1.2` — durable named tmux pane hold through the adapter seam.

Falsifier, verbatim: kill the seat process; `restart` reattaches to the SAME
tmux pane name; `tmux list-panes` still shows the seat.

Half (a) runs REAL tmux 3.4 on a throwaway `-L` socket: create the pane
through the seam, kill its process, `restart` with the same name, and assert
the `pane_id` `%N` is UNCHANGED while the `pane_pid` CHANGED — the name is
held across pid churn. Half (b) is a fake-`tmux` PATH shim that logs argv: the
create and the respawn both target the SAME `<session>:<name>`, and the
respawn uses `respawn-pane -k`.
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

#: Captured at import, BEFORE conftest's autouse `_tmux_guard` replaces
#: `subprocess.run`. The guard answers every `tmux` call with rc-1 (so no test
#: reaches the live `agi-rc` session). These tests are the documented
#: override: they re-patch in the test body and let ONLY the PATH shim
#: through, to a throwaway `-L` socket, never the live default socket.
_REAL_RUN = subprocess.run

#: A `tmux` shim. Always logs argv when `FAKE_TMUX_LOG` is set. With
#: `FAKE_TMUX_REAL` set it delegates to the real binary on `FAKE_TMUX_SOCKET`;
#: otherwise it answers canned `list-windows` / `list-panes` output.
FAKE_TMUX = '''#!/bin/bash
[ -n "$FAKE_TMUX_LOG" ] && echo "$*" >> "$FAKE_TMUX_LOG"
if [ -n "$FAKE_TMUX_REAL" ]; then
  exec "$FAKE_TMUX_REAL" -L "$FAKE_TMUX_SOCKET" "$@"
fi
case "$1" in
  list-windows) [ -n "$FAKE_TMUX_WINDOW" ] && echo "$FAKE_TMUX_WINDOW" || exit 1 ;;
  list-panes) echo "${FAKE_TMUX_PANE_PID:-1001}" ;;
esac
'''


@pytest.fixture
def shim(tmp_path, monkeypatch):
    """Put the logging `tmux` shim on PATH; hand back the argv log path.

    Re-patches `subprocess.run` AFTER the autouse guard (same function-scoped
    `monkeypatch` instance) so the guard's blanket `tmux` -> rc-1 does not
    swallow the shim; every non-`tmux` call still reaches the guard.
    """
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
    log = tmp_path / "tmux.log"
    monkeypatch.setenv("FAKE_TMUX_LOG", str(log))
    monkeypatch.setenv("PATH", str(d) + os.pathsep + os.environ["PATH"])
    return log


def _wait_dead(*, session: str, name: str, timeout: float = 5.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if pane_hold.pane_field(tmux_session=session, name=name,
                                field="pane_dead") == "1":
            return
        time.sleep(0.05)
    raise AssertionError(f"pane {session}:{name} never reported pane_dead=1")


# ---------------------------------------------------------------- real tmux


def test_real_tmux_restart_reuses_the_same_pane_id_and_name(tmp_path, shim,
                                                            monkeypatch):
    if not REAL_TMUX:
        pytest.skip("tmux not installed")
    monkeypatch.setenv("FAKE_TMUX_REAL", REAL_TMUX)
    sock = f"agi-pane-{os.getpid()}-{os.urandom(4).hex()}"
    monkeypatch.setenv("FAKE_TMUX_SOCKET", sock)
    session = f"agi-pane-{os.getpid()}-{os.urandom(2).hex()}"

    seat_bin = tmp_path / "seat.sh"
    seat_bin.write_text("#!/bin/bash\nsleep 300\n")
    seat_bin.chmod(0o755)
    harness = {"adapter": "grok_bot", "bin": str(seat_bin),
               "models": {"kid": "grok-kid"}}
    sess_dir = tmp_path / "sess"
    sess_dir.mkdir()
    try:
        pid0 = pane_hold.ensure_pane(tmux_session=session, name="seatA",
                                     argv=[str(seat_bin)])
        pane0 = pane_hold.pane_id(tmux_session=session, name="seatA")
        assert pid0 and pane0, "pane must start with a live pid and %N"

        os.kill(pid0, signal.SIGKILL)
        _wait_dead(session=session, name="seatA")
        assert pane_hold.pane_id(tmux_session=session, name="seatA") == pane0, (
            "the dead pane must keep its %N — that is the hold")

        record = {"id": "a00-pane", "pane": "seatA", "pane_session": session,
                  "worktree": str(tmp_path)}
        pid1 = grok.restart(
            harness=harness, tier="kid",
            context_file=str(sess_dir / "context.md"),
            agent_id="a00-pane", iter_n=1, sess_dir=sess_dir,
            agent_record=record)

        assert pid1 and pid1 != pid0, (
            f"restart must give a NEW pane pid, got {pid0} -> {pid1}")
        assert pane_hold.pane_id(tmux_session=session, name="seatA") == pane0, (
            "restart must reattach to the SAME pane id")
        assert pane_hold.pane_pid(tmux_session=session, name="seatA") == pid1
        assert pane_hold.pane_field(tmux_session=session, name="seatA",
                                    field="pane_dead") == "0", (
            "the respawned seat must be alive")
        assert pane_hold.pane_field(tmux_session=session, name="seatA",
                                    field="window_name") == "seatA", (
            "tmux must still show the same window name")
    finally:
        subprocess.run([REAL_TMUX, "-L", sock, "kill-server"], check=False)


# ------------------------------------------------------------- fake tmux


def test_create_and_respawn_both_target_the_same_pane(tmp_path, shim,
                                                      monkeypatch):
    monkeypatch.delenv("FAKE_TMUX_REAL", raising=False)
    pid0 = pane_hold.ensure_pane(tmux_session="rc", name="seatZ",
                                 argv=["sleep", "300"])
    assert pid0 == 1001

    monkeypatch.setenv("FAKE_TMUX_WINDOW", "seatZ")
    monkeypatch.setenv("FAKE_TMUX_PANE_PID", "2002")
    pid1 = pane_hold.ensure_pane(tmux_session="rc", name="seatZ",
                                 argv=["sleep", "300"])
    assert pid1 == 2002

    lines = shim.read_text().splitlines()
    assert any(l.startswith("new-session -d -s rc -n seatZ") for l in lines), (
        f"create must target rc:seatZ under the session, got {lines}")
    assert "set-option -w -t rc:seatZ remain-on-exit on" in lines, (
        "the created window must hold the pane after its process dies")
    respawn = [l for l in lines if l.startswith("respawn-pane")]
    assert respawn and respawn[0].startswith("respawn-pane -k -t rc:seatZ"), (
        f"respawn must use -k on the SAME target, got {respawn}")
