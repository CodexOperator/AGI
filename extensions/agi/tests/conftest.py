"""Collection-time tier gate (goal:g15.6, hypothesis:l4-full-suite-tier-gate).

A brief-level instruction is not a mechanism: text in a node cannot refuse
anything. This conftest makes the "run a targeted path, not the whole suite"
rule a real gate for kid agents.

The signal already exists -- dispatch.py exports AGI_TIER into every spawn's
environment (a kid runs under AGI_TIER=kid). We only READ it here; nothing
else in production changes and no existing test is edited.

RULE (fire before collection, exit uncollected):
  * AGI_TIER == "kid"  AND  the invocation is a BARE DIRECTORY run
    (no specific test file named, no -k filter)  ->  REFUSED, one-line reason.
  * any other case  ->  behaviour exactly as today, including a bare
    directory run at every tier other than kid.

Which hook and why: ``pytest_cmdline_main(config)``. It fires immediately
after the command line has been parsed but BEFORE any collection begins, so a
refusal cannot be bypassed by letting collection start. At that point
``config.args`` still holds the positional paths the invocation named and
``config.option.kw`` holds the -k filter; both are exactly what we need to
tell a bare directory run from a targeted one.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

GATE_TIER = "kid"
REFUSAL_REASON = (
    "AGI_TIER=kid refuses a bare full-suite directory run; "
    "run a specific test file or a -k filter instead."
)

#: The gate hunts for running agent records under the resolved project tree's
#: `.agi/sessions` and nothing else (hypothesis:l4-the-kid-tier-gate-has-no-
#: env-seam, hypothesis:l4-the-record-root-has-no-test-seam-either). There is
#: NO env override and NO pytest option -- the old `--agent-records-root`
#: option and its `PYTEST_CURRENT_TEST` guard were dropped entirely, because
#: the guard was itself an env var, so a kid cleared the gate with one flag +
#: one spoofed var. In-process tests monkeypatch `_default_record_root`;
#: subprocess falsifier tests plant their record under the REAL tree's
#: sessions dir in a throwaway `iter-test-<uuid>` dir and remove it.


def _named_paths(args):
    """Return the positional args that look like paths (drop flag tokens)."""
    return [a for a in (args or []) if a and not a.startswith("-")]


#: Record paths already named as phantoms THIS session. A phantom running
#: record (dead pid) is reported at most once per process even when several
#: roots scan the same leftover record, so the trace stays one line per
#: phantom, not one line per scan pass (hypothesis:l4-a-phantom-running-
#: record-with-a-dead-pid-is-named).
_phantom_reported = set()


def _running_record_tiers(root) -> dict:
    """{pid: int: tier: str} for every agent.json under root/**/agent.json
    that records a LIVE running agent (status == "running", numeric pid,
    string tier). Malformed or non-running records are skipped.

    A record whose pid has no /proc/<pid> entry is skipped too
    (hypothesis:l4-a-running-record-with-a-dead-pid-is-not-a-running-agent):
    a SIGKILLed test run skips its `finally`-cleanup and leaves a phantom
    `status: running` record with a dead pid behind, which every later scan
    would otherwise count -- a reused pid number on a later run's ancestor
    chain would inherit that phantom's tier. Liveness is the cheap,
    Linux-only `os.path.exists(f"/proc/{pid}")` probe, matching the reaper's
    own /proc-based liveness test: a running record whose pid is gone is not
    a running agent, whatever its status field says.
    """
    result = {}
    if not root or not os.path.isdir(str(root)):
        return result
    for agent_file in Path(root).rglob("agent.json"):
        try:
            with open(agent_file, encoding="utf-8") as f:
                rec = json.load(f)
        except (OSError, ValueError):
            continue
        status = rec.get("status")
        pid = rec.get("pid")
        tier = rec.get("tier")
        if status != "running" or not isinstance(pid, int) or not isinstance(tier, str):
            continue
        # A dead-pid running record is a phantom, not an agent: skip it,
        # but NAME it on stderr so a SIGKILLed leftover is visible instead of
        # silently ignored (hypothesis:l4-a-phantom-running-record-with-a-
        # dead-pid-is-named). One line per record path per session. This is
        # trace, not action: the tests dir is not the record's owner, so we
        # never delete -- cleaning the phantom is the reaper's job.
        if not os.path.exists(f"/proc/{pid}"):
            if str(agent_file) not in _phantom_reported:
                _phantom_reported.add(str(agent_file))
                print(
                    f"tier-gate: phantom running record {agent_file} "
                    f"pid={pid} (dead) -- skipped",
                    file=sys.stderr,
                )
            continue
        result[pid] = tier
    return result


def _default_record_root():
    """The ONE production root, always tree-derived. The agent.json dispatch
    writes per run lives under the graph's sessions dir:
    `<graph>/.agi/sessions/iter-*/<agent>/agent.json`. locations.
    find_project_root resolves the `.agi` DIRECTORY itself (the one holding
    config.json), so the sessions dir is `root / "sessions"` -- NOT
    `root /.agi / sessions`, which doubles the dotdir and scans nothing.
    There is deliberately NO env override (hypothesis:l4-the-kid-tier-gate-
    has-no-env-seam): a production env var a kid can set must not point the
    scan elsewhere.
    """
    root = locations.find_project_root(Path(__file__).resolve())
    if root is None:
        return None
    return str(Path(root) / "sessions")


def _record_root():
    """The invoking tree's OWN root -- tree-derived and nothing else
    (hypothesis:l4-the-record-root-has-no-test-seam-either). The old
    `--agent-records-root` option, the `_TEST_AGENT_RECORDS_ROOT` global and
    the `PYTEST_CURRENT_TEST` guard are gone: a kid cannot move the scan
    with any env var or any flag. In-process tests monkeypatch
    `_default_record_root`. This single root is the FIRST of the multiple
    roots `_record_roots()` scans (hypothesis:l4-the-kid-tier-gate-scans-
    every-root-it-can-reach); it is kept separate so a test may isolate the
    per-tree root from the reach-across-worktrees scan.
    """
    return _default_record_root()


def _record_roots():
    """Every sessions dir THIS invocation scans, as unique resolved paths
    (hypothesis:l4-the-kid-tier-gate-scans-every-root-it-can-reach): first
    the invoking tree's OWN sessions dir, then the project's shared sessions
    dir, then the sessions dir of every worktree registered under the main
    graph's `.agi/worktrees/*`.

    Before this fix the gate derived its root from ONLY the conftest's own
    tree (`find_project_root(Path(__file__))`). A kid that pointed pytest at
    MAIN's absolute tests dir (`python3 -m pytest /home/.../extensions/agi/
    tests/`) therefore scanned MAIN's sessions dir, found no agent.json for
    its OWN pid chain, derived no tier and ran the bare directory suite it is
    refused from its own worktree. Scanning every reachable root closes that:
    the kid's running record lives in its OWN worktree's sessions, which this
    scan reaches no matter which tree's tests dir the invocation names.
    """
    roots = []
    seen = set()

    def _add(p):
        if p is None:
            return
        rp = str(Path(p).resolve())
        if rp not in seen:
            seen.add(rp)
            roots.append(rp)

    # 1) the invoking tree's own sessions dir (the per-worktree fork).
    _add(_default_record_root())

    # 2) the shared room + every worktree, resolved from the main checkout
    #    through git_common_root so a scan from any worktree reaches the room
    #    every seat writes (the boundary's recurring face -- shared state
    #    resolved per-worktree instead of through git_common_root).
    #    hypothesis:l4-the-tier-gate-scan-is-not-redirectable-by-git-env:
    #    when git reports NOTHING (no enclosing repo, or `git rev-parse`
    #    fails under a gutted GIT_DIR / GIT_COMMON_DIR -- which the caller
    #    has already popped, but defensively fall back all the same), the
    #    main graph resolves from the conftest's OWN file path -- the one
    #    root a kid cannot redirect. Never let a failed git lookup silently
    #    narrow the scan to fewer roots.
    root = locations.find_project_root(Path(__file__).resolve())
    if root is not None:
        try:
            main_graph = locations.shared_project_root(root)
        except Exception:
            main_graph = None
        if main_graph is None:
            main_graph = root
        if main_graph:
            wt_root = Path(main_graph) / "worktrees"
            if wt_root.is_dir():
                for wt in sorted(wt_root.iterdir()):
                    if not wt.is_dir():
                        continue
                    wt_graph = locations.find_project_root(wt)
                    if wt_graph is not None:
                        _add(Path(wt_graph) / "sessions")
            if (Path(main_graph) / "nodes").is_dir():
                _add(Path(main_graph) / "sessions")
            elif (Path(main_graph) / ".agi" / "nodes").is_dir():
                _add(Path(main_graph) / ".agi" / "sessions")
            else:
                _add(Path(main_graph) / "sessions")
    return roots


def _ppid_of(pid):
    """Real parent pid of `pid` from /proc, or None. The live process uses
    os.getppid(); every other pid reads field 4 of /proc/<pid>/stat. The comm
    field may itself contain spaces and ) characters, so split on the LAST ).
    """
    if pid == os.getpid():
        return os.getppid()
    try:
        with open(f"/proc/{pid}/stat", encoding="utf-8") as f:
            data = f.read()
        rest = data.rsplit(")", 1)[1].split()
        return int(rest[1])  # state rest[0], ppid rest[1]
    except (OSError, ValueError, IndexError):
        return None


def _resolve_tier_from_ancestors(pid_tier, ppid_lookup, pid):
    """The tier of the first running record whose pid lies on the ancestor
    chain of `pid`, nearest ancestor wins; None when no running record
    matches any ancestor. `ppid_lookup(pid) -> parent pid | None` is injected
    so the pure decision is unit-testable with a fake chain.
    """
    cur = pid
    for _ in range(128):  # loop guard on a cyclic/pid-recycled chain
        if cur in pid_tier:
            return pid_tier[cur]
        nxt = ppid_lookup(cur)
        if nxt is None or nxt == cur:
            return None
        cur = nxt
    return None


def _effective_tier():
    """The tier for THIS invocation. hypothesis:l4-the-kid-tier-gate-is-not-
    clearable-from-inside-a-kid: prefer the tier of a running agent record
    (agent.json) whose pid is an ANCESTOR of the pytest process, so the gate
    derives the tier from the environment that actually spawned the run
    rather than from AGI_TIER -- which a kid could simply `env -u`. The scan
    spans EVERY reachable sessions root (hypothesis:l4-the-kid-tier-gate-
    scans-every-root-it-can-reach), so a kid cannot escape by pointing pytest
    at another tree's tests dir: its running record lives in ITS OWN
    worktree's sessions, which `_record_roots()` reaches from any tree.
    The pid->tier map is process-global, so EVERY reachable root is merged
    into ONE dict BEFORE the ancestor chain is resolved. Merging first makes
    the outcome independent of root scan order: a pytest process carries
    multiple records on its own chain (its own record, the parent that
    spawned it, the director above that) and they may live in different
    roots. Resolving per-root and taking the first hit let root ORDER decide
    which one won -- a kid whose own record sat in a later-scanned root while
    a parent record sat in an earlier-scanned root cleared the gate. With the
    merged map, nearest ancestor wins: the process's own pid is the nearest,
    so its own record always beats an ambient (parent/director) record
    farther up the chain. Only when NO running record in ANY root matches
    any ancestor does it fall back to AGI_TIER, exactly as before, so a
    plain interactive run at any tier keeps working.
    """
    merged = {}
    for root in _record_roots():
        merged.update(_running_record_tiers(root))
    record_tier = _resolve_tier_from_ancestors(merged, _ppid_of, os.getpid())
    if record_tier is not None:
        return record_tier
    return os.environ.get("AGI_TIER")


def _is_bare_directory_run(config) -> bool:
    """True when this invocation collects a whole directory with no target.

    Bare means: no -k filter AND every path argument is a directory (or there
    is no path argument at all, so pytest falls back to the configured
    testpaths). Naming any specific ``.py`` test file makes it a targeted run.
    """
    option = getattr(config, "option", None)
    # In pytest the -k filter lands on option.keyword (not option.kw).
    kw = getattr(option, "keyword", None) or getattr(option, "kw", None)
    if kw:
        return False
    paths = _named_paths(getattr(config, "args", None))
    if not paths:
        # No path named -> bare directory run (routes to testpaths).
        return True
    # Refuse only if EVERY named arg is a directory (no explicit test file).
    return all(p.endswith(os.sep) or os.path.isdir(p) or not p.endswith(".py") for p in paths)


def pytest_cmdline_main(config):
    # No test-only seam remains: no option to read, no global to feed, no
    # PYTEST_CURRENT_TEST to be spoofed (hypothesis:l4-the-record-root-has-
    # no-test-seam-either). Forget any stale dead env vars a host may still
    # carry, then derive the tier. Nothing below can be re-armed.
    os.environ.pop("AGI_AGENT_SESSIONS_ROOT", None)
    # Strip the git-redirection vars BEFORE any root is resolved
    # (hypothesis:l4-the-tier-gate-scan-is-not-redirectable-by-git-env).
    # `_record_roots()` reaches `<main>/.agi/worktrees/*` through
    # `locations.shared_project_root` -> `git_common_root` -> `git -C <d>
    # rev-parse --git-common-dir`, which honours GIT_DIR / GIT_COMMON_DIR /
    # GIT_WORK_TREE in the environment. A kid that exports any of these
    # before `pytest` points the scan at a repo of its choosing, finds no
    # record for its own pid chain, and runs the bare-directory suite it is
    # refused. Popping them here closes the env seam one layer down, exactly
    # as AGI_AGENT_SESSIONS_ROOT was already popped just above.
    for _g in ("GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE"):
        os.environ.pop(_g, None)
    if _effective_tier() != GATE_TIER:
        # Invisible at every tier other than kid (record-derived), and when
        # the tier is unset AND no running agent record matches an ancestor.
        return
    if _is_bare_directory_run(config):
        raise pytest.UsageError(REFUSAL_REASON)


@pytest.fixture(autouse=True)
def _no_real_tmux(monkeypatch):
    """hypothesis:l4-conftest-tmux-guard — project-wide tmux guard, widened
    from test_send.py's old file-local `_SafeSubprocess`/`_no_real_tmux`
    (hypothesis:l4b23-fixture-leak, CLOSED proved but scoped to send.py only).

    Every test must never reach the live tmux session
    (`rotate.DEFAULT_TMUX_SESSION`, "agi-rc"), where a recipient whose name
    matches a real window would have text typed into a live agent's terminal.
    The guard answers any `tmux` subprocess call with a safe rc-1
    CompletedProcess (so `_nudge_window`/`_existing_windows` short-circuit to
    "no such session", exactly as the old `_SafeSubprocess` did for tmux).

    **Selective, not blanket**: every NON-tmux call (in particular the real
    `git` invocations test_season.py/test_rotate.py's own fixtures depend on)
    is passed through untouched to the real `subprocess.run`. Requesting a
    raise on any non-tmux call (the old `_SafeSubprocess` behaviour) would
    break those tests — see the L4.5x brief.

    Patch target: the real stdlib `subprocess.run`.
    send.py/rotate.py/season.py `import subprocess`, and mail_alert.py
    `import send` (whose module object `import subprocess` too), so every
    module's tmux call ultimately resolves through this one attribute — one
    fixture covers the whole suite. A per-module-alias patch would defeat
    the "project-wide" point.

    Override-precedence for the three `_fake_tmux` tests in test_send.py:
    they monkeypatch `send_mod.subprocess.run` (= this same global
    `subprocess.run`) in the TEST BODY, after this autouse fixture's setup, so
    their fake wins for the duration of the test. (monkeypatch is
    function-scoped, so the fixture's and the test's instances are the same;
    both revert at teardown.)
    """
    real_run = subprocess.run

    def _guarded_run(cmd, *a, **k):
        if isinstance(cmd, list) and cmd[:1] == ["tmux"]:
            return subprocess.CompletedProcess(cmd, 1)
        return real_run(cmd, *a, **k)

    monkeypatch.setattr(subprocess, "run", _guarded_run)


@pytest.fixture(autouse=True)
def _no_real_provisioning_call(monkeypatch):
    """hypothesis:l4-mint-refuses-under-pytest-unless-mocked — project-wide
    provisioning guard: no test may ever reach the real key-management HTTP
    seam (`provisioning._call`), which would mint/revoke a REAL key against
    OpenRouter.

    The `mint`/`revoke` guard in provisioning.py is the first line (it
    refuses under `PYTEST_CURRENT_TEST` when the seams are real). This
    autouse fixture is the second, independent line: it replaces
    `provisioning._call` with a function that raises, so ANY test that
    reaches the HTTP seam without mocking it in its own body fails loudly
    instead of minting.

    Every test that exercises mint/revoke mocks `_call` (and
    `_read_provisioning_key`) in its own BODY, and monkeypatch is
    function-scoped (same instance as this fixture), so the test's fake wins
    for the duration of the test and this raised sentinel never fires. Only a
    test that forgot to mock — or a live-API test — reaches it, and both are
    exactly what must fail loudly under this round's policy.
    """
    import provisioning

    def _refuse(method, url, key, payload=None, timeout=30):
        raise RuntimeError(
            "real provisioning HTTP call from a test")

    monkeypatch.setattr(provisioning, "_call", _refuse)


# --- the suite lock belongs to the resource, not a caller -------------------
# `hypothesis:l4-the-suite-lock-belongs-to-pytest-not-its-caller`. Every path
# that starts the pytest suite goes THROUGH this conftest (commands.py run
# tests, verification.py --suite, season.py merge-up, a bare shell), so the
# lock lives here, resolved from Path(__file__) — never cwd — and every caller
# contends for the one file.
_BIN = Path(__file__).resolve().parent.parent / "bin"
if str(_BIN) not in sys.path:
    sys.path.insert(0, str(_BIN))
import locations  # noqa: E402
import verification  # noqa: E402

#: Whether the provisioning mutation guard (hypothesis:l4-mint-refuses-under-
#: pytest-unless-mocked) is engaged for this suite. When True, the `@live`
#: real-API provisioning tests are skipped by policy: a test can never mint or
#: revoke a real key, so no test may reach provisioning._call un-mocked. Read
#: by test_provisioning.py's `live` marker to skip them cleanly.
PROVISIONING_TESTS_ARE_GUARDED = True


#: Reentrancy marker. The suite runs pytest INSIDE pytest (test_tier_gate.py's
#: nested runs) and verification.py --suite spawns pytest as a child with no
#: env=, so children inherit os.environ. A nested pytest must NO-OP here, or it
#: refuses itself against its own parent's live lock and deadlocks the round.
#: The name must NOT begin AGI_ or AUTORESEARCH_ (extensions/agi/conftest.py
#: strips those prefixes) — that is why it is VERIFY_*.
SUITE_LOCK_MARKER = "VERIFY_SUITE_LOCK_PID"


@pytest.fixture(scope="session", autouse=True)
def _suite_lock_guard():
    """Acquire the suite lock for the whole pytest session, once.

    A bare `python3 -m pytest extensions/agi/tests/` creates
    `<graph>/sessions/verify-suite.lock` with its own pid and removes it on
    exit. A second independent pytest started while the first runs finds the
    lock held by a LIVE pid and REFUSES, naming that holder. A nested pytest
    (pytest inside pytest) inherits SUITE_LOCK_MARKER from its acquiring
    parent and NO-OPS — the parent still holds the window, so the child must
    not re-acquire.
    """
    if os.environ.get(SUITE_LOCK_MARKER):
        # Inherited: our parent process holds the suite window for this run.
        yield
        return

    root = locations.find_project_root(Path(__file__).resolve())
    if root is None:
        # Not inside an agi project — no graph sessions dir to guard. No-op.
        yield
        return
    lock_path, holder = verification.acquire_suite_lock(root)
    if lock_path is None:
        if holder is None:
            raise RuntimeError(
                "suite window refused — the suite lock could not be written "
                f"under {root / 'sessions'}")
        raise RuntimeError(
            f"suite window refused — pid {holder} is a LIVE runner holding "
            f"{root / 'sessions' / verification.SUITE_LOCK}; one suite at a "
            "time — wait for it or ask whoever owns it")
    os.environ[SUITE_LOCK_MARKER] = str(os.getpid())
    try:
        yield
    finally:
        os.environ.pop(SUITE_LOCK_MARKER, None)
        if lock_path.exists():
            try:
                lock_path.unlink()
            except OSError:
                pass