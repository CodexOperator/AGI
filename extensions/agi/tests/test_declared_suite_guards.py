"""The DECLARED second suite runs under the engine suite's guards.

hypothesis:the-declared-context-suite-runs-under-the-engine-suite-guards --
every `paths.core.suite_roots` entry is spawned by `check_extra_suite` with no
env of its own, while the suite lock, the dispatch-env strip and the opt-in
real-process / live-config guard lived only in the engine conftests. These
tests drive the REAL runner over a tmp graph, so each conjunct is measured on
the bytes a real `--suite` uses:

  (a) a second concurrent declared-suite run REFUSES BY NAME (the lock, held
      by a LIVE foreign pid, refuses the child rather than letting two run);
  (b) a context test that signals a real pid or opens the live
      `.agi/config.json` FAILS, the guard naming the resource;
  (c) the child sees NO caller AGI_SEAT / AGI_TIER / AGI_AGENT.

Every child is spawned under `timeout 300 prlimit --cpu=300:300
--nofile=4096:4096` with a --basetemp under /tmp, and NEVER at a directory
holding the calling test (FORK-BOUND 2/3 -- DH.419 forked 127 pytest
processes). `--nproc` is NOT used: RLIMIT_NPROC counts THREADS per uid on
this kernel, the uid already runs 934 threads, so ANY --nproc below that
makes the FIRST fork fail with EAGAIN (measured: `prlimit --nproc=300
python3 -m pytest` cannot fork at all). --cpu/--nofile bound a runaway child
without that cliff.
"""
import json
import os
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

import pytest

_BIN = Path(__file__).resolve().parent.parent / "bin"
if str(_BIN) not in sys.path:
    sys.path.insert(0, str(_BIN))
import suite_guards  # noqa: E402
import verification  # noqa: E402

#: Exactly what .agi/context/conftest.py does: ONE import, no exec of the
#: engine conftest. Kept as a string here so a generated suite is a suite the
#: declared-root contract can actually point at.
CONTEXT_CONFTEST = '''
import pathlib, sys
sys.path.insert(0, {bin!r})
from suite_guards import (  # noqa
    agi_env_stripped, install_import_fence, no_real_process, suite_lock,
    uninstall_import_fence)

_IMPORT_FENCE_SAVED = install_import_fence()


def pytest_unconfigure(config):
    uninstall_import_fence(_IMPORT_FENCE_SAVED)
'''


def _make_project(tmp_path: Path, suite: str, body: str) -> Path:
    """(groot) a tmp graph declaring `suite` as its one suite root, with one
    test file whose body is `body`."""
    groot = tmp_path / "proj" / ".agi"
    (groot / "sessions").mkdir(parents=True)
    (groot / "config.json").write_text(json.dumps(
        {"paths": {"core": {"suite_roots": [suite]}}}), encoding="utf-8")
    suite_dir = tmp_path / "proj" / suite
    suite_dir.mkdir(parents=True, exist_ok=True)
    (suite_dir / "conftest.py").write_text(
        CONTEXT_CONFTEST.format(bin=str(_BIN)), encoding="utf-8")
    (suite_dir / "test_ctx.py").write_text(textwrap.dedent(body),
                                           encoding="utf-8")
    return groot


def _run(groot: Path, suite_dir: Path, monkeypatch) -> subprocess.CompletedProcess:
    """Run the REAL declared suite the way --suite does, under a /tmp
    basetemp and a process rlimit."""
    base = tempfile.mkdtemp(prefix="ctxsuite-", dir="/tmp")
    monkeypatch.setenv(suite_guards.GRAPH_ROOT_ENV, str(groot))
    return subprocess.run(
        ["timeout", "300", "prlimit", "--cpu=300:300", "--nofile=4096:4096",
         sys.executable, "-m",
         "pytest", str(suite_dir), "-q", "-p", "no:cacheprovider",
         "--basetemp", base],
        capture_output=True, text=True, timeout=300, cwd=str(groot),
        env=suite_guards.spawn_env())


