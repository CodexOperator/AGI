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
  quick    = links + goals-check + write-guard + anonymize   (pre-commit set)
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
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import locations  # noqa: E402
import commands  # noqa: E402
import spawn_budget  # noqa: E402 -- the ONE budget-dir reader (never re-globbed)
import rotate  # noqa: E402  -- _sessions_dir (the ONE resolver the pins share)
import branches  # noqa: E402  -- ref_candidates (canonical-first season grammar)
import schema_registry  # noqa: E402  -- the ONE schema reader the gates use

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

#: The SECOND declared suite -- `.agi/context`'s fixture test modules, outside
#: every configured suite. Its ROOTS are a config cell of repo-relative paths,
#: never a literal here; absent cell = a named SKIP
#: (hypothesis:context-fixture-tests-run-in-a-configured-suite).
EXTRA_SUITE_CMD = "context-suite"
EXTRA_SUITE_CELL = ("paths", "core", "suite_roots")

STATE_FILE = "verify-count.json"        # under <groot>/sessions/
#: Where a pid's cwd/cmdline/ppid are read (a test seam: non-Linux has none).
PROC = Path("/proc")

SUITE_LOCK = "verify-suite.lock"        # under <groot>/sessions/
#: The env marker a caller that ALREADY holds the suite lock exports into the
#: suite it spawns, naming its own live pid. `_suite_lock_guard` reads it so
#: the spawned runner PROCEEDS against a lock its own caller holds, instead of
#: reading that caller as a live FOREIGN pid and refusing itself
#: (SM.25b defect (2)). conftest.py is the other reader (same string).
SUITE_LOCK_MARKER = "VERIFY_SUITE_LOCK_PID"

#: Named non-zero exit when --suite is refused because another LIVE runner
#: holds the suite window. Named, not a bare 1, so the caller abroad can tell
#: "locked" from "suite ran and failed".
EXIT_SUITE_LOCKED = 2
# One persisted "when did the suite last run" timestamp (L4.81), written on
# --suite completion and read by the no-suite rotation check so "a new
# bin/*.py needs the suite" is a CHECK, not a memo (goal:g15.10).
SUITE_TS_FILE = "verify-suite-ts.json"  # under <groot>/sessions/
#: The all-green --suite marker, read by `cli.py --delete-old`'s freshness
#: gate (cli.py:5336) at exactly `<groot>/sessions/verified.stamp`. That gate
#: tests EXISTENCE only, so this is a presence marker, not a ledger; its body
#: names the sha the run executed and the wall clock so a human can date it.
#: Before this, the only writers were test fixtures -- a real production
#: `--suite` never created it, so the gate could never be satisfied by real
#: work (hypothesis:l5-verification-writes-its-own-stamp-file-on-an-all-
#: green-suite-run).
VERIFIED_STAMP_FILE = "verified.stamp"  # under <groot>/sessions/


@dataclass
class CheckResult:
    """One check's verdict, its elapsed time, and the number it produces."""

    name: str
    status: str                 # PASS | FAIL | SKIP
    elapsed: float
    number: dict | None = None
    note: str = ""
    message: str = ""
    #: The suite's slowest tests, parsed from pytest's --durations table.
    #: [] means the table was absent or unparsable -- never a fabricated one.
    durations: list = field(default_factory=list)


def _cleanup_basetemp(path: Path | None) -> None:
    """Best-effort removal of a runner-owned pytest basetemp. A removal
    failure never fails the check (claim (4))."""
    if path is None:
        return
    try:
        shutil.rmtree(path)
    except OSError:
        pass


def _suite_basetemp_refusal(engine_root: Path,
                            base: Path | None = None) -> int | None:
    """Probe the runner's system-tmp basetemp before pytest (claims 1+2); a
    live checkout prints the SAME line the conftest gate uses, exit 3."""
    base = Path(base) if base is not None else Path(tempfile.gettempdir())
    if not locations.is_live_checkout(base):
        return None
    print(locations.live_checkout_refusal(
        base, locations.git_common_root(engine_root)))
    return 3


_PYTEST_COUNT_PATTERNS = (
    ("passed", r"(\d+)\s+passed"),
    ("skipped", r"(\d+)\s+skipped"),
    ("failed", r"(\d+)\s+failed"),
    ("errors", r"(\d+)\s+errors?"),
)


def _parse_pytest_counts(output: str) -> dict:
    """Counts from pytest's own FINAL summary line, in whatever order pytest
    emits them.

    pytest writes `N passed, M skipped, K failed, E errors` with only the
    nonzero categories present, in a stable order of its own. We read each
    category independently so order never matters, and we return only the
    keys that actually appear. An empty dict means the output carried no
    countable line at all — a PASS that still must say so rather than print
    an empty bracket (hypothesis:l4-verification-counts-and-engine-root).
    Only the session's FINAL count line counts (CLASS E): a nested banner in
    captured stdout would otherwise win; pytest's footer is the LAST one.
    """
    tail = ""
    for line in output.splitlines():
        if any(re.search(pat, line) for _, pat in _PYTEST_COUNT_PATTERNS):
            tail = line
    if not tail:
        return {}
    counts: dict = {}
    for key, pat in _PYTEST_COUNT_PATTERNS:
        m = re.search(pat, tail)
        if m:
            counts[key] = int(m.group(1))
    return counts


_DURATION_LINE = re.compile(
    r"^\s*(\d+\.\d+)s\s+(call|setup|teardown)\s+(\S+)\s*$", re.MULTILINE)


def _parse_pytest_durations(output: str) -> list[dict]:
    """pytest's `--durations=N` table as [{"test", "seconds"}], or [].

    The table is the ONLY source (hypothesis:l4-the-full-suite-runs-under-600-s
    -solo-real-waits-and-process-reaps-are-seamed-not-slept claim (4)): no
    table, no list -- an empty list is recorded and MUST NOT be invented
    into a slowest-15, so a passing run with no durations reads as none.
    """
    return [{"test": m.group(3), "seconds": float(m.group(1))}
            for m in _DURATION_LINE.finditer(output)]


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


def _node_manifest(groot: Path) -> list[str] | None:
    """The COMMITTED node blobs (`git ls-tree -r HEAD`, sorted). None when
    `groot` is not a git tree or HEAD has no tree. Neither the working tree
    NOR the index: `git ls-files` is the INDEX, so a staged-but-uncommitted
    node entered the "committed" manifest and a later read named a file no
    commit ever held (SM.34 conjunct 2).

    `*.md` only, because the metric this stands in for is
    `nodes_dir.rglob("*.md")` — a `.bak` or a `.py` under `nodes/` is not a
    node, and counting one offsets the committed active count upward and
    MASKS a real node drop (SM.34 kid 3)."""
    out = _git(groot, ["ls-tree", "-r", "--name-only", "HEAD", "--", "nodes"])
    if out is None:
        return None
    return sorted(p for p in out.splitlines()
                  if p.strip().endswith(".md"))


