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
import atexit
import importlib.util
import json
import os
import shutil
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


def _some_dead_pid():
    """A pid guaranteed (with overwhelming probability) to have NO /proc entry
    right now, for modelling a phantom left by a SIGKILLed run."""
    pid = 1 << 29
    while os.path.exists(f"/proc/{pid}"):
        pid += 1
    return pid


def _plant_in_tree(tier, status="running"):
    """Plant a running (or stale, per `status`) agent.json whose pid is THIS
    process -- an ANCESTOR of the nested pytest -- under the REAL tree's
    sessions dir, in a throwaway `iter-test-<uuid>` dir.

    This is the subprocess-falsifier seam now that --agent-records-root is
    gone (hypothesis:l4-the-record-root-has-no-test-seam-either): the record
    has to live where the gate actually scans, and the caller removes it in
    `finally`. Returns the throwaway marker dir (its parent to clean up).

    hypothesis:l4-a-running-record-with-a-dead-pid-is-not-a-running-agent:
    the marker ALSO self-cleans via `atexit` (``shutil.rmtree(marker, True)``)
    on top of the caller's `finally`, so a normal exit or a `finally` that is
    abandoned cannot leave a phantom under the REAL tree. Python's atexit
    stack runs on normal exit and on SIGINT (which the interpreter converts
    into a KeyboardInterrupt); it does NOT run on SIGTERM (whose default
    disposition terminates without unwinding -- measured: SIGTERM exits with
    rc=-15 and the atexit handler never fires) and cannot run on SIGKILL.
    So a SIGTERM/SIGKILL kill may leave the marker behind. That leftover is
    harmless -- the liveness gate in conftest._running_record_tiers ignores a
    dead-pid record -- and hypothesis:l4-a-phantom-running-record-with-a-dead-pid-is-named
    (L4.238) is what names that phantom instead of this self-clean path.
    """
    tree_root = gate._default_record_root()
    assert tree_root, "tree-derived record root must resolve"
    marker = Path(tree_root) / f"iter-test-{uuid.uuid4().hex[:8]}"
    marker.mkdir(parents=True, exist_ok=True)
    _write_agent_record(marker, "rec", os.getpid(), tier, status=status)
    atexit.register(shutil.rmtree, marker, True)
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

    There is deliberately NO git-redirect parameter here: this harness's
    throwaway dir is not a real git repo, so git is never consulted and
    GIT_COMMON_DIR would be inert (hypothesis:l4-the-tier-gate-scan-is-not-
    redirectable-by-git-env proved the redirect only routs git's own root
    resolution). The redirect falsifiers run through `_run_pytest_on_fake_main`
    (which builds a real fake-MAIN repo), setting
    `extra_env={'GIT_COMMON_DIR': ...}`. The host's GIT_* vars are ALWAYS
    stripped from the inherited env first, in BOTH harnesses, so a
    contaminated host is not what a test measures. The old `git_redirect`
    parameter was dead: no caller used it, and even wired it would have set
    GIT_DIR == GIT_COMMON_DIR, the exact shape the round proved CANCELS the
    redirect.
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
        # Never leak a host's git-redirect vars into the child; a falsifier
        # that WANTS one sets it via `_run_pytest_on_fake_main`'s extra_env,
        # on a real fake-MAIN repo where git is actually consulted.
        for _g in ("GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE"):
            env.pop(_g, None)
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
    import tempfile
    root = tempfile.mkdtemp()
    try:
        _write_agent_record(root, "stale", 999999, "kid", status="done")
        # a LIVE pid (this process, guaranteed present in /proc) counts...
        _write_agent_record(root, "live", os.getpid(), "director", status="running")
        # ...but a running record at a guone pid (hypothesis:l4-a-running-
        # record-with-a-dead-pid-is-not-a-running-agent) is skipped.
        _write_agent_record(root, "phantom", _some_dead_pid(), "kid", status="running")
        tiers = gate._running_record_tiers(root)
        assert tiers == {os.getpid(): "director"}, f"got {tiers}"
        # empty root -> no tiers -> the pure fallback decides (None)
        empty = tempfile.mkdtemp()
        try:
            assert gate._running_record_tiers(empty) == {}
            assert gate._resolve_tier_from_ancestors({}, lambda p: None, 1) is None
        finally:
            shutil.rmtree(empty)
    finally:
        shutil.rmtree(root)