def test_a_second_declared_suite_run_refuses_by_name(tmp_path, monkeypatch):
    """(a) A LIVE foreign holder owns the window; the declared suite refuses
    and NAMES it, rather than running beside it."""
    groot = _make_project(tmp_path, "ctx", """
        def test_ok():
            assert True
        """)
    holder = os.getpid()          # this process is alive and is not the child
    (groot / "sessions" / verification.suite_lock_name(groot)).write_text(
        str(holder), encoding="utf-8")
    monkeypatch.delenv(verification.SUITE_LOCK_MARKER, raising=False)
    res = verification.check_extra_suite(groot)
    out = f"{res.status} {res.note} {res.message}"
    assert "suite window refused" in out, out
    assert str(holder) in out, out
    (groot / "sessions" / verification.suite_lock_name(groot)).unlink()


def test_a_context_test_cannot_signal_a_real_pid_or_read_the_live_config(
        tmp_path, monkeypatch):
    """(b) The opt-in guard bites inside the declared suite. The config the
    test opens lives OUTSIDE its own tmp_path, so it is the live one."""
    groot = _make_project(tmp_path, "ctx", '''
        import os
        NO_REAL_PROCESSES = True


        def test_signalling_a_real_pid_is_refused(tmp_path):
            try:
                os.kill(1, 0)
            except AssertionError as e:
                assert "signalled pid 1" in str(e), e
            else:
                raise SystemExit("guard did not bite: os.kill(1, 0) reached pid 1")


        def test_opening_the_live_config_is_refused(tmp_path):
            live = os.environ["LIVE_CONFIG"]
            try:
                open(live, encoding="utf-8")
            except AssertionError as e:
                assert "LIVE config" in str(e), e
            else:
                raise SystemExit(f"guard did not bite: read {live}")
        ''')
    (groot.parent / ".agi" / "config.json").write_text("{}", encoding="utf-8")
    monkeypatch.setenv("LIVE_CONFIG", str(groot / "config.json"))
    res = _run(groot, tmp_path / "proj" / "ctx", monkeypatch)
    out = (res.stdout or "") + (res.stderr or "")
    assert "guard did not bite" not in out, out
    # both halves must have been REFUSED, not merely survived
    assert res.returncode == 0 and "2 passed" in out, out


def test_the_child_sees_no_caller_agi_env(tmp_path, monkeypatch):
    """(c) AGI_SEAT / AGI_TIER / AGI_AGENT are gone in the child, both at the
    spawn boundary and in the child's own os.environ."""
    for key, value in (("AGI_SEAT", "a00-deadbeef"), ("AGI_TIER", "kid"),
                       ("AGI_AGENT", "a00-deadbeef")):
        monkeypatch.setenv(key, value)
    groot = _make_project(tmp_path, "ctx", """
        import os

        def test_no_caller_agi_env():
            leaked = sorted(k for k in os.environ
                            if k.startswith(("AGI_", "AUTORESEARCH_")))
            assert leaked == [], leaked
        """)
    res = _run(groot, tmp_path / "proj" / "ctx", monkeypatch)
    out = (res.stdout or "") + (res.stderr or "")
    assert res.returncode == 0, out
    assert "1 passed" in out, out
    # the spawn boundary itself
    env = suite_guards.spawn_env()
    assert not any(k.startswith(("AGI_", "AUTORESEARCH_")) for k in env)
    assert env.get(verification.SUITE_LOCK_MARKER) == os.environ.get(
        verification.SUITE_LOCK_MARKER)
    # the parent's own environment is untouched by the strip helper
    assert os.environ["AGI_SEAT"] == "a00-deadbeef"