def _committed_deprecated(groot: Path, manifest: list[str]) -> int | None:
    """How many of HEAD's manifest blobs declare `status: deprecated`, read
    with the SAME parser the metric uses — `frontmatter.read_frontmatter` +
    `str.strip().lower()` — over the whole manifest in ONE
    `git cat-file --batch`.

    A line anchor errs BOTH ways: `status: "deprecated"` is retired to the
    parser and invisible to `^status: deprecated`, so committed active reads
    HIGH and masks a drop; the same line inside a BODY is the reverse and
    raises a spurious FAIL (SM.33). A malformed header (`<path> missing`)
    returns None rather than ending the parse with a PARTIAL count; None when
    git cannot answer."""
    from frontmatter import read_frontmatter
    try:
        r = subprocess.run(["git", "cat-file", "--batch"], cwd=str(groot),
                           input="".join(f"HEAD:./{p}\n" for p in manifest)
                           .encode(), capture_output=True, timeout=120)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    out, dep, i = r.stdout, 0, 0
    while i < len(out):
        nl = out.find(b"\n", i)
        if nl < 0:
            return None
        head = out[i:nl].split()
        i = nl + 1
        # `--batch` answers `<path> missing` (2 fields) for an object it
        # cannot read, and HEAD can move between `_node_manifest` and this
        # call, so this is REACHABLE: `break` returned a PARTIAL count as if
        # complete, reading the active count HIGH and masking a drop silently.
        # None is the function's own "git cannot answer" contract.
        if len(head) != 3 or head[1] != b"blob" or not head[2].isdigit():
            return None
        size = int(head[2])
        blob = out[i:i + size]
        i += size + 1
        if b"deprecated" not in blob:   # cheap superset: skip the yaml load
            continue
        st = (read_frontmatter(blob.decode("utf-8", "replace"))
              or {}).get("status")
        if isinstance(st, str) and st.strip().lower() == "deprecated":
            dep += 1
    return dep


def _committed_counts(groot: Path, manifest: list[str] | None = None
                      ) -> dict | None:
    """Smoke's active/deprecated/total triple read from HEAD's COMMITTED tree
    instead of the working tree, so the number that GATES the FAIL is a
    committed number (SM.34 conjunct 3): a worktree read whose working-tree
    count was inflated by an untracked filler no longer masks a real drop.

    Both cells come from the same `.md`-only population (kid 3) and the
    deprecated cell goes through the parser, so on a CLEAN checkout the triple
    EQUALS `metrics.node_lifecycle_stats` for every spelling (kid 4)."""
    if manifest is None:
        manifest = _node_manifest(groot)
    if manifest is None:
        return None
    dep = _committed_deprecated(groot, manifest)
    if dep is None:
        return None
    return {"active": max(len(manifest) - dep, 0),
            "deprecated": dep, "total": len(manifest)}


def _node_dirt(groot: Path) -> list[str] | None:
    """Node paths `git status --short` flags here, or None when not a git
    tree. Non-empty means smoke's count is NOT a committed count, so a stamp
    from it would record bytes no other checkout can see — refused by name."""
    out = _git(groot, ["status", "--short", "--", "nodes"])
    if out is None:
        return None
    return [ln[3:].strip() for ln in out.splitlines() if ln.strip()]


def _manifest_mint_ids(groot: Path, paths: list[str]) -> dict[str, str] | None:
    """The `mint_id` frontmatter cell of each HEAD blob, read in ONE
    `git cat-file --batch` (never one subprocess per path). `""` when a blob
    carries none; None when git cannot answer — no proof of a move."""
    from frontmatter import read_frontmatter
    if not paths:
        return {}
    try:
        r = subprocess.run(["git", "cat-file", "--batch"], cwd=str(groot),
                           input="".join(f"HEAD:./{p}\n" for p in paths)
                           .encode(), capture_output=True, timeout=120)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    out, ids, i, n = r.stdout, {}, 0, 0
    while i < len(out):
        nl = out.find(b"\n", i)
        if nl < 0:
            return None
        head = out[i:nl].split()
        i = nl + 1
        if len(head) != 3 or head[1] != b"blob" or not head[2].isdigit():
            return None
        size = int(head[2])
        blob = out[i:i + size]
        i += size + 1
        # `--batch` answers in INPUT order but echoes the resolved sha, not
        # the spec, so the path comes from `paths` by index, never the header.
        if n >= len(paths):
            return None
        fm = read_frontmatter(blob.decode("utf-8", "replace")) or {}
        mid = fm.get("mint_id")
        ids[paths[n]] = mid.strip() if isinstance(mid, str) else ""
        n += 1
    return ids if n == len(paths) else None


def _stamped_manifest(groot: Path, manifest: list[str] | None):
    """The manifest cell to STAMP: `{path: mint_id}` (old path list if no git)."""
    if manifest is None:
        return None
    ids = _manifest_mint_ids(groot, manifest)
    return ids if ids is not None else manifest


def _legacy_baseline(prior: list | dict | None) -> bool:
    """A baseline that carries no mint-id identity: the old path LIST, or a
    dict whose values are all empty (a defensive read of a malformed record).
    A legacy baseline can PROVE no move; it proves nothing at all, so it is
    MIGRATED to the dict form, never trusted for one more run."""
    if isinstance(prior, list):
        return True
    if isinstance(prior, dict):
        return not any(isinstance(v, str) and v for v in prior.values())
    return True


