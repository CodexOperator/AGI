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

import builtins
import io
import json
import os
import subprocess
import sys
from pathlib import Path

# AA1/W: send.py + workflow.py live under deprecated/bin (no live bin shims).
# Suite tests still import those module names; put deprecated/bin on path so
# collection resolves the real deprecated modules without resurrecting bin/*.
_DEPR_BIN = Path(__file__).resolve().parents[1] / "deprecated" / "bin"
if _DEPR_BIN.is_dir() and str(_DEPR_BIN) not in sys.path:
    sys.path.insert(0, str(_DEPR_BIN))

import pytest

GATE_TIER = "kid"

# FAIL CLOSED (corrective DH.DG1.02 item 1): a worktrees entry we cannot read
# is an UNKNOWN record, never an absent one. `_record_roots` sets this when
# its per-entry guard drops an entry; `_effective_tier` reads it so an
# unreadable entry can never be laundered into an AGI_TIER fallback.
# Never reset on purpose: a process that has seen an unknown record stays
# closed; the one-shot pytest_cmdline_main use makes that harmless.
_WORKTREES_ENTRY_DROPPED = False
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
    """Resolve `<graph>/.agi/sessions` from the invoking tree via the
    registered `sessions_dir` resolver (claim 1); refuse a scratch (claim 2)."""
    root = locations.find_project_root(Path.cwd())
    if root is None:
        return None
    out = _PROD_SESSIONS_DIR(root)
    locations.refuse_live_sessions_from_plain_scratch(out)
    return str(out)


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
                global _WORKTREES_ENTRY_DROPPED  # set by either OSError arm
                try:
                    entries = sorted(wt_root.iterdir())
                except OSError:
                    _WORKTREES_ENTRY_DROPPED = True  # unknown, not absent
                    entries = []  # an unreadable worktrees dir scans empty
                for wt in entries:
                    try:
                        if not wt.is_dir():
                            continue
                        wt_graph = locations.find_project_root(wt)
                    except OSError:
                        _WORKTREES_ENTRY_DROPPED = True  # unknown, not absent
                        continue  # one unreadable entry never kills collection
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
    if _WORKTREES_ENTRY_DROPPED:
        # Fail closed: the skipped entry may have held ANY record, so the gate
        # answers with the most restrictive tier it knows rather than falling
        # through to an env var the caller controls.
        return GATE_TIER
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
    # Strip the RUNNER'S sender identity too. `send._detect_sender` reads
    # AGI_AGENT_ID, then AGI_POST/AGI_SEAT, AHEAD of an explicit --from, so a
    # suite run from a rotate-self-spawned seat (which exports AGI_POST +
    # AGI_SEAT since 18a09849d) or from a dispatched kid (AGI_AGENT_ID since
    # L3.20) signs every test message under the runner's name: measured
    # 2026-09-12 07:1xZ on the sensei-director seat, test_send.py 81 failed /
    # 274 with AGI_SEAT set, 75 failed with AGI_AGENT_ID set, 274 passed with
    # neither. A test that needs one sets it with monkeypatch AFTER this pop.
    for _g in ("AGI_AGENT_ID", "AGI_SEAT", "AGI_POST"):
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
        # goal:g6.41.1 R1 (sanctuary-master mur wf_67ad5686-154 residue 69): no
        # test moves, stops or scopes a REAL unit unless AGI_LIVE_SYSTEMD=1 --
        # busctl, `systemctl stop|kill`, and a systemd-run that starts tmux
        if isinstance(cmd, list) and not _LIVE_SYSTEMD_ON and (
                cmd[:1] == ["busctl"]
                or (cmd[:1] == ["systemctl"] and ("stop" in cmd or "kill" in cmd))
                or (cmd[:1] == ["systemd-run"] and "tmux" in cmd)):
            return subprocess.CompletedProcess(cmd, 1)
        return real_run(cmd, *a, **k)

    monkeypatch.setattr(subprocess, "run", _guarded_run)


