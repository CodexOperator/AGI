"""The suite guards, in ONE importable home, for EVERY suite in a project.

`extensions/agi/tests/` and the DECLARED second suite (`paths.core.suite_roots`,
e.g. `.agi/context`, spawned by verification.py:check_extra_suite) are two
suites of the SAME project. Before this module they were two worlds: the lock,
the dispatch-env strip and the real-process / live-config guard lived in the
engine conftests, so two declared-suite runs overlapped, a context test could
signal a live pid or read the live `.agi/config.json`, and the caller's
AGI_SEAT/AGI_TIER/AGI_AGENT reached the child
(hypothesis:the-declared-context-suite-runs-under-the-engine-suite-guards).

PLAIN import, never exec: a conftest that execs another conftest is how DH.419
forked 127 pytest processes (FORK-BOUND 1). A conftest installs the guards by
importing the fixtures below:

    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "extensions" / "agi" / "bin"))
    from suite_guards import suite_lock, agi_env_stripped, no_real_process

Imported fixtures are collected normally: pytest finds them by NAME in the
conftest module's namespace, and the name keeps the autouse property of the
definition site.
"""

import builtins
import io
import os
import sys
from pathlib import Path

import pytest

_BIN = Path(__file__).resolve().parent
if str(_BIN) not in sys.path:
    sys.path.insert(0, str(_BIN))
import locations    # noqa: E402
import verification  # noqa: E402

#: One spelling, re-exported: verification.py and both conftests read the
#: marker from here so a rename cannot desync the three readers.
SUITE_LOCK_MARKER = verification.SUITE_LOCK_MARKER
#: Graph root override. VERIFY_-prefixed so the AGI_* strip below keeps it; a
#: suite run inside a tmp graph must lock ITS OWN window, never the live one.
GRAPH_ROOT_ENV = "VERIFY_GRAPH_ROOT"
#: The dispatcher's non-AGI spawn channel (extensions/agi/conftest.py): a kid
#: is spawned with core.hooksPath in the env, so every `git` a test shells out
#: to would run the commit guard.
GIT_CONFIG_SPAWN_VARS = ("GIT_CONFIG_COUNT", "GIT_CONFIG_KEY_0",
                         "GIT_CONFIG_VALUE_0")


def spawn_env(base=None) -> dict:
    """The env a suite child is spawned with: no caller AGI_*/AUTORESEARCH_*
    and no git-hook channel. The suite lock MARKER is deliberately KEPT -- it
    is not AGI_* and it is what lets a spawned suite run inside the window its
    own caller already holds (a nested/second suite must not refuse itself)."""
    env = dict(os.environ if base is None else base)
    for key in list(env):
        if key.startswith(("AGI_", "AUTORESEARCH_")) or key in GIT_CONFIG_SPAWN_VARS:
            env.pop(key, None)
    return env


def graph_root():
    """(Path|None) the graph whose window this suite contends for: the
    VERIFY_GRAPH_ROOT override, else the project of the invocation cwd, else
    the project the guards ship from."""
    override = os.environ.get(GRAPH_ROOT_ENV)
    if override:
        return Path(override)
    return locations.find_project_root(Path.cwd()) or locations.find_project_root(
        Path(__file__))


def make_suite_lock_fixture(root_resolver):
    """The suite-lock guard as ONE body with a caller-supplied ROOT POLICY.

    `root_resolver()` names the graph whose window this run contends for: the
    engine suite passes `find_project_root(Path(__file__))` (its own file,
    never the cwd, hypothesis:l4-the-suite-lock-belongs-to-pytest-not-its-
    caller), the declared context suite keeps `graph_root()`. Same lock file,
    same marker, same refusal -- only the root is an argument."""
    @pytest.fixture(scope="session", autouse=True)
    def suite_lock():
        if os.environ.get(SUITE_LOCK_MARKER):
            yield
            return
        root = root_resolver()
        if root is None:
            yield
            return
        lock_path, holder = verification.acquire_suite_lock(root)
        if lock_path is None:
            raise RuntimeError(
                "suite window refused — the suite lock could not be written "
                f"under {root / 'sessions'}" if holder is None else
                f"suite window refused — pid {holder} is a LIVE runner holding "
                f"{root / 'sessions' / verification.SUITE_LOCK}; one suite at a "
                "time — wait for it or ask whoever owns it")
        os.environ[SUITE_LOCK_MARKER] = str(os.getpid())
        try:
            yield
        finally:
            os.environ.pop(SUITE_LOCK_MARKER, None)
            lock_path.unlink(missing_ok=True)
    return suite_lock


#: The declared-suite policy: VERIFY_GRAPH_ROOT, else the invocation cwd's
#: project, else the project the guards ship from.
suite_lock = make_suite_lock_fixture(graph_root)


