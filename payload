#!/usr/bin/env python3
"""plan_master.py — the Plan Master seat's push-further loop (hypothesis:l3w4-plan-master).

The Plan Master seat summons the brief-drafting workflow
(`extensions/agi/workflows/agi-brief-drafting.js`), whose critic returns
`{ok, fixed, left, ...}` — an array of slugs it fixed in place and the slugs it
left. `fixes_per_draft = len(critic.fixed) / len(drafts)` is the seat's
health number: one line per summon, appended to a seat-local log, read back by
`trend`.

## Why a number, not a feeling

The Master layer's promise (owner, L3.33 brief): "...seats aim to get better...
at their jobs." A seat that gets better at summoning the drafting workflow
fixes fewer drafts over time, so `fixes_per_draft` falling is the seat's
improvement signal. `trend --last N` turns the raw log into the one-word
classification the director can act on. The mechanism is deliberately the
Plan Master's own instance of the every-seat push-further idea
(`hypothesis:l3w4-seat-push-further` owns the general machinery; this is only
this seat's version).

Usage:
    plan_master.py record-run --drafts N --fixed N [--iter I] [--log PATH]
    plan_master.py trend --last N [--log PATH] [--tol F]
"""
from __future__ import annotations

import argparse
import json
import sys
import time


DEFAULT_LOG = ".agi/sessions/plan-master/pushfurther.jsonl"


def _default_log(path: str | None) -> str:
    """A --log that names a file wins; otherwise the seat-local default."""
    if path:
        return path
    return DEFAULT_LOG


def record_run(args: argparse.Namespace) -> int:
    """Append one {ts,iter,n_drafts,n_fixed,fixes_per_draft} line per summon."""
    n_drafts = args.drafts
    n_fixed = args.fixed
    if n_drafts <= 0:
        print("record-run: --drafts must be > 0", file=sys.stderr)
        return 2
    if n_fixed < 0:
        print(f"record-run: --fixed must be >= 0, got {n_fixed}", file=sys.stderr)
        return 2
    fixes_per_draft = n_fixed / n_drafts
    record = {
        "ts": args.ts,
        "iter": args.iter,
        "n_drafts": n_drafts,
        "n_fixed": n_fixed,
        "fixes_per_draft": fixes_per_draft,
    }
    path = _default_log(args.log)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")
    return 0


def _load_records(path: str) -> list[dict]:
    records = []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        return []
    return records


def _classify(values: list[float], tol: float) -> str:
    """First-vs-last difference beyond +/-tol reads rising/falling; else flat."""
    if len(values) < 2:
        return "flat"
    delta = values[-1] - values[0]
    if abs(delta) <= tol:
        return "flat"
    if delta > 0:
        return "rising"
    return "falling"


def trend(args: argparse.Namespace) -> int:
    """Read the last N records; report whether fixes_per_draft is rising/falling/flat."""
    path = _default_log(args.log)
    records = _load_records(path)
    tail = records[-args.last:] if args.last > 0 else records
    if not tail:
        print("trend: no records")
        return 1
    values = [float(r["fixes_per_draft"]) for r in tail if "fixes_per_draft" in r]
    if not values:
        print("trend: no fixes_per_draft fields in the last records")
        return 1
    print(_classify(values, args.tol))
    return 0


def main(argv: list[str] | None = None) -> int:
    """Subcommand dispatch; returns a shell exit code."""
    parser = argparse.ArgumentParser(
        prog="plan_master.py",
        description="Plan Master seat push-further loop: record-run + trend.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    rr = sub.add_parser("record-run", help="append one run line to the seat log")
    rr.add_argument("--drafts", type=int, required=True, help="number of drafts this summon")
    rr.add_argument("--fixed", type=int, required=True, help="len(critic.fixed)")
    rr.add_argument("--iter", type=str, default="", help="loop/iteration label for the run")
    rr.add_argument("--ts", type=str, default=None, help="timestamp; defaults to epoch seconds")
    rr.add_argument("--log", type=str, default=None, help="seat-local jsonl path")
    rr.set_defaults(func=record_run)

    tr = sub.add_parser("trend", help="classify fixes_per_draft over the last N runs")
    tr.add_argument("--last", type=int, default=10, help="how many trailing records to read (0 = all)")
    tr.add_argument("--tol", type=float, default=1e-6, help="flat threshold on first-vs-last delta")
    tr.add_argument("--log", type=str, default=None, help="seat-local jsonl path")
    tr.set_defaults(func=trend)

    args = parser.parse_args(argv)
    if getattr(args, "ts", None) is None:
        args.ts = str(int(time.time()))
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())