def _moved_deprecated(groot: Path, prior: list | dict | None,
                      manifest: list | None,
                      ) -> tuple[list[str], list[str], list[str]]:
    """Partition baseline-manifest paths absent at HEAD into MOVEs, LOSSes
    and UNPROVABLE candidates, so a deprecation is counted as a move, never as
    a node lost.

    A retire moves a node from `nodes/<type>/<name>.md` to
    `nodes/deprecated/<type>/<name>.md`: active falls and deprecated rises
    while the TOTAL (active+deprecated) is unchanged. A baseline path absent
    at HEAD is a MOVE only when its deprecated twin exists at HEAD AND its
    frontmatter `mint_id` EQUALS the one the baseline recorded -- mint id
    equality is the proof, so an unrelated new file at the matching deprecated
    path is a LOSS, named. A LEGACY baseline (`_legacy_baseline`: path list,
    or a dict of only empty ids) carries no identity, so a basename twin
    CANNOT be proven a move -- but it cannot be called a LOSS either, since
    the total is what H0/H0b gates on. Those go to `unprovable`, which
    `compare_count` migrates in ONE visible run instead of failing forever.
    `prior` not a list/dict, or `manifest` None (not a git tree), yields no
    classifier: nothing is nameable and reads fall back to counts-only.
    """
    if not isinstance(prior, (list, dict)) or manifest is None:
        return [], [], []
    have = set(manifest)
    absent = [p for p in prior if p not in have]
    cand = {}
    for p in absent:
        parts = p.split("/")
        if len(parts) == 3 and parts[0] == "nodes" and parts[1] != "deprecated":
            moved = f"nodes/deprecated/{parts[1]}/{parts[2]}"
            if moved in have:
                cand[p] = moved
    legacy = _legacy_baseline(prior)
    ids = (_manifest_mint_ids(groot, sorted(set(cand.values())))
           if cand and not legacy else {})
    moves, losses, unprovable = [], [], []
    for p in absent:
        if p in cand:
            if legacy:
                unprovable.append(p)
                continue
            base = prior.get(p)
            if (isinstance(base, str) and base and ids is not None
                    and ids.get(cand[p]) == base):
                moves.append(p)
                continue
        losses.append(p)
    return moves, losses, unprovable


def compare_count(groot: Path, current: dict | None,
                  *, stamp: bool = False,
                  run_sha: str | None = None,
                  suite_in_call: bool = False) -> CheckResult:
    """The node-count check: FAIL when active is below the recorded baseline.

    The baseline is STAMPED only on bytes that are KEPT (`_stamp_context`)
    or when an explicit `--stamp` is passed (the merge-up step, AFTER its
    push). Every other read — a worktree, a seat branch, an unpushed MAIN —
    COMPARES but prints `NOT STAMPED: <reason>` and never writes the file
    (the falsifier: a red or dropped read that stamps). A recorded baseline
    whose `sha` is no longer an ancestor of HEAD is stale: REPORTED and
    treated as absent, never silently leaned on.

    With `--stamp` the sha recorded is the one the last recorded `--suite`
    actually RAN ON (`suite_ran_on`), and HEAD past it refuses by name. A tree
    with NO suite record at all does not refuse: a first-ever stamp keeps its
    old behaviour. A record written BEFORE `suite_ran_on` existed (has
    `suite_ran_at` only) refuses by name -- never a fail-open stamp (SM.66
    M1). `suite_in_call`: a `--suite` ran in THIS invocation, so its own start
    sha (`run_sha`) is the authority and the previous record is ignored (a
    combined `--suite --stamp`; main() writes the record after this closes).
    """
    start = time.monotonic()
    if current is None or current.get("active", -1) < 0:
        return CheckResult("node-count", "SKIP", time.monotonic() - start,
                           note="smoke did not report an active count")
    if stamp:
        can_stamp, why = True, "explicit --stamp"
        head_sha = _git(groot, ["rev-parse", "HEAD"])
        suite_ran_on = None if suite_in_call else _read_suite_ran_on(groot)
        # old-format record (no suite_ran_on) refuses, never a fail-open
        # stamp on a guessed HEAD (SM.66 M1).
        if (suite_ran_on is None and not suite_in_call
                and _read_suite_ts(groot) is not None):
            return CheckResult(
                "node-count", "FAIL", time.monotonic() - start, current,
                note="suite record predates run-start tracking: "
                     "re-run --suite")
        if suite_ran_on and head_sha and head_sha != suite_ran_on:
            return CheckResult(
                "node-count", "FAIL", time.monotonic() - start, current,
                note=f"HEAD {head_sha} moved past the run {suite_ran_on}: re-run")
        if run_sha and head_sha and head_sha != run_sha:
            return CheckResult(
                "node-count", "FAIL", time.monotonic() - start, current,
                note=f"HEAD {head_sha} moved past the run {run_sha}: re-run")
        head_sha = suite_ran_on or run_sha or head_sha
    else:
        can_stamp, head_sha, why = _stamp_context(groot)
    manifest = _node_manifest(groot)
    committed = _committed_counts(groot, manifest)
    dirt = _node_dirt(groot) or []
    if can_stamp and dirt:
        can_stamp = False
        why = (f"{why}; refused by name — {len(dirt)} uncommitted node "
               f"path(s) here: {', '.join(dirt[:5])}")
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
            _write_state(groot, current, head_sha, why,
                         _stamped_manifest(groot, manifest))
            return CheckResult(
                "node-count", "PASS", time.monotonic() - start, current,
                note=f"baseline recorded (sha={head_sha}){stale}",
                message=f"active={current['active']} recorded, stamped {why}")
        note = f"no baseline; NOT STAMPED: {why}{stale}"
        return CheckResult(
            "node-count", "PASS", time.monotonic() - start, current,
            note=note,
            message=f"active compared, no baseline stamped: {why}")
    # The gate reads the COMMITTED active count whenever the working tree can
    # lie about it — i.e. whenever `_node_dirt` is non-empty, which is exactly
    # when an untracked filler could inflate `current['active']` and hide a
    # real committed-node drop (SM.34 conjunct 3). On a clean tree the metric
    # already IS the committed number, so `current` is used unchanged.
    using_committed = bool(committed and dirt)
    # A deprecation MOVES a node from `nodes/<type>/` to
    # `nodes/deprecated/<type>/`: the active count falls and the deprecated
    # count rises while the TOTAL (active+deprecated) is unchanged. The gate
    # therefore FAILs on the committed total against the baseline total, and
    # names a genuine LOSS (an absent baseline path that did not move to the
    # deprecated tree) before ever blaming a move. The H0/H0b protection is
    # deliberate: a node quietly gone is still named and still red.
    measured_active = (committed["active"] if using_committed
                       else current.get("active", 0))
    measured_dep = (committed["deprecated"] if using_committed
                    else current.get("deprecated", 0))
    measured_total = measured_active + measured_dep
    label = "committed total" if using_committed else "total"
    prior = state.get("manifest")
    baseline_total = state.get("total")
    if not isinstance(baseline_total, int):
        # a baseline written before totals were stamped, or without one
        baseline_total = (len(prior) if isinstance(prior, list)
                          else int(state.get("active", 0))
                          + int(state.get("deprecated", 0)))
    moves, losses, unprovable = _moved_deprecated(groot, prior, manifest)
    if measured_total < baseline_total or losses:
        parts = []
        if losses:
            parts.append("missing committed file(s): " + ", ".join(losses[:5]))
        elif moves:
            parts.append("moved to deprecated: " + ", ".join(moves[:5]))
        elif measured_total < baseline_total:
            parts.append(
                "no committed manifest on record (counts only)"
                if not isinstance(prior, list)
                else "total dropped without an explanation")
        detail = "; ".join(parts)
        return CheckResult(
            "node-count", "FAIL", time.monotonic() - start, current,
            note=("NODE COUNT DROPPED: "
                  f"{label}={measured_total} below baseline={baseline_total}; "
                  f"(working tree reported active={current.get('active')}, "
                  f"deprecated={current.get('deprecated')}) {detail} "
                  + ("(H0/H0b: 29k nodes lost to a silent drop)"
                     if losses else "")),
            message=("committed node total below recorded baseline: "
                     f"{measured_total} < {baseline_total}; {detail}"))
    if unprovable:
        # A legacy baseline proves nothing, so each basename twin is
        # UNPROVABLE, not lost. The total is steady and every absent path has
        # a deprecated home -- H0/H0b is untouched because a genuine loss (no
        # twin) is in `losses` and a dropped total already FAILed above. The
        # one-run fail-open window is unavoidable (the baseline carries no
        # identity) and is bounded: this stamp rewrites the manifest in dict
        # form, so from the next run the strict mint-id rule applies.
        kind = ("legacy list baseline" if isinstance(prior, list)
                else "legacy baseline")
        migrated = ("migrated unprovable move(s) to mint-id baseline: "
                    + ", ".join(unprovable[:5]) + f" ({kind} proved nothing)")
        if can_stamp and head_sha:
            _write_state(groot, current, head_sha, why,
                         _stamped_manifest(groot, manifest))
            note = f"{migrated}; baseline updated (sha={head_sha}){stale}"
        else:
            note = f"{migrated}; NOT STAMPED: {why}{stale}"
        message = (f"{label} steady: {measured_total} >= baseline "
                   f"{baseline_total}; {migrated}")
        return CheckResult("node-count", "PASS", time.monotonic() - start,
                           current, note=note, message=message)
    if can_stamp and head_sha:
        _write_state(groot, current, head_sha, why,
                     _stamped_manifest(groot, manifest))
        note = f"node total steady; baseline updated (sha={head_sha}){stale}"
    else:
        note = f"node total steady; NOT STAMPED: {why}{stale}"
    if moves:
        note += "; moved to deprecated: " + ", ".join(moves[:5])
    message = f"{label} steady: {measured_total} >= baseline {baseline_total}"
    if moves:
        message += "; moved to deprecated: " + ", ".join(moves[:5])
    return CheckResult("node-count", "PASS", time.monotonic() - start, current,
                       note=note, message=message)


