"""Tests for the L4-tier full-suite gate (hypothesis:l4-full-suite-tier-gate).

The testable claim: a conftest.py in extensions/agi/tests/ REFUSES a bare
whole-directory pytest run when AGI_TIER=kid, names a one-line reason with the
variable and the fix, and is invisible at every other tier (and when unset).

These tests exercise BOTH branches directly:
  - decision unit test: _is_bare_directory_run() on the three invocation shapes
  - hook integration test: subprocess runs of the real conftest under
    AGI_TIER=kid (bare dir refused, named file / -k passed) and AGI_TIER unset
    / parent (bare dir passed unchanged).
"""
import copy
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

CONFTEST = os.path.join(os.path.dirname(__file__), "conftest.py")

# Load the gate BY PATH, not as `extensions.agi.tests.conftest`.
# The package-path import only resolves when the repo root happens to be on
# sys.path -- i.e. when pytest is invoked with a cwd inside it. `commands.py
# run tests` and `verification.py --suite` run the declared argv with cwd set
# to the GRAPH root (`.agi/`), where it is not, and the ImportError there is a
# COLLECTION error: it aborts the whole run, so the entire suite reports as
# failed with zero tests executed. A test module must not depend on the cwd it
# was launched from. (Found at merge-up 3; hypothesis:l4-full-suite-tier-gate.)
_spec = importlib.util.spec_from_file_location("_agi_tier_gate_conftest", CONFTEST)
gate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gate)

TEST_SRC = 'def test_ok():\n    assert True\n'

#: Sentinel for _run_pytest.agent_root: an EMPTY throwaway sessions dir, so
#: no running record is an ancestor and the env fallback decides — without
#: depending on whatever the live tree holds.
_EMPTY = object()


class _Opt:
    def __init__(self, keyword=""):
        self.keyword = keyword
        self.kw = None


class _Cfg:
    def __init__(self, args, keyword=""):
        self.args = list(args)
        self.option = _Opt(keyword)


def test_decision_bare_directory_kid_refuses():
    assert gate._is_bare_directory_run(_Cfg(["extensions/agi/tests/"])) is True
    assert gate._is_bare_directory_run(_Cfg([])) is True


def test_decision_named_file_passes():
    assert gate._is_bare_directory_run(
        _Cfg(["extensions/agi/tests/test_send.py"])
    ) is False


def test_decision_k_filter_passes_even_on_directory():
    assert gate._is_bare_directory_run(
        _Cfg(["extensions/agi/tests/"], keyword="send")
    ) is False


