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

import os
import shutil
import subprocess
import sys
import tempfile

CONFTEST = os.path.join(os.path.dirname(__file__), "conftest.py")


def _run_identity_pop_subprocess(test_src, env_extra):
    """Run pytest against a throwaway dir that symlinks the real conftest,
    with the runner-identity env vars exported, and return (rc, stderr).
    The env is scrubbed of any pre-existing AGI_AGENT_ID/AGI_SEAT/AGI_POST
    and AGI_TIER first, so the only way the child sees the exported identity
    is the callers' `env_extra`."""
    d = tempfile.mkdtemp()
    try:
        os.symlink(CONFTEST, os.path.join(d, "conftest.py"))
        with open(os.path.join(d, "test_a.py"), "w") as f:
            f.write(test_src)
        env = dict(os.environ)
        env.pop("AGI_TIER", None)
        env.pop("AGI_AGENT_ID", None)
        env.pop("AGI_SEAT", None)
        env.pop("AGI_POST", None)
        env.update(env_extra)
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", os.path.join(d, "test_a.py"), "-q"],
            capture_output=True,
            text=True,
            env=env,
        )
        return proc.returncode, proc.stderr
    finally:
        shutil.rmtree(d)


ABSENT_SRC = (
    "import os\n"
    "\n"
    "def test_identity_env_absent():\n"
    "    for _n in (\"AGI_AGENT_ID\", \"AGI_SEAT\", \"AGI_POST\"):\n"
    "        assert _n not in os.environ, f\"{_n} must be popped by conftest\"\n"
)


def test_runner_identity_pop_removes_all_three_end_to_end():
    """conftest.pytest_cmdline_main pops AGI_AGENT_ID / AGI_SEAT / AGI_POST
    from a suite's inherited environment BEFORE any test runs, so a suite
    launched from a rotate-self-spawned seat (exports AGI_POST + AGI_SEAT)
    or a dispatched kid (AGI_AGENT_ID) does not sign its test messages under
    the runner's identity.

    End-to-end proof: a nested pytest that inherits all three exported must
    see NONE of them at test time. If a future edit drops one name from the
    pop list, the nested test fails and this suite goes red."""
    code, err = _run_identity_pop_subprocess(
        ABSENT_SRC,
        {"AGI_AGENT_ID": "z", "AGI_SEAT": "x", "AGI_POST": "y"},
    )
    assert code == 0, f"pop not effective end-to-end; stderr:\n{err}"


def test_runner_identity_pop_leaves_monkeypatch_setenv_working():
    """The pop forecloses only the environment a test INHERITED; a test may
    still set the identity it needs with monkeypatch DURING the test, and the
    suite runs it — red-first proof the pop does not over-prune."""
    src = (
        "import os\n"
        "\n"
        "def test_can_set_after_pop(monkeypatch):\n"
        "    monkeypatch.setenv(\"AGI_SEAT\", \"seat\")\n"
        "    assert os.environ.get(\"AGI_SEAT\") == \"seat\"\n"
    )
    code, err = _run_identity_pop_subprocess(
        src, {"AGI_AGENT_ID": "z", "AGI_SEAT": "x", "AGI_POST": "y"})
    assert code == 0, f"monkeypatch.setenv blocked after pop; stderr:\n{err}"


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
