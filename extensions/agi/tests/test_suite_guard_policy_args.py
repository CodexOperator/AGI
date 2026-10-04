"""The two duplicate guard bodies are ONE body with a caller-supplied POLICY.

experiment:a00-c02d5b4f-ae8fb0 (DH.440) -- residue of the DH.430 unification:
`_suite_lock_guard` (extensions/agi/tests/conftest.py) vs
`suite_guards.suite_lock` were the same lock with a DIFFERENT root resolver,
and `extensions/agi/conftest.py::_agi_env_stripped` vs
`suite_guards.agi_env_stripped` were the same strip with a DIFFERENT extra
channel. Both are now `make_suite_lock_fixture(root_resolver)` and
`make_agi_env_stripped_fixture(extra_keys=())`, instantiated per suite.

Every row is a NEGATIVE probe: it shows the two policies still DIFFER, so
unifying the body was not a silent aliasing of one suite's behaviour onto the
other's. If the difference ever disappears, the parameter is dead and one of
the two suites has quietly been changed.
"""
import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

_BIN = Path(__file__).resolve().parent.parent / "bin"
if str(_BIN) not in sys.path:
    sys.path.insert(0, str(_BIN))
import suite_guards  # noqa: E402
import verification  # noqa: E402

ENGINE_ROOT = Path(__file__).resolve().parents[3]


def _drive(fixture):
    """(enter, exit) around ONE raw fixture body, bypassing pytest's wrapper:
    pytest marks a fixture function object, so drive `__wrapped__`."""
    raw = getattr(fixture, "__wrapped__", None)
    assert raw is not None, "pytest stopped exposing __wrapped__; drive it another way"
    gen = raw()
    next(gen)
    return gen


def _tmp_project(parent, name):
    """(groot) a throwaway project graph; `find_project_root` resolves to the
    `.agi` dir itself, which is what both resolvers return."""
    groot = parent / name / ".agi"
    (groot / "sessions").mkdir(parents=True)
    (groot / "config.json").write_text("{}", encoding="utf-8")
    return groot


def _no_inherited_marker(monkeypatch):
    """This suite is ITSELF running under an acquired lock, so the marker is
    live in this process. The probes drive the body by hand, so they clear it
    first (monkeypatch restores it at teardown)."""
    monkeypatch.delenv(suite_guards.SUITE_LOCK_MARKER, raising=False)


# --- residue 1: one lock body, two ROOT POLICIES ---------------------------

def test_the_two_locks_resolve_two_different_roots(tmp_path, monkeypatch):
    """NEGATIVE probe. Standing in a DIFFERENT project, the context suite's
    resolver (VERIFY_GRAPH_ROOT-else-cwd) follows the cwd, and the engine
    suite's resolver (its own conftest file) does not. Same lock file, two
    windows -- which is why aliasing the two wholesale was refused."""
    other = _tmp_project(tmp_path, "other")
    monkeypatch.delenv(suite_guards.GRAPH_ROOT_ENV, raising=False)
    monkeypatch.chdir(other.parent)
    engine_resolver = (lambda: suite_guards.locations.find_project_root(
        ENGINE_ROOT / "extensions" / "agi" / "tests" / "conftest.py"))
    assert suite_guards.graph_root() == other
    assert engine_resolver() != other


def test_verify_graph_root_overrides_the_context_policy_only(tmp_path, monkeypatch):
    """The override is honoured by the CONTEXT suite's resolver; the engine
    suite's root is derived from its file and no env var can move it."""
    groot = _tmp_project(tmp_path, "declared")
    monkeypatch.setenv(suite_guards.GRAPH_ROOT_ENV, str(groot))
    assert suite_guards.graph_root() == groot
    assert suite_guards.make_suite_lock_fixture(
        lambda: ENGINE_ROOT) is not suite_guards.suite_lock


def test_one_lock_body_under_an_arbitrary_root(tmp_path, monkeypatch):
    """The shared body really is the body: handed a root, it writes THAT
    root's lock file, stamps the window, and unlinks both on exit."""
    groot = _tmp_project(tmp_path, "proj")
    _no_inherited_marker(monkeypatch)
    lock_file = groot / "sessions" / verification.suite_lock_name(groot)
    guard = suite_guards.make_suite_lock_fixture(lambda: groot)
    gen = _drive(guard)
    try:
        assert lock_file.exists(), "the lock was not written under the GIVEN root"
        assert lock_file.read_text(encoding="utf-8").strip() == str(os.getpid())
        assert os.environ[suite_guards.SUITE_LOCK_MARKER] == str(os.getpid())
    finally:
        with pytest.raises(StopIteration):
            next(gen)
    assert not lock_file.exists(), "the lock outlived the session"
    assert suite_guards.SUITE_LOCK_MARKER not in os.environ, (
        "the marker outlived the body")


def test_the_same_body_refuses_a_live_foreign_holder_by_name(tmp_path, monkeypatch):
    """NEGATIVE probe: the SAME factory, a second run against a root whose
    lock names a LIVE foreign pid (our parent -- alive, and not us, since a
    lock naming our own pid is stale by contract), is refused BY NAME."""
    groot = _tmp_project(tmp_path, "proj")
    _no_inherited_marker(monkeypatch)
    holder = os.getppid()
    (groot / "sessions" / verification.suite_lock_name(groot)).write_text(
        str(holder), encoding="utf-8")
    assert verification.suite_lock_holder(groot) == holder
    guard = suite_guards.make_suite_lock_fixture(lambda: groot)
    with pytest.raises(RuntimeError, match=f"pid {holder} is a LIVE runner"):
        _drive(guard)
    assert suite_guards.SUITE_LOCK_MARKER not in os.environ