def test_decide_running_record_with_dead_pid_derives_no_tier():
    """hypothesis:l4-a-running-record-with-a-dead-pid-is-not-a-running-agent.
    The falsifier -- a running record with a dead pid deriving a tier -- is
    refused: a `status: running` record whose pid has no /proc entry is a
    phantom left by a SIGKILLed run and must not cradle the gate, even during
    the pid-reuse window on a later run's ancestor chain. A running record at
    a LIVE pid (os.getpid()) still derives its tier, and the pure fallback
    (AGI_TIER) is what a chain rooted at the dead pid gets.
    """
    import tempfile
    root = tempfile.mkdtemp()
    try:
        dead = _some_dead_pid()
        _write_agent_record(root, "phantom", dead, "kid", status="running")
        tiers = gate._running_record_tiers(root)
        # dead-pid record is skipped entirely
        assert tiers == {}, f"expected no tiers, got {tiers}"
        # a chain rooted at the dead pid (a reused pid number) derives nothing
        assert gate._resolve_tier_from_ancestors(tiers, lambda p: None, dead) is None
        # control: the SAME record written at a live pid derives its tier
        live_root = tempfile.mkdtemp()
        try:
            _write_agent_record(live_root, "rec", os.getpid(), "director", status="running")
            live = gate._running_record_tiers(live_root)
            assert live == {os.getpid(): "director"}, f"got {live}"
            assert gate._resolve_tier_from_ancestors(live, lambda p: os.getpid(), os.getpid()) == "director"
        finally:
            shutil.rmtree(live_root)
    finally:
        shutil.rmtree(root)


def test_decide_phantom_dead_pid_is_named_once_on_stderr():
    """hypothesis:l4-a-phantom-running-record-with-a-dead-pid-is-named.
    When the scan skips a `status: running` record whose pid has no /proc
    entry, it prints ONE stderr line naming the record path and pid
    (`tier-gate: phantom running record <path> pid=<n> (dead) -- skipped`),
    deduplicated per session -- two calls name it once. A live-pid running
    record prints NOTHING. The phantom is named, not deleted: the file\'s
    still there afterwards (cleaning is the reaper\'s, not the scan\'s).
    """
    import tempfile, io, contextlib
    root = tempfile.mkdtemp()
    try:
        dead = _some_dead_pid()
        rec_dir = _write_agent_record(root, "phantom", dead, "kid", status="running")
        # live control: a running record at a live pid names nothing.
        live_dir = _write_agent_record(root, "live", os.getpid(), "director", status="running")

        def _capture():
            buf = io.StringIO()
            with contextlib.redirect_stderr(buf):
                tiers = gate._running_record_tiers(root)
            return tiers, buf.getvalue()

        tiers, err = _capture()
        # the phantom derives no tier; the live record still does
        assert tiers == {os.getpid(): "director"}, f"got {tiers}"
        # the named line appears exactly once, naming path + pid, no deletion
        expected = f"tier-gate: phantom running record {rec_dir/'agent.json'} pid={dead} (dead) -- skipped"
        assert err.count(expected) == 1, f"phantom named {err.count(expected)}x: {err!r}"
        assert (rec_dir / "agent.json").exists(), "scan must not delete the record"
        # second call -- same session -- names it zero more times.
        _, err2 = _capture()
        assert expected not in err2, f"phantom re-named on second call: {err2!r}"
        # live record path is never named as a phantom
        assert f"{live_dir/'agent.json'}" not in err
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


def _conftest_without_git_pop():
    """The production conftest bytes with the three-line GIT_* pop REMOVED --
    the PRE-FIX bytes the mutation harness runs against.

    Non-vacuity proof for hypothesis:l4-the-tier-gate-scan-is-not-
    redirectable-by-git-env: a falsifier only measures the fix if it is RED
    without it. Running this mutated copy proves the exact same invocation
    the fixed test expects to refuse ESCAPES (bare directory runs, exit 0)
    when the pop is gone.
    """
    import re
    text = Path(CONFTEST).read_text(encoding="utf-8")
    pat = re.compile(
        r'    for _g in \("GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE"\):\n'
        r'        os\.environ\.pop\(_g, None\)\n'
    )
    stripped, n = pat.subn("", text)
    assert n == 1, f"expected exactly one GIT_* pop block, stripped {n}"
    return stripped


