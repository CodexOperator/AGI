"""Tests for the L4-tier full-suite gate (hypothesis:l4-full-suite-tier-gate).

The testable claim: a conftest.py in extensions/agi/tests/ REFUSES a bare
whole-directory pytest run when the effective tier is kid, names a one-line
reason with the fix, and is invisible at every other tier (and when unset).

Which tier? The gate derives it from the running agent record whose pid is an
ANCESTOR of the pytest process (hypothesis:l4-the-kid-tier-gate-is-not-
clearable-from-inside-a-kid), falling back to AGI_TIER. And the record root
is ALWAYS the resolved project tree (hypothesis:l4-the-kid-tier-gate-has-no-
env-seam, hypothesis:l4-the-record-root-has-no-test-seam-either): there is
NO --agent-records-root option and NO env var that moves the scan, so a kid
cannot clear the gate by pointing it at an empty root.

Those tests exercise BOTH branches directly:
  - decision unit test: _is_bare_directory_run() on the three invocation shapes
  - hook integration test: subprocess runs of the real conftest under a
    planted kid record / AGI_TIER=kid (bare dir refused, named file / -k
    passed) and AGI_TIER unset / parent (bare dir passed unchanged).

The subprocess falsifier tests plant their running agent record under the
REAL tree's sessions dir in a throwaway `iter-test-<uuid>` dir and remove it
in `finally` -- the only seam a subprocess test has now that the option is
gone. The in-process tests monkeypatch `_default_record_root` instead.
"""
import copy
import importlib.util
import json
import os
import subprocess
import sys
import uuid
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


# --- the record root has NO test seam (hypothesis:l4-the-record-root-has-  ---
# --- no-test-seam-either). _record_root() IS _default_record_root() and  ---
# --- nothing else; the option/global/PYTEST_CURRENT_TEST guard are gone.  ---


def test_decision_record_root_is_always_tree_derived(monkeypatch):
    """_record_root() returns _default_record_root() and nothing else. The
    only way a test moves the scan is monkeypatching _default_record_root
    (the in-process seam); no option, no global, no env var.
    """
    monkeypatch.setattr(gate, "_default_record_root", lambda: "/seam/path")
    assert gate._record_root() == "/seam/path"


def test_decision_no_option_and_no_env_seam_remain():
    """The old mechanism is fully gone: no pytest_addoption hook, no
    _TEST_AGENT_RECORDS_ROOT global, no dead AGENT_RECORDS_ROOT_ENV const,
    and the record root ignores a spoofed (actually non-existent) env var the
    old guard would have trusted (PYTEST_CURRENT_TEST).
    """
    assert not hasattr(gate, "pytest_addoption")
    assert not hasattr(gate, "_TEST_AGENT_RECORDS_ROOT")
    assert not hasattr(gate, "AGENT_RECORDS_ROOT_ENV")


def test_decision_record_root_ignores_spoofed_env_and_seam():
    """A spoofed PYTEST_CURRENT_TEST / AGI_AGENT_SESSIONS_ROOT in the
    environment changes nothing: the root is always the tree-derived root.
    """
    import tempfile
    empty = tempfile.mkdtemp()
    try:
        monkey = {"PYTEST_CURRENT_TEST": "spoofed::test",
                  "AGI_AGENT_SESSIONS_ROOT": empty}
        saved = {k: os.environ.get(k) for k in monkey}
        for k, v in monkey.items():
            os.environ[k] = v
        try:
            root = gate._record_root()
        finally:
            for k, v in saved.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
        assert root == gate._default_record_root()
        assert root != empty
    finally:
        import shutil
        shutil.rmtree(empty)


def _write_agent_record(sessions_root, agent_dir, pid, tier, status="running"):
    """Write a fixture agent.json under `sessions_root`; return the dir that
    rglob would find."""
    d = Path(sessions_root) / f"iter-test/{agent_dir}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "agent.json").write_text(json.dumps({
        "id": agent_dir, "status": status, "tier": tier, "pid": pid}))
    return d


