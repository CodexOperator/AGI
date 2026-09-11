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


def _run_pytest(path_args, env_extra, named_file=False, agent_root=None):
    """Run pytest against a throwaway dir that symlinks the real conftest.

    `agent_root`: the sessions root handed to the gate via
    AGI_AGENT_SESSIONS_ROOT. Default None -> an EMPTY (never created) dir, so
    no running agent record is an ancestor and the gate exercises its env
    fallback deterministically -- without the HOST's own real agent.json
    (always an ancestor of any pytest it spawns) injecting an unbreakable
    tier. Pass a fixture tree full of agent.json records to drive the
    record-derived branch instead.
    """
    import tempfile

    d = tempfile.mkdtemp()
    try:
        os.symlink(CONFTEST, os.path.join(d, "conftest.py"))
        with open(os.path.join(d, "test_a.py"), "w") as f:
            f.write(TEST_SRC)
        target = os.path.join(d, "test_a.py") if named_file else d
        env = dict(os.environ)
        if env_extra is None:
            env.pop("AGI_TIER", None)
        else:
            env["AGI_TIER"] = env_extra
        if agent_root is None:
            # Empty sessions root -> no record matches -> env fallback.
            env[gate.AGENT_RECORDS_ROOT_ENV] = os.path.join(d, "sessions")
        else:
            env[gate.AGENT_RECORDS_ROOT_ENV] = str(agent_root)
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", target, "-q"],
            capture_output=True, text=True, env=env,
        )
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