def test_falsifier_git_env_cannot_redirect_the_scan_to_a_scratch_repo():
    """FALSIFIER for hypothesis:l4-the-tier-gate-scan-is-not-redirectable-
    by-git-env -- NON-VACUOUS, built on the fake-MAIN + DECOY harness.

    `_record_roots()` reaches `<main>/.agi/worktrees/*` through
    `locations.shared_project_root` -> `git_common_root` -> `git rev-parse
    --git-common-dir`, which honours GIT_COMMON_DIR in the environment. Root
    #1 (the fake MAIN's own sessions dir) holds NO record; the ONLY record
    lives in the fake main's registered worktree sessions, reachable ONLY
    through the git-resolved root #2 scan. GIT_COMMON_DIR is set ALONE (GIT_DIR
    is deliberately NOT set -- the parent measured that GIT_DIR set equal to
    it cancels the redirect) to a DECOY git repo graph that carries
    `config.json`+`nodes` but no record.

    On the pre-fix bytes (no pop) the scan follows GIT_COMMON_DIR to the
    decoy, finds no record, derives no tier and RUNS the bare suite. The fix
    (popping the three GIT_* vars before any root resolves) restores true git
    resolution, root #2 finds the worktree kid record, and the bare directory
    run is REFUSED (exit 4) -- so the run under the fix proves the redirect
    cannot reach a repo of a kid's choosing even when attempted.
    """
    import tempfile
    import shutil
    with tempfile.TemporaryDirectory() as td:
        main = _build_fake_main(td, with_kid_record=True)
        decoy = _build_decoy_graph(td)
        try:
            tests_dir = main / "extensions" / "agi" / "tests"
            code, err = _run_pytest_on_fake_main(
                str(tests_dir), str(main),
                extra_env={"GIT_COMMON_DIR": str(decoy / ".git")})
            assert code == 4, (
                f"the FIXED conftest must REFUSE the git-redirected worktree "
                f"kid, got {code}: {err}")
            assert "AGI_TIER=kid" in err
            assert "specific test file or a -k filter" in err
        finally:
            shutil.rmtree(main)
            shutil.rmtree(decoy)


def test_falsifier_git_env_redirect_mutation_escapes_without_the_pop():
    """NON-VACUITY PROOF for hypothesis:l4-the-tier-gate-scan-is-not-
    redirectable-by-git-env. The EXACT SAME bare-directory invocation as the
    main falsifier, but run against a copy of the conftest with the three
    GIT_* pop lines REMOVED -- the pre-fix bytes, via `_conftest_without_git_pop`.

    Because the scan stays redirectable, root #2 follows GIT_COMMON_DIR to
    the DECOY, finds no record, derives no tier and the bare-directory suite
    RUNS (exit 0). This is the RED-on-pre-fix evidence: the fixed test above
    does not pass "anyway" -- it passes ONLY because the pop restores true git
    resolution, so it genuinely measures the fix.
    """
    import tempfile
    import shutil
    with tempfile.TemporaryDirectory() as td:
        main = _build_fake_main(td, with_kid_record=True)
        decoy = _build_decoy_graph(td)
        try:
            tests_dir = main / "extensions" / "agi" / "tests"
            (tests_dir / "conftest.py").write_text(_conftest_without_git_pop())
            code, err = _run_pytest_on_fake_main(
                str(tests_dir), str(main),
                extra_env={"GIT_COMMON_DIR": str(decoy / ".git")})
            assert code == 0, (
                f"the MUTATED conftest (pop removed) must let the redirect "
                f"ESCAPE the gate, got {code}: {err}")
        finally:
            shutil.rmtree(main)
            shutil.rmtree(decoy)


def test_falsifier_git_env_redirect_no_redirect_still_refuses():
    """NEGATIVE CONTROL. Same fake MAIN (record only in the worktree) and
    DECOY, but GIT_COMMON_DIR UNSET -- no redirect attempted. The scan
    resolves the fake main's own git repo, root #2 finds the worktree kid
    record and the bare directory is refused. The fix must not depend on a
    redirect being present; the false-positive direction (a kid that never
    attacks the env still being blocked) is exactly what the gate owes.
    """
    import tempfile
    import shutil
    with tempfile.TemporaryDirectory() as td:
        main = _build_fake_main(td, with_kid_record=True)
        _build_decoy_graph(td)
        try:
            tests_dir = main / "extensions" / "agi" / "tests"
            code, err = _run_pytest_on_fake_main(str(tests_dir), str(main))
            assert code == 4, f"no-redirect worktree kid must be refused, got {code}: {err}"
            assert "AGI_TIER=kid" in err
        finally:
            shutil.rmtree(main)