def _write_state(groot: Path, current: dict, sha: str | None,
                 reason: str, manifest: list[str] | dict[str, str] | None = None) -> None:
    """The stamped baseline carries provenance: the counts, the head sha, the
    moment, and WHY it was stamped — so a hand reset is never needed and a
    stale baseline can be REPORTED rather than silently trusted.

    It carries the committed FILE MANIFEST too (sorted relative paths + its
    sha256), so a later drop can name the file it lost. The manifest cell is
    `{path: mint_id}` when git could answer, so a move is proven by identity;
    an old-record path LIST still loads. The `reason` cell is left
    byte-for-byte as before; the manifest is named by `manifest_sha256`.
    """
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
    if manifest is not None:
        doc["manifest"] = manifest
        keys = sorted(manifest) if isinstance(manifest, dict) else manifest
        doc["manifest_sha256"] = hashlib.sha256(
            "\n".join(keys).encode("utf-8")).hexdigest()
    path.write_text(json.dumps(doc), encoding="utf-8")


#: The two top-level directories under `nodes/` that are structural rather
#: than node types, declared legitimate by CLAUDE.md's own Conventions
#: section: `.geometry` (commands/crons/shape config) and `deprecated`
#: (retired nodes, moved here rather than deleted).
STRUCTURAL_NODE_DIRS = frozenset({".geometry", "deprecated"})


def check_node_dirs(groot: Path, *, nodes_dir: Path | None = None,
                    schemas_dir: Path | None = None) -> CheckResult:
    """FAIL, by name, when a top-level directory under `<groot>/nodes/`
    matches no schema and is neither `.geometry` nor `deprecated`.

    Detect, never repair: it names the stray directory and touches nothing.
    The allowed set is every schema the registry knows — ACTIVE OR INACTIVE,
    so a directory for a schema whose file is not bracket-named (a deprecated
    /inactive type) is legitimate, and only a name matching no schema at all
    is stray. `schema_registry.load_schemas_from_dir` is the SAME reader
    `spawn_gate.check_spawn` uses; this check builds no second reader.
    (hypothesis:l4-a-verify-suite-check-refuses-a-node-directory-outside-the-
    active-schema-set.)
    """
    start = time.monotonic()
    nodes = nodes_dir if nodes_dir is not None else groot / "nodes"
    schemas = (schemas_dir if schemas_dir is not None
               else groot / "context" / "schemas")
    reg = schema_registry.load_schemas_from_dir(schemas)
    allowed = set(reg.names()) | STRUCTURAL_NODE_DIRS
    if not nodes.is_dir():
        return CheckResult("node-dirs", "SKIP", time.monotonic() - start,
                           note=f"no nodes directory at {nodes}")
    dirs = sorted(p.name for p in nodes.iterdir() if p.is_dir())
    stray = [d for d in dirs if d not in allowed]
    number = {"dirs": len(dirs), "stray": len(stray),
              "schemas": len(reg.names())}
    if stray:
        return CheckResult(
            "node-dirs", "FAIL", time.monotonic() - start, number,
            note=(f"STRAY NODE DIR(S): {', '.join(stray)} -- no schema "
                  "(active or inactive) matches and neither is .geometry/"
                  "deprecated. Read-only: nothing moved, nothing deleted; "
                  "what to do with it is a reviewer's call."),
            message=f"{len(stray)} directory(ies) outside the schema set")
    return CheckResult(
        "node-dirs", "PASS", time.monotonic() - start, number,
        note=(f"{len(dirs)} dir(s); all match a schema or "
              f".geometry/deprecated"))


