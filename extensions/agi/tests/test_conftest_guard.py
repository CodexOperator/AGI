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
import signal
import subprocess
import sys
import tempfile
import types

import pytest

CONFTEST = os.path.join(os.path.dirname(__file__), "conftest.py")


def _load_tests_conftest():
    """`import conftest` would resolve to extensions/agi/conftest.py, so the
    tests-dir conftest (the file that OWNS the guard) is loaded by path.

    The env var tells that conftest this is a UNIT LOAD: a unit load must
    not install the session-wide import-time fence (and then uninstall it)
    under the running suite's feet."""
    import importlib.util  # noqa: PLC0415
    os.environ["AGI_TESTS_CONFTEST_UNIT_LOAD"] = "1"
    try:
        spec = importlib.util.spec_from_file_location("_tests_conftest", CONFTEST)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        os.environ.pop("AGI_TESTS_CONFTEST_UNIT_LOAD", None)
    return mod

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
        "    # signal 0 is an EXISTENCE PROBE: it delivers nothing, so this\n"
        "    # call is harmless even if the guard is deleted -- the test then\n"
        "    # fails on 'guard did not fire', never on a dead pid 1.\n"
        "    os.kill(1, 0)\n"),
    "kill_parent": _OPTIN_HEAD + (
        "import os, signal\n"
        "def test_offender():\n"
        "    # the parent pid is a pid this test never spawned; a signal-0\n"
        "    # probe on it is harmless and must still be refused.\n"
        "    os.kill(os.getppid(), 0)\n"),
    "import_time_kill": _OPTIN_HEAD + (
        "import os, signal\n"
        "# IMPORT time, where no fixture can guard it -- the hole of\n"
        "# residue 1 of verify_DH.440-k1: the import fence checked pid\n"
        "# membership alone, so this reached the real syscall. SIGCONT\n"
        "# cannot kill anything (its default action is 'continue'), so the\n"
        "# test is RED on the hole and harmless if the guard is deleted:\n"
        "# it never dies, it only fails to be refused.\n"
        "os.kill(os.getpid(), signal.SIGCONT)\n"
        "def test_offender():\n"
        "    raise SystemExit('guard did not fire')\n"),
    "bound_run": _OPTIN_HEAD + (
        "import rotate\n"
        "def test_offender():\n"
        "    # rotate._RUN was bound to subprocess.run AT IMPORT, so the\n"
        "    # stdlib hooks never see this call.\n"
        "    rotate._RUN(['true'])\n"),
    "bound_popen": _OPTIN_HEAD + (
        "import workflow\n"
        "def test_offender():\n"
        "    # workflow._REAL_POPEN IS the real class, captured at import:\n"
        "    # no stdlib hook can see this call at all.\n"
        "    workflow._REAL_POPEN(['true'])\n"),
    "system": _OPTIN_HEAD + (
        "import os\n"
        "def test_offender():\n"
        "    # os.system ran a REAL shell inside an opted-in module: the old\n"
        "    # fence listed four subprocess names and os.fork/forkpty only.\n"
        "    os.system('true')\n"),
    "execv": _OPTIN_HEAD + (
        "import os\n"
        "def test_offender():\n"
        "    # heal.py:1780 reaches os.execv; unfenced, this REPLACES the\n"
        "    # pytest process, so red-on-old is a silent rc 0 with no report.\n"
        "    os.execv('/bin/true', ['true'])\n"),
    "posix_spawn": _OPTIN_HEAD + (
        "import os\n"
        "def test_offender():\n"
        "    os.posix_spawn('/bin/true', ['true'], {})\n"),
    "pty_spawn": _OPTIN_HEAD + (
        "import pty\n"
        "def test_offender():\n"
        "    pty.spawn(['true'])\n"),
    "killpg": _OPTIN_HEAD + (
        "import os\n"
        "def test_offender():\n"
        "    # signal 0 delivers NOTHING, so this probe is harmless; the\n"
        "    # guard refuses the GROUP outright (see _make_guarded_killpg).\n"
        "    os.killpg(os.getpgid(0), 0)\n"),
    "import_time_spawn": _OPTIN_HEAD + (
        "import subprocess\n"
        "# NOT inside a test body: collection imports this module before any\n"
        "# fixture exists, so the function-scoped guard cannot see it.\n"
        "subprocess.run(['echo', 'IMPORT-TIME-SPAWN-ESCAPED'],"
        "capture_output=True)\n"),
    "import_time_system": _OPTIN_HEAD + (
        "import os\n"
        "os.system('true')  # a REAL shell at import time\n"),
    "live_config": _OPTIN_HEAD + (
        "import json, pathlib\n"
        "def test_offender():\n"
        f"    json.loads(pathlib.Path({str(LIVE_CONFIG)!r}).read_text())\n"),
}


