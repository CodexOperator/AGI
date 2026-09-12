#!/usr/bin/env python3
"""verification.py — ONE command replaces the four-tool rotation ritual.

This is NOT `verify_unified.py`. `verify_unified.py` is the `goal:g11`
migration checker — it proves the old staged-checkout repo collapsed into one
tree, and it has nothing to do with rotation. `verification.py` is the
rotation/health-check round; the two names are one keystroke apart and must
never be merged or shared. `hypothesis:l4-unified-verification`, for
`goal:g1.10`: a successor runs ONE command at rotation and spends tokens on one
summary block, not four scrollbacks, and every check it runs is resolved
THROUGH `commands.py` from `command:commands`
(`.agi/nodes/.geometry/commands.md`) — never argv written literally here.

Levels (`--level quick|rotation|full`, default `rotation`):
  quick    = links + goals-check + write-guard        (pre-commit set, <15s)
  rotation = quick + smoke + viewport-verify + dispatch-help + budget
  full     = rotation + schema + credentials + secrets + crons
NO level runs pytest. `--suite` is OPT-IN and ORTHOGONAL to level: it adds the
pytest run and nothing else, and its absence is never a failure. The suite
window is the Prime's to grant, one runner at a time, and until `goal:g17.1`'s
L4.10 lands, `test_send.py` nudges real tmux panes — so `verification.py` must
never take that window unasked. When L4.10 lands, `full` folds the suite in
and this file holds the lock that guarantees one runner; until then the lock
(plain pid file, stale-broken) is present but `--suite` stays opt-in.

The node-count check is a COMPARISON, not a print. Smoke prints counts; "the
active count must not drop" is meaningless without a baseline. The active /
deprecated / total triple is recorded between runs in `.agi/sessions/`, and
this file FAILS when active is below the recorded value — the one failure this
tool exists to catch (H0/H0b: 29k nodes lost).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import locations  # noqa: E402
import commands  # noqa: E402
import rotate  # noqa: E402  -- _sessions_dir (the ONE resolver the pins share)
import branches  # noqa: E402  -- ref_candidates (canonical-first season grammar)

#: Per-check wall-clock ceiling. A check that hangs past this is a failure the
#: successor must see, not a run that never returns.
PER_CHECK_TIMEOUT = 600

#: The SUITE's own ceiling. One number for every check made the one check that
#: legitimately takes minutes the one check that false-FAILs: the engine suite
#: is ~2300 tests, and reporting a green suite as "timed out after 600s" is a
#: failure the tool invented. A hang is still caught, three times further out.
SUITE_TIMEOUT = 1800

#: How each level is composed. Names are COMMAND NAMES resolved through
#: `commands.py` against the node — never argv written here.
LEVELS: dict[str, list[str]] = {
    "quick": ["links", "goals-check", "write-guard"],
    "rotation": ["links", "goals-check", "write-guard",
                 "smoke", "viewport-verify", "dispatch-help", "budget"],
    "full": ["links", "goals-check", "write-guard",
             "smoke", "viewport-verify", "dispatch-help", "budget",
             "schema", "credentials", "secrets", "crons"],
}

#: The declared command `--suite` adds to a level. Opt-in only.
SUITE_CMD = "tests"

STATE_FILE = "verify-count.json"        # under <groot>/sessions/
SUITE_LOCK = "verify-suite.lock"        # under <groot>/sessions/

#: Named non-zero exit when --suite is refused because another LIVE runner
#: holds the suite window. Named, not a bare 1, so the caller abroad can tell
#: "locked" from "suite ran and failed".
EXIT_SUITE_LOCKED = 2
# One persisted "when did the suite last run" timestamp (L4.81), written on
# --suite completion and read by the no-suite rotation check so "a new
# bin/*.py needs the suite" is a CHECK, not a memo (goal:g15.10).
SUITE_TS_FILE = "verify-suite-ts.json"  # under <groot>/sessions/


@dataclass
class CheckResult:
    """One check's verdict, its elapsed time, and the number it produces."""

    name: str
    status: str                 # PASS | FAIL | SKIP
    elapsed: float
    number: dict | None = None
    note: str = ""
    message: str = ""


_PYTEST_COUNT_PATTERNS = (
    ("passed", r"(\d+)\s+passed"),
    ("skipped", r"(\d+)\s+skipped"),
    ("failed", r"(\d+)\s+failed"),
    ("errors", r"(\d+)\s+errors?"),
)


def _parse_pytest_counts(output: str) -> dict:
    """Counts from pytest's own summary line, in whatever order pytest emits.

    pytest writes `N passed, M skipped, K failed, E errors` with only the
    nonzero categories present, in a stable order of its own. We read each
    category independently so order never matters, and we return only the
    keys that actually appear. An empty dict means the output carried no
    countable line at all — a PASS that still must say so rather than print
    an empty bracket (hypothesis:l4-verification-counts-and-engine-root).
    """
    counts: dict = {}
    for key, pat in _PYTEST_COUNT_PATTERNS:
        m = re.search(pat, output)
        if m:
            counts[key] = int(m.group(1))
    return counts


