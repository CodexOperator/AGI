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
import time
from pathlib import Path

import locations  # noqa: E402
from spawn_budget import TERMINAL  # noqa: E402 — the ONE terminal set

#: Default age threshold, seconds (45 minutes). A parent younger than this is
#: merely slow, not stalled. Configurable at every call site.
STALL_THRESHOLD_S = 45 * 60

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