def test_process_config_guard_fires_on_every_fenced_resource():
    """conftest's `_no_real_process_or_live_config` is IN FORCE, not merely
    documented, and so is the import-time fence that covers the leaves a
    function-scoped fixture cannot reach: for each fenced resource a
    deliberately offending test in an opted-in module FAILS, and the guard's
    own message is the reason.

    Red-first: drop the fixture (or its opt-in read) and every nested suite
    except the two import-time ones reports rc 0 — the offenders would then
    really fork, really run a shell, really scan /proc and really signal a
    pid. Drop the IMPORT-TIME fence and `import_time_spawn` reports rc 0
    again (its `echo` really runs at collection)."""
    for name, src in OFFENDING_SRCS.items():
        code, out = _run_guarded_subprocess(src)
        assert code != 0, f"guard did not fire on {name}:\n{out}"
        assert "NO_REAL_PROCESSES" in out, out


def test_import_time_fence_lets_a_plain_module_spawn_at_import():
    """The import-time fence is opt-in like the fixture, not a session-wide
    ban: a module with no `NO_REAL_PROCESSES` still spawns for real at
    collection, which is how the wider suite's own helpers keep working."""
    code, out = _run_guarded_subprocess(
        "import subprocess\n"
        "subprocess.run(['echo', 'ok'], capture_output=True)\n"
        "def test_x():\n"
        "    assert True\n")
    assert code == 0, f"import-time fence over-reached a plain module:\n{out}"


def test_unit_loading_the_conftest_leaves_the_session_fence_alone():
    """A unit load of conftest.py BY PATH (every leaf test above does it)
    must not install-then-remove the process-wide import-time fence: the
    stdlib this suite is using has to come out byte-identical."""
    before_run, before_popen = subprocess.run, subprocess.Popen
    _load_tests_conftest()
    assert subprocess.run is before_run, "unit load clobbered subprocess.run"
    assert subprocess.Popen is before_popen, "unit load clobbered subprocess.Popen"


def test_every_fenced_spawn_leaf_exists_and_is_fenced():
    """The leaf list is one source per rule, so a renamed or deleted stdlib
    leaf (or a typo in the name) must be RED here rather than silently
    unfenced at runtime."""
    leaves = _load_tests_conftest()._FENCED_SPAWN_LEAVES
    resolved = _load_tests_conftest()._resolve_leaves(leaves)
    assert len(resolved) == len(leaves), (
        "these fenced leaves do not exist in this interpreter -- the fence "
        f"is dead weight: {[m + '.' + a for m, a in leaves[len(resolved):]]}")
    names = {f"{m.__name__}.{a}" for m, a in resolved}
    for required in ("os.system", "os.execv", "os.posix_spawn", "pty.spawn",
                     "subprocess.Popen", "os.fork"):
        assert required in names, f"{required} is not in the fence: {sorted(names)}"


def test_spawn_fence_install_and_uninstall_restore_the_module():
    """The import-time fence is undo-able: install it on a STUB module (never
    on os/subprocess, which the running suite is using) and assert (a) a
    caller that has not opted in still reaches the real leaf and (b) the
    ORIGINAL leaf object is back after uninstall. Without this the fence
    would outlive the session that installed it."""
    import types  # noqa: PLC0415
    cf = _load_tests_conftest()
    real = lambda *a, **k: "real"  # noqa: E731 -- a stub, not a spawn
    stub = types.SimpleNamespace(run=real)
    saved = cf._install_spawn_fence(leaves=((stub, "run"),), kills=False)
    assert stub.run() == "real", "a caller that never opted in must pass through"
    assert stub.run.__name__.startswith("_import_fence"), "fence not installed"
    cf._uninstall_spawn_fence(saved)
    assert stub.run is real, "uninstall did not restore the real leaf"


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
        # signal 0, never SIGKILL: pids on this box pass 4 million, so a
        # fixed pid can be LIVE -- drop the patch line above by mistake and
        # a SIGKILL here would land on a stranger (DH.422 harvest)
        "    os.kill(424242, 0)\n"
        "    subprocess.Popen(['true'])\n"))
    assert code == 0, f"guard blocked a test's own injected seams:\n{out}"


# --- the kill leaf, unit-tested with a recorder instead of a live pid -----
#
# These three are the CONJUNCTIVE half: the guard above proves the fixture
# fires end-to-end, and these prove the leaf itself still refuses. Delete
# the parent-pid fix, or the bound-runner fence, and this file goes RED
# rather than quietly weaker.