def strip_dispatch_env(extra_keys=(), env=None, memo=None) -> dict:
    """Remove every AGI_*/AUTORESEARCH_* key, plus `extra_keys`, from `env`
    (default os.environ), remembering the values in the returned `memo` so a
    caller with its OWN dict (extensions/agi/conftest.py's `_AGI_STRIPPED`,
    driven by path from test_agi_env_strip.py) keeps reading and writing it.
    The engine suite passes the dispatcher's git-hook channel as `extra_keys`
    (core.hooksPath is not AGI_*-prefixed, so the glob alone leaves it and
    every `git` a test shells out to would run the commit guard); the declared
    context suite passes nothing."""
    env = os.environ if env is None else env
    memo = {} if memo is None else memo
    extra = tuple(extra_keys or ())
    for key in list(env):
        if key.startswith(("AGI_", "AUTORESEARCH_")) or key in extra:
            memo[key] = env.pop(key, None)
    return memo


def restore_dispatch_env(memo) -> None:
    """Put back exactly what `strip_dispatch_env` removed, and nothing else."""
    for key, value in (memo or {}).items():
        os.environ.pop(key, None)
        if value is not None:
            os.environ[key] = value


def make_agi_env_stripped_fixture(extra_keys=()):
    """The dispatch-env strip as ONE body, plus whatever extra non-AGI channel
    the caller names: a suite is green or red on the same bytes whichever seat
    spawned it.

    The memo is PER FIXTURE INSTANCE, held in the closure: it used to be the
    module-global `_STRIPPED`, so two instances (the engine suite's
    make_agi_env_stripped_fixture() and the declared suite's, in one process
    where both conftests load) shared one dict and one's teardown restored
    what the other had stripped -- note 1 of verify_DH.440-k1."""
    @pytest.fixture(scope="session", autouse=True)
    def agi_env_stripped():
        stripped = strip_dispatch_env(extra_keys)
        yield
        restore_dispatch_env(stripped)
        stripped.clear()
    return agi_env_stripped


#: The declared-suite policy: the AGI_*/AUTORESEARCH_* channel only.
agi_env_stripped = make_agi_env_stripped_fixture()


def own_pid_signal0_only(pid, sig, own_pids) -> bool:
    """The ONE legality predicate for `os.kill` traffic under a
    NO_REAL_PROCESSES guard: the OWN pid AND signal 0, nothing else. Signal 0
    on our own pid is a liveness probe -- it delivers nothing -- so it is the
    only signal a guarded leaf may pass through, and `own_pids` is the caller's
    own pid and NOTHING else.

    TWO leaves call it and neither may re-decide: the fixture leaf
    (`no_real_process` -> `_make_guarded_kill`) and the IMPORT-time leaf
    (extensions/agi/tests/conftest.py's `_make_import_time_fence`, which had
    its own copy checking pid membership ALONE, so a module that
    `os.kill(os.getpid(), SIGKILL)`ed at collection really killed the runner
    -- residue 1 of verify_DH.440-k1)."""
    try:
        return int(pid) in own_pids and int(sig) == 0
    except (TypeError, ValueError):
        return False


#: A test module opts in with `NO_REAL_PROCESSES = True`; the guard is opt-in
#: because a suite-wide spawn ban would red every test that runs real `git`.
OPT_IN_ATTR = "NO_REAL_PROCESSES"
#: (module-name, attr) process-creating stdlib leaves. ONE list for the whole
#: repo: the engine conftest IMPORTS this name from here instead of keeping a
#: copy that could drift from it, so a leaf added in one place is fenced in
#: both suites.
_FENCED_SPAWN_LEAVES = (
    ("subprocess", "Popen"), ("subprocess", "run"), ("subprocess", "call"),
    ("subprocess", "check_output"), ("os", "fork"), ("os", "forkpty"),
    ("os", "execv"), ("os", "execve"), ("os", "execvp"), ("os", "execvpe"),
    ("os", "posix_spawn"), ("os", "posix_spawnp"), ("os", "system"),
    ("pty", "spawn"),
)
#: The engine BOUNDS the stdlib spawners at import time (`rotate._RUN`,
#: `workflow._REAL_POPEN/_REAL_RUN`), so a stdlib hook alone misses them.
_FENCED_MODULE_RUNNERS = (
    ("rotate", "_RUN"),
    ("workflow", "_REAL_POPEN"),
    ("workflow", "_REAL_RUN"),
)


def _fence_bound_runners(setattr_, refuse):
    """Fence the engine's import-time spawner bindings. Best effort: a module
    that is not importable here contributes nothing and raises nothing."""
    for mod_name, attr in _FENCED_MODULE_RUNNERS:
        try:
            mod = __import__(mod_name)
        except Exception:            # noqa: BLE001 -- absent here, no fence
            continue
        if hasattr(mod, attr):
            setattr_(mod, attr, refuse)