def _plant_in_tree(tier, status="running"):
    """Plant a running (or stale, per `status`) agent.json whose pid is THIS
    process -- an ANCESTOR of the nested pytest -- under the REAL tree's
    sessions dir, in a throwaway `iter-test-<uuid>` dir.

    This is the subprocess-falsifier seam now that --agent-records-root is
    gone (hypothesis:l4-the-record-root-has-no-test-seam-either): the record
    has to live where the gate actually scans, and the caller removes it in
    `finally`. Returns the throwaway marker dir (its parent to clean up).
    """
    tree_root = gate._default_record_root()
    assert tree_root, "tree-derived record root must resolve"
    marker = Path(tree_root) / f"iter-test-{uuid.uuid4().hex[:8]}"
    marker.mkdir(parents=True, exist_ok=True)
    _write_agent_record(marker, "rec", os.getpid(), tier, status=status)
    return marker


def _run_pytest(path_args, env_extra, named_file=False, plant_tier="",
                plant_status="running", env_seam=None, extra_argv=(),
                plant_marker=None):
    """Run pytest against a throwaway dir that symlinks the real conftest.

    `env_extra`: what to set AGI_TIER to in the child env; None leaves it unset.
    `plant_tier`: when non-empty, plant a running agent record (an ancestor
      pid) in the REAL tree's sessions dir for the run and remove it in
      finally. `plant_status` overrides the record's status.
    `env_seam`: if not None, sets the OLD dead env var AGI_AGENT_SESSIONS_ROOT
      in the child env, to prove the gate ignores it (the env-seam falsifier).
    `extra_argv`: extra pytest argv (e.g. a stale --agent-records-root flag) to
      prove no flag can clear the gate.
    `plant_marker`: an externally-created throwaway dir (e.g. one a test
      planted itself) for this run to own and remove in finally, instead of
      creating a fresh one. Only meaningful with `plant_tier`/`plant_status`.
    """
    import tempfile

    d = tempfile.mkdtemp()
    marker = None
    try:
        os.symlink(CONFTEST, os.path.join(d, "conftest.py"))
        with open(os.path.join(d, "test_a.py"), "w") as f:
            f.write(TEST_SRC)
        target = os.path.join(d, "test_a.py") if named_file else d
        env = dict(os.environ)
        env.pop("AGI_TIER", None)
        if env_extra is not None:
            env["AGI_TIER"] = env_extra
        # The env seam is dead: never carry it into the child; the only root
        # is the tree. `env_seam` is an explicit re-add for the falsifier.
        env.pop("AGI_AGENT_SESSIONS_ROOT", None)
        if env_seam is not None:
            env["AGI_AGENT_SESSIONS_ROOT"] = str(env_seam)
        if plant_marker is not None:
            marker = plant_marker
        elif plant_tier:
            marker = _plant_in_tree(plant_tier, plant_status)
        argv = [sys.executable, "-m", "pytest", target, "-q"]
        argv.extend(extra_argv)
        proc = subprocess.run(argv, capture_output=True, text=True, env=env)
        return proc.returncode, proc.stderr
    finally:
        import shutil
        shutil.rmtree(d)
        if marker is not None and marker.exists():
            shutil.rmtree(marker)


def test_hook_bare_directory_kid_refused():
    # Plant a kid record at THIS process's own pid so the nested pytest's
    # NEAREST running ancestor is a kid even when an ambient parent/director
    # record (this suite sometimes runs under one) is a farther ancestor.
    # Merged-map nearest-wins makes the planted kid decisive under any
    # runtime; without the plant, a live parent on the chain would supply the
    # tier and the bare-directory refusal would be skipped (the Defect 1 that
    # made this RED under a live parent runner).
    code, err = _run_pytest([], "kid", plant_tier="kid")
    assert code == 4  # pytest.UsageError
    assert "AGI_TIER=kid" in err
    assert "specific test file or a -k filter" in err