def _parse_number(name: str, exitcode: int, output: str) -> dict | None:
    """The one number each check exists to produce.

    Four checks carry a real number: smoke's active/deprecated/total triple,
    links' broken count, goals-check's byte-identity yes/no, and the suite's
    pytest counts (passed/skipped/failed/errors). Everywhere else the exit
    code is the fact and the number column is empty. A `tests` count is a
    number for the reader, never a verdict — pass/fail still comes from the
    exit code, and a run whose output yields no count is still judged on the
    exit code, with the missing count stated in the note.
    """
    if name == "tests":
        return _parse_pytest_counts(output)
    if name == "smoke":
        vals = dict(re.findall(r"METRIC\s+(\w+)=(-?\d+)", output))
        return {
            "active": int(vals["active_node_count"]) if "active_node_count" in vals else -1,
            "deprecated": int(vals["deprecated_node_count"]) if "deprecated_node_count" in vals else -1,
            "total": int(vals["node_count"]) if "node_count" in vals else -1,
        }
    if name == "links":
        m = re.search(r"(\d+)\s+broken", output)
        return {"broken": int(m.group(1)) if m else -1}
    if name == "goals-check":
        return {"byte-identical": 1 if exitcode == 0 else 0}
    return None


def _passed(name: str, exitcode: int, number: dict | None) -> bool:
    """Decide pass/fail for one check, beyond the bare exit code.

    `links` exits 0 even with broken links (it only fails with `--broken`), so
    the broken count is the fact, not the code. Everything else passes on
    exit 0.
    """
    if name == "links":
        return number is not None and number.get("broken") == 0 and exitcode == 0
    if name == "smoke":
        return exitcode == 0 and number is not None and number["active"] >= 0
    return exitcode == 0


# --- the count baseline (a comparison, not a print) -------------------------
# hypothesis:l4-the-never-lower-baseline-is-stamped-only-by-a-kept-merge. The
# baseline is a STAMP on bytes that are KEPT — the integration branch whose
# HEAD is pushed — never a first read of droppable bytes. A merge-up 28
# defect: a red 28c read stamped 1921, 28c was dropped, and a green re-run
# then FAILED node-count against a baseline that never existed on the branch.


def _state_path(groot: Path) -> Path:
    return Path(groot) / "sessions" / STATE_FILE


def _shared_state_path(groot: Path) -> Path:
    """The baseline's path, resolved to the SHARED sessions dir.

    The SAME rule `_suite_ts_path` applies to the suite stamp (item 3 of
    hypothesis:l4-a-check-that-answers-a-question-it-is-not-asking): the
    never-lower baseline is STAMPED in MAIN on the integration branch, so the
    merge-up `window` reply running from a seat WORKTREE must read MAIN's
    stamped baseline, not the caller's freshly-absent per-worktree
    `<groot>/sessions/verify-count.json`. Routes through
    `rotate._sessions_dir` (the ONE resolver the pins share) ->
    `locations.shared_sessions_dir` -> `git_common_root`. A plain non-git
    root returns the identity, so fixtures and the main checkout read byte-
    for-byte as before.
    """
    return rotate._sessions_dir(groot) / STATE_FILE