# --- the suite lock (opt-in; one runner at a time) --------------------------


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def suite_lock_holder(groot: Path) -> int | None:
    """READ-ONLY: the suite lock's LIVE FOREIGN holder pid, else None. Never
    creates, never unlinks, never plants a probe pid (closes the SM.88
    acquire-then-unlink window). Dead/absent/corrupt read as None: a probe
    refuses only on a LIVE foreign owner; stale-breaking stays in
    acquire_suite_lock, the single WRITER."""
    path = Path(groot) / "sessions" / SUITE_LOCK
    try:
        holder = int(path.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return None
    if holder == os.getpid() or not _pid_alive(holder):
        return None
    return holder


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

    SM.25b defect (2): when the CALLER already holds the lock (cmd_merge_up
    takes it, then spawns this runner with SUITE_LOCK_MARKER naming its own
    pid), the marker pid IS the lock's live holder -- that is not a foreign
    hold, so PROCEED without touching the file. The lock stays held across
    the suite (the falsifier 'a merge-up that runs the suite without holding
    the lock' must stay false); this arm never releases it.
    """
    marker = os.environ.get(SUITE_LOCK_MARKER)
    if marker:
        try:
            _mpid = int(marker)
        except ValueError:
            _mpid = None
        if _mpid is not None and _pid_alive(_mpid):
            path = Path(groot) / "sessions" / SUITE_LOCK
            try:
                _holder = int(path.read_text(encoding="utf-8").strip())
            except (OSError, ValueError):
                _holder = None
            if _holder == _mpid:
                return None  # our own caller holds it: proceed, do not touch
    holder = suite_lock_holder(groot)
    if holder is not None:
        try:
            since = time.strftime(
                "%H:%M:%SZ",
                time.gmtime((Path(groot) / "sessions" / SUITE_LOCK)
                            .stat().st_mtime))
        except OSError:
            since = "?"
        return (f"suite: lock held by {holder} since {since}"
                " — refusing, not spawning")
    # Dead pid broken here (pinned stale test) so conftest starts clean.
    try:
        pid = int((Path(groot) / "sessions" / SUITE_LOCK)
                  .read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        pid = None
    if pid is not None and not _pid_alive(pid):
        try:
            (Path(groot) / "sessions" / SUITE_LOCK).unlink(missing_ok=True)
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


def _verified_stamp_path(groot: Path) -> Path:
    """The path `cli.py --delete-old` reads: `_find_root()/sessions/verified.stamp`.

    `cli._find_root()` is `locations.find_project_root()` from the CALLER's
    cwd, and the gate reads `root / "sessions/verified.stamp"` literally
    (`cli.py:5336`). A seat running the gate from a linked worktree resolves
    that worktree's graph, so the read is the LOCAL graph dir there -- not the
    shared one `_suite_ts_path` resolves. This writer must land on the gate's
    own expression exactly, or a green worktree run certifies nothing.
    """
    root = locations.find_project_root(groot) or groot
    return root / "sessions" / VERIFIED_STAMP_FILE


def _verified_stamp_paths(groot: Path) -> list[Path]:
    """Every path a `--delete-old` gate can read, local graph first.

    ONE all-green run must satisfy both the worktree it ran in (the local
    join above) and the main checkout whose shared sessions dir the gate
    reads when run from there. Duplicates collapse to one write.
    """
    out = [_verified_stamp_path(groot)]
    shared = _suite_ts_path(groot).parent / VERIFIED_STAMP_FILE
    if shared != out[0]:
        out.append(shared)
    return out


def _write_verified_stamp(groot: Path, *, ran_at: float | None,
                          ran_on: str | None) -> None:
    """Certify an all-green `--suite` run where the freshness gate looks.

    Called only when no result is FAIL (the same predicate main() returns on),
    so a red run writes nothing and the stamp's absence is honest.
    """
    ts = ran_at if ran_at is not None else time.time()
    stamp_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts))
    body = f"green suite {stamp_utc} on {ran_on or 'unknown'}\n"
    for path in _verified_stamp_paths(groot):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")


def _retract_verified_stamp(groot: Path) -> None:
    """Retract an earlier green certification after a RED `--suite` run.

    `cli.py:5336`'s gate tests `stamp.exists()` and nothing else, so a stamp
    left behind by a previous green run would certify a suite that has since
    gone red -- the gate would pass `--delete-old` on red evidence. The
    predicate here is the SAME one `main()` returns its rc on, so
    "rc==0 iff certified" holds in both directions: green writes, red
    retracts. Missing files are not an error (a first red run retracts
    nothing).
    """
    for path in _verified_stamp_paths(groot):
        path.unlink(missing_ok=True)


def _read_suite_ts(groot: Path) -> float | None:
    """Epoch of the last recorded --suite completion, or None if never."""
    try:
        doc = json.loads(_suite_ts_path(groot).read_text(encoding="utf-8"))
        return float(doc["suite_ran_at"])
    except (OSError, ValueError, TypeError, KeyError):
        return None


def _read_suite_ran_on(groot: Path) -> str | None:
    """The sha the last recorded --suite actually RAN ON, or None."""
    try:
        return json.loads(_suite_ts_path(groot).read_text(
            encoding="utf-8")).get("suite_ran_on")
    except (OSError, ValueError, TypeError):
        return None


def _record_suite_ts(groot: Path, decision: dict | None = None, *,
                     wall_s: float | None = None,
                     slowest_15: list | None = None,
                     ran_at: float | None = None,
                     ran_on: str | None = None) -> None:
    """Persist the suite-completed timestamp (same idiom as _write_state).

    Written to the SHARED sessions dir (see `_suite_ts_path`), so a first
    `--suite` run on the main checkout is immediately visible to every seat
    branch -- the round-trip falsifier (g3) of this round's item 3. When a
    `--suite-ring` gate admitted this run, its mastered ``decision`` cell
    (hypothesis:l4-a-ring-decision-carries-m-of-n-signatures claim (2)) is
    merged into the SAME record the suite already writes -- not a second
    ledger -- so a later reader loads it from disk and re-verifies m-of-n
    WITHOUT argv, and a tampered record reads short-of-m by name."""
    path = _suite_ts_path(groot)
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = {"suite_ran_at": ran_at if ran_at is not None else time.time()}
    if ran_on is not None:
        doc["suite_ran_on"] = ran_on
    if decision is not None:
        doc["ring_decision"] = decision
    # Conjunct 4: the wall time is the CHECK's own `.seconds`, never a
    # second measurement, and the slowest-15 is what pytest printed ([] when
    # it printed no table). None means "this caller did not run a suite" and
    # leaves any existing value alone.
    if wall_s is not None:
        doc["suite_wall_s"] = round(float(wall_s), 3)
    if slowest_15 is not None:
        doc["slowest_15"] = slowest_15
    # Merge over any existing record so the grant decision is not lost when a
    # second --suite (no ring) refreshes the timestamp.
    try:
        existing = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(existing, dict):
            doc = {**existing, **doc}
    except (OSError, ValueError, TypeError):
        pass
    path.write_text(json.dumps(doc), encoding="utf-8")


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


def check_anonymize(groot: Path) -> CheckResult:
    """SM.122 — FAIL when staged text carries a token read from this box."""
    start = time.monotonic()
    argv = [sys.executable,
            str(Path(__file__).resolve().parent / "anonymize.py"),
            "check", "--root", str(groot)]
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError) as exc:
        return CheckResult("anonymize", "FAIL", time.monotonic() - start,
                           note=f"could not execute: {exc}")
    tail = (proc.stdout + proc.stderr).strip().splitlines()
    return CheckResult("anonymize", "PASS" if proc.returncode == 0 else "FAIL",
                       time.monotonic() - start,
                       note="" if proc.returncode == 0 else (tail[-1] if tail else ""))


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


def _lock_chain(pid: int) -> list[int]:
    """`pid` and up to FOUR ancestors, from `PROC/<pid>/status`."""
    chain: list[int] = []
    for _ in range(5):
        if pid <= 0 or pid in chain:
            break
        chain.append(pid)
        try:
            raw = (PROC / str(pid) / "status").read_text(encoding="utf-8")
        except OSError:
            break
        m = re.search(r"^PPid:\s+(\d+)", raw, re.M)
        pid = int(m.group(1)) if m else 0
    return chain


def _lock_tree(groot: Path, pid: int) -> str:
    """The holder's tree: its worktree name, `main`, or `unresolved`."""
    try:
        cwd = os.readlink(PROC / str(pid) / "cwd")
    except OSError:
        return "unresolved"
    main = str(locations.git_common_root(groot) or groot)
    wt = os.path.join(main, ".agi", "worktrees") + "/"
    if cwd.startswith(wt):
        return cwd[len(wt):].split("/")[0] or "unresolved"
    if cwd == main or cwd.startswith(main + "/"):
        return "main"
    return Path(cwd).name or "unresolved"


def _lock_runner(groot: Path, chain: list[int]) -> str:
    """The spawn-budget row for a pid on `chain`, through its own reader."""
    try:
        leases = spawn_budget.live_leases_readonly(groot)
    except Exception:                    # a diagnostic reader never raises
        return ""
    for rec in leases:
        if {rec.get("agent_pid"), rec.get("holder_pid")} & set(chain):
            return (f" runner {rec.get('agent_id')} tier={rec.get('tier')}"
                    f" iter={rec.get('iter')}")
    return ""


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
            mtime = lock_path.stat().st_mtime
            since = time.strftime("%H:%M:%SZ", time.gmtime(mtime))
            age = f"{int(time.time() - mtime)}s"
        except OSError:
            since, age = "?", "unresolved"
        try:                       # the holder's argv head (60 bytes, NULs
            raw = (PROC / str(holder) / "cmdline").read_bytes()[:60]
            cmd = raw.replace(b"\0", b" ").decode("utf-8", "replace").strip()
        except OSError:            # as spaces) -- unreadable is not fatal
            cmd = ""
        lines.append(f"lock: held by {holder} since {since} "
                     f"(age {age}, tree {_lock_tree(groot, holder)}, "
                     f"cmd {cmd or 'unresolved'})"
                     + _lock_runner(groot, _lock_chain(holder)))
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
            f"ran on {_read_suite_ran_on(groot) or '?'} "
            f"reason={state.get('reason', '?')}")
    reply = "\n".join(lines)
    if grant:
        reply = f"GRANT {grant} — merge-up window open\n" + reply
    return reply


# --- the runner ------------------------------------------------------------


def _declared_suite_roots(groot: Path) -> tuple[list[Path], str]:
    """(roots, cell-name) from the config cell; repo-relative, never a
    literal. An absent/empty cell -> ([], cell): the caller SKIPs by name."""
    cell = ".".join(EXTRA_SUITE_CELL)
    node = locations.load_config(groot)
    for part in EXTRA_SUITE_CELL:
        node = node.get(part) if isinstance(node, dict) else None
        if node is None:
            return [], cell
    if not isinstance(node, list):
        return [], cell
    # cell values are REPO-RELATIVE (owner 09-23); the repo is the parent of
    # the `.agi/` graph dir in the G11 layout.
    base = groot.parent if groot.name == ".agi" else locations.source_root(groot)
    return [(base / str(r)).resolve() for r in node if str(r)], cell


def check_extra_suite(groot: Path) -> CheckResult:
    """The DECLARED second suite: pytest over the configured roots. A
    collection ERROR is a FAIL with the failing tail -- a context module that
    cannot import is skipped BY NAME (`pytest.importorskip`), not dropped."""
    start = time.monotonic()
    roots, cell = _declared_suite_roots(groot)
    if not roots:
        return CheckResult(EXTRA_SUITE_CMD, "SKIP", time.monotonic() - start,
                           note=f"no suite roots declared in config cell {cell}")
    counts: dict = {}
    notes: list[str] = []
    ok = True
    for root in roots:
        if not root.is_dir():
            notes.append(f"{root}: not a directory")
            ok = False
            continue
        proc = subprocess.run([sys.executable, "-m", "pytest", str(root),
                               "-q", "-rs"], capture_output=True, text=True,
                              timeout=SUITE_TIMEOUT, cwd=groot)
        out = (proc.stdout or "") + (proc.stderr or "")
        counts.update(_parse_pytest_counts(out))
        if proc.returncode:
            ok = False
            notes.append(f"{root.name}: exit {proc.returncode}\n" +
                         "\n".join(out.splitlines()[-10:]))
    return CheckResult(EXTRA_SUITE_CMD, "PASS" if ok else "FAIL",
                       time.monotonic() - start, counts or None, "\n".join(notes))


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
    argv = list(cmd.argv)
    # The SUITE alone gets the slowest-15 table and a PRIVATE pytest basetemp.
    # A concurrent pytest prunes the SHARED /tmp/pytest-of-<user> basetemp
    # to 3, which deleted this runner's tree mid-run (SM stamp run 2). The
    # runner owns a dir under the shared sessions tree and removes it best
    # effort after the run (claim (4)). No shell habit; never a shared default.
    basetemp: Path | None = None
    if name == SUITE_CMD:
        # Refuse AT THE LAUNCH SITE, where pytest would actually spawn: a
        # --suite runner launched from inside a test (PYTEST_CURRENT_TEST set)
        # re-launches pytest nested inside a live --suite run (the detached
        # second suite, ppid 1). Only when the argv IS pytest, so a stubbed
        # fake suite under test still runs; a shell-driven runner has
        # PYTEST_CURRENT_TEST unset and is unaffected.
        if os.environ.get("PYTEST_CURRENT_TEST") and any(
                os.path.basename(str(a)).startswith("pytest") for a in argv):
            return CheckResult(name, "FAIL", time.monotonic() - start,
                               note="a runner launched from inside a test "
                                    "(PYTEST_CURRENT_TEST set) is not a "
                                    "legitimate rotation check; refusing")
        if not any(a.startswith("--durations") for a in argv):
            argv.append("--durations=15")
        if not any(a.startswith("--basetemp") for a in argv):
            try:
                # claim (2): private runner basetemp = system-tmp mkdtemp.
                base = tempfile.mkdtemp(prefix="agi-suite-")
                argv.append(f"--basetemp={base}")
                basetemp = base
            except OSError:
                basetemp = None   # skip, never fail the check on create
    try:
        proc = subprocess.run(
            argv, capture_output=True, text=True,
            timeout=ceiling, cwd=cmd.cwd or None)
    except subprocess.TimeoutExpired:
        return CheckResult(name, "FAIL", time.monotonic() - start,
                           note=f"timed out after {ceiling}s")
    except OSError as exc:
        return CheckResult(name, "FAIL", time.monotonic() - start,
                           note=f"could not execute: {exc}")
    finally:
        _cleanup_basetemp(basetemp)
    output = (proc.stdout or "") + (proc.stderr or "")
    durations = _parse_pytest_durations(output) if name == SUITE_CMD else []
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
                       time.monotonic() - start, number, note=note,
                       durations=durations)