@pytest.fixture(autouse=True)
def _calm_box_psi(monkeypatch, tmp_path_factory):
    """goal:g6.41.1 R2 (sanctuary-master mur wf_67ad5686-154 residue 72): no
    test reads the HOST /proc/pressure/memory -- heal's recovery gate would go
    red on a pressured box for a reason unrelated to the code. memory_alarm's
    BOX_PSI points at a zero-pressure file; a row that needs another reading
    stubs memory_alarm.read_psi in its own body (that wins)."""
    import memory_alarm
    calm = tmp_path_factory.getbasetemp() / "calm-psi"
    if not calm.exists():
        calm.write_text("some avg10=0.00 avg60=0.00 avg300=0.00 total=0\n"
                        "full avg10=0.00 avg60=0.00 avg300=0.00 total=0\n")
    monkeypatch.setattr(memory_alarm, "BOX_PSI", calm)


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

#: The guard pieces this conftest used to keep a second copy of. ONE home
#: (`suite_guards`); this module IMPORTS them -- a plain import, never an exec
#: (residue 1 of verify_DH.430-k1: suite_guards claimed to be THE one home
#: while three copies of these bodies lived in the conftests). The names are
#: re-exported under their historical spellings so the leaf tests that load
#: this conftest BY PATH keep reading the same attributes.
from suite_guards import (  # noqa: E402,F401 -- the guard, imported not copied
    SUITE_LOCK_MARKER,
    _FENCED_MODULE_RUNNERS,
    _FENCED_SPAWN_LEAVES,
    _fence_bound_runners,
    _make_guarded_kill,
    _make_guarded_killpg,
    FENCE_MARKER as _FENCE_MARKER,
    install_import_fence,
    make_import_fence as _make_import_time_fence,
    make_suite_lock_fixture,
    no_real_process as _no_real_process_or_live_config,
    own_pid_signal0_only,
    resolve_leaves as _resolve_leaves,
    uninstall_import_fence as _uninstall_spawn_fence,
)

#: PROD `sessions_dir`, captured BEFORE the autouse fixture rebinds it under
#: tmp (a WRITE-rehome); the tier-gate's READ goes through the real join.
_PROD_SESSIONS_DIR = locations.sessions_dir

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
#: The engine suite's ROOT POLICY, and all that is left of it: the lock body
#: is `suite_guards.make_suite_lock_fixture`, instantiated with this conftest's
#: own `find_project_root(Path(__file__))` -- the FILE, never the cwd, so a
#: `cd` cannot move the window (hypothesis:l4-the-suite-lock-belongs-to-
#: pytest-not-its-caller). The declared context suite instantiates the same
#: factory with the VERIFY_GRAPH_ROOT-else-cwd resolver.
_suite_lock_guard = make_suite_lock_fixture(
    lambda: locations.find_project_root(Path(__file__).resolve()))


@pytest.fixture(scope="session", autouse=True)
def _suite_basetemp_live_gate(tmp_path_factory):
    """hypothesis:l4-the-suite-refuses-to-start-when-its-basetemp-resolves-
    to-the-live-checkout... claim (1) -- the suite REFUSES TO START, before
    any test, when its basetemp resolves to the live engine checkout.

    The engine checkout this conftest ships from is the one a suite may never
    write (a basetemp inside it makes every git-escaping writer land IN THE
    LIVE tree). Compare `git_common_root(getbasetemp())` with the engine's
    own checkout; equal => refuse with the SAME line verification.py --suite
    prints, exit 3. Interim rule (--basetemp under /tmp) keeps the gate
    silent; it only speaks when a run is (or was) rooted inside the repo.
    """
    base = Path(tmp_path_factory.getbasetemp()).resolve()
    if locations.is_live_checkout(base):
        pytest.exit(locations.live_checkout_refusal(
            base, locations.git_common_root(Path(__file__).resolve())),
            returncode=3)

# --- real-judge (ModelJudge) opt-in gate (goal:g15, hypothesis:l4-real-judge-
# tests-run-only-under-one-explicit-opt-in-env-flag-default-off-a-key-alone-
# spends-nothing). Shared by test_stream_master_semantic_screen.py and
# test_stream_master_blind_measure_v2.py -- ONE name, ONE helper, never two
# spellings. A present OPENROUTER_API_KEY alone spends nothing: the suite is
# fixture-only unless AGI_REAL_JUDGE=1 is set AND a key is present.
#
# The `_no_openrouter` autouse fixture below is the second half of the SAME
# rule and shares the SAME opt-in flag, AGI_REAL_JUDGE: when it is NOT "1",
# every meter/pin balance GET to openrouter.ai is stubbed and the key env is
# dropped, so a developer box that has a key never spends or hits the
# network; when it IS "1" (the real-judge ModelJudge tests run), the stub
# stands down so the real measurement still works.