def _git(groot: Path, args: list[str]) -> str | None:
    """A git probe from `groot`'s tree. Returns stdout stripped, or None when
    git cannot answer (not a tree, absent binary, non-zero exit)."""
    try:
        r = subprocess.run(["git", *args], cwd=str(groot),
                           capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    return r.stdout.strip()


def _is_ancestor(groot: Path, sha: str) -> bool | None:
    """Is `sha` an ancestor of HEAD? True/False definite; None when git
    cannot answer (not a git tree, sha meaningless)."""
    try:
        r = subprocess.run(["git", "merge-base", "--is-ancestor", sha, "HEAD"],
                           cwd=str(groot), capture_output=True, text=True,
                           timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode == 0:
        return True
    if r.returncode == 1:
        return False
    return None


def _integration_branch_candidates(groot: Path) -> list[str] | None:
    """The refs [canonical, legacy] these bytes may sit on and be pushed to,
    from the ladder's `town_branches` — canonical first, then the declared
    spelling as a one-season fallback (branches.ref_candidates), so a read
    survives the season rename either way round: while the tree still declares
    the legacy `season/s<N>`, and after it has been flipped to the canonical
    `season<N>/main`. NEVER hardcoded (goal:g10.2); the season is whatever the
    declared value resolves to. Core's branch is the default; a non-core
    town's own branch is used when the graph resolves to that town. None when
    no branch is declared."""
    tb = rotate.load_ladder_field(groot, "town_branches", None)
    declared = None
    if isinstance(tb, dict):
        if tb.get("core"):
            declared = str(tb["core"])
        else:
            for b in tb.values():
                declared = str(b)
                break
    if declared is None:
        return None
    return branches.ref_candidates(declared)


def _integration_branch(groot: Path) -> str | None:
    """The CANONICAL integration branch these bytes merge up to — the [0] of
    `_integration_branch_candidates`, so callers that need ONE stable name
    (the tip label, `origin/<branch>`) keep using the resolved form rather
    than the raw declared spelling. None when no branch is declared."""
    cands = _integration_branch_candidates(groot)
    return cands[0] if cands else None


def _stamp_context(groot: Path) -> tuple[bool, str | None, str]:
    """(can_stamp, head_sha, reason) for THIS run's bytes.

    KEPT means the read is on the declared integration branch AND HEAD is an
    ancestor of a pushed `origin/<candidate>` — a kept merge is pushed, while
    a worktree or a seat branch (not on the declared branch, in either the
    canonical or legacy spelling) is not. The check is branch + reachability
    only: an uncommitted working tree whose HEAD is already pushed still
    counts as kept here. A read that cannot stamp still COMPARES (it just
    never writes the baseline).
    """
    cands = _integration_branch_candidates(groot)
    if not cands:
        return False, None, "no integration branch declared in the ladder"
    cur = _git(groot, ["rev-parse", "--abbrev-ref", "HEAD"])
    if cur is None:
        return False, None, "not a git tree"
    if cur not in cands:
        names = " ".join(repr(c) for c in cands)
        return False, None, f"not on integration branch ({names}) (on {cur!r})"
    head = _git(groot, ["rev-parse", "HEAD"])
    if head is None:
        return False, None, "not a git tree"
    pushed = next((c for c in cands
                   if _git(groot, ["merge-base", "--is-ancestor", "HEAD",
                                   f"origin/{c}"]) is not None), None)
    if pushed is None:
        names = ", ".join(f"origin/{c}" for c in cands)
        return False, head, f"unpushed — HEAD not an ancestor of {names}"
    return True, head, f"kept (on {cur!r}, pushed to origin/{pushed})"


def _read_state(groot: Path) -> dict | None:
    try:
        return json.loads(_state_path(groot).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def compare_count(groot: Path, current: dict | None,
                  *, stamp: bool = False) -> CheckResult:
    """The node-count check: FAIL when active is below the recorded baseline.

    The baseline is STAMPED only on bytes that are KEPT (`_stamp_context`)
    or when an explicit `--stamp` is passed (the merge-up step, AFTER its
    push). Every other read — a worktree, a seat branch, an unpushed MAIN —
    COMPARES but prints `NOT STAMPED: <reason>` and never writes the file
    (the falsifier: a red or dropped read that stamps). A recorded baseline
    whose `sha` is no longer an ancestor of HEAD is stale: REPORTED and
    treated as absent, never silently leaned on.
    """
    start = time.monotonic()
    if current is None or current.get("active", -1) < 0:
        return CheckResult("node-count", "SKIP", time.monotonic() - start,
                           note="smoke did not report an active count")
    if stamp:
        can_stamp, head_sha, why = (
            True, _git(groot, ["rev-parse", "HEAD"]), "explicit --stamp")
    else:
        can_stamp, head_sha, why = _stamp_context(groot)
    state = _read_state(groot)
    stale = ""
    if state and state.get("sha"):
        anc = _is_ancestor(groot, str(state["sha"]))
        if anc is False:
            stale = (f"; baseline sha {state['sha']} not an ancestor of HEAD "
                     "(stale — treated as absent)")
            state = None
    if state is None:
        if can_stamp and head_sha:
            _write_state(groot, current, head_sha, why)
            return CheckResult(
                "node-count", "PASS", time.monotonic() - start, current,
                note=f"baseline recorded (sha={head_sha}){stale}",
                message=f"active={current['active']} recorded, stamped {why}")
        note = f"no baseline; NOT STAMPED: {why}{stale}"
        return CheckResult(
            "node-count", "PASS", time.monotonic() - start, current,
            note=note,
            message=f"active compared, no baseline stamped: {why}")
    if current["active"] < state["active"]:
        return CheckResult(
            "node-count", "FAIL", time.monotonic() - start, current,
            note=("ACTIVE COUNT DROPPED: "
                  f"active={current['active']} below baseline={state['active']} "
                  "(H0/H0b: 29k nodes lost to a silent drop)"),
            message=("active below recorded baseline: "
                     f"{current['active']} < {state['active']}"))
    if can_stamp and head_sha:
        _write_state(groot, current, head_sha, why)
        note = f"active steady; baseline updated (sha={head_sha}){stale}"
    else:
        note = f"active steady; NOT STAMPED: {why}{stale}"
    return CheckResult("node-count", "PASS", time.monotonic() - start, current,
                       note=note, message=("active steady: "
                                           f"{current['active']} >= baseline "
                                           f"{state['active']}"))


def _write_state(groot: Path, current: dict, sha: str | None,
                 reason: str) -> None:
    """The stamped baseline carries provenance: the counts, the head sha, the
    moment, and WHY it was stamped — so a hand reset is never needed and a
    stale baseline can be REPORTED rather than silently trusted."""
    path = _state_path(groot)
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = {
        "active": int(current.get("active", -1)),
        "deprecated": int(current.get("deprecated", -1)),
        "total": int(current.get("total", -1)),
        "sha": sha,
        "stamped_at": time.time(),
        "reason": reason,
    }
    path.write_text(json.dumps(doc), encoding="utf-8")


# --- the suite lock (opt-in; one runner at a time) --------------------------


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def acquire_suite_lock(groot: Path) -> tuple[Path | None, int | None]:
    """A plain lock file holding the holder's pid, stale-broken by a dead pid.

    Returns `(path, None)` on success and `(None, holder_pid)` when another
    LIVE runner owns the window — the pid is returned rather than swallowed so
    the refusal can name who to wait for; "refused" without a holder is a
    message that tells a successor nothing it can act on. `(None, None)` means
    the lock could not be written at all.

    Keeping `--suite` opt-in is what rules today; the lock is the mechanism
    that rules when L4.10 folds the suite into `full`.
    """
    path = Path(groot) / "sessions" / SUITE_LOCK
    path.parent.mkdir(parents=True, exist_ok=True)
    for _ in range(2):
        if path.exists():
            try:
                holder = int(path.read_text(encoding="utf-8").strip())
            except (OSError, ValueError):
                path.unlink(missing_ok=True)
                continue
            if _pid_alive(holder) and holder != os.getpid():
                return None, holder  # another live runner owns the window
            path.unlink(missing_ok=True)  # stale: dead pid
        try:
            path.write_text(str(os.getpid()), encoding="utf-8")
            return path, None
        except OSError:
            return None, None
    return None, None


def _suite_lock_guard(groot: Path) -> str | None:
    """Probe the suite lock BEFORE pytest is spawned; refuse with one line.

    The lock's real owner is the pytest session it guards -- conftest.py is the
    single live acquirer (hypothesis:l4-the-suite-lock-belongs-to-pytest-not-
    its-caller) -- so this runner must NOT hold the window across the spawn or
    the child conftest would see OUR live pid and refuse itself. This guard
    REUSES acquire_suite_lock for the held/stale judgement (a dead pid is
    broken exactly as today, never reimplemented) and, whenever the acquisition
    actually succeeds, immediately releases again so the child pytest is the
    one pid holding the window when it spawns.

    The point is the EARLY clean refusal: a held lock means "do not spawn at
    all, print one line" instead of letting conftest raise one setup error per
    collected test (3650 errors on the round that measured this -- residue (5)
    of hypothesis:l4-one-line-anchored-frontmatter-reader-and-the-suite-
    runner-refuses-a-held-lock-before-spawning).

    Returns the one refusal line when a LIVE foreign pid holds the window,
    else None (proceed -- the purpose-built acquirer rules).
    """
    lock_path, holder = acquire_suite_lock(groot)
    if lock_path is None and holder is not None:
        try:
            since = time.strftime(
                "%H:%M:%SZ",
                time.gmtime((Path(groot) / "sessions" / SUITE_LOCK)
                            .stat().st_mtime))
        except OSError:
            since = "?"
        return (f"suite: lock held by {holder} since {since}"
                " — refusing, not spawning")
    if lock_path is not None:
        # We took the window only to probe it. Hand it back so conftest -- the
        # one live acquirer -- owns it across the spawned suite.
        try:
            lock_path.unlink(missing_ok=True)
        except OSError:
            pass
    return None


# --- the bin freshness guard (a new bin/*.py needs the suite) ---------------


def _bin_scripts(bin_dir: Path) -> list[Path]:
    """Every *.py directly under bin/, the SAME universe test_bin_help_smoke
    auto-enrolls. Reusing its exclusions (no `_`-prefix, no `__init__.py`)
    rather than re-deriving a possibly-divergent second list."""
    return [f for f in sorted(bin_dir.iterdir())
            if f.is_file() and f.name.endswith(".py")
            and not f.name.startswith("_") and f.name != "__init__.py"]


def _git_tracked(bin_dir: Path) -> set[str]:
    """Names under bin/ the working tree considers tracked (`git ls-files`).
    A bin/ outside any git tree returns empty (all-untracked is a false alarm
    a non-git checkout must not raise), and the mtime arm still rules there."""
    try:
        r = subprocess.run(["git", "ls-files", str(bin_dir)], cwd=bin_dir,
                           capture_output=True, text=True, timeout=30)
        return {Path(x).name for x in r.stdout.splitlines()}
    except (OSError, subprocess.SubprocessError):
        return set()


def _suite_ts_path(groot: Path) -> Path:
    """The suite stamp's path, resolved to the SHARED sessions dir.

    ITEM 3 of hypothesis:l4-a-check-that-answers-a-question-it-is-not-asking:
    the stamp that `bin-suite-fresh` guards must live where the thing it guards
    lives -- the shared engine tree -- not in whichever per-worktree sessions
    dir happened to run `--suite`. `rotate._sessions_dir` is the ONE resolver
    the meter pins already share (routes through `git_common_root` to the
    main checkout), so a seat branch reads the same stamp the prime's suite
    wrote instead of a freshly-missing one. A plain non-git root returns the
    identity, so fixtures and the main checkout are byte-for-byte unchanged.
    """
    return rotate._sessions_dir(groot) / SUITE_TS_FILE


def _read_suite_ts(groot: Path) -> float | None:
    """Epoch of the last recorded --suite completion, or None if never."""
    try:
        doc = json.loads(_suite_ts_path(groot).read_text(encoding="utf-8"))
        return float(doc["suite_ran_at"])
    except (OSError, ValueError, TypeError, KeyError):
        return None


def _record_suite_ts(groot: Path) -> None:
    """Persist the suite-completed timestamp (same idiom as _write_state).

    Written to the SHARED sessions dir (see `_suite_ts_path`), so a first
    `--suite` run on the main checkout is immediately visible to every seat
    branch -- the round-trip falsifier (g3) of this round's item 3."""
    path = _suite_ts_path(groot)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"suite_ran_at": time.time()}), encoding="utf-8")