def test_an_opted_in_context_module_that_spawns_at_import_is_refused(
        tmp_path, monkeypatch):
    """(d) The collection-time hole is closed in the DECLARED suite too. The
    three FIXTURES cannot cover this: fixtures do not exist yet while pytest
    imports a test module, so `os.system` at module scope in an opted-in
    context test really forked a shell until this conftest installed the
    import-time fence at ITS import.

    The refusal must arrive DURING collection, by name -- not as a later test
    failure. Red-first: drop the `install_import_fence()` call from
    CONTEXT_CONFTEST (and from .agi/context/conftest.py) and this suite is
    green again, with a REAL `os.system` shell at collection."""
    groot = _make_project(tmp_path, "ctx", '''
        import os
        NO_REAL_PROCESSES = True

        # NOT inside a test body: collection imports this module before any
        # fixture exists, so the function-scoped guard cannot see it.
        os.system("true")
        ''')
    res = _run(groot, tmp_path / "proj" / "ctx", monkeypatch)
    out = (res.stdout or "") + (res.stderr or "")
    assert res.returncode != 0, out
    assert ("guard: a NO_REAL_PROCESSES module called os.system at IMPORT time"
            in out), out
    assert "error" in out and "test_ctx" in out, out   # refused AT COLLECTION


def test_an_opted_in_context_module_that_killpgs_at_import_is_refused(
        tmp_path, monkeypatch):
    """(e) ONE call, ONE rule: `os.killpg` is refused OUTRIGHT in BOTH leaves.
    The fixture leaf already was (`_make_guarded_killpg`); the import-time
    fence routed it through the own-pid signal-0 predicate, so a group the
    test never spawned was signalled during collection.

    SIGCONT is the offending signal: its default action is 'continue', so the
    row is harmless if the guard ever goes missing -- it would only fail to be
    refused. The second half proves, with a RECORDER rather than a syscall,
    that the refusal arms no real `killpg` at all: the opted-in call is driven
    through a stub leaf, from a frame that carries the opt-in flag."""
    import types  # noqa: PLC0415
    groot = _make_project(tmp_path, "ctx", '''
        import os, signal
        NO_REAL_PROCESSES = True

        os.killpg(os.getpgid(0), signal.SIGCONT)
        ''')
    res = _run(groot, tmp_path / "proj" / "ctx", monkeypatch)
    out = (res.stdout or "") + (res.stderr or "")
    assert res.returncode != 0, out
    assert ("guard: a NO_REAL_PROCESSES module called os.killpg at IMPORT time"
            in out), out

    # recorder half, and the TRUE red-first for the divergence: the old
    # import-time fence routed os.killpg through the own-pid signal-0
    # predicate, so a group LEADER (pgid == own pid) signalling its OWN group
    # with signal 0 at collection PASSED THROUGH to the real killpg, while the
    # fixture leaf refused it outright. Driven on a stub leaf from an opted-in
    # frame: the refusal arms no syscall at all.
    calls = []
    stub = types.SimpleNamespace(
        kill=lambda *a, **k: calls.append(("kill", a)),
        killpg=lambda *a, **k: calls.append(("killpg", a)))
    saved = suite_guards.install_import_fence(
        leaves=(), kills=True, os_module=stub)
    try:
        ns = {"NO_REAL_PROCESSES": True, "stub": stub, "own": os.getpid()}
        # os.kill(own pid, 0) -- the liveness probe: still passes through,
        # so the fix NARROWED killpg rather than moving the divergence.
        exec("stub.kill(own, 0)", ns)          # noqa: S102 -- opted-in frame
        # os.killpg(own pgid, 0) -- a GROUP, refused outright in BOTH leaves.
        with pytest.raises(AssertionError, match="killpg at IMPORT time"):
            exec("stub.killpg(own, 0)", ns)     # noqa: S102
    finally:
        suite_guards.uninstall_import_fence(saved)
    assert calls == [("kill", (os.getpid(), 0))], (
        f"the killpg refusal armed a real syscall (or kill stopped "
        f"passing the own-pid probe): {calls}")


def test_the_real_context_conftest_installs_the_shared_guards():
    """Wiring pin: the DECLARED root on this box imports the one shared guard
    module rather than carrying its own (or exec'ing the engine conftest)."""
    src = (Path(__file__).resolve().parents[3] / ".agi" / "context"
           / "conftest.py").read_text(encoding="utf-8")
    assert "from suite_guards import" in src
    assert "exec(" not in src
    # the collection-time fence is installed by the DECLARED conftest too:
    # the fixtures alone cannot cover a module that spawns at import.
    assert "install_import_fence()" in src, (
        "the declared suite has no collection-time fence: an opted-in module "
        "that spawns AT IMPORT is unfenced")
    assert verification.__file__.endswith("verification.py")