def _make_guarded_kill(real_kill, own_pids):
    """The `os.kill` leaf the guard installs, parameterised so a test can unit
    it with a recorder and never arm a syscall. `own_pids` is the caller's own
    pid and NOTHING else, and signal 0 is the ONLY traffic that reaches the
    real call -- residue 2 of verify_DH.430-k1: both copies of this guard
    claimed "signal-0 only" while the code checked pid membership alone."""
    def _guarded_kill(pid, sig, *a, **k):
        if own_pid_signal0_only(pid, sig, own_pids):
            return real_kill(pid, sig, *a, **k)
        if int(pid) not in own_pids:
            raise AssertionError(
                f"guard: a NO_REAL_PROCESSES test signalled pid {pid}; only "
                "its own pid may be signalled, and only for a signal-0 "
                "liveness probe")
        raise AssertionError(
            f"guard: a NO_REAL_PROCESSES test sent signal {sig} to its own "
            "pid; signal 0 (the liveness probe) is the only signal a guarded "
            "test may send")
    return _guarded_kill


def _make_guarded_killpg(real_killpg):
    """`os.killpg` is refused OUTRIGHT: a group leader the test spawned may sit
    in a group that also holds a shell the test never spawned, so "own pid" is
    not a sound exemption for a GROUP. `real_killpg` is a parameter so a test
    can prove with a RECORDER that no syscall is armed."""
    def _guarded_killpg(pgid, sig, *a, **k):
        raise AssertionError(
            f"guard: a NO_REAL_PROCESSES test signalled process GROUP {pgid}; "
            "a group is refused outright -- a group leader this test spawned "
            "can share a group with a shell it did not")
    return _guarded_killpg


@pytest.fixture(autouse=True)
def no_real_process(request, monkeypatch):
    """An opted-in module may not: spawn a process, read `/proc`, `os.kill` a
    pid that is not its own, `os.killpg` at all, or open a real
    `.agi/config.json` outside its own tmp_path.

    Three patch points, all at the stdlib leaf every caller resolves through:
    builtins.open AND io.open (Path.read_text resolves io.open at call time;
    the C _io.open never calls the Python os.open, so an os.open hook catches
    nothing), and os.scandir/os.listdir for the directory walk. `os.kill` is
    fenced to the test's OWN pid, signal-0 only -- signal 0 on our own pid is
    a liveness probe, not a kill."""
    module = getattr(request, "module", None)
    if not getattr(module, OPT_IN_ATTR, False):
        yield
        return
    tmp = str(request.getfixturevalue("tmp_path"))
    own = frozenset({os.getpid()})
    real_open, real_scandir, real_listdir = builtins.open, os.scandir, os.listdir
    real_kill, real_killpg = os.kill, os.killpg

    def _check(path):
        try:
            seen = os.fspath(path)
        except TypeError:          # an int fd
            return
        if seen.startswith("/proc"):
            raise AssertionError(
                "guard: a NO_REAL_PROCESSES test read /proc; stub the "
                "process table, never the live one")
        if seen.endswith(".agi/config.json") and not seen.startswith(tmp):
            raise AssertionError(
                f"guard: a NO_REAL_PROCESSES test opened the LIVE config "
                f"{seen!r}; the live cell belongs to "
                "tests/test_live_config_cells.py")

    def _open(path, *a, **k):
        _check(path)
        return real_open(path, *a, **k)

    def _refuse_spawn(*a, **k):
        raise AssertionError(
            "guard: a NO_REAL_PROCESSES test spawned a process; inject the "
            "seam (pid list, kill, liveness probe) instead")

    def _scandir(path=".", *a, **k):
        _check(path)
        return real_scandir(path, *a, **k)

    def _listdir(path=".", *a, **k):
        _check(path)
        return real_listdir(path, *a, **k)

    monkeypatch.setattr(builtins, "open", _open)
    monkeypatch.setattr(io, "open", _open)
    monkeypatch.setattr(os, "scandir", _scandir)
    monkeypatch.setattr(os, "listdir", _listdir)
    monkeypatch.setattr(os, "kill", _make_guarded_kill(real_kill, own))
    monkeypatch.setattr(os, "killpg", _make_guarded_killpg(real_killpg))
    for mod_name, attr in _FENCED_SPAWN_LEAVES:
        mod = sys.modules.get(mod_name)
        if mod is None:
            try:                     # noqa: PLC0415 -- lazy on purpose
                mod = __import__(mod_name)
            except Exception:        # noqa: BLE001 -- absent here, no fence
                continue
        if hasattr(mod, attr):
            monkeypatch.setattr(mod, attr, _refuse_spawn)
    _fence_bound_runners(monkeypatch.setattr, _refuse_spawn)
    yield