def run_level(groot: Path, level: str, suite: bool, verbose: bool,
               stamp: bool = False, run_ts: float | None = None,
               run_sha: str | None = None) -> list[CheckResult]:
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
    if suite:
        # the DECLARED second suite, from the config cell, never a literal
        results.append(check_extra_suite(groot))
    # SM.122 — the write-seam guard, appended at EVERY level, as a built-in.
    results.append(check_anonymize(groot))
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
        eff_ts = ((run_ts or time.time()) if (suite and suite_res is not None
                  and suite_res.status == "PASS") else None)
        results.append(check_bin_freshness(groot, effective_ts=eff_ts))
    # surface 2 of hypothesis:l4-a-seats-live-model-is-measured-not-assumed
    # -- the READER that turns the measured seat model into a verdict. Runs in
    # the rotation/full rounds so `verify` (verification.py) carries it.
    if level in ("rotation", "full"):
        results.append(check_seat_model(groot))
    # surface 1 of hypothesis:l4-a-verify-suite-check-refuses-a-node-
    # directory-outside-the-active-schema-set -- the stray-directory guard,
    # wired at the SAME levels as bin-freshness and seat-model above (the
    # LEVELS dict names only commands.py-resolved check NAMES; a check built
    # from the graph itself is appended by level here) and NOT at `quick`,
    # which is the pre-commit set that must stay under 15s and has not earned
    # a graph-wide directory scan. Read-only, so it is safe at rotation.
    if level in ("rotation", "full"):
        results.append(check_node_dirs(groot))
    smoke = next((r for r in results if r.name == "smoke"), None)
    current = smoke.number if smoke is not None else None
    # --stamp FORCED smoke above, so `current` is this run's fresh count and a
    # prior baseline is never re-used (hypothesis:l4-a-stamp-forces-the-smoke-
    # count). compare_count closes on node-count whenever a smoke round ran
    # (SKIPing if it reported no number) or --stamp was passed — the stamp is
    # never a silent no-op. Only a bare quick with no stamp stays without a
    # node-count result.
    if smoke is not None or stamp:
        results.append(compare_count(groot, current, stamp=stamp,
                                     run_sha=run_sha,
                                     suite_in_call=suite))
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