def test_guarded_kill_refuses_parent_pid_and_arms_no_syscall():
    """conftest._make_guarded_kill routes ONLY the caller's own pid to the
    real `os.kill`, and the recorder proves no other pid ever reached it --
    including the parent, which the guard used to exempt."""
    calls = []
    guarded = _load_tests_conftest()._make_guarded_kill(
        lambda pid, sig, *a, **k: calls.append((pid, sig)), frozenset({4242}))

    guarded(4242, 0)                       # own pid, liveness probe: allowed
    for foreign in (os.getppid(), os.getpid(), 1, 4243):
        with pytest.raises(AssertionError, match="NO_REAL_PROCESSES"):
            guarded(foreign, signal.SIGKILL)
    assert calls == [(4242, 0)], f"a real syscall was armed: {calls}"


def test_guarded_killpg_refuses_outright_and_arms_no_syscall():
    """conftest._make_guarded_killpg refuses a process GROUP without calling
    through: a group leader the test spawned can share a group with a shell
    the test never spawned, so no pid is exempt. The recorder proves the real
    killpg is never reached -- no live group is ever signalled by this file.
    The probe itself is signal 0 (delivers nothing) in the offender table."""
    calls = []
    guarded = _load_tests_conftest()._make_guarded_killpg(
        lambda pgid, sig, *a, **k: calls.append((pgid, sig)))
    for pgid in (os.getpgrp(), os.getpid(), 1, 4242):
        with pytest.raises(AssertionError, match="NO_REAL_PROCESSES"):
            guarded(pgid, 0)
    with pytest.raises(AssertionError, match="process GROUP"):
        guarded(os.getpgrp(), signal.SIGTERM)
    assert calls == [], f"a real killpg was armed: {calls}"


def test_the_guard_offender_table_arms_no_fatal_signal():
    """The guard's own red-first proof is MOCKED, never armed: no entry in
    OFFENDING_SRCS sends a fatal signal to a pid the test did not spawn, so
    dropping the guard can only make this file red, never this box."""
    for name, src in OFFENDING_SRCS.items():
        assert "SIGKILL" not in src and "SIGTERM" not in src, (
            f"offender {name!r} arms a real signal -- use signal 0")


def test_fenced_module_runners_cover_the_engines_bound_names():
    """The stdlib hooks are not enough: the engine BOUNDS subprocess.run at
    import (`rotate._RUN`, `workflow._REAL_POPEN/_REAL_RUN`), so the fence
    must name every binding. A new bound name the engine adds is a residue
    this assertion surfaces as a failing import/name, not as a silent gap."""
    fenced = set(_load_tests_conftest()._FENCED_MODULE_RUNNERS)
    import rotate  # noqa: PLC0415
    import workflow  # noqa: PLC0415
    assert ("rotate", "_RUN") in fenced, "rotate._RUN is a real captured run"
    for mod_name, attr in (("rotate", "_RUN"),
                           ("workflow", "_REAL_POPEN"),
                           ("workflow", "_REAL_RUN")):
        bound = getattr({"rotate": rotate, "workflow": workflow}[mod_name], attr)
        assert callable(bound), f"{mod_name}.{attr} vanished; update the fence"
    assert getattr(rotate._RUN, "__module__", "") == "subprocess", (
        "rotate._RUN is no longer the stdlib run captured at import -- the "
        "fence premise changed and this list must be re-derived")

def test_a_second_conftest_exec_wraps_no_already_fenced_leaf():
    """hypothesis:conftest-spawn-fence-install-is-idempotent-across-a-second-conftest-exec

    test_tier_gate.py loads conftest.py a SECOND time in one interpreter, so
    `_install_spawn_fence()` runs twice over the same leaves. A fence over a
    fence made `subprocess.Popen is workflow._REAL_POPEN` (workflow.py:1806)
    false, and 48 tests that pass ALONE went red under full-dir collection.

    Red-first: drop the `_FENCE_MARKER` skip in `_install_spawn_fence` and the
    identity assertion below fails (the second exec replaces the leaf with a
    NEW fence object) and `second` is no longer empty."""
    conf = _load_tests_conftest()
    real = lambda *a, **k: "real"  # noqa: E731 -- a stub, not a spawn
    stub = types.SimpleNamespace(run=real)
    leaves = ((stub, "run"),)
    first = conf._install_spawn_fence(leaves=leaves, kills=False)
    fenced = stub.run
    second = conf._install_spawn_fence(leaves=leaves, kills=False)
    assert stub.run is fenced, "a second exec wrapped an already-fenced leaf"
    assert second == [], "the second exec saved an undo for a leaf it skipped"
    conf._uninstall_spawn_fence(second)          # must be a no-op
    assert stub.run is fenced, "the second exec's uninstall tore down the first"
    conf._uninstall_spawn_fence(first)
    assert stub.run is real, "the first exec's uninstall did not restore"
    # Live half: the running interpreter's own conftest already fenced the
    # real leaves, so a second exec over them must also change nothing.
    if hasattr(subprocess.Popen, conf._FENCE_MARKER):
        was = subprocess.Popen
        again = conf._install_spawn_fence()
        try:
            assert subprocess.Popen is was, (
                "a second exec re-fenced the live conftest's subprocess.Popen; "
                "every engine `is _REAL_POPEN` check then fails")
        finally:
            conf._uninstall_spawn_fence(again)
        assert subprocess.Popen is was, "the second exec's uninstall tore it down"


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