def test_hook_named_file_kid_passes():
    code, _ = _run_pytest([], "kid", named_file=True)
    assert code == 0


def test_hook_unset_bare_dir_invisible():
    """With AGI_TIER UNSET and the nearest running ancestor a PARENT record,
    the bare directory run passes -- the gate is invisible at non-kid tiers.
    A parent record must be planted because this suite itself RUNS as a kid
    (its dispatch record is a real running ancestor), so "no kid on the
    chain" is unreachable by real-tree subprocess; nearest-wins makes the
    planted parent the decisive ancestor.
    """
    code, _ = _run_pytest([], None, plant_tier="parent")
    assert code == 0


def test_hook_parent_bare_dir_invisible():
    """A parent record (nearest ancestor) + AGI_TIER=parent: passes unchanged.
    """
    code, _ = _run_pytest([], "parent", plant_tier="parent")
    assert code == 0


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


def test_decision_effective_tier_is_root_order_independent(monkeypatch):
    """The pid->tier map is GLOBAL: every root's running records are merged
    into ONE dict before the ancestor chain resolves, so the outcome is
    independent of root scan order. A pytest process has multiple records on
    its chain (its own kid record AND the parent that spawned it). The old
    per-root code returned the FIRST root with ANY ancestor hit, so a kid
    whose own record sat in a later-scanned root while a parent record sat in
    an earlier-scanned root CLEARED the gate (root order flipped the verdict).
    Merged + nearest-wins fixes it: the process's own pid is the nearest
    ancestor, so its own record always wins. (hypothesis:l4-the-kid-tier-
    gate-scans-every-root-it-can-reach)
    """
    own = os.getpid()
    parent_pid = own + 1000_000  # a distinct pid higher on the ancestor chain
    fake_ppid = {own: parent_pid, parent_pid: None}

    def fake_records(root):
        # The root scanned first (R1) holds ONLY the distant PARENT record;
        # the later root (R2) holds the process's OWN kid record. On the old
        # per-root code, order ['R1','R2'] resolved the parent (gate cleared)
        # and ['R2','R1'] resolved the kid (refused) -- the same bytes, a
        # different verdict, decided by scan order alone.
        return {parent_pid: "parent"} if root == "R1" else {own: "kid"}

    monkeypatch.setattr(gate, "_running_record_tiers", fake_records)
    monkeypatch.setattr(gate, "_ppid_of", lambda p: fake_ppid.get(p))
    # safe against a host AGI_TIER leaking into the assertion
    monkeypatch.setenv("AGI_TIER", "parent")

    monkeypatch.setattr(gate, "_record_roots", lambda: ["R1", "R2"])
    assert gate._effective_tier() == "kid"  # own record beats distant parent

    monkeypatch.setattr(gate, "_record_roots", lambda: ["R2", "R1"])
    assert gate._effective_tier() == "kid"  # and with the roots swapped too


def test_hook_kid_ancestor_refuses_bare_dir_with_env_unset():
    """THE fix proof. A running agent.json with tier=kid whose pid is an
    ancestor of the nested pytest, AGI_TIER UNSET, must still refuse a bare
    directory run -- unsetting the env var can no longer clear the gate.
    """
    code, err = _run_pytest([], None, plant_tier="kid")
    assert code == 4, f"expected refusal, got {code}: {err}"
    assert "AGI_TIER=kid" in err
    assert "specific test file or a -k filter" in err


def test_hook_kid_ancestor_named_file_passes_with_env_unset():
    """The record-derived kid must still be able to run a NAMED file (its
    own targeted tests), only the bare directory is refused.
    """
    code, err = _run_pytest([], None, named_file=True, plant_tier="kid")
    assert code == 0, f"named-file run should pass, got {code}: {err}"