def check_bin_freshness(groot: Path, *, bin_dir: Path | None = None,
                        tracked_of=None,
                        effective_ts: float | None = None) -> CheckResult:
    """FAIL ("SUITE REQUIRED") when a bin/*.py is untracked by git or newer
    than the last recorded --suite run.

    test_bin_help_smoke auto-enrolls ANY new script under bin/, so a fresh
    bin/*.py can break the Prime's suite unseen by the no--suite rotation
    check (L4.78). Three-way gate so it is a check, not a tripwire:
      1. nothing untracked and nothing newer than the last suite -> PASS
      2. an untracked bin/*.py -> FAIL, SUITE REQUIRED
      3. a bin/*.py OLDER than the last suite run -> PASS even if it is
         untracked (the "/ or newer" half is bidirectional)
    No recorded timestamp ever -> conservative FAIL: a suite that has never
    run is exactly the state we must surface, so the default is "required".

    `effective_ts`, when given, replaces the recorded stamp as the reference
    for the mtime arm: it is how a --suite call that JUsT passed within the
    same invocation teaches the guard to judge against the run completing now
    rather than the run before it (L4.101 item 2) -- a first-ever suite run
    must not self-FAIL because no PRIOR stamp exists. The no-recorded-stamp
    FAIL arm is untouched: `effective_ts` is only ever supplied by a --suite
    run that is itself passing, never to silence a never-run tree.
    """
    start = time.monotonic()
    bdir = bin_dir or Path(__file__).resolve().parent
    tracked = tracked_of(bdir) if tracked_of else _git_tracked(bdir)
    suite_ts = effective_ts if effective_ts is not None else _read_suite_ts(groot)
    stale: list[str] = []
    for f in _bin_scripts(bdir):
        if suite_ts is not None and f.stat().st_mtime > suite_ts:
            why = "(untracked; mtime newer than the last suite run)" \
                if f.name not in tracked \
                else "(mtime newer than the last suite run)"
            stale.append(f"{f.name} {why}")
    if suite_ts is None:
        stale.append("no suite has EVER run (no recorded timestamp)")
    elif not stale:
        note = ("all bin/*.py covered by the suite run completing now"
                if effective_ts is not None
                else "all bin/*.py older than the last recorded suite run")
        return CheckResult("bin-suite-fresh", "PASS",
                           time.monotonic() - start, note=note)
    return CheckResult("bin-suite-fresh", "FAIL", time.monotonic() - start,
                       note="SUITE REQUIRED: " + "; ".join(stale))