def test_the_engine_strips_the_caller_env_for_the_declared_suite(
        tmp_path, monkeypatch):
    """The declared-suite spawn's `env=` used to be pinned by a SOURCE STRING
    (`assert "env=suite_guards.spawn_env()" in vsrc`), which any edit that kept
    the words and dropped the behaviour would satisfy. Behavioural instead: the
    env dict actually handed to the child LACKS a planted caller AGI_* var.

    The spawn is RECORDED, not run: a real declared-suite run is a whole extra
    pytest inside the caller's memory cap (this is how the previous kid on
    this node died -- `died-no-work` at 129 s), and the claim is only about
    the env dict, so nothing is spawned at all."""
    monkeypatch.setenv("AGI_SEAT", "a00-deadbeef")
    groot = _make_project(tmp_path, "ctx", """
        def test_ok():
            assert True
        """)
    seen = {}

    def _recorded_run(argv, **kw):
        seen["argv"], seen["env"] = list(argv), kw.get("env")
        return subprocess.CompletedProcess(argv, 0, "1 passed in 0.01s", "")

    monkeypatch.setattr(subprocess, "run", _recorded_run)
    res = verification.check_extra_suite(groot)
    assert res.status == "PASS", f"{res.status} {res.note} {res.message}"
    child = seen.get("env")
    assert isinstance(child, dict), (
        f"the declared suite was spawned with no env= of its own: {child!r}; "
        "it then inherits the caller's AGI_* wholesale")
    assert not [k for k in child if k.startswith(("AGI_", "AUTORESEARCH_"))], (
        f"caller AGI_* leaked into the declared-suite child: "
        f"{[k for k in child if k.startswith('AGI_')]}")
    # the parent's own environment is untouched by the strip
    assert os.environ["AGI_SEAT"] == "a00-deadbeef"


def test_the_shared_kill_leaf_allows_only_signal_zero_on_the_own_pid():
    """Residue 2 of verify_DH.430-k1: the guard's docstring said os.kill was
    fenced "signal-0 only" while the code checked pid membership alone, so an
    opted-in module could really `os.kill(os.getpid(), SIGKILL)`. The CODE now
    enforces what the docstring said. Driven with a RECORDER, so no syscall is
    ever armed: signal 0 on the own pid passes through and nothing else does."""
    import signal  # noqa: PLC0415
    calls = []
    guarded = suite_guards._make_guarded_kill(
        lambda pid, sig, *a, **k: calls.append((pid, sig)),
        frozenset({os.getpid()}))
    guarded(os.getpid(), 0)                       # the liveness probe: allowed
    with pytest.raises(AssertionError, match="signal 0"):
        guarded(os.getpid(), signal.SIGKILL)
    assert calls == [(os.getpid(), 0)], f"a real syscall was armed: {calls}"


def test_the_engine_conftest_imports_the_guard_instead_of_copying_it(
        monkeypatch):
    """Residue 1: suite_guards claims to be the ONE home, so the engine
    conftest must IMPORT the pieces, not carry a second body of each. Wired
    by NAME (a plain import, never exec -- DH.419's 127-process fork), and
    the historical spellings the leaf tests read by path are still there."""
    conf_path = Path(__file__).resolve().parent / "conftest.py"
    src = conf_path.read_text(encoding="utf-8")
    assert "from suite_guards import" in src
    assert "exec(" not in src
    assert "_FENCED_SPAWN_LEAVES = (" not in src, (
        "the engine conftest re-spells the leaf list; there is ONE list and "
        "it lives in suite_guards")
    # the names ARE the shared objects: the leaf list, the bound runners, the
    # kill leaves and the fixture itself, under its historical name.
    monkeypatch.setenv("AGI_TESTS_CONFTEST_UNIT_LOAD", "1")   # no session fence
    import importlib.util  # noqa: PLC0415
    spec = importlib.util.spec_from_file_location("engine_conftest_probe",
                                                  conf_path)
    conf = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(conf)                             # noqa: S102
    assert conf._FENCED_SPAWN_LEAVES is suite_guards._FENCED_SPAWN_LEAVES
    assert conf._FENCED_MODULE_RUNNERS is suite_guards._FENCED_MODULE_RUNNERS
    assert conf._make_guarded_kill is suite_guards._make_guarded_kill
    assert conf._make_guarded_killpg is suite_guards._make_guarded_killpg
    assert (getattr(conf, "_no_real_process_or_live_config", None)
            is suite_guards.no_real_process)