def test_the_kill_fence_is_idempotent_across_a_second_install(monkeypatch):
    """RESIDUE 1 of verify_DH.424-k1: the `_FENCE_MARKER` skip in
    `_install_spawn_fence`'s kill branch was UNTESTED -- only the leaf loop
    had a row. Drop that one `continue` and this goes red.

    (a) is the honest seam here: the kill branch reads `getattr(os, attr)`
    from the module-global `os` of conftest, NOT from the caller's leaf list,
    so the stub's leaves can only be the thing under test if conftest's own
    `os` name IS the stub for the duration (monkeypatch restores it after).

    The stub is a SimpleNamespace (house style) and NOTHING is signalled: the
    fences are installed, compared by identity and uninstalled without ever
    being called."""
    conf = _load_tests_conftest()
    real = lambda *a, **k: "real"  # noqa: E731 -- a stub, never a signal
    stub = types.SimpleNamespace(kill=real, killpg=real)
    monkeypatch.setattr(conf, "os", stub)   # (a): the branch's real source
    first = conf._install_spawn_fence(leaves=(), kills=True)
    fenced_kill, fenced_killpg = stub.kill, stub.killpg
    assert fenced_kill is not real, "the kill fence was not installed at all"
    second = conf._install_spawn_fence(leaves=(), kills=True)
    try:
        assert second == [], (
            "a second exec re-fenced os.kill/os.killpg: "
            f"{[getattr(m, a) for m, a, _ in second]}")
        assert stub.kill is fenced_kill, "a fence went over the kill fence"
        assert stub.killpg is fenced_killpg, "a fence went over the killpg fence"
    finally:
        conf._uninstall_spawn_fence(second)      # no-op when idempotent
        conf._uninstall_spawn_fence(first)
    assert stub.kill is real and stub.killpg is real, "uninstall did not restore"


def test_a_second_install_over_live_leaves_changes_no_leaf():
    """RESIDUE 2 of verify_DH.424-k1: the live half of the idempotence row
    asserted ONE leaf (`subprocess.Popen`), so any OTHER entry of
    `_FENCED_SPAWN_LEAVES` -- or the kill pair -- could lose the marker skip
    and the row stayed green. This row covers EVERY leaf.

    The live tree is not uniformly marked: autouse fixtures REPLACE
    subprocess.run (the tmux `_guarded_run`) and os.kill/os.killpg
    (`_make_guarded_kill`), and those replacements carry no marker. So the
    honest live shape is "install once, then a SECOND install is a no-op",
    which is exactly the hypothesis; the first install's undo list is what
    puts the interpreter back exactly as it was found. No fence is ever
    called, and no process is touched."""
    conf = _load_tests_conftest()
    live = conf._resolve_leaves()
    before = [(m, a, getattr(m, a)) for m, a in live]
    before += [(os, a, getattr(os, a)) for a in ("kill", "killpg")]
    assert any(hasattr(o, conf._FENCE_MARKER) for _, _, o in before), (
        "the session conftest has fenced nothing; this row's premise is that "
        "a SECOND install meets leaves the first one already fenced")
    first = conf._install_spawn_fence()      # fills whatever a fixture swapped
    fenced = [(m, a, getattr(m, a)) for m, a, _real in first]
    again = conf._install_spawn_fence()      # the second exec, under test
    try:
        assert again == [], (
            "a second exec re-fenced: "
            f"{[f'{m.__name__}.{a}' for m, a, _ in again]} -- every engine "
            "`is _REAL_POPEN` check then fails")
        for m, a, now in fenced:
            assert getattr(m, a) is now, (
                f"{m.__name__}.{a} changed identity across a second install: "
                f"{getattr(m, a)} replaced {now}")
    finally:
        conf._uninstall_spawn_fence(again)   # no-op when idempotent
        conf._uninstall_spawn_fence(first)   # back to exactly `before`
    for m, a, was in before:
        assert getattr(m, a) is was, (
            f"{getattr(m, '__name__', m)}.{a} left the interpreter fenced "
            "differently than the row found it")
    assert fenced, "the first install fenced nothing; the row proved no idempotence"