def test_falsifier_git_env_redirect_to_configless_repo_still_refuses():
    """NEGATIVE CONTROL. GIT_COMMON_DIR points at a DECOY git repo with NO
    `.agi` (a plain empty scratch repo, not a graph). Pre-fix the scan would
    redirect to it, `find_project_root` would resolve NONE, and the fallback
    (`main_graph = root`) keeps scanning the fake main's own worktree -- so the
    kid record is still found and the bare directory is refused. Even a
    redirect to a non-project must never silently narrow the scan to fewer
    roots.
    """
    import tempfile
    import shutil
    with tempfile.TemporaryDirectory() as td:
        main = _build_fake_main(td, with_kid_record=True)
        plain = Path(td) / "plain"
        subprocess.run(["git", "init", "-q", str(plain)], check=True)
        try:
            tests_dir = main / "extensions" / "agi" / "tests"
            code, err = _run_pytest_on_fake_main(
                str(tests_dir), str(main),
                extra_env={"GIT_COMMON_DIR": str(plain / ".git")})
            assert code == 4, f"configless-repo redirect must be refused, got {code}: {err}"
            assert "AGI_TIER=kid" in err
        finally:
            shutil.rmtree(main)
            shutil.rmtree(plain)


def test_falsifier_git_env_redirect_no_record_anywhere_passes():
    """NEGATIVE CONTROL. Fake MAIN with NO record anywhere PLUS the DECOY and
    GIT_COMMON_DIR redirect set: no running agent record matches the ancestor
    chain in ANY scanned root, so the bare directory run passes unchanged.
    The git-var strip must never by itself turn a genuinely record-free run
    into a refusal.
    """
    import tempfile
    import shutil
    with tempfile.TemporaryDirectory() as td:
        main = _build_fake_main(td, with_kid_record=False)
        decoy = _build_decoy_graph(td)
        try:
            tests_dir = main / "extensions" / "agi" / "tests"
            code, err = _run_pytest_on_fake_main(
                str(tests_dir), str(main),
                extra_env={"GIT_COMMON_DIR": str(decoy / ".git")})
            assert code == 0, f"no-record bare dir must pass, got {code}: {err}"
        finally:
            shutil.rmtree(main)
            shutil.rmtree(decoy)


def test_decision_git_common_dir_alone_redirects_shared_root(tmp_path):
    """Locks the mechanism the subprocess falsifiers depend on, in isolation:
    `shared_project_root(fake main graph)` routes through `git_common_root`,
    which honours GIT_COMMON_DIR in the environment. Set ALONE (GIT_DIR
    unset), the decoy's `.git` makes git report differing --git-dir and
    --git-common-dir, so `git_common_root` resolves to the DECOY and `shared_-
    project_root` loses the fake main's worktrees. Once the three GIT_* vars
    are popped (the fix), git reports equal dirs, `git_common_root` returns
    the walk-up repo root, and the fake main's worktree graph is resolved
    again. (hypothesis:l4-the-tier-gate-scan-is-not-redirectable-by-git-env)
    """
    import shutil
    main = _build_fake_main(tmp_path, with_kid_record=True)
    decoy = _build_decoy_graph(tmp_path)
    try:
        graph = gate.locations.find_project_root(
            main / "extensions" / "agi" / "tests")
        assert graph is not None
        # root #1 is the fake main's own sessions (empty); verify that the
        # ONLY record lives in the worktree graph, via the real resolvers.
        kid_graph = gate.locations.find_project_root(
            main / ".agi" / "worktrees" / "kidA")
        assert kid_graph is not None

        # GIT_COMMON_DIR ALONE redirects shared_project_root to the decoy.
        os.environ["GIT_COMMON_DIR"] = str(decoy / ".git")
        redirected = gate.locations.shared_project_root(graph)
        assert redirected == (decoy / ".agi").resolve(), redirected

        # GIT_DIR set equal to the SAME path cancels the redirect: git reports
        # git-dir == common-dir and git_common_root returns the walk-up root.
        os.environ["GIT_DIR"] = str(decoy / ".git")
        cancelled = gate.locations.shared_project_root(graph)
        assert cancelled == (main / ".agi").resolve(), cancelled

        # The fix pops all three -> true resolution to the fake main's graph.
        for _g in ("GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE"):
            os.environ.pop(_g, None)
        restored = gate.locations.shared_project_root(graph)
        assert restored == (main / ".agi").resolve(), restored
    finally:
        for _g in ("GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE"):
            os.environ.pop(_g, None)
        shutil.rmtree(main)
        shutil.rmtree(decoy)


