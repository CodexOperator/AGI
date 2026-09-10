#!/usr/bin/env python3
"""stall_detect.py — DETECTION ONLY, no repair.

**hypothesis:l4-stalled-is-a-state-the-harness-can-see.** `stalled` becomes a
first-class RECORDED agent state the harness can SEE. The prime's spec:

THE SHAPE, all four conditions together:
  (1) every kid of that parent is terminal;
  (2) the DISPATCHER-side `agent.json` still reads `status: running`;
  (3) that record's mtime is unchanged since spawn — the crisp one. `cmd_done`
      writes `status`/`finished_at` into the record BEFORE it commits
      (proved by `experiment:a00-f2f8465a-b4eb8e`), so an untouched mtime is
      positive evidence that `done` was never called, not an inference from
      silence;
  (4) the parent's worktree holds uncommitted work.

Plus threshold T (minutes) so a merely slow parent is not called stalled. T is
configurable; the default here is 45 minutes.

RECORD, DO NOT REPAIR. `detect_stalled` returns a label; `note_stalled`
records the state on the agent.json record. Neither kills, neither restarts,
neither commits. And `stalled` is NOT terminal — a stalled parent is still
alive and still holds its lease, so it must never join
`spawn_budget.TERMINAL` (the ONE set, L4.70). The absence from that set is
tested, not assumed.

Usage (embedded; this module is a library, not a CLI):
    from stall_detect import scan_iteration, note_stalled
    stalled = scan_iteration(iter_dir)
    for aid in stalled:
        note_stalled(agent_json_path(aid))
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import locations  # noqa: E402
from spawn_budget import TERMINAL  # noqa: E402 — the ONE terminal set

#: Default age threshold, seconds (45 minutes). A parent younger than this is
#: merely slow, not stalled. Configurable at every call site.
STALL_THRESHOLD_S = 45 * 60

#: Default age threshold for the sibling before-work shape, seconds
#: (15 minutes — the assigning director's own operational rule, "a parent
#: that spawns no kid within ~15 minutes is as bad as an idle one, kill it").
#: That rule is about when a HUMAN/operator should act; this threshold is
#: about when the state becomes worth RECORDING, the same distinction L4.78
#: draws with its 45-minute T for the after-work shape. Configurable at every
#: call site, same as STALL_THRESHOLD_S.
STALL_BEFORE_WORK_THRESHOLD_S = 15 * 60

#: The recorded label for the before-work sibling shape. Distinct from
#: `stalled` so the two shapes remain distinguishable in the record and to any
#: downstream consumer; a before-work parent and an after-work parent are not
#: the same mechanism and should not wear the same status. Like `stalled`, it
#: is a RECORDED state and must NEVER join `spawn_budget.TERMINAL`.
STALL_BEFORE_WORK_LABEL = "stalled_before_work"

#: Tolerance for "mtime unchanged since spawn", seconds. Filesystem writes on
#: spawn and the record write share a wallclock; 1s is generous for the
#: same-second writes `spawn` performs.
_MTIME_EPS = 1.0


def detect_stalled(*, kids_terminal: bool, record_status: str,
                   record_mtime_unchanged: bool, worktree_has_uncommitted: bool,
                   age_s: float, threshold_s: int = STALL_THRESHOLD_S) -> bool:
    """Judge one parent against the four conditions plus the age threshold.

    DETECTION ONLY — returns a bool, has no side effects. A detector that
    fires on three of four conditions is a false-alarm generator, so every
    condition is load-bearing (the negative cases are tested one per missing
    condition).
    """
    if not kids_terminal:
        return False
    if record_status != "running":
        return False
    if not record_mtime_unchanged:
        return False
    if not worktree_has_uncommitted:
        return False
    if age_s < threshold_s:
        return False
    return True


def detect_stalled_before_work(*, zero_kids: bool, record_status: str,
                               worktree_clean: bool, age_s: float,
                               threshold_s: int = STALL_BEFORE_WORK_THRESHOLD_S) -> bool:
    """Judge one parent against the before-work shape's four conditions.

    **hypothesis:l4-stall-before-work.** A SIBLING of `detect_stalled`, for
    the parent that NEVER spawned a kid at all. DETECTION ONLY — returns a
    bool, has no side effects. Every condition is load-bearing (the negative
    cases are tested one per missing condition):
      (1) `zero_kids` — the parent spawned NO kid, genuinely none, ever
          (the inverse of L4.78's kids-terminal: here kids must not EXIST);
      (2) `record_status == "running"` — same dispatcher-side check;
      (3) `worktree_clean` — a CLEAN worktree, the inverse of L4.78's
          uncommitted-work condition (a parent that never spawned a kid and
          never touched a file is exactly what "nothing attempted" looks
          like, so clean here is CONFIRMING evidence);
      (4) `age_s >= threshold_s` — past the age threshold.
    """
    if not zero_kids:
        return False
    if record_status != "running":
        return False
    if not worktree_clean:
        return False
    if age_s < threshold_s:
        return False
    return True


def _cohort_zero_kids(agent_ids: list[str], exclude: str) -> bool:
    """Condition (1): the parent has spawned ZERO kids — genuinely none, ever.

    Distinct from `_cohort_terminal`, which returns True VACUOUSLY over an
    empty set (every of zero kids is terminal). Here the count is the whole
    point: any kid id other than the parent itself means a kid WAS spawned,
    and the shape fails even if that kid is not yet terminal.
    """
    for aid in agent_ids:
        if aid and aid != exclude:
            return False
    return True


def _worktree_clean(rec: dict, itdir: Path) -> bool:
    """Condition (3): the parent's worktree is CLEAN — no uncommitted work.

    The INVERSE of `_worktree_dirty`. A parent that never spawned a kid and
    never touched a file is exactly what "nothing attempted" looks like, so
    a clean worktree here is CONFIRMING evidence of the before-work shape.
    Conservative on error: if cleanliness cannot be determined (git fails,
    no worktree), return False rather than risk a false liveness alarm.
    """
    wt = rec.get("worktree")
    if not wt:
        wt = str(itdir)
    try:
        r = subprocess.run(
            ["git", "-C", wt, "status", "--porcelain"],
            capture_output=True, text=True, timeout=10,
        )
    except (subprocess.SubprocessError, OSError):
        return False
    return not bool(r.stdout.strip())


def record_mtime_unchanged(rec_path: Path, started_at: float,
                           eps: float = _MTIME_EPS) -> bool:
    """Condition (3): is the record's mtime still at spawn time?

    `started_at` is the wallclock `dispatch.py` stamped when the agent
    spawned. If the file's own mtime matches it, the record has not been
    rewritten since — and since `cmd_done` writes the record before it
    commits, an untouched mtime means `done` was never called.
    """
    if started_at <= 0:
        return False
    try:
        return abs(rec_path.stat().st_mtime - started_at) <= eps
    except OSError:
        return False


def _cohort_terminal(itdir: Path, agent_ids: list[str], exclude: str) -> bool:
    """Every agent in the cohort except `exclude` is terminal.

    Reads each record's live `agent.json`, never the manifest copy, so a
    stale manifest line cannot hide a still-running kid.
    """
    for aid in agent_ids:
        if not aid or aid == exclude:
            continue
        p = itdir / aid / "agent.json"
        if not p.exists():
            return False
        try:
            rec = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return False
        if str(rec.get("status") or "") not in TERMINAL:
            return False
    return True


def _worktree_dirty(rec: dict, itdir: Path) -> bool:
    """Condition (4): the parent's worktree holds uncommitted work.

    `rec['worktree']` is the git worktree path the `--branch` parent runs in
    (absolute, recorded at dispatch). Check `git status --porcelain` there for
    any output. No worktree recorded -> no evidence of uncommitted work.
    """
    wt = rec.get("worktree")
    if not wt:
        # Fall back to the iteration dir's own parent, so a non-branch parent
        # is still inspected; still a read-only check.
        wt = str(itdir)
    try:
        r = subprocess.run(
            ["git", "-C", wt, "status", "--porcelain"],
            capture_output=True, text=True, timeout=10,
        )
    except (subprocess.SubprocessError, OSError):
        return False
    return bool(r.stdout.strip())


def scan_iteration(iter_dir, *, threshold_s: int = STALL_THRESHOLD_S,
                   now: float | None = None,
                   worktree_dirty=None) -> list[str]:
    """Return the ids of parents in `iter_dir` judged stalled.

    Reads the manifest for the cohort, each record's `agent.json` for status /
    mtime / started_at, and resolves the worktree for the uncommitted-work
    condition. DETECTION ONLY — writes nothing. `now` and `worktree_dirty`
    are injectable for tests.
    """
    itdir = Path(iter_dir)
    now = time.time() if now is None else now
    manifest_path = itdir / "manifest.json"
    if not manifest_path.exists():
        return []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    agents = manifest.get("agents", [])
    ids = [str(e.get("id") or "") for e in agents if isinstance(e, dict)]
    stalled: list[str] = []
    dirty_fn = worktree_dirty or _worktree_dirty
    for aid in ids:
        rec_path = itdir / aid / "agent.json"
        if not rec_path.exists():
            continue
        try:
            rec = json.loads(rec_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        status = str(rec.get("status") or "")
        if status != "running":
            continue
        started_at = int(rec.get("started_at") or 0)
        age = now - started_at
        if detect_stalled(
            kids_terminal=_cohort_terminal(itdir, ids, aid),
            record_status=status,
            record_mtime_unchanged=record_mtime_unchanged(rec_path, started_at),
            worktree_has_uncommitted=bool(dirty_fn(rec, itdir)),
            age_s=age,
            threshold_s=threshold_s,
        ):
            stalled.append(aid)
    return stalled


def scan_iteration_before_work(iter_dir, *,
                               threshold_s: int = STALL_BEFORE_WORK_THRESHOLD_S,
                               now: float | None = None,
                               worktree_clean=None) -> list[str]:
    """Return the ids of parents in `iter_dir` judged stalled before work.

    The read-only scan for the sibling shape: reads the manifest for the
    cohort and each record's `agent.json` for status / started_at, checks the
    parent spawned no kid and holds a clean worktree, and applies the age
    threshold. DETECTION ONLY — writes nothing. `now` and `worktree_clean`
    are injectable for tests.
    """
    itdir = Path(iter_dir)
    now = time.time() if now is None else now
    manifest_path = itdir / "manifest.json"
    if not manifest_path.exists():
        return []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    agents = manifest.get("agents", [])
    ids = [str(e.get("id") or "") for e in agents if isinstance(e, dict)]
    stalled: list[str] = []
    clean_fn = worktree_clean or _worktree_clean
    for aid in ids:
        rec_path = itdir / aid / "agent.json"
        if not rec_path.exists():
            continue
        try:
            rec = json.loads(rec_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        status = str(rec.get("status") or "")
        if status != "running":
            continue
        started_at = int(rec.get("started_at") or 0)
        age = now - started_at
        if detect_stalled_before_work(
            zero_kids=_cohort_zero_kids(ids, aid),
            record_status=status,
            worktree_clean=bool(clean_fn(rec, itdir)),
            age_s=age,
            threshold_s=threshold_s,
        ):
            stalled.append(aid)
    return stalled


def record_stalled_before_work_in_iteration(iter_dir, *,
                                            threshold_s: int = STALL_BEFORE_WORK_THRESHOLD_S,
                                            now: float | None = None,
                                            worktree_clean=None) -> list[str]:
    """The one hook the harvest path calls for the before-work shape.

    Wires `scan_iteration_before_work` (read-only detection) to
    `note_stalled_before_work` (the stamp) so the dispatch/reaper cycle can
    record this sibling state with a single call. RECORD, DO NOT REPAIR: the
    only write is the `status`/`stalled_at` stamp on the live `agent.json`;
    nothing is killed, restarted or committed, and the label never joins
    `spawn_budget.TERMINAL`.
    """
    itdir = Path(iter_dir)
    stamped: list[str] = []
    for aid in scan_iteration_before_work(itdir, threshold_s=threshold_s,
                                          now=now, worktree_clean=worktree_clean):
        note_stalled_before_work(itdir / aid / "agent.json")
        stamped.append(aid)
    return stamped


def note_stalled_before_work(rec_path) -> None:
    """RECORD, DO NOT REPAIR: stamp `status: stalled_before_work`.

    The only write the before-work shape performs, mirroring `note_stalled`.
    Updates the record's own `agent.json` in place with `status` and
    `stalled_at`; never kills, never restarts, never commits, never touches
    `spawn_budget.TERMINAL`. Idempotent.
    """
    rec_path = Path(rec_path)
    if not rec_path.exists():
        return
    try:
        rec = json.loads(rec_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return
    if not isinstance(rec, dict):
        return
    if str(rec.get("status") or "") == STALL_BEFORE_WORK_LABEL:
        return
    rec["status"] = STALL_BEFORE_WORK_LABEL
    rec["stalled_at"] = int(time.time())
    rec_path.write_text(json.dumps(rec, indent=2), encoding="utf-8")


def record_stalled_in_iteration(iter_dir, *, threshold_s: int = STALL_THRESHOLD_S,
                                now: float | None = None,
                                worktree_dirty=None) -> list[str]:
    """The one hook the harvest path calls: scan + stamp in one step.

    Wires `scan_iteration` (read-only detection) to `note_stalled` (the only
    write this module performs) so the dispatch/reaper cycle can record
    `stalled` as a first-class agent state with a single call. Returns the ids
    stamped. RECORD, DO NOT REPAIR: the write is only the `status`/`stalled_at`
    stamp on the live `agent.json`; nothing is killed, restarted or committed,
    and `stalled` never joins `spawn_budget.TERMINAL`.
    """
    itdir = Path(iter_dir)
    stamped: list[str] = []
    for aid in scan_iteration(itdir, threshold_s=threshold_s, now=now,
                              worktree_dirty=worktree_dirty):
        note_stalled(itdir / aid / "agent.json")
        stamped.append(aid)
    return stamped


def note_stalled(rec_path, *, burst: bool = True) -> None:
    """RECORD, DO NOT REPAIR: stamp `status: stalled` on the record.

    The only write this module performs, and it is the point — `stalled`
    becomes a first-class RECORDED agent state. It updates the record's own
    `agent.json` in place with `status` and `stalled_at`; it never kills,
    never restarts, never commits, and never touches `spawn_budget.TERMINAL`.
    Idempotent: a record already `stalled` is left untouched.
    """
    rec_path = Path(rec_path)
    if not rec_path.exists():
        return
    try:
        rec = json.loads(rec_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return
    if not isinstance(rec, dict):
        return
    if str(rec.get("status") or "") == "stalled":
        return
    rec["status"] = "stalled"
    rec["stalled_at"] = int(time.time())
    rec_path.write_text(json.dumps(rec, indent=2), encoding="utf-8")

def main(argv: list[str] | None = None) -> int:
    """`stall_detect.py <iter-dir> [--record] [--threshold-min N]`

    An operator surface for the state `dispatch.py`'s reaper already records.
    It exists because the detection was done BY HAND twice in one loop before
    this module was written, and a check nobody can run is a check nobody
    runs.

    READ-ONLY BY DEFAULT, which is the whole posture of this module. Without
    `--record` it lists the agents that WOULD be stamped and writes nothing;
    with `--record` it performs the same single stamp the reaper performs.
    Either way nothing is killed, restarted or committed -- RECORD, DO NOT
    REPAIR (the prime's ruling, hypothesis:l4-stalled-is-a-state-the-harness-
    can-see).
    """
    import argparse

    ap = argparse.ArgumentParser(description=(
        "Detect parents stalled with their round finished: every kid "
        "terminal, the dispatcher-side record still `running` with its mtime "
        "unchanged since spawn, uncommitted work in the worktree, and older "
        "than the threshold. Reports; does not repair."))
    ap.add_argument("iter_dir", help="an iteration dir, e.g. .agi/sessions/iter-L4.78")
    ap.add_argument("--record", action="store_true",
                    help="stamp the label on the records (default: report only)")
    ap.add_argument("--threshold-min", type=int, default=STALL_THRESHOLD_S // 60,
                    help="minutes before a merely slow parent counts as stalled")
    ap.add_argument("--before-work", dest="before_work", action="store_true",
                    help="detect the SIBLING shape instead: parent spawned NO kid, "
                         "record `running`, CLEAN worktree, past threshold")
    args = ap.parse_args(argv)

    itdir = Path(args.iter_dir)
    if not itdir.is_dir():
        print(f"ERR: no such iteration dir: {itdir}", file=sys.stderr)
        return 1
    threshold_s = max(0, args.threshold_min) * 60
    if args.before_work:
        if args.record:
            stamped = record_stalled_before_work_in_iteration(
                itdir, threshold_s=threshold_s)
            for aid in stamped:
                print(f"{STALL_BEFORE_WORK_LABEL} (recorded): {aid}")
            if not stamped:
                print("no stalled-before-work agents")
            return 0
        found = list(scan_iteration_before_work(itdir, threshold_s=threshold_s))
        for aid in found:
            print(f"{STALL_BEFORE_WORK_LABEL} (would record): {aid}")
        if not found:
            print("no stalled-before-work agents")
        return 0
    if args.record:
        stamped = record_stalled_in_iteration(itdir, threshold_s=threshold_s)
        for aid in stamped:
            print(f"stalled (recorded): {aid}")
        if not stamped:
            print("no stalled agents")
        return 0
    found = list(scan_iteration(itdir, threshold_s=threshold_s))
    for aid in found:
        print(f"stalled (would record): {aid}")
    if not found:
        print("no stalled agents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