def test_hook_parent_ancestor_bare_dir_allowed_with_env_unset():
    """A running record with tier=parent (the director/prime) allows a bare
    directory run even with AGI_TIER unset -- the gate reads the real tier.
    """
    code, err = _run_pytest([], None, plant_tier="parent")
    assert code == 0, f"parent bare-dir should pass, got {code}: {err}"


def test_decide_only_running_records_count():
    """Pure decision: _running_record_tiers() skips non-running / malformed
    records, so a stale (done) agent.json never cradles the gate. Tested
    in-process because under a kid runtime the real tree always carries a
    live running record on the chain, which a real-tree subprocess cannot
    clear.
    """
    import tempfile, shutil
    root = tempfile.mkdtemp()
    try:
        _write_agent_record(root, "stale", 999999, "kid", status="done")
        _write_agent_record(root, "live", 111111, "director", status="running")
        tiers = gate._running_record_tiers(root)
        assert tiers == {111111: "director"}, f"got {tiers}"
        # empty root -> no tiers -> the pure fallback decides (None)
        empty = tempfile.mkdtemp()
        try:
            assert gate._running_record_tiers(empty) == {}
            assert gate._resolve_tier_from_ancestors({}, lambda p: None, 1) is None
        finally:
            shutil.rmtree(empty)
    finally:
        shutil.rmtree(root)


def test_planted_dir_is_removed_after_the_test():
    """The throwaway iter-test dir a falsifier plants in the REAL tree is
    gone after the run -- the real tree must be left exactly as it was.
    """
    tree_root = gate._default_record_root()
    before = set(p.name for p in Path(tree_root).glob("iter-test-*")) \
        if os.path.isdir(tree_root) else set()
    # _run_pytest plants its OWN throwaway dir and must remove it in
    # finally; verify none of the tree's iter-test dirs survive it.
    code, err = _run_pytest([], None, plant_tier="kid")
    assert code == 4
    _ = err
    after = set(p.name for p in Path(tree_root).glob("iter-test-*")) \
        if os.path.isdir(tree_root) else set()
    assert after == before, f"tree sessions changed: {before} -> {after}"


def test_planted_dir_is_removed_after_the_run():
    """Direct proof of the finally-cleanup: the marker dir a plant creates
    is gone immediately after `_run_pytest` returns.
    """
    import tempfile, shutil
    tree_root = gate._default_record_root()
    before = set(p.name for p in Path(tree_root).glob("iter-test-*")) \
        if os.path.isdir(tree_root) else set()
    marker = _plant_in_tree("kid")
    try:
        assert marker.exists()
        # hand the marker to the run so IT owns the finally-cleanup
        code, err = _run_pytest([], None, plant_marker=marker)
        _ = err
        assert not marker.exists(), "planted dir must be removed in finally"
    finally:
        if marker.exists():
            shutil.rmtree(marker)
    after = set(p.name for p in Path(tree_root).glob("iter-test-*")) \
        if os.path.isdir(tree_root) else set()
    assert after == before, f"tree sessions changed: {before} -> {after}"


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


# --- fix: the gate has NO env seam and NO test-seam-at-all ----------------
# hypothesis:l4-the-kid-tier-gate-has-no-env-seam + hypothesis:l4-the-record-
# root-has-no-test-seam-either. The production root is ALWAYS tree-derived;
# there is no --agent-records-root option, no _TEST_AGENT_RECORDS_ROOT global
# and no PYTEST_CURRENT_TEST guard to spoof. A kid can neither set an env var
# nor pass any flag to point the scan at a non-kid root.