def _run_pytest(path_args, env_extra, named_file=False, agent_root=_EMPTY,
                outer_pytest=True, env_seam=None, extra_argv=()):
    """Run pytest against a throwaway dir that symlinks the real conftest.

    `agent_root`: the sessions root handed to the gate via the TEST-ONLY
    `--agent-records-root` option.
      * `_EMPTY` (default) -> a fresh EMPTY throwaway sessions dir, so no
        running record is an ancestor and the env/record fallback decides
        deterministically (independent of whatever the live tree holds).
      * a path -> passed as `--agent-records-root=<path>` to exercise the
        record-derived branch.
      * `None` -> NO option and no env seam: the tree-derived root is used
        (exercises the bare-shell production path).

    `outer_pytest=True` (the default, a nested run under this suite) leaves
    PYTEST_CURRENT_TEST in the env, so the option is honored.
    `outer_pytest=False` simulates a BARE SHELL kid: PYTEST_CURRENT_TEST is
    stripped, so the option (and any env-seam) is ignored and the root is
    always the tree.

    `env_seam`: if not None, sets the OLD dead env var AGI_AGENT_SESSIONS_ROOT
    in the child env, to prove the gate ignores it (the env-seam falsifier).
    Normally the env var is simply popped, so a leftover value in the host
    environment cannot leak into a nested scan.
    """
    import tempfile

    d = tempfile.mkdtemp()
    try:
        os.symlink(CONFTEST, os.path.join(d, "conftest.py"))
        with open(os.path.join(d, "test_a.py"), "w") as f:
            f.write(TEST_SRC)
        target = os.path.join(d, "test_a.py") if named_file else d
        env = dict(os.environ)
        env.pop("AGI_TIER", None)
        if env_extra is not None:
            env["AGI_TIER"] = env_extra
        # The env seam is dead (hypothesis:l4-the-kid-tier-gate-has-no-env-
        # seam): never carry it into the child; the only root is tree- or
        # option-derived. `env_seam` is an explicit re-add for the falsifier.
        env.pop(gate.AGENT_RECORDS_ROOT_ENV, None)
        if env_seam is not None:
            env[gate.AGENT_RECORDS_ROOT_ENV] = str(env_seam)
        if not outer_pytest:
            env.pop("PYTEST_CURRENT_TEST", None)
        argv = [sys.executable, "-m", "pytest", target, "-q"]
        if agent_root is _EMPTY:
            argv.append("--agent-records-root=" + os.path.join(d, "sessions"))
        elif agent_root is not None:
            argv.append(f"--agent-records-root={agent_root}")
        argv.extend(extra_argv)
        proc = subprocess.run(argv, capture_output=True, text=True, env=env)
        return proc.returncode, proc.stderr
    finally:
        import shutil
        shutil.rmtree(d)


def test_hook_bare_directory_kid_refused():
    code, err = _run_pytest([], "kid")
    assert code == 4  # pytest.UsageError
    assert "AGI_TIER=kid" in err
    assert "specific test file or a -k filter" in err


def test_hook_named_file_kid_passes():
    code, _ = _run_pytest([], "kid", named_file=True)
    assert code == 0


def test_hook_unset_bare_dir_invisible():
    code, _ = _run_pytest([], None)
    assert code == 0


def test_hook_parent_bare_dir_invisible():
    code, _ = _run_pytest([], "parent")
    assert code == 0


def _write_agent_record(sessions_root, agent_dir, pid, tier, status="running"):
    """Write a fixture agent.json; return the dir that rglob would find."""
    d = Path(sessions_root) / f"iter-test/{agent_dir}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "agent.json").write_text(json.dumps({
        "id": agent_dir, "status": status, "tier": tier, "pid": pid}))
    return d


# --- fix: tier derives from the running agent record ancestor chain ---------
# hypothesis:l4-the-kid-tier-gate-is-not-clearable-from-inside-a-kid. The
# gate must derive the tier from the agent.json whose pid is an ANCESTOR of
# the pytest process (status: running), falling back to AGI_TIER only when no
# record matches -- so `env -u AGI_TIER` no longer clears a kid's gate.

def test_decision_ancestor_resolution_core():
    """Pure decision: nearest running ancestor wins; none -> fallback."""
    # fake ancestor chain: the process 222 -> 111 -> 55 -> 1 (dead end)
    lookup = {222: 111, 111: 55, 55: 1, 1: None}
    # the process itself has NO record; a kid at 111 (mid-chain) is found
    assert gate._resolve_tier_from_ancestors(
        {111: "kid", 55: "director"}, lookup.get, 222) == "kid"
    # nearest ancestor wins: a record at 222 (self) beats 55
    assert gate._resolve_tier_from_ancestors(
        {222: "parent", 55: "kid"}, lookup.get, 222) == "parent"
    # a parent at 222 beats a kid at 55 (nearer wins, not higher-tier)
    assert gate._resolve_tier_from_ancestors(
        {222: "parent", 55: "kid"}, lookup.get, 222) == "parent"
    # no record anywhere on the chain -> None (env fallback still decides)
    assert gate._resolve_tier_from_ancestors(
        {888: "kid"}, lookup.get, 222) is None
    # empty map -> None
    assert gate._resolve_tier_from_ancestors({}, lookup.get, 222) is None