def _suite_grant_fields(groot: Path, level: str, ring_name: str,
                        *, ts=None, nonce=None) -> dict:
    """The FULL suite-grant decision fields a ring's signatures cover -- the
    same bytes the gate signs, the suite persists, and a reader re-verifies
    (hypothesis:l4-a-ring-decision-carries-m-of-n-signatures, HOLE 2: the
    signed bytes must cover the decision it authorises, so a quorum for one
    level/groot/ring cannot replay onto another). FRESH (kid B): the returned
    dict carries the reserved ``_fresh`` (ts|nonce) via rings.fresh_fields, so
    a persisted quorum does NOT replay across time -- the SAME bytes a producer
    signs and the gate verifies. ts/nonce default to freshly minted here; pass
    them to keep the sign side and the gate deterministic (fixtures do).
    """
    from seatsig import rings as _rings  # noqa: PLC0415
    return _rings.fresh_fields(
        {"level": level, "root": str(groot), "ring": ring_name},
        ts=ts, nonce=nonce)


def _ring_gate_refusal(groot: Path, ring_name: str, level: str,
                       signatures: list, *, fields: dict | None = None,
                       remember: bool = True
                       ) -> str | None:
    """Rung 2 suite-ring gate: refuse the suite/merge grant when its record
    lacks the named ring's m valid signatures. Returns the refusal line (naming
    the m-of-n count) or None to admit. OPT-IN: a ring the geometry does not
    name is not demanded. Verified through seatsig/rings.py (the SAME Scheme
    interface send.py's verify labels against), never this gate's own crypto.
    FRESH (kid B): when ``fields`` is given it is the exact decision signed
    (never argv); when None the fields are built fresh HERE, and an admitted
    grant must also pass freshness_refusal (within its replay window, nonce
    not already spent) against the on-disk nonce ledger. ``remember`` (kid D):
    when False, an admitted grant READS the ledger (a replayed nonce still
    refuses) but never writes it -- a dry/preview run records nothing."""
    try:
        from seatsig import rings as _rings

        rings_rows = _rings.load_rings(groot)
        ring = _rings.ring_by_name(rings_rows, ring_name)
    except Exception:  # noqa: BLE001
        ring = None
    if ring is None:
        return None  # no such ring declared -> opt-in means nothing demanded
    fields = fields if fields is not None else \
        _suite_grant_fields(groot, level, ring_name)
    canonical = _rings.canonical_bytes("suite-grant", fields)

    def resolver(post):
        try:
            import geometry_config  # noqa: PLC0415

            for row in geometry_config.load_rows(groot):
                if row.get("name") == post:
                    return row.get("pubkey") or None
        except Exception:  # noqa: BLE001
            return None
        return None

    res = _rings.verify_ring(ring, canonical, signatures or [],
                             pubkey_for_post=resolver)
    if res.ok:
        # FRESH (kid B): the quorum is satisfied, so the decision must also
        # sit inside its replay window and not carry a spent nonce.
        seen, remember_fn = _rings.nonce_ledger(groot)
        # RUNG 2b clause 3: a failed ledger WRITE or READ (LedgerWriteError /
        # LedgerReadError) refuses BY NAME -- the nonce was not remembered (or
        # the seen set could not be read), so the decision is not admitted (a
        # nonce is never spent silently, and an unreadable ledger is never
        # read as an empty one).
        try:
            fr = _rings.freshness_refusal(
                fields,
                max_age_s=_rings._effective_max_age_s(ring),
                seen=seen, remember=remember_fn if remember else None)
        except (_rings.LedgerWriteError, _rings.LedgerReadError) as le:
            return (f"merge grant refused: {le}")
        if fr:
            return (f"merge grant refused: freshness {fr}")
        return None
    return (f"merge grant short of {ring_name!r} ring quorum: {res.refused}")


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
    ap.add_argument("--suite-ring", default=None, metavar="RING",
                    help="rung 2: with `--suite`, demand the quorum of this "
                         "ring (an approval record the merge grant needs) "
                         "before the suite window opens; short of m the "
                         "suite is REFUSED by name with the count (opt-in)")
    ap.add_argument("--ring-sig", dest="ring_sigs", action="append",
                    default=[],
                    help="rung 2: repeatable; a `<post>:<scheme>:<sig_hex>` "
                         "signature over the suite-grant record backing "
                         "`--suite-ring` (seatsig/rings.py)")
    ap.add_argument("--ring-fresh", default=None, metavar="TS|NONCE",
                    help="rung 2 freshness seam (kid D): pin the EXACT "
                         "'<ts>|<nonce>' the suite-grant decision's `_fresh` "
                         "carries, so an out-of-process signer computes the "
                         "SAME canonical bytes and a `--suite-ring` run admits "
                         "at m>0. Absent -> the gate mints fresh (unpredictable).")
    ap.add_argument("--ring-fields", action="store_true",
                    help="rung 2 signer's view (kid D): print the exact suite-"
                         "grant fields and canonical bytes `--suite-ring` will "
                         "verify for this argv (+ `--ring-fresh`), then exit 0 -- "
                         "never runs the suite, records a nonce, or calls pytest.")
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
        _base_refusal = _suite_basetemp_refusal(engine_root)
        if _base_refusal is not None:
            return _base_refusal

    # RUNG 2 suite-ring gate (hypothesis:l4-a-ring-decision-carries-m-of-n-
    # signatures). OPT-IN: only when `--suite-ring <name>` is given AND the
    # geometry names that ring is the suite-window/merge grant gated on the
    # ring's quorum -- verified through the SAME seatsig Scheme interface
    # send.py uses (seatsig/rings.py), never this gate's own crypto; a
    # short-of-m grant is REFUSED BY NAME with the m-of-n count and the suite
    # never runs.
    if args.suite and args.suite_ring:
        from seatsig import rings as _rings  # noqa: PLC0415
        # FRESH seam (kid D): a caller-supplied `<ts>|<nonce>` pins the EXACT
        # `_fresh` so an out-of-process signer computes the same bytes.
        try:
            _fresh = _rings.parse_ring_fresh(args.ring_fresh)
        except ValueError as _ve:
            print(f"suite-ring: {_ve}")
            return 1
        _t, _n = (_fresh if _fresh is not None else (None, None))
        # FRESH (kid B): compute the decision ONCE (fresh ts/nonce) so the
        # gate verifies, the signatures cover, and the persisted record all
        # agree on the same bytes -- freshness never minted twice.
        grant_fields = _suite_grant_fields(groot, args.level, args.suite_ring,
                                           ts=_t, nonce=_n)
        # SIGNER'S VIEW (kid D): print the exact bytes the gate will verify
        # for this argv + --ring-fresh, then exit 0 -- never runs the suite.
        if args.ring_fields:
            print(_rings.render_ring_fields(
                "suite-grant", grant_fields,
                _rings.canonical_bytes("suite-grant", grant_fields)))
            return 0
        refusal = _ring_gate_refusal(groot, args.suite_ring,
                                     args.level, args.ring_sigs,
                                     fields=grant_fields)
        if refusal is not None:
            print(f"suite-ring: {refusal}")
            return 1
        # RUNG 2 claim (2): the admitted suite-grant signatures are persisted
        # onto the ONE record the suite already writes (see _record_suite_ts)
        # so a later reader re-verifies m-of-n from disk, never argv. The
        # canonical fields are the same bytes the gate just signed (with the
        # fresh ts|nonce the quorum covered).
        _suite_decision = _rings.decision_cell(
            args.suite_ring, "suite-grant", grant_fields,
            args.ring_sigs)
    else:
        _suite_decision = None

    # The suite record names the RUN START: wall clock + sha BEFORE pytest.
    _run_ts = _run_sha = None
    if args.suite or args.stamp:
        _run_ts = time.time()
        _run_sha = _git(groot, ["rev-parse", "HEAD"])
    results = run_level(groot, args.level, args.suite, args.verbose,
                        stamp=args.stamp, run_ts=_run_ts, run_sha=_run_sha)
    if args.suite:
        # A COMPLETED suite run records its timestamp, pass or fail. The
        # freshness check answers "has the suite run since this file
        # changed", not "did it pass" -- pass/fail is the suite's own
        # business (THOUGHT on hypothesis:l4-bin-suite-freshness-check).
        _suite_res = next((r for r in results if r.name == SUITE_CMD), None)
        _record_suite_ts(groot, _suite_decision, ran_at=_run_ts,
                         ran_on=_run_sha,
                         wall_s=_suite_res.elapsed if _suite_res else None,
                         slowest_15=(_suite_res.durations
                                     if _suite_res else None))
        # An ALL-GREEN suite run certifies itself at the exact path
        # `cli.py --delete-old` reads. The predicate is the SAME one the return
        # code uses, so "green" and rc==0 can never disagree. A red run writes
        # NOTHING -- the stamp is a pass marker, and absence is the correct
        # state on FAIL (never a stale marker claiming a green run that did
        # not happen).
        if not any(r.status == "FAIL" for r in results):
            _write_verified_stamp(groot, ran_at=_run_ts, ran_on=_run_sha)
        else:
            # A RED run RETRACTS any earlier certification at every path the
            # gate can read, so the stamp can never outlive the green run it
            # recorded (cli.py:5336 tests existence only).
            _retract_verified_stamp(groot)

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