def test_falsifier_env_seam_dead_kid_still_refuses():
    """FALSIFIER. AGI_TIER UNSET and the OLD dead env var
    AGI_AGENT_SESSIONS_ROOT pointed at an EMPTY throwaway dir: the record
    root must be tree-derived, NOT the env var, so a planted kid record
    (ancestor pid) still refuses a bare-directory run. Before this fix,
    setting the var to an empty root scanned nothing and the bare dir run
    exited 0.
    """
    import tempfile
    empty = tempfile.mkdtemp()
    try:
        code, err = _run_pytest([], None, plant_tier="kid", env_seam=empty)
        assert code == 4, f"expected refusal, got {code}: {err}"
        assert "AGI_TIER=kid" in err
        assert "specific test file or a -k filter" in err
    finally:
        import shutil
        shutil.rmtree(empty)


def test_falsifier_kid_record_wins_over_env_tier_and_seam_root():
    """Even AGI_TIER=parent (the old env fallback) cannot clear a kid whose
    record is on the ancestor chain, and the dead env seam pointing at an
    empty root changes nothing either: the record wins over both.
    """
    import tempfile
    empty = tempfile.mkdtemp()
    try:
        code, err = _run_pytest([], "parent", plant_tier="kid", env_seam=empty)
        assert code == 4, f"expected refusal, got {code}: {err}"
        assert "AGI_TIER=kid" in err
    finally:
        import shutil
        shutil.rmtree(empty)


def test_falsifier_recorded_kid_named_file_still_passes():
    """The record-derived kid must still run a NAMED file through the real
    tree record -- only the bare directory is refused.
    """
    code, err = _run_pytest([], None, named_file=True, plant_tier="kid")
    assert code == 0, f"named-file run should pass, got {code}: {err}"


def test_falsifier_non_kid_effective_tier_passes_unchanged():
    """With no kid record decisive, the gate is invisible: a nearer parent
    record makes the effective tier non-kid and the bare directory run
    passes unchanged. (This suite itself RUNS as a kid whose dispatch record
    is a real running ancestor, so the only deterministic real-tree way to a
    non-kid effective tier is a planted nearer parent record; the pure
    empty-fallback is covered in test_decide_only_running_records_count.)
    """
    code, _ = _run_pytest([], "parent", plant_tier="parent")
    assert code == 0


def test_falsifier_real_tree_record_alone_refuses_bare_dir():
    """FALSIFIER (the only seam). With no option and no env var of any kind
    (AGI_TIER unset, no seam), a planted kid record in the REAL tree's
    sessions dir must ALONE refuse the bare-directory run. On the old bytes a
    kid could point the gate at an empty root via --agent-records-root; now
    the record root IS the tree and nothing moves it.
    """
    code, err = _run_pytest([], None, plant_tier="kid")
    assert code == 4, f"expected refusal, got {code}: {err}"
    assert "AGI_TIER=kid" in err
    assert "specific test file or a -k filter" in err


def test_falsifier_flag_cannot_clear_gate_on_new_bytes():
    """FALSIFIER. The old escape (spoofed PYTEST_CURRENT_TEST + the
    --agent-records-root flag) is gone BY CONSTRUCTION: the option no longer
    exists, so there is no flag left to point at an empty root. Passing the
    stale flag as a kid (record in the REAL tree, AGI_TIER=kid) must NOT let
    the bare-directory suite run: either pytest refuses the unknown option or
    the tier gate refuses the bare dir -- never exit 0.
    """
    import tempfile
    empty = tempfile.mkdtemp()
    try:
        code, err = _run_pytest([], "kid", plant_tier="kid", env_seam=empty,
                                extra_argv=[f"--agent-records-root={empty}"])
        assert code == 4, f"expected refusal, got {code}: {err}"
    finally:
        import shutil
        shutil.rmtree(empty)


# --- fix: the gate scans EVERY reachable sessions root ---------------------
# hypothesis:l4-the-kid-tier-gate-scans-every-root-it-can-reach. Before the
# fix the gate derived its record root from ONLY the conftest's own tree
# (`find_project_root(Path(__file__))`), so a kid that pointed pytest at
# MAIN's absolute tests dir scanned MAIN's sessions, found no agent.json for
# its own pid chain, derived no tier and ran the bare directory suite it is
# refused from its own worktree. The fix scans the shared sessions dir and the
# sessions dir of every worktree registered under the main graph's
# `.agi/worktrees/*` in addition to the invoking tree's own sessions dir.