def test_two_env_strip_instances_keep_their_own_memo(monkeypatch):
    """The per-INSTANCE memo: two fixture instances live in ONE process (the
    engine suite's and the declared suite's, whose conftests both load), and
    one instance's teardown must not restore what the OTHER instance stripped.

    The REAL fixture body is driven directly -- the generator
    `make_agi_env_stripped_fixture()` returns is entered with `next()` and
    exited the way pytest finalizes it (resume to `StopIteration`; a bare
    `close()` would throw GeneratorExit at the yield and SKIP the restore
    after it). No child pytest, no spawned process.

    Enter A, enter B, exit B. B stripped nothing of its own (A had already
    taken the keys) so B's teardown must restore NOTHING: the keys A is
    still holding down must still be down. Red-first: with the old shared
    module-global `_STRIPPED` both instances read the SAME dict, so exiting B
    put the AGI_* channel back while A was still entered."""
    planted = "AGI_SEAT_TWO_INSTANCE_PROBE"
    monkeypatch.setenv(planted, "a00-deadbeef")
    assert planted in os.environ

    # pytest's @fixture wrapper refuses a direct call, so drive the GENERATOR
    # body itself -- `__wrapped__` is the undecorated function the decorator
    # wraps. Still the real fixture body: strip_dispatch_env, the yield, the
    # restore and the clear, all as pytest runs them.
    def _raw():
        made = suite_guards.make_agi_env_stripped_fixture()
        return getattr(made, "__wrapped__", made)()

    def _enter(gen):
        next(gen)
        return gen

    def _exit(gen):
        # pytest's own finalization: resume the body past its yield, so the
        # restore actually RUNS (close() would skip it -- GeneratorExit).
        with pytest.raises(StopIteration):
            next(gen)

    a = _raw()
    b = _raw()
    _enter(a)                     # A strips the AGI_* channel
    assert planted not in os.environ, "the fixture did not strip the channel"
    _enter(b)                     # B enters: there is nothing left to strip
    _exit(b)                      # B exits while A is STILL entered
    try:
        assert planted not in os.environ, (
            f"a second fixture instance's teardown restored what the FIRST "
            f"instance had stripped -- the memo is shared, not per-instance: "
            f"{planted}={os.environ.get(planted)!r} while instance A is still "
            f"entered")
    finally:
        _exit(a)                 # A's own teardown restores the channel
    assert os.environ[planted] == "a00-deadbeef", (
        "the owning instance's teardown did not restore what it stripped")


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))


#: the ONLY files that may name the fence marker (which holds the RAW stdlib
#: leaf): the installer, the tests OF the fence, this scan, and the one test
#: whose bash tick needs a real child. Adding a name here is the review.
_FENCE_MARKER_HOLDERS = {"conftest.py", "test_conftest_guard.py",
                         "test_declared_suite_guards.py",
                         "test_workflow_slice_isolation.py"}


def test_the_raw_leaf_escape_hatch_has_a_declared_allow_list():
    """Any opted-in file can read the raw `Popen` off the fence marker; no
    file may name the marker unless it is declared above."""
    tests = Path(__file__).resolve().parent
    holders = {f.name for f in tests.glob("*.py")
               if any(n in f.read_text(encoding="utf-8")
                      for n in ("__agi_spawn_fence__", "FENCE_MARKER"))}
    assert holders <= _FENCE_MARKER_HOLDERS, sorted(holders - _FENCE_MARKER_HOLDERS)