def test_hook_kid_ancestor_refuses_bare_dir_with_env_unset():
    """THE fix proof. A running agent.json with tier=kid whose pid is an
    ancestor of the nested pytest, AGI_TIER UNSET, must still refuse a bare
    directory run -- unsetting the env var can no longer clear the gate.
    """
    import tempfile
    root = tempfile.mkdtemp()
    try:
        # The HOST test process (os.getpid) is the direct parent of the nested
        # pytest, so its pid lies on the nested process's ancestor chain.
        _write_agent_record(root, "kid1", os.getpid(), "kid", status="running")
        code, err = _run_pytest([], None, agent_root=root)
        assert code == 4, f"expected refusal, got {code}: {err}"
        assert "AGI_TIER=kid" in err
        assert "specific test file or a -k filter" in err
    finally:
        import shutil
        shutil.rmtree(root)


def test_hook_kid_ancestor_named_file_passes_with_env_unset():
    """The record-derived kid must still be able to run a NAMED file (its
    own targeted tests), only the bare directory is refused.
    """
    import tempfile
    root = tempfile.mkdtemp()
    try:
        _write_agent_record(root, "kid1", os.getpid(), "kid", status="running")
        code, err = _run_pytest([], None, named_file=True, agent_root=root)
        assert code == 0, f"named-file run should pass, got {code}: {err}"
    finally:
        import shutil
        shutil.rmtree(root)


def test_hook_parent_ancestor_bare_dir_allowed_with_env_unset():
    """A running record with tier=parent (the director/prime) allows a bare
    directory run even with AGI_TIER unset -- the gate reads the real tier.
    """
    import tempfile
    root = tempfile.mkdtemp()
    try:
        _write_agent_record(root, "dir1", os.getpid(), "parent", status="running")
        code, err = _run_pytest([], None, agent_root=root)
        assert code == 0, f"parent bare-dir should pass, got {code}: {err}"
    finally:
        import shutil
        shutil.rmtree(root)


def test_hook_stale_nonrunning_ancestor_record_is_ignored():
    """Only status == "running" records count; a done record must NOT cradle
    the gate, so a stale agent.json from a finished sibling can't lock a live
    parent out of the bare-directory run.
    """
    import tempfile
    root = tempfile.mkdtemp()
    try:
        _write_agent_record(root, "oldkid", os.getpid(), "kid", status="done")
        code, err = _run_pytest([], None, agent_root=root)
        assert code == 0, f"non-running record must be ignored, got {code}: {err}"
    finally:
        import shutil
        shutil.rmtree(root)


