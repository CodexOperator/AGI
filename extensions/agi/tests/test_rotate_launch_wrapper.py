import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate

PLUGIN = Path(rotate.__file__).resolve().parent
ROTATE = PLUGIN / "rotate.py"


def _run_wrapper(log_path, *child, seat="seatT"):
    """Popen a real `rotate.py launch-wrapper` around `child`.

    Real subprocess only — never a tmux pane, never a live seat. The child
    argv is what the wrapper would get for a seat successor.
    """
    return subprocess.Popen(
        [sys.executable, str(ROTATE), "launch-wrapper",
         "--seat", seat, "--log", str(log_path), "--", *child],
    )


def _wait_log(path, needle, timeout=12.0):
    """Poll `path` until it contains `needle`, then return the full text."""
    deadline = time.time() + timeout
    body = ""
    while time.time() < deadline:
        if path.exists():
            body = path.read_text(encoding="utf-8")
            if needle in body:
                return body
        time.sleep(0.05)
    return body


def _children(pid):
    try:
        out = subprocess.check_output(["pgrep", "-P", str(pid)],
                                      text=True).split()
    except subprocess.CalledProcessError:
        return []
    return [int(p) for p in out]


def _poll_child(wrapper_pid, timeout_s=5.0):
    """Wait until the wrapper has a direct child (its wrapped argv)."""
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        kids = [p for p in _children(wrapper_pid) if p != wrapper_pid]
        if kids:
            return kids[0]
        time.sleep(0.02)
    return None


# TERM the WRAPPER itself: the log names the sender's pid and the wrapper
# forwards, so the child dies too.
def test_wrapper_termed_forwards_and_names_sender(tmp_path):
    log = tmp_path / "seat.log"
    child = _run_wrapper(log, "sleep", "30")
    try:
        # wait until the wrapper has masked signals and centred its child
        # (only after pthread_sigmask does a TERM get queued, not fatal).
        assert _poll_child(child.pid), "wrapper child (sleep) never appeared"
        os.kill(child.pid, signal.SIGTERM)
        # the TERM is process-sent to the WRAPPER: the log names this pytest
        # process's pid (sender, /proc comm alive) and the wrapper forwards,
        # so the child dies too.
        body = _wait_log(log, "from pid")
        assert f"from pid {os.getpid()}" in body, body or "no sender line"
        rc = child.wait(timeout=12)
        body = _wait_log(log, "wrapper received")
        assert "exited signal 15" in body
        assert "wrapper received 15" in body
        assert rc == 128 + signal.SIGTERM
    finally:
        if child.poll() is None:
            child.kill()
            child.wait()


# HANG UP the wrapper's controlling tty (what `tmux kill-window` does): the
# kernel signals ONLY the session leader — the wrapper — never the child's
# group, so the wrapper must FORWARD the hangup or the child survives as an
# orphan. Measured pre-fix at the L4.285 harvest (sanctuary-director
# 182119Z 19:05Z): SIG1 logged "NOT forwarded", wrapper + sleep both alive
# after the window was gone. Real pty, real session leader, no tmux.
def test_wrapper_tty_hangup_forwards_to_the_child(tmp_path):
    import fcntl
    import termios
    log = tmp_path / "seat.log"
    master, slave = os.openpty()

    def _lead():
        os.setsid()
        fcntl.ioctl(0, termios.TIOCSCTTY, 0)

    wrapper = subprocess.Popen(
        [sys.executable, str(ROTATE), "launch-wrapper",
         "--seat", "seatH", "--log", str(log), "--", "sleep", "30"],
        stdin=slave, stdout=slave, stderr=slave, preexec_fn=_lead,
    )
    os.close(slave)
    try:
        sleeper = _poll_child(wrapper.pid)
        assert sleeper, "wrapper child (sleep) never appeared"
        os.close(master)          # the hangup: the pty's master side is gone
        body = _wait_log(log, "FORWARDED to child")
        assert "SIG1 from kernel/tty (si_pid 0)" in body, body or "no HUP line"
        assert f"FORWARDED to child {sleeper}" in body, body
        rc = wrapper.wait(timeout=12)
        body = _wait_log(log, "wrapper received")
        assert "exited signal 1" in body, body
        assert rc == 128 + signal.SIGHUP
        deadline = time.time() + 5
        while time.time() < deadline and Path(f"/proc/{sleeper}").exists():
            time.sleep(0.05)
        assert not Path(f"/proc/{sleeper}").exists(), "sleep survived the hangup"
    finally:
        if wrapper.poll() is None:
            wrapper.kill()
            wrapper.wait()


# TERM the CHILD directly: the sender is unknown to the wrapper (signal went
# straight to the child's own pid), so the log shows signal 15 with
# `wrapper received none` and NO sender line.
def test_wrapper_child_termed_directly_has_no_sender(tmp_path):
    log = tmp_path / "seat.log"
    child = _run_wrapper(log, "sleep", "30")
    try:
        # wait for the wrapper to centre its child.
        grandkid = _poll_child(child.pid)
        assert grandkid, "wrapper child (sleep) never appeared"
        os.kill(grandkid, signal.SIGTERM)
        rc = child.wait(timeout=12)
        body = _wait_log(log, "exited signal 15")
        assert "exited signal 15" in body
        assert "wrapper received none" in body
        assert "from pid" not in body
        assert rc == 128 + signal.SIGTERM
    finally:
        if child.poll() is None:
            child.kill()
            child.wait()


# Child exits cleanly: a self-teardown line, wrapper rc 0, no wrapper signal.
def test_wrapper_child_self_teardown(tmp_path):
    log = tmp_path / "seat.log"
    child = _run_wrapper(log, sys.executable, "-c", "raise SystemExit(0)")
    rc = child.wait(timeout=12)
    body = _wait_log(log, "exited status 0")
    assert "exited status 0" in body
    assert "wrapper received none" in body
    assert rc == 0


# _shell_cmd: seat wraps, no-seat stays byte-identical.
def test_shell_cmd_seat_wraps_no_seat_byte_identical():
    cli = ["claude", "--remote-control", "s", "-prompt"]
    no_seat = rotate._shell_cmd(cli, None)
    assert "launch-wrapper" not in no_seat
    assert no_seat == ("export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1 "
                       "&& claude --remote-control s -prompt")
    seated = rotate._shell_cmd(cli, None, seat="belam-X")
    assert "launch-wrapper" in seated
    # a seat exports BOTH AGI_POST and AGI_SEAT so either spelling resolves
    # (hypothesis:l4-a-seat-is-a-post-everywhere).
    assert "export AGI_POST=belam-X AGI_SEAT=belam-X &&" in seated
    # the raw claude argv rides after the wrapper's `--` separator.
    assert " -- claude --remote-control s -prompt" in seated
    assert seated.index("launch-wrapper") < seated.index("claude")