#: Import-time snapshot (the AGI_REAL_JUDGE reason below: the session fixture
#: strips every AGI_* var before a function fixture runs) of the opt-in that
#: lets a test touch REAL systemd units (goal:g6.41.1 R1, residue 69).
_LIVE_SYSTEMD_ON = os.environ.get("AGI_LIVE_SYSTEMD") == "1"

REAL_JUDGE_FLAG = "AGI_REAL_JUDGE"

#: Import-time snapshot of the opt-in flag, the ONLY value `_no_openrouter`
#: may read it from. The parent `extensions/agi/conftest.py` `_agi_env_stripped`
#: is SESSION-scoped and autouse, so it strips every AGI_* var (including
#: AGI_REAL_JUDGE) from the LIVE os.environ BEFORE any function-scoped
#: fixture's body runs. A live `os.environ.get(AGI_REAL_JUDGE)` inside
#: `_no_openrouter` (a runtime fixture) is therefore ALWAYS None once the
#: suite is up, even when the operator launched `AGI_REAL_JUDGE=1` -- the
#: opt-in escape would be dead under the suite (measured: pytest_runtest_-
#: setup saw flag='1' and the key, the fixture body saw flag=None and then
#: DELETED the key anyway). The fix: conftest import runs during collection,
#: BEFORE any session fixture body, so this snapshot taken here captures the
#: launched value ahead of the strip. Default-off is unchanged: unset at
#: launch -> _REAL_JUDGE_ON=False, exactly what the fixture behaved as before.
_REAL_JUDGE_ON = os.environ.get(REAL_JUDGE_FLAG) == "1"


def real_judge_skip():
    """Return the skip reason if the real ModelJudge should NOT run, else None.

    The real (paid, network) stream-master ModelJudge runs only under one
    explicit opt-in env flag, AGI_REAL_JUDGE=1, AND a present
    OPENROUTER_API_KEY. A key alone, or the flag alone, still spends nothing.
    """
    if os.environ.get(REAL_JUDGE_FLAG) != "1":
        return (f"{REAL_JUDGE_FLAG} not set; the real semantic measurement is "
                "opt-in and OFF by default (set AGI_REAL_JUDGE=1 to run it)")
    if not os.environ.get("OPENROUTER_API_KEY"):
        return ("ModelJudge has no OPENROUTER_API_KEY; real semantic "
                "measurement unavailable in this environment")
    return None


@pytest.fixture
def _no_pin_socket(monkeypatch):
    """hypothesis:l4-test-only-the-real-judge... (e) -- raise on ANY socket
    low-level open, proving a --pin test opens no network connection whether
    it reaches `rotate._openrouter_get` via `urllib.request.urlopen` or any
    other path. A test that genuinely opens a socket under this guard fails
    loudly instead of silently spending -- that is the proof, not the tests'
    own higher-level stubs. Applied to the spend-status / --pin tests in
    test_rotate.py.
    """
    import socket

    def _refuse(*_a, **_k):
        raise RuntimeError(
            "a socket was opened during a --pin test; spend-status must be "
            "stubbed, never reach the network (hypothesis:l4-test-only-the-"
            "real-judge-opt-in...)")

    monkeypatch.setattr(socket, "socket", _refuse)
    monkeypatch.setattr(socket, "create_connection", _refuse)


