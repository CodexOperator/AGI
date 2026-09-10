#!/usr/bin/env python3
"""reconciler.py — NO AUTHORITY EVER RECONCILES A RECORD AGAINST REALITY.

**hypothesis:l4-the-reconciler-one-root-three-faces.** Three stall shapes,
one root cause: an agent record lies because nothing ever checks it against
the process table. (1) kids terminal, parent staged, no commit — `stall_
detect.py` already sees it; (2) no kid spawned, nothing changed, parent
burning — undetected; (3) kid DEAD, its record still `running`, parent polls
forever — a pi process died on a 404, its `agent.json` still read
`status: running` two minutes after the pid was confirmed dead. A detector
per shape is N detectors and the fourth shape is already out there. ONE
reconciler makes all three of them queries over a corpus that stopped lying:
one pass over an iteration's agent records that compares RECORDED status
against PROCESS LIVENESS and DERIVES the truth.

THE ONE-WAY RULE, the whole safety argument:
  a pid that is NOT alive PROVES the process is not running;
  a pid that IS alive proves NOTHING, because pids are reused.
Derive terminal from a DEAD pid only; NEVER derive `running` from a live one.
A reconciler that trusts liveness in both directions will eventually
resurrect a corpse under a recycled pid, and that failure is silent and
unreproducible — the worst kind this project has.

The derived status is named `hung-dead` — DISTINCTLY from any actor-reported
one, in the same family and the same convention as `done-unreported` (which
the reaper derives, L4.67). `hung-dead` is NEVER written by an actor; it is
only EVER derived here. `_AGENT_STATUS_RANK` already resolves inferred
statuses by content (`done-unreported`), so an inferred status must not
masquerade as a reported one; distinct-by-name is the enforcement of that.
It is a NEW name, absent from `_AGENT_STATUS_RANK`, so nothing ever ranks it
against a reported one by accident.

RECONCILE, DO NOT REPAIR: nothing is killed, restarted or committed, and
nothing derived enters `spawn_budget.TERMINAL` by side effect. `hung-dead`
IS DEFENDED here as terminal, explicitly, not slipped in: a process whose
pid is dead is by definition not running — it can never reacquire its lease,
never poll, never finish, never simplify its record. The dead pid has also
already let `spawn_budget` reclaim its lease (a lease outlives its holder by
construction), so the corrected record merely agrees with a budget that has
already moved on. It is declared in `DERIVED_TERMINAL_SET` here, and it is
the caller's deliberate choice whether that set joins `spawn_budget.TERMINAL`.

THE POLL-LOOP TIMEOUT IS NOT THIS ROUND. A parent that polls forever should
also time out — a kid can be alive and WEDGED, which no reconciler ever
catches — but that belt is second and must not become the fix. Left here,
unbelted, on purpose.

CITES `goal:g17.1` §6 item 74: a `--detach` kid is invisible to
`spawn_budget.py status` and reparents to init when its wrapper dies — the
BUDGET-visibility face of this same construction. `iter-L4.85`'s kid is the
COMPLETION-visibility face: `status: running`, pid dead, in the frozen
artifact at `.agi/worktrees/a00-e9572046/.agi/sessions/iter-L4.85/`.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import locations  # noqa: E402
from spawn_budget import TERMINAL, _pid_alive  # noqa: E402 — both ONE definitions


#: The DERIVED terminal status. Named DIFFERENTLY from any actor-reported
#: status, in the family of `done-unreported` (an inferred, not reported,
#: ending). Only this module ever produces it; no actor writes it.
DERIVED_TERMINAL = "hung-dead"

#: `hung-dead` IS terminal, defended here where it is declared rather than
#: slipped into `spawn_budget.TERMINAL` by side effect — see module docstring.
#: Kept as its own frozenset so the caller can opt the set (or a union with
#: `TERMINAL`) into whatever reader needs the correction, visibly and
#: reviewably, instead of this module mutating the ONE shared set.
DERIVED_TERMINAL_SET = frozenset({DERIVED_TERMINAL})


def reconcile_record(record, *, pid_alive=None) -> str:
    """Derived truth for ONE record. Returns the DERIVED status where the
    recorded one is a lie; otherwise the recorded status, UNCHANGED.

    ONE-WAY, and only dead pids move anything: a NON-TERMINAL record whose
    pid is DEAD is derived to `hung-dead` (a dead pid PROVES the process
    stopped). A LIVE pid proves NOTHING, so a live-pid record is left exactly
    as reported, on both sides: a record saying `running` for a live pid is
    left alone (liveness changes nothing, (d)), and a record saying `done`
    for a live pid is left alone (the inference never runs the other
    way, (c)). An already-terminal record (`done`, `failed`, ...) is left as
    reported regardless of its pid — `done` is the actor speaking for itself
    and outranks any inference, so reconciling it toward anything would
    WEAKEN the record, never strengthen it.

    READ-ONLY: returns a status string, writes no record, kills nothing,
    restarts nothing, commits nothing.
    """
    pid_alive = pid_alive or _pid_alive
    recorded = str((record or {}).get("status") or "")
    if recorded in TERMINAL:
        # Already terminal: nothing to reconcile. `done` reports the ending;
        # a dead pid adds nothing and a live pid proves nothing, so the
        # recorded truth stands (c).
        return recorded
    if recorded != "running":
        # Unknown or sentinel status: touch nothing. Inferring a truth from a
        # status we do not recognise is how a corpus starts lying again.
        return recorded
    try:
        pid = int(record.get("pid") or 0)
    except (TypeError, ValueError):
        pid = 0
    if pid <= 0:
        # No pid to check — liveness proves nothing, so change nothing.
        return recorded
    if not pid_alive(pid):
        # DEAD pid PROVES the process stopped. The record said `running`; the
        # reality is terminal. One-way: this is the ONLY direction inference
        # may travel.
        return DERIVED_TERMINAL
    # LIVE pid proves NOTHING. Leave the record exactly as reported — neither
    # confirming nor contradicting `running` (d).
    return recorded


def reconcile_iteration(iter_dir, *, pid_alive=None) -> list[tuple[str, str, str]]:
    """One pass over an iteration's agent records -> `(id, recorded, derived)`
    triples where the DERIVED truth differs from the recorded one.

    Reads each live `agent.json` (never the manifest copy — a stale manifest
    line cannot hide a corrected record); reconciliation NEVER WRITES. The
    returned list is exactly the set of records that are lying about their
    process. READ-ONLY: no record is modified, nothing killed, restarted or
    committed.
    """
    itdir = Path(iter_dir)
    manifest_path = itdir / "manifest.json"
    if not manifest_path.exists():
        return []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    agents = manifest.get("agents", [])
    corrected: list[tuple[str, str, str]] = []
    for entry in agents:
        aid = str((entry or {}).get("id") or "")
        if not aid:
            continue
        rec_path = itdir / aid / "agent.json"
        try:
            rec = json.loads(rec_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            # An unreadable record is not evidence of a live or dead process;
            # leave it out rather than guess.
            continue
        recorded = str(rec.get("status") or "")
        derived = reconcile_record(rec, pid_alive=pid_alive)
        if derived != recorded:
            corrected.append((aid, recorded, derived))
    return corrected


def main(argv: list[str] | None = None) -> int:
    """`reconciler.py <iter-dir> [--style status]`

    An operator surface for the reconciler: list which of an iteration's agent
    records lie about a dead process. READ-ONLY REPORT BY DEFAULT — this
    module's one posture is RECONCILE, DO NOT REPAIR, so there is no
    `--write` flag to reach for; the correction is a derived status for a
    reader to consume, not a mutation this process performs.

    The whole design in one line for an operator who just ran it: a `running`
    record whose pid is dead is not evidence of a stalled-but-alive agent; it
    is a corpse the corpus is still counting.
    """
    import sys as _sys

    _sys.path.insert(0, str(Path(__file__).resolve().parent))
    import locations as _loc  # noqa: E402

    ap = argparse.ArgumentParser(description=(
        "Derive the truth of an iteration's agent records against the process "
        "table. One-way: a DEAD pid proves the process stopped; a LIVE pid "
        "proves nothing. Reports the correction; repairs nothing, kills "
        "nothing, commits nothing."))
    ap.add_argument("iter_dir", help="an iteration dir, e.g. .agi/sessions/iter-L4.85")
    ap.add_argument("--style", choices=["status", "ids"], default="status",
                    help="report all recorded/derived statuses, or just the ids")
    args = ap.parse_args(argv)

    itdir = Path(args.iter_dir)
    if not itdir.is_dir():
        print(f"ERR: no such iteration dir: {itdir}", file=_sys.stderr)
        return 1
    corrected = reconcile_iteration(itdir)
    if not corrected:
        print("reconciled: every record agrees with the process table")
        return 0
    for aid, recorded, derived in corrected:
        if args.style == "ids":
            print(f"{aid}:{derived}")
        else:
            print(f"  {aid}  recorded={recorded!r}  derived={derived!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())