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
from suite_guards import agi_env_stripped, no_real_process, suite_lock  # noqa
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
    (groot / "sessions" / verification.SUITE_LOCK).write_text(
        str(holder), encoding="utf-8")
    monkeypatch.delenv(verification.SUITE_LOCK_MARKER, raising=False)
    res = verification.check_extra_suite(groot)
    out = f"{res.status} {res.note} {res.message}"
    assert "suite window refused" in out, out
    assert str(holder) in out, out
    (groot / "sessions" / verification.SUITE_LOCK).unlink()


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


def test_the_real_context_conftest_installs_the_shared_guards():
    """Wiring pin: the DECLARED root on this box imports the one shared guard
    module rather than carrying its own (or exec'ing the engine conftest)."""
    src = (Path(__file__).resolve().parents[3] / ".agi" / "context"
           / "conftest.py").read_text(encoding="utf-8")
    assert "from suite_guards import" in src
    assert "exec(" not in src
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


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