def test_lock_body_no_ops_on_a_resolver_returning_nothing(tmp_path, monkeypatch):
    """A root resolver that finds no project (not inside an agi project) is a
    silent no-op in BOTH suites -- the shared body, not two copies."""
    _no_inherited_marker(monkeypatch)
    guard = suite_guards.make_suite_lock_fixture(lambda: None)
    gen = _drive(guard)
    with pytest.raises(StopIteration):
        next(gen)
    assert suite_guards.SUITE_LOCK_MARKER not in os.environ, (
        "a no-root suite stamped the window marker anyway")


def test_an_inherited_marker_makes_every_policy_a_no_op(tmp_path, monkeypatch):
    """A nested pytest inherits the marker and must not re-acquire, whichever
    resolver it was handed."""
    groot = _tmp_project(tmp_path, "proj")
    monkeypatch.setenv(suite_guards.SUITE_LOCK_MARKER, "12345")
    guard = suite_guards.make_suite_lock_fixture(lambda: groot)
    gen = _drive(guard)
    try:
        assert not (groot / "sessions" / verification.suite_lock_name(groot)).exists()
        with pytest.raises(StopIteration):
            next(gen)
    finally:
        monkeypatch.delenv(suite_guards.SUITE_LOCK_MARKER, raising=False)


# --- residue 2: one strip body, one EXTRA-CHANNEL policy -------------------

def test_the_extra_channel_is_an_argument_not_a_copy(monkeypatch):
    """NEGATIVE probe. The default (declared-suite) policy leaves
    GIT_CONFIG_* ALONE; the engine policy removes it. One body, two answers."""
    monkeypatch.setenv("GIT_CONFIG_COUNT", "1")
    monkeypatch.setenv("AGI_TIER", "kid")
    memo = suite_guards.strip_dispatch_env()
    assert "GIT_CONFIG_COUNT" in os.environ, (
        "the default policy now strips the git-hook channel -- that is the "
        "ENGINE suite's policy, and the declared suite must not inherit it")
    assert "AGI_TIER" not in os.environ
    suite_guards.restore_dispatch_env(memo)
    assert os.environ.get("AGI_TIER") == "kid"


def test_engine_policy_strips_the_git_hook_channel(monkeypatch):
    """The engine policy is `extra_keys=GIT_CONFIG_SPAWN_VARS`, and it is
    STRICTLY STRONGER than the default on that axis -- so the shared body
    defaults to the weaker one and the engine caller narrows it explicitly."""
    for key in suite_guards.GIT_CONFIG_SPAWN_VARS:
        monkeypatch.setenv(key, "x")
    memo = suite_guards.strip_dispatch_env(suite_guards.GIT_CONFIG_SPAWN_VARS)
    assert not [k for k in os.environ if k.startswith("GIT_CONFIG_")]
    suite_guards.restore_dispatch_env(memo)
    assert sorted(k for k in os.environ if k.startswith("GIT_CONFIG_")) == sorted(
        suite_guards.GIT_CONFIG_SPAWN_VARS)


def test_the_engine_conftest_passes_its_own_policy(tmp_path):
    """The live engine conftest -- loaded BY PATH, the way its own test does
    -- really delegates to the shared body with the git-hook channel, and
    keeps the seam `test_agi_env_strip.py` drives."""
    path = ENGINE_ROOT / "extensions" / "agi" / "conftest.py"
    spec = importlib.util.spec_from_file_location("_engine_conftest_probe", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.GIT_CONFIG_SPAWN_VARS == suite_guards.GIT_CONFIG_SPAWN_VARS
    memo = {}
    before = dict(os.environ)
    try:
        os.environ["GIT_CONFIG_COUNT"] = "1"
        os.environ["AGI_TIER"] = "kid"
        mod._strip_agi_env()
        assert "GIT_CONFIG_COUNT" not in os.environ
        assert "AGI_TIER" not in os.environ
    finally:
        mod._restore_agi_env()
        os.environ.clear()
        os.environ.update(before)
    assert os.environ.get("GIT_CONFIG_COUNT") is None
    assert os.environ.get("AGI_TIER") is None


def test_the_declared_conftest_keeps_the_weaker_policy():
    """.agi/context/conftest.py imports the DEFAULT fixtures by name -- no
    extra keys -- so the context suite is not silently given the engine's
    git-hook strip (or the engine's file-relative lock root)."""
    text = (ENGINE_ROOT / ".agi" / "context" / "conftest.py").read_text(
        encoding="utf-8")
    assert "from suite_guards import" in text
    assert "make_suite_lock_fixture" not in text
    assert "make_agi_env_stripped_fixture" not in text
    cfg = json.loads((ENGINE_ROOT / ".agi" / "config.json").read_text(
        encoding="utf-8"))
    assert cfg  # the config the context suite's suite_roots cell lives in
