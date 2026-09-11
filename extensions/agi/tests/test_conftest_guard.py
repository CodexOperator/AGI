"""Tests for hypothesis:l4-conftest-tmux-guard — the project-wide tmux guard.

Defence-in-depth (L4.258 helper): until this test existed, NOTHING asserted
the conftest `_no_real_tmux` autouse fixture was actually in force. Nothing
tests the guard itself, so the fixture could be renamed, narrowed or dropped
and every other suite stays green while the next tmux-touching test lands on
the live `agi-rc` session (the way test_send.py's file-local guard once did).

This file proves the guard both halves:
  * positive — a `tmux` subprocess call from inside a test is answered by the
    guard's safe CompletedProcess (rc 1, stdout None), not a real tmux and
    not a FileNotFoundError;
  * negative — a NON-tmux call still runs for real (rc 0, real stdout), so
    the guard is selective (tmux-only) and does not swallow the legitimate
    subprocess calls test_season.py/test_rotate.py's git fixtures depend on.
"""
from __future__ import annotations

import subprocess
import sys


def test_conftest_tmux_guard_is_in_force():
    """The autouse `_no_real_tmux` guard answers tmux with a safe rc-1
    CompletedProcess and passes every non-tmux call through to the real
    `subprocess.run`.

    Red-first proof: if the autouse fixture were gone, `subprocess.run`
    would be the real stdlib function (`__name__ == 'run'`), the tmux call
    would either reach a real tmux (a str stdout) or raise
    FileNotFoundError, and the non-tmux half would be indistinguishable from
    the guarded case. The three assertions below therefore fail together if
    the guard is dropped."""
    # Positive half: a tmux call is faked, not executed.
    tmux_ok = subprocess.run(
        ["tmux", "display-message", "-p", "#S"],
        capture_output=True,
        text=True,
    )
    assert subprocess.run.__name__ == "_guarded_run"
    assert tmux_ok.returncode == 1
    assert tmux_ok.stdout is None

    # Negative half: a non-tmux call still runs for real (selective guard).
    real_ok = subprocess.run(
        [sys.executable, "-c", "print(1)"],
        capture_output=True,
        text=True,
    )
    assert real_ok.returncode == 0
    assert real_ok.stdout == "1\n"