# --- the seat-model check (surface 2: verify FAILS on a drifted seat) --------
# hypothesis:l4-a-seats-live-model-is-measured-not-assumed. The DATA half
# (experiment:a00-9af5f5f0-38aaed) confirmed message.model rides every
# assistant turn of a CC transcript and the real gen VII drift reads cleanly
# (129 opus-5 turns, a model_refusal_fallback system event, 297 opus-4-8
# after). This is the READER: walk config:seats rows that have a live
# session_ref, resolve each seat's OWN transcript THROUGH rotate.py's pin
# resolution (find_pin_log / _parse_pin_record) -- identity supplied, never
# inferred, trap 0c: no seat is ever opened as "newest file in a directory" --
# and FAIL (not warn) when the newest assistant turn's model differs from the
# row's declared model, naming seat, live/row models, the first drifted turn
# and the last model_refusal_fallback event. DETECT, NEVER REPAIR: no code
# path here may rewrite a seat row or restart a session. A row with no
# session_ref, or a pin that does not resolve, is SKIPPED silently.


def _scan_seat_transcript(path: Path, declared: str) -> dict:
    """One transcript .jsonl -> the fields the seat-model check needs.

    Returns {live, first_drift, fallback_ts, fallback_category,
    fallback_request_id}. `live` is the newest assistant-turn `message.model`
    (a turn with no model never overrides a measured one); `first_drift` is
    the timestamp of the first assistant turn whose model differs from the
    `declared` row model; the fallback keys are the LAST
    model_refusal_fallback system event observed. Any of them may be None.
    """
    live = None
    first_drift = None
    fb = {"fallback_ts": None, "fallback_category": None,
          "fallback_request_id": None}
    try:
        fh = open(path, encoding="utf-8", errors="replace")
    except OSError:
        return {"live": None, "first_drift": None, **fb}
    with fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                o = json.loads(line)
            except ValueError:
                continue
            if not isinstance(o, dict):
                continue
            typ = o.get("type")
            if typ == "assistant":
                msg = o.get("message") or {}
                model = msg.get("model")
                if model is None:
                    continue  # an unmeasured turn never overrides a measured one
                live = model
                if first_drift is None and model != declared:
                    first_drift = o.get("timestamp")
            elif o.get("subtype") == "model_refusal_fallback":
                fb = {"fallback_ts": o.get("timestamp"),
                      "fallback_category": o.get("apiRefusalCategory"),
                      "fallback_request_id": o.get("requestId")}
    return {"live": live, "first_drift": first_drift, **fb}


def _seat_transcript(groot: Path, seat: str) -> tuple[Path | None, str]:
    """The transcript a seat's own pin names, or None when it does not resolve.

    Identity is SUPPLIED by the seat's pin (`rotate.find_pin_log` reads the
    seat-stable `<sessions>/<seat>.meter`), never inferred from a directory's
    newest mtime -- trap 0c of the hypothesis. A generation-bearing pin is
    checked against the seat's CURRENT occupant generation (`rotate.
    _read_generation`), mirroring rotate.resolve_transcript step 3 (rotate.py
    ~380): a pin the rotation never re-pointed is a PREDECESSOR's, and is
    reported as `stale-pin` and treated as unresolvable rather than silently
    read as a session that already ended. A legacy pin with no generation
    field (written_gen is None) predates gen-stamping and passes through
    unchanged, exactly as rotate.py's own guard does. Returns
    `(Path, "")` on success, or `(None, reason)` with the caller's skip line.
    """
    reason = "no pin-to-transcript (skipped)"
    pin = rotate.find_pin_log(groot, seat)
    if pin is None:
        return None, reason
    written_gen, target = rotate._parse_pin_record(pin)
    if not target:
        return None, reason
    if written_gen is not None:
        cur_gen = rotate._read_generation(groot, seat)
        if written_gen != cur_gen:
            return None, (f"stale-pin (gen {written_gen} vs current "
                          f"{cur_gen}), skipped")
    lp = Path(target).expanduser().resolve()
    if not lp.exists():
        return None, reason
    return lp, ""