@pytest.fixture(autouse=True)
def _no_openrouter(monkeypatch):
    """hypothesis:l4-the-suite-never-reaches-openrouter-one-autouse-stub-on-
    openrouter-get-unless-the-real-judge-flag-is-set -- the suite never
    reaches openrouter.ai. rotate reaches a live balance through
    `_openrouter_get` whenever `_openrouter_key` resolves a key (env first,
    then the repo `.env`), so a developer box that has a key makes every
    `meter --pin` run two real HTTP calls -- measured on this tree with a
    junk key exported: fresh_spend_status opened urlopen to
    openrouter.ai/api/v1/key and /credits. This autouse fixture is the
    suite-wide second line (alongside the real-judge gate above): unless the
    SAME opt-in flag AGI_REAL_JUDGE=="1" is set, it (a) drops the key env so
    `_openrouter_key` resolves nothing even for a test that forgot to stub,
    and (b) stubs `rotate._openrouter_get` to return None so spend-status
    takes its no-key shape without touching urllib. rotate may not be
    importable in every test env, so both imports are lazy and gated by
    try/except ImportError -- the delenv always runs.

    THE FLAG IS READ FROM THE IMPORT-TIME SNAPSHOT `_REAL_JUDGE_ON`, NOT a
    live `os.environ.get` here. The parent `extensions/agi/conftest.py`
    `_agi_env_stripped` is SESSION-scoped and autouse, so it strips every
    AGI_* var from the LIVE env before any function-scoped fixture body runs
    -- a live read inside THIS fixture would always see None, silently
    killing the opt-in escape even when launched `AGI_REAL_JUDGE=1`. The
    snapshot is taken at conftest import (collection), which runs before the
    session strip, and is the one value this fixture trusts.

    TWO aliases are patched, never one: the test files load rotate as
    `from agi.bin import rotate` while this conftest's own `import rotate`
    resolves a DIFFERENT module object for the same file, and `fresh_spend_
    status` closes over the module-global `_openrouter_get` of whichever
    object is actually exercising it -- patching only one alias is exactly
    the per-module-alias trap `_no_real_tmux` avoids by patching the shared
    stdlib leaf. `_openrouter_get` has no shared leaf, so both module
    objects get the stub. A test that needs a real key or a real stub sets
    it in its own BODY after this fixture's setup; monkeypatch is
    function-scoped and shared, so the later setenv/setattr wins for the
    test's duration (same ordering fact as `_no_real_tmux`).
    """
    if _REAL_JUDGE_ON:
        return
    for _k in ("OPENROUTER_API_KEY", "OPENROUTER_PROVISIONING_KEY"):
        monkeypatch.delenv(_k, raising=False)
    _patched = False
    try:
        import rotate  # noqa: PLC0415 -- may not be importable in every env
        monkeypatch.setattr(rotate, "_openrouter_get", lambda url, key: None)
        _patched = True
    except ImportError:
        pass
    try:
        from agi.bin import rotate as _agi_rotate  # noqa: PLC0415
        monkeypatch.setattr(_agi_rotate, "_openrouter_get", lambda url, key: None)
        _patched = True
    except ImportError:
        pass
    if not _patched:
        # no rotate module importable here; nothing to stub, delenv stands.
        return


#: Module attribute a test file sets to True to OPT IN to the process guard
#: below. Opt-in, not blanket: the guard refuses EVERY subprocess spawn, and
#: the wider suite legitimately runs real `git`/`python3` (the tmux guard's
#: own negative half does too), so a suite-wide ban would red 178 files.
#: A test file that promises "no real process, no live config" says so here.
_GUARD_OPTIN_ATTR = "NO_REAL_PROCESSES"


# `os.kill` / `os.killpg` / the fenced leaves / the bound engine runners all
# live in `suite_guards` now: signal 0 on the OWN pid is the only traffic the
# kill leaf passes through, and the leaf list is ONE shared tuple.
#: Every fence carries the real leaf it wraps under `_FENCE_MARKER` (imported
#: from suite_guards, the ONE body) and `install_import_fence` SKIPS a leaf
#: already carrying it: conftest.py is exec'd twice in one interpreter
#: (test_tier_gate.py), and a fence over a fence made `subprocess.Popen is
#: _REAL_POPEN` false for 48 tests (measured 2026-09-26 a00-585205f4).

#: A caller that set this module attribute opted in to the process guard.
_GUARD_FLAG = _GUARD_OPTIN_ATTR

#: The pids the kill leaves may touch: this process, and NOTHING else.
_OWN_PIDS = frozenset({os.getpid()})


#: Set by a test that loads this conftest BY PATH to unit-test one of its
#: leaves: the unit load must not install (and then remove) the session-wide
#: import-time fence under the running suite's feet.
_UNIT_LOAD_ENV = "AGI_TESTS_CONFTEST_UNIT_LOAD"

#: This suite's NAME for the one install entry point. The BODY is
#: `suite_guards.install_import_fence` (the same one the declared context
#: suite installs at ITS import time); this wrapper carries this suite's
#: POLICY -- its leaf tuple, its opt-in flag name, its own-pid set -- and
#: reads `os` from THIS module's globals at CALL time, so an in-process unit
#: test can point the kill branch at a stub instead of the real os module
#: (test_conftest_guard's kill-branch rows).
def _install_spawn_fence(leaves=_FENCED_SPAWN_LEAVES, kills=True, **kwargs):
    kwargs.setdefault("guard_flag", _GUARD_FLAG)
    kwargs.setdefault("own_pids", _OWN_PIDS)
    return install_import_fence(leaves=leaves, kills=kills, os_module=os,
                                **kwargs)