BIN_DIR = os.path.dirname(os.path.dirname(CONFTEST)) + os.sep + "bin"


def _build_fake_main(tmp_parent, with_kid_record=True):
    """Build a throwaway "MAIN" checkout whose tests/conftest.py is THIS
    (fixed) conftest, optionally with a registered worktree `kidA` carrying a
    running kid agent record whose pid is THIS process -- an ANCESTOR of the
    nested pytest this test then spawns.

    Returns the fake main's root Path. The fake layout mirrors production:
      <main>/.agi/{config.json,nodes,sessions}
      <main>/.agi/worktrees/<name>/.agi/{config.json,nodes,sessions/...}
      <main>/extensions/agi/tests/{conftest.py,test_ok.py}
      <main>/extensions/agi/bin -> REAL bin (so the copied conftest's
        `import locations` / `import verification` resolve).
    """
    import shutil
    main = Path(tmp_parent) / "main"
    graph = main / ".agi"
    graph.mkdir(parents=True, exist_ok=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes").mkdir()
    (graph / "sessions").mkdir()

    if with_kid_record:
        kid_graph = graph / "worktrees" / "kidA" / ".agi"
        kid_graph.mkdir(parents=True, exist_ok=True)
        (kid_graph / "config.json").write_text("{}")
        (kid_graph / "nodes").mkdir()
        rec_dir = kid_graph / "sessions" / "iter-test" / "rec"
        rec_dir.mkdir(parents=True)
        (rec_dir / "agent.json").write_text(json.dumps({
            "status": "running", "tier": "kid", "pid": os.getpid()}))

    tests = main / "extensions" / "agi" / "tests"
    tests.mkdir(parents=True)
    shutil.copy(CONFTEST, tests / "conftest.py")
    (tests / "test_ok.py").write_text(TEST_SRC)
    bin_link = main / "extensions" / "agi" / "bin"
    bin_link.parent.mkdir(parents=True, exist_ok=True)
    os.symlink(BIN_DIR, bin_link)
    return main


def _run_pytest_on_fake_main(main_tests_dir, cwd, extra_env=None):
    """Run pytest as a bare-directory run against a fake MAIN tests dir with
    AGI_TIER unset; return (returncode, stderr).
    """
    env = dict(os.environ)
    env.pop("AGI_TIER", None)
    env.pop("AGI_AGENT_SESSIONS_ROOT", None)
    if extra_env:
        env.update(extra_env)
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", main_tests_dir, "-q"],
        cwd=cwd, capture_output=True, text=True, env=env, timeout=300)
    return proc.returncode, proc.stderr


def test_falsifier_kid_record_in_foreign_worktree_refuses_main_scripts_dir():
    """FALSIFIER for the multi-root fix. A kid CONFIRMS it runs from its own
    worktree (real tree, so AGI_TIER is rightly unset) and points pytest at a
    DIFFERENT tree's (a fake MAIN's) absolute tests dir -- the pre-fix escape.
    Because the fake MAIN carries a registered worktree whose sessions holds a
    running kid record whose pid is an ANCESTOR of the nested pytest, the gate
    must scan that worktree's sessions AND refuse the bare directory run.
    """
    import tempfile
    import shutil
    with tempfile.TemporaryDirectory() as td:
        main = _build_fake_main(td, with_kid_record=True)
        tests_dir = main / "extensions" / "agi" / "tests"
        code, err = _run_pytest_on_fake_main(str(tests_dir), str(main))
        try:
            assert code == 4, (
                f"foreign-worktree kid must be refused, got {code}: {err}")
            assert "AGI_TIER=kid" in err
            assert "specific test file or a -k filter" in err
        finally:
            shutil.rmtree(main)