def check_seat_model(groot: Path) -> CheckResult:
    """FAIL when any config:seats row's live transcript model drifted from its
    declared model; PASS otherwise. Detect, never repair. (Surface 2 of
    hypothesis:l4-a-seats-live-model-is-measured-not-assumed.)"""
    start = time.monotonic()
    rows = rotate._load_seats(groot)
    candidate = [r for r in rows if (r.get("session_ref") or "").strip()]
    lines: list[str] = []
    drifted: list[str] = []
    skipped = 0
    for row in candidate:
        seat = row.get("name") or "?"
        declared = (row.get("model") or "").strip()
        tp, reason = _seat_transcript(groot, seat)
        if tp is None:
            skipped += 1
            lines.append(f"{seat}: {reason}")
            continue
        scan = _scan_seat_transcript(tp, declared)
        live = scan["live"]
        if live is None:
            skipped += 1
            lines.append(f"{seat}: no assistant turns with a model (skipped)")
            continue
        # The last model_refusal_fallback event is surfaced on BOTH branches
        # (Prime merge-up 24 residue b): a seat that is clean NOW but had a
        # fallback blip earlier in its own transcript should still show it.
        fb = ""
        if scan["fallback_ts"] is not None:
            fb = (f"; last model_refusal_fallback ts={scan['fallback_ts']} "
                  f"category={scan['fallback_category']} "
                  f"requestId={scan['fallback_request_id']}")
        if live == declared:
            lines.append(f"{seat}: model={live} row={declared}{fb}")
            continue
        lines.append(f"{seat}: DRIFT live={live} row={declared} "
                     f"first-drifted-turn={scan['first_drift']}{fb}")
        drifted.append(seat)
    n_cand = len(candidate)
    note = ("; ".join(lines) if lines else "no seated rows to check")
    if drifted:
        note = ("DRIFTED SEAT(S): " + ", ".join(drifted) + " -- " + note)
    return CheckResult(
        "seat-model", "FAIL" if drifted else "PASS",
        time.monotonic() - start,
        {"seats": n_cand, "drifted": len(drifted), "skipped": skipped},
        note=note)


# --- the merge-up window reply (step 3: print-only, never send) -----------
# hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps. The
# point holds for a merge-up window (sanctuary-director.md §Merge-up step 2:
# "lock state + tip + baseline") before it merges. This command PRINTS that
# reply in paste-ready shape. The DECISION to grant stays the Prime's — this
# path never sends, writes, or grants anything (the node's falsifier: a step
# that SENDS the reply is refused, not landed).