#: The import-time fence is installed at CONFTEST import, which pytest does
#: before it imports any test module in this dir: the only ordering that
#: covers a module that spawns AT IMPORT (measured 2026-09-26 a00-6e17df77 --
#: both a function-scoped and a session-scoped fixture are too late).
_IMPORT_FENCE_SAVED = None
if os.environ.get(_UNIT_LOAD_ENV) != "1":
    _IMPORT_FENCE_SAVED = _install_spawn_fence()


def pytest_unconfigure(config):
    """Undo the import-time fence when the session ends: it is installed in
    the pytest PROCESS, so a suite that embeds pytest must get its stdlib
    back."""
    global _IMPORT_FENCE_SAVED  # noqa: PLW0603 -- one install per process
    if _IMPORT_FENCE_SAVED is not None:
        _uninstall_spawn_fence(_IMPORT_FENCE_SAVED)
        _IMPORT_FENCE_SAVED = None


@pytest.fixture(autouse=True)
def _registry_default_to_tmp(tmp_path, monkeypatch):
    """goal:g7.16.1.7.1.1.2.1 -- heal builds the session table on EVERY watch
    pass, so the registry default (`~/.claude/sessions`, the LIVE box) is
    pointed at a per-test dir on both rotate aliases (the `_no_openrouter`
    two-alias rule). A test that wants a registry passes `registry_dir`."""
    for _mod in ("rotate", "agi.bin.rotate"):
        try:
            _r = __import__(_mod, fromlist=["_"])
        except ImportError:
            continue
        monkeypatch.setattr(_r, "REGISTRY_DEFAULT_DIR",
                            str(tmp_path / "cc-registry"))


@pytest.fixture(autouse=True)
def _pin_sessions_and_comms_roots_to_tmp(tmp_path, monkeypatch):
    """goal:g15 (hypothesis:l4-the-suite-never-writes-the-live-sessions-or-
    comms-root-heal-and-send-take-the-root-they-are-given) -- the suite NEVER
    writes the LIVE sessions or comms root.

    The four resolver leaves the engine reads are bound so that any resolution
    landing OUTSIDE the running test's own tmp_path is rehomed under it. The
    live escape this closes: the kid harness roots pytest's basetemp inside
    the LIVE repo, so `locations.shared_sessions_dir` / `send.comms_root`
    called on a test-constructed graph root re-resolve through
    `locations.git_common_root` -> `git rev-parse --git-common-dir` to the
    MAIN checkout's `.agi` -- and a heal that threads its given root then
    lands rotation records, crash-recovery dms and pin-reap alarms in the
    LIVE tree. Rebinding an escaping result under tmp_path makes the leak
    impossible while leaving every resolver whose result is already inside
    the test's tmp (all fixture roots) byte-for-byte unchanged -- so the
    resolver-behaviour tests (comms season root, worktree-shared sessions)
    stay green and the suite is made safe by construction, not by
    hand-seaming each producer. No env var (a subprocess could drop it), the
    production definitions are untouched.
    """
    tmp = tmp_path
    try:
        import locations as _loc    # shared module object every alias binds
        import send as _send
    except Exception:               # noqa: BLE001 -- nothing to pin without
        return                      # the resolvers, so stay a silent no-op

    def _bound(fn, bucket):
        def wrapper(root, *args, **kwargs):
            real = Path(fn(root, *args, **kwargs)).resolve()
            if real == tmp or tmp in real.parents:
                return real         # already a test-owned path: use as-is
            return tmp / bucket     # escaped to the LIVE tree: rehome under tmp
        return wrapper

    monkeypatch.setattr(_loc, "shared_sessions_dir",
                        _bound(_loc.shared_sessions_dir, "sessions"))
    monkeypatch.setattr(_loc, "sessions_dir",
                        _bound(_loc.sessions_dir, "sessions"))
    monkeypatch.setattr(_send, "comms_root", _bound(_send.comms_root, "comms"))
    monkeypatch.setattr(_send, "_default_comms_root",
                        _bound(_send._default_comms_root, "comms"))