def test_falsifier_foreign_worktree_kid_named_file_passes():
    """Same fake-MAIN setup, but a NAMED file instead of a bare directory: the
    record-derived kid may still run a targeted file even when the tests dir
    it names is another tree's absolute dir -- only the bare directory suite
    is refused.
    """
    import tempfile
    import shutil
    with tempfile.TemporaryDirectory() as td:
        main = _build_fake_main(td, with_kid_record=True)
        tests_dir = main / "extensions" / "agi" / "tests"
        env = dict(os.environ)
        env.pop("AGI_TIER", None)
        env.pop("AGI_AGENT_SESSIONS_ROOT", None)
        proc = subprocess.run(
            [sys.executable, "-m", "pytest",
             str(tests_dir / "test_ok.py"), "-q"],
            cwd=str(main), capture_output=True, text=True, env=env, timeout=300)
        try:
            assert proc.returncode == 0, (
                f"named-file run should pass, got {proc.returncode}: "
                f"{proc.stderr}")
        finally:
            shutil.rmtree(main)


def test_foreign_tree_with_no_record_anywhere_passes_unchanged():
    """NEGATIVE CONTROL for the multi-root fix. A fake MAIN with NO registered
    worktree record and AGI_TIER unset: no running record matches the ancestor
    chain anywhere, so the bare directory run passes unchanged -- the scan
    reaching extra roots must never refuse a run with genuinely no kid.
    """
    import tempfile
    import shutil
    with tempfile.TemporaryDirectory() as td:
        main = _build_fake_main(td, with_kid_record=False)
        tests_dir = main / "extensions" / "agi" / "tests"
        code, err = _run_pytest_on_fake_main(str(tests_dir), str(main))
        try:
            assert code == 0, (
                f"no-record bare dir must pass, got {code}: {err}")
        finally:
            shutil.rmtree(main)


def test_decision_record_roots_include_own_shared_and_every_worktree(
        tmp_path, monkeypatch):
    """In-process unit of `_record_roots()`: given a fake main graph with one
    registered worktree, the returned roots are exactly (deduplicated) the
    invoking tree's sessions, the worktree's sessions and the shared sessions
    -- and the invoking-tree root is present first.
    """
    fake = tmp_path / "main"
    (fake / ".agi").mkdir(parents=True)
    (fake / ".agi" / "config.json").write_text("{}")
    (fake / ".agi" / "nodes").mkdir(parents=True)
    (fake / ".agi" / "sessions").mkdir()
    wt = fake / ".agi" / "worktrees" / "kidA"
    (wt / ".agi").mkdir(parents=True)
    (wt / ".agi" / "config.json").write_text("{}")
    (wt / ".agi" / "nodes").mkdir(parents=True)
    (wt / ".agi" / "sessions").mkdir()

    # point every tree-derived resolver the gate consults at the fake tree.
    monkeypatch.setattr(
        gate,
        "_default_record_root",
        lambda: str((fake / ".agi" / "sessions").resolve()))

    def _fake_root(start=None):
        # A worktree path (`.../.agi/worktrees/<name>`) resolves to its OWN
        # graph dir; any other path resolves to the fake main graph.
        sp = Path(start) if start is not None else Path()
        if "worktrees" in sp.parts and sp.name:
            return sp / ".agi"
        return fake / ".agi"

    monkeypatch.setattr(gate.locations, "find_project_root", _fake_root)
    monkeypatch.setattr(gate.locations, "shared_project_root",
                        lambda _start=None: fake / ".agi")

    roots = gate._record_roots()
    want = {
        str((fake / ".agi" / "sessions").resolve()),
        str((wt / ".agi" / "sessions").resolve()),
    }
    assert set(roots) == want
    # dedup: the invoking-tree sessions root appears exactly once.
    assert len(roots) == len(set(roots))
    assert roots[0] == str((fake / ".agi" / "sessions").resolve())