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

#: The LIVE config the `live_config` offender below tries to read — the same
#: file test_live_config_cells.py is allowed to read and an opted-in module
#: is not. Computed from THIS file (never a literal), so the offender fails
#: on the GUARD, not on a missing path.
LIVE_CONFIG = (os.path.join(os.path.dirname(__file__), "..", "..", "..",
                            ".agi", "config.json"))


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


def _run_guarded_subprocess(test_src):
    """Run pytest against a throwaway dir that symlinks the real conftest and
    returns (rc, output). No identity env: the guard under test is opt-in by
    module attribute, not by env."""
    d = tempfile.mkdtemp()
    try:
        os.symlink(CONFTEST, os.path.join(d, "conftest.py"))
        with open(os.path.join(d, "test_a.py"), "w") as f:
            f.write(test_src)
        env = dict(os.environ)
        for _k in ("AGI_TIER", "AGI_AGENT_ID", "AGI_SEAT", "AGI_POST"):
            env.pop(_k, None)
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", os.path.join(d, "test_a.py"), "-q"],
            capture_output=True, text=True, env=env)
        return proc.returncode, proc.stdout + proc.stderr
    finally:
        shutil.rmtree(d)


_OPTIN_HEAD = "NO_REAL_PROCESSES = True\n"

#: One offending module per fenced resource, each the shape the pre-fix
#: test_rotate_term_grace.py actually had (a spawn, a /proc scan, a real
#: os.kill, a live config read).
OFFENDING_SRCS = {
    "spawn": _OPTIN_HEAD + (
        "import subprocess\n"
        "def test_offender():\n"
        "    subprocess.Popen(['true'])\n"),
    "fork": _OPTIN_HEAD + (
        "import os\n"
        "def test_offender():\n"
        "    os.fork()\n"),
    "proc": _OPTIN_HEAD + (
        "import pathlib\n"
        "def test_offender():\n"
        "    [p for p in pathlib.Path('/proc').iterdir()]\n"),
    "kill": _OPTIN_HEAD + (
        "import os, signal\n"
        "def test_offender():\n"
        "    os.kill(1, signal.SIGKILL)\n"),
    "live_config": _OPTIN_HEAD + (
        "import json, pathlib\n"
        "def test_offender():\n"
        f"    json.loads(pathlib.Path({str(LIVE_CONFIG)!r}).read_text())\n"),
}


def test_process_config_guard_fires_on_every_fenced_resource():
    """conftest's `_no_real_process_or_live_config` is IN FORCE, not merely
    documented: for each fenced resource a deliberately offending test in an
    opted-in module FAILS, and the guard's own message is the reason.

    Red-first: drop the fixture (or its opt-in read) and all five nested
    suites report rc 0 — the offenders would then really fork, really scan
    /proc and really signal pid 1."""
    for name, src in OFFENDING_SRCS.items():
        code, out = _run_guarded_subprocess(src)
        assert code != 0, f"guard did not fire on {name}:\n{out}"
        assert "NO_REAL_PROCESSES" in out, out


def test_process_config_guard_is_opt_in_not_blanket():
    """A module that does NOT opt in is untouched: the identical spawn, /proc
    scan and os.kill run, which is how the wider suite's legitimate `git`
    fixtures keep working."""
    code, out = _run_guarded_subprocess(
        "import os, signal, subprocess, pathlib\n"
        "def test_real_calls():\n"
        "    assert subprocess.run(['echo', 'ok'], capture_output=True)"
        ".stdout == b'ok\\n'\n"
        "    assert any(pathlib.Path('/proc').iterdir())\n"
        "    os.kill(os.getpid(), 0)\n")
    assert code == 0, f"guard over-reached a non-opted-in module:\n{out}"


def test_process_config_guard_lets_a_test_inject_its_own_seams():
    """The guard is a floor, not a wall: a test that monkeypatches AFTER the
    autouse fixture's setup wins for the test's duration (same ordering fact
    as `_no_real_tmux`). This is what makes the rewritten reap test's fake
    `os.kill` legal."""
    code, out = _run_guarded_subprocess(_OPTIN_HEAD + (
        "import os, signal, subprocess\n"
        "def test_injected(monkeypatch):\n"
        "    monkeypatch.setattr(os, 'kill', lambda p, s: None)\n"
        "    monkeypatch.setattr(subprocess, 'Popen', lambda *a, **k: None)\n"
        "    os.kill(424242, signal.SIGKILL)\n"
        "    subprocess.Popen(['true'])\n"))
    assert code == 0, f"guard blocked a test's own injected seams:\n{out}"


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