def render_window(groot: Path, grant: str | None = None) -> str:
    """The merge-up window reply: lock state + tip + baseline.

    - lock = `free`, or `held by <pid> since <ts>` when a LIVE pid owns the
      suite/window lock under `<groot>/sessions/` (the SAME file
      `acquire_suite_lock` writes, so a window and a suite runner contend for
      one lock). A dead pid reads as a stale lock and shows `free`, exactly
      as the acquirer would break it.
    - tip = the integration branch sha read from `origin/<branch>` (never
      guessed — read from the local copy of origin's refs the automation
      keeps fresh) plus whether MAIN's HEAD equals it.
    - baseline = the never-lower counts and their stamping sha/reason from
      the lookup STATE_FILE.
    """
    lines: list[str] = []
    # lock
    lock_path = Path(groot) / "sessions" / SUITE_LOCK
    holder: int | None = None
    try:
        holder = int(lock_path.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        holder = None
    if holder is not None and _pid_alive(holder) and holder != os.getpid():
        try:
            since = time.strftime("%H:%M:%SZ",
                                  time.gmtime(lock_path.stat().st_mtime))
        except OSError:
            since = "?"
        lines.append(f"lock: held by {holder} since {since}")
    else:
        lines.append("lock: free")
    # tip: pick the FIRST candidate whose origin ref actually resolves, so a
    # tree still pushed under the legacy spelling (not yet renamed) shows a
    # real tip instead of an unresolved canonical that only exists after the
    # flip. Same canonical-first order the stamp uses.
    candidates = _integration_branch_candidates(groot)
    branch = tip = None
    if candidates:
        for c in candidates:
            tip = _git(groot, ["rev-parse", f"origin/{c}"])
            if tip is not None:
                branch = c
                break
        if branch is None:
            branch = candidates[0]
    # MAIN's real HEAD, resolved through `git_common_root`. The tip line labels
    # the head "MAIN HEAD", so it must BE main's HEAD -- a seat WORKTREE's own
    # HEAD is a different commit and must never wear that label. When root IS
    # main (or a non-git fixture), `git_common_root` is the identity and this
    # prints exactly what it did before.
    main_repo = locations.git_common_root(groot) or groot
    main_head = _git(main_repo, ["rev-parse", "HEAD"])
    if branch is None or tip is None:
        lines.append("tip: (no integration branch declared / origin "
                     "unresolved — read the ladder or sync first)")
    else:
        eq = "yes" if main_head == tip else "no"
        lines.append(f"tip: {branch} = {tip} (MAIN HEAD "
                     f"{main_head or '?'} {'==' if main_head == tip else '!='} "
                     f"tip → {eq})")
    # baseline -- the never-lower counts and their stamping sha/reason. Read
    # from the SHARED sessions dir (where the stamp lives in MAIN), never the
    # caller's per-worktree one (the parent's measured SL1.04 defect).
    state_file = _shared_state_path(groot)
    try:
        state = json.loads(state_file.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        state = None
    if state is None:
        lines.append("baseline: none recorded (verify-count.json absent)")
    else:
        lines.append(
            f"baseline: active={state.get('active', '?')} "
            f"deprecated={state.get('deprecated', '?')} "
            f"total={state.get('total', '?')} "
            f"stamped sha={state.get('sha', '?')} "
            f"reason={state.get('reason', '?')}")
    reply = "\n".join(lines)
    if grant:
        reply = f"GRANT {grant} — merge-up window open\n" + reply
    return reply


# --- the runner ------------------------------------------------------------


def run_check(groot: Path, name: str, verbose: bool) -> CheckResult:
    """Run ONE declared command and judge it. Never raises for the check.

    The argv comes from `commands.load(groot)[name].argv` — resolved from the
    node, never written here. A check that is not declared in the node is a
    FAIL with a message saying so: the graph is the single source, and a level
    that names a check the node has not declared is a graph that has drifted.
    """
    start = time.monotonic()
    table = commands.load(groot)
    if name not in table or not table[name].argv:
        return CheckResult(name, "FAIL", time.monotonic() - start,
                           note=f"check {name!r} is not a declared command in "
                                ".geometry/commands.md — add it to the node")
    cmd = table[name]
    ceiling = SUITE_TIMEOUT if name == SUITE_CMD else PER_CHECK_TIMEOUT
    try:
        proc = subprocess.run(
            cmd.argv, capture_output=True, text=True,
            timeout=ceiling, cwd=cmd.cwd or None)
    except subprocess.TimeoutExpired:
        return CheckResult(name, "FAIL", time.monotonic() - start,
                           note=f"timed out after {ceiling}s")
    except OSError as exc:
        return CheckResult(name, "FAIL", time.monotonic() - start,
                           note=f"could not execute: {exc}")
    output = (proc.stdout or "") + (proc.stderr or "")
    number = _parse_number(name, proc.returncode, output)
    ok = _passed(name, proc.returncode, number)
    note = ""
    # A passing suite whose output yielded NO countable line must say so
    # rather than print an empty bracket — otherwise `PASS tests` reads the
    # same for 2340 tests as for 3, or for none (hypothesis:l4-...and-root).
    if name == SUITE_CMD and ok and number is not None and not number:
        note = "tests ran but NO count parsed from pytest output (exit 0)"
    # stdout is suppressed unless the check fails or --verbose is passed; the
    # failure's tail is the evidence the successor needs.
    if not ok or verbose:
        tail = "\n".join(output.splitlines()[-12:])
        note = (note + "\n" + tail) if note else tail
    return CheckResult(name, "PASS" if ok else "FAIL",
                       time.monotonic() - start, number, note=note)


def run_level(groot: Path, level: str, suite: bool, verbose: bool,
               stamp: bool = False) -> list[CheckResult]:
    """Execute a level: its checks in order, then the count comparison."""
    names = list(LEVELS[level])
    if suite:
        names.append(SUITE_CMD)
    if stamp and "smoke" not in names:
        # --stamp forces the smoke round at ANY level: the fresh count is the
        # price of a stamp (hypothesis:l4-a-stamp-forces-the-smoke-count). A
        # stamp that re-used the PRIOR baseline would record success on
        # nothing — a kept merge that added nodes leaves the never-lower
        # floor where it was. So `--level quick --stamp` runs smoke too, and
        # the node-count check stamps the FRESH numbers with the sha; under an
        # explicit --stamp the recorded baseline is never re-stamped.
        names.append("smoke")
    results = [run_check(groot, n, verbose) for n in names]
    if level in ("rotation", "full"):
        # A fresh bin/*.py needs the suite, and needs it seen at rotation, not
        # only under --suite. Before the count compare so node-count stays the
        # closing check. (quick is the pre-commit set; the suite gate there
        # would cost the commit a check it has not earned.)
        #
        # The freshness guard must judge against the run that is COMPLETING,
        # not the run before it. When --suite is on and the suite PASSED within
        # this very call, every bin/*.py was just covered; passing the guard
        # its own timestamp means the FIRST-ever suite run passes instead of
        # reading a None prior stamp and self-FAILing before main() records
        # one. When the suite failed (or --suite is off) `effective_ts` stays
        # None and the guard reads the recorded stamp, untouched (L4.101
        # item 2 -- the ordering, never the judgement).
        suite_res = next((r for r in results if r.name == SUITE_CMD), None)
        eff_ts = time.time() if (suite and suite_res is not None
                                 and suite_res.status == "PASS") else None
        results.append(check_bin_freshness(groot, effective_ts=eff_ts))
    # surface 2 of hypothesis:l4-a-seats-live-model-is-measured-not-assumed
    # -- the READER that turns the measured seat model into a verdict. Runs in
    # the rotation/full rounds so `verify` (verification.py) carries it.
    if level in ("rotation", "full"):
        results.append(check_seat_model(groot))
    smoke = next((r for r in results if r.name == "smoke"), None)
    current = smoke.number if smoke is not None else None
    # --stamp FORCED smoke above, so `current` is this run's fresh count and a
    # prior baseline is never re-used (hypothesis:l4-a-stamp-forces-the-smoke-
    # count). compare_count closes on node-count whenever a smoke round ran
    # (SKIPing if it reported no number) or --stamp was passed — the stamp is
    # never a silent no-op. Only a bare quick with no stamp stays without a
    # node-count result.
    if smoke is not None or stamp:
        results.append(compare_count(groot, current, stamp=stamp))
    return results


# --- reporting -------------------------------------------------------------


def _one_line(r: CheckResult) -> str:
    num = ""
    if r.number:
        num = "  [" + ", ".join(f"{k}={v}" for k, v in r.number.items()) + "]"
    note = f"  {r.note}" if r.note and not r.note.startswith("\n") else ""
    return (f"{r.status:4}  {r.name:16} {r.elapsed:6.1f}s{num}{note}").rstrip()


def render_summary(level: str, suite: bool, results: list[CheckResult],
                   graph_root: str = "", engine_root: str = "",
                   stamp: bool = False) -> str:
    lines = [f"== verification summary (level={level}, suite={'on' if suite else 'off'}"
             f", stamp={'on' if stamp else 'auto'}) =="]
    # The tool must say WHAT it measured. A number without provenance is the
    # thing this project keeps paying for — a mixed tree slips through silent
    # (hypothesis:l4-verification-counts-and-engine-root).
    if graph_root or engine_root:
        lines.append(f"roots: engine={engine_root or '?'}, graph={graph_root or '?'}")
    for r in results:
        lines.append(_one_line(r))
    failed = [r for r in results if r.status == "FAIL"]
    lines.append("")
    if failed:
        lines.append(f"RESULT: FAIL ({len(failed)} of {len(results)} checks failed)")
    else:
        lines.append(f"RESULT: PASS (all {len(results)} checks green)")
    return "\n".join(lines)


def render_json(level: str, suite: bool, results: list[CheckResult],
                graph_root: str = "", engine_root: str = "",
                stamp: bool = False) -> dict:
    return {
        "level": level,
        "suite": suite,
        "stamp": stamp,
        "graph_root": graph_root,
        "engine_root": engine_root,
        "result": "FAIL" if any(r.status == "FAIL" for r in results) else "PASS",
        "checks": [{
            "name": r.name,
            "status": r.status,
            "elapsed": round(r.elapsed, 3),
            "number": r.number,
            "note": r.note,
        } for r in results],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="levels: " + ", ".join(
            f"{k}={','.join(v)}" for k, v in LEVELS.items()))
    ap.add_argument("--level", choices=list(LEVELS), default="rotation")
    ap.add_argument("--suite", action="store_true",
                    help="opt-in: also run the pytest suite (never taken)")
    ap.add_argument("--json", action="store_true",
                    help="emit only a JSON object of the same facts")
    ap.add_argument("--seat-model", action="store_true",
                    help="run only the seat-model check (config:seats drift)")
    ap.add_argument("subcommand", nargs="?", choices=["window"], default=None,
                    help="window: print the merge-up window reply "
                         "(lock + tip + baseline); PRINTS only, never sends")
    ap.add_argument("--grant", default=None, metavar="SEAT",
                    help="with `window`: name the seat to grant so the line is "
                         "paste-ready (the grant decision stays the Prime's)")
    ap.add_argument("--stamp", action="store_true",
                    help="force-stamp the never-lower baseline (merge-up step, AFTER its push)")
    ap.add_argument("--verbose", "-v", action="store_true",
                    help="show per-check output even when it passes")
    ap.add_argument("--root", default=".",
                    help="any path inside the project")
    args = ap.parse_args(argv)

    groot = locations.find_project_root(Path(args.root).resolve())
    if groot is None:
        print(f"ERR: not an agi project: {args.root}", file=sys.stderr)
        return 1
    # Which engine OWNED the graph we are measuring? <engine> resolves from the
    # engine enclosing the --root graph, not from wherever this script lives —
    # and the report names BOTH so a mixed tree is never silent. The engine
    # and graph line must appear even when they agree (it is provenance, not
    # a diff).
    engine_root = commands.engine_for(groot)

    # The merge-up window reply — step 3 of the node. Prints the lock state +
    # tip + baseline the point holds for before merging; never sends, writes or
    # grants (the falsifier: a step that SENDS the reply is refused).
    if args.subcommand == "window":
        print(render_window(groot, args.grant))
        return 0

    # Standalone seat-model round — proof (d) of hypothesis:l4-...-measured-
    # not-assumed, and the operator shorthand. Runs only this check; `verify`
    # gets the same verdict from the rotation/full level wiring.
    if args.seat_model:
        r = check_seat_model(groot)
        if args.json:
            print(json.dumps(render_json("seat-model", False, [r],
                                         graph_root=str(groot),
                                         engine_root=str(engine_root)),
                             indent=2))
        else:
            print(render_summary("seat-model", False, [r],
                                 graph_root=str(groot),
                                 engine_root=str(engine_root)))
        return 1 if r.status == "FAIL" else 0

    # The suite lock no longer lives here — it moved to the RESOURCE.
    # `extensions/agi/tests/conftest.py` acquires it (`hypothesis:l4-the-suite-
    # lock-belongs-to-pytest-not-its-caller`), so every path that starts the
    # pytest suite — verification.py --suite, commands.py run tests, season.py
    # merge-up, a bare shell — contends for the SAME lock. This runner spawns
    # pytest as a child with no env= (so it inherits os.environ), and that
    # child acquires. Exactly one acquirer exists now.
    if args.suite:
        refusal = _suite_lock_guard(groot)
        if refusal is not None:
            print(refusal)
            return EXIT_SUITE_LOCKED

    results = run_level(groot, args.level, args.suite, args.verbose,
                        stamp=args.stamp)
    if args.suite:
        # A COMPLETED suite run records its timestamp, pass or fail. The
        # freshness check answers "has the suite run since this file
        # changed", not "did it pass" -- pass/fail is the suite's own
        # business (THOUGHT on hypothesis:l4-bin-suite-freshness-check).
        _record_suite_ts(groot)

    if args.json:
        print(json.dumps(render_json(args.level, args.suite, results,
                                     graph_root=str(groot),
                                     engine_root=str(engine_root),
                                     stamp=args.stamp),
                         indent=2))
    else:
        print(render_summary(args.level, args.suite, results,
                             graph_root=str(groot),
                             engine_root=str(engine_root),
                             stamp=args.stamp))

    return 1 if any(r.status == "FAIL" for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