def test_falsifier_git_env_redirect_named_file_still_passes():
    """NEGATIVE CONTROL for the git-env falsifier: with the same
    fake-MAIN + DECOY + GIT_COMMON_DIR-alone redirect, but a NAMED file (a
    targeted run), the record-derived kid may still run it -- only the bare
    directory is refused. Confirms the git-var strip does not over-block
    legitimate targeted runs.
    """
    import tempfile
    import shutil
    with tempfile.TemporaryDirectory() as td:
        main = _build_fake_main(td, with_kid_record=True)
        decoy = _build_decoy_graph(td)
        try:
            tests_dir = main / "extensions" / "agi" / "tests"
            env = dict(os.environ)
            env.pop("AGI_TIER", None)
            env.pop("AGI_AGENT_SESSIONS_ROOT", None)
            for _g in ("GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE"):
                env.pop(_g, None)
            env["GIT_COMMON_DIR"] = str(decoy / ".git")
            proc = subprocess.run(
                [sys.executable, "-m", "pytest",
                 str(tests_dir / "test_ok.py"), "-q"],
                cwd=str(main), capture_output=True, text=True, env=env,
                timeout=300)
            assert proc.returncode == 0, (
                f"named-file run should pass, got {proc.returncode}: "
                f"{proc.stderr}")
        finally:
            shutil.rmtree(main)
            shutil.rmtree(decoy)


def test_decision_git_redirect_vars_are_popped_before_root_resolution(monkeypatch):
    """In-process unit: `pytest_cmdline_main` must strip GIT_DIR, GIT_COMMON_DIR
    and GIT_WORK_TREE from os.environ BEFORE `_effective_tier()` runs, so the
    root resolution a kid would redirect never sees them. Call the hook with a
    non-refusing config and assert the three vars are gone afterwards.
    """
    cfg = _Cfg([], keyword="x")  # -k filter -> never refuses, but the pop runs.
    monkeypatch.setenv("GIT_DIR", "/fake/gitdir")
    monkeypatch.setenv("GIT_COMMON_DIR", "/fake/common")
    monkeypatch.setenv("GIT_WORK_TREE", "/fake/wt")
    gate.pytest_cmdline_main(cfg)
    for _g in ("GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE"):
        assert os.environ.get(_g) is None, f"{_g} must be popped before resolution"


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

    # Make the fake main a REAL git repo. `_record_roots()` reaches the
    # worktrees through `git_common_root`, which consults `git rev-parse` only
    # once a `.git` is found walking up from the graph -- and GIT_COMMON_DIR
    # can only redirect the scan when git is actually consulted
    # (hypothesis:l4-the-tier-gate-scan-is-not-redirectable-by-git-env). A
    # fake main with no `.git` is inert against the redirect, so the redirect
    # falsifier could never fire. git-init makes the walk stop at `main` and
    # the scan genuinely routable.
    subprocess.run(["git", "init", "-q", str(main)], check=True)
    return main


def _build_decoy_graph(parent):
    """A throwaway "DECOY" graph a redirect can point the scan at: a REAL git
    repo whose `.agi` carries config.json + nodes (so `find_project_root`
    resolves it to a valid graph) but NO agent record anywhere.

    The whole point of the decoy (hypothesis:l4-the-tier-gate-scan-is-not-
    redirectable-by-git-env): if a kid can redirect `_record_roots()`'s
    git-resolved root #2 at a repo of its choosing, it feeds it a graph that
    looks like a project but whose sessions dir is EMPTY -- so the scan finds
    no running agent on the kid's own pid chain and the bare-directory suite
    runs. The decoy has to lie to `git_common_root` (carry a `.git`) AND to
    `find_project_root` (carry `.agi/config.json`) to be a convincing target.
    """
    decoy = Path(parent) / "decoy"
    graph = decoy / ".agi"
    graph.mkdir(parents=True, exist_ok=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes").mkdir()
    subprocess.run(["git", "init", "-q", str(decoy)], check=True)
    return decoy


def _run_pytest_on_fake_main(main_tests_dir, cwd, extra_env=None):
    """Run pytest as a bare-directory run against a fake MAIN tests dir with
    AGI_TIER unset; return (returncode, stderr). Host GIT_* vars are always
    stripped first so a contaminated host does not redirect the scan on its
    own; `extra_env` re-adds them explicitly for the redirect falsifiers.
    """
    env = dict(os.environ)
    env.pop("AGI_TIER", None)
    env.pop("AGI_AGENT_SESSIONS_ROOT", None)
    for _g in ("GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE"):
        env.pop(_g, None)
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