def test_module_collects_with_cwd_outside_the_repo_root(tmp_path):
    """This module must import no matter where pytest was launched from.

    It previously did `from extensions.agi.tests import conftest`, which only
    resolves when the repo root happens to be on sys.path — true when pytest is
    invoked with a cwd inside the repo, false when `commands.py run tests` and
    `verification.py --suite` run the declared argv with cwd set to the GRAPH
    root (`.agi/`). An ImportError at module scope is a COLLECTION error, so it
    does not fail one test: it aborts the run and reports the WHOLE suite as
    failed with zero tests executed. Found at merge-up 3 by running the suite
    through the tool rather than by hand.

    The guard is a real collection from a cwd that cannot possibly have the
    repo root on sys.path.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", os.path.abspath(__file__),
         "-q", "--collect-only"],
        cwd=str(tmp_path), capture_output=True, text=True, timeout=300)
    assert proc.returncode == 0, (
        "collection failed from a foreign cwd — the module has a cwd-dependent "
        f"import again:\n{proc.stdout[-2000:]}\n{proc.stderr[-2000:]}")
    assert "ModuleNotFoundError" not in (proc.stdout + proc.stderr)
    assert os.path.isfile(os.path.join(here, "conftest.py"))


# --- fix: the gate has NO env seam (hypothesis:l4-the-kid-tier-gate-has-  ---
# --- no-env-seam). The production root is ALWAYS tree-derived; the only  ---
# --- re-root is the TEST-ONLY --agent-records-root option, guarded by an ---
# --- outer PYTEST_CURRENT_TEST. A kid can neither set an env var nor (in ---
# --- bare shell) pass the flag to point the scan at a non-kid root.     ---


def test_falsifier_env_seam_dead_kid_still_refuses():
    """FALSIFIER. AGI_TIER UNSET and the OLD dead env var
    AGI_AGENT_SESSIONS_ROOT pointed at an EMPTY throwaway dir: the record
    root must be tree/option derived, NOT the env var, so a planted kid
    record (ancestor pid) still refuses a bare-directory run. Before this
    fix, setting the var to an empty root scanned nothing and the bare dir
    run exited 0.
    """
    import tempfile
    root = tempfile.mkdtemp()
    empty = tempfile.mkdtemp()  # the throwaway dir the env seam would point at
    try:
        _write_agent_record(root, "kid1", os.getpid(), "kid", status="running")
        code, err = _run_pytest([], None, agent_root=root, env_seam=empty)
        assert code == 4, f"expected refusal, got {code}: {err}"
        assert "AGI_TIER=kid" in err
        assert "specific test file or a -k filter" in err
    finally:
        import shutil
        shutil.rmtree(root)
        shutil.rmtree(empty)


def test_falsifier_kid_record_wins_over_env_tier_and_seam_root():
    """Even AGI_TIER=parent (the old env fallback) cannot clear a kid whose
    record is on the ancestor chain, and the dead env seam pointing at an
    empty root changes nothing either: the record wins over both.
    """
    import tempfile
    root = tempfile.mkdtemp()
    empty = tempfile.mkdtemp()
    try:
        _write_agent_record(root, "kid1", os.getpid(), "kid", status="running")
        code, err = _run_pytest([], "parent", agent_root=root, env_seam=empty)
        assert code == 4, f"expected refusal, got {code}: {err}"
        assert "AGI_TIER=kid" in err
    finally:
        import shutil
        shutil.rmtree(root)
        shutil.rmtree(empty)


def test_falsifier_recorded_kid_named_file_still_passes():
    """The record-derived kid must still run a NAMED file through the
    test-only seam -- only the bare directory is refused.
    """
    import tempfile
    root = tempfile.mkdtemp()
    try:
        _write_agent_record(root, "kid1", os.getpid(), "kid", status="running")
        code, err = _run_pytest([], None, named_file=True, agent_root=root)
        assert code == 0, f"named-file run should pass, got {code}: {err}"
    finally:
        import shutil
        shutil.rmtree(root)


def test_falsifier_no_record_tier_unset_passes_unchanged():
    """A plain run with no planted record and AGI_TIER unset still passes."""
    code, _ = _run_pytest([], None)  # _EMPTY root -> no record -> fallback
    assert code == 0


def test_bare_shell_kid_cannot_clear_gate_with_the_flag():
    """FALSIFIER (bare shell). With PYTEST_CURRENT_TEST absent the
    --agent-records-root option is IGNORED: the root is tree-derived, so a
    planted kid record in the REAL tree refuses the bare-directory run even
    when the kid points the flag at an empty throwaway dir.
    """
    import tempfile
    tree_root = gate._default_record_root()
    assert tree_root, "tree-derived root must resolve"
    marker = Path(tree_root) / "iter-envseam-test"
    empty = tempfile.mkdtemp()
    try:
        _write_agent_record(marker, "kidshell", os.getpid(), "kid",
                            status="running")
        code, err = _run_pytest(
            [], None, agent_root=empty, outer_pytest=False)
        assert code == 4, f"expected refusal, got {code}: {err}"
        assert "AGI_TIER=kid" in err
    finally:
        import shutil
        shutil.rmtree(empty)
        if marker.exists():
            shutil.rmtree(marker)
