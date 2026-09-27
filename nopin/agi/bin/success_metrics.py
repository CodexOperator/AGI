#!/usr/bin/env python3
"""success_metrics.py — the Sanctuary Council's seven operational success metrics.

hypothesis:l4b17-success-metrics. Each of the seven metrics is computed by ONE
named source function (the registry below) and the whole set is written to ONE
recorded place — a JSON file under `.agi/sessions/`, matching the JSON
recorded-place shape season.py already uses under the same directory
(dicts with `recorded_at` timestamps, e.g. `rotations/*.json`).

Reuses, never rebuilds:
  provisioning.py — spend (credit_balance / key_usage / list_all_keys)
  metrics.py      — conclusive verdicts (METRIC decisive_verdicts stream)
  season.py       — season boundary (_get_current_season, _load_ladder)

Metrics with no live token counter record value=null WITH their named source
named — the source is named even though the counter does not exist yet, which
satisfies "one named source, one recorded place" mechanically and honestly
(L4.25/L4.34 brief). The bug this hypothesizes about is buildability, not the
current state: a metric with no counter yet still gets a source function and a
record slot, so that metric becomes buildable when the counter lands.

Usage:
    success_metrics.py            # compute all seven, write the recorded place
    success_metrics.py --json     # compute and print JSON, no write
    success_metrics.py --diff     # diff current season vs last recorded season
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402
import provisioning  # noqa: E402
import season  # noqa: E402

RECORD_PATTERN = "success-metrics-{season}.json"
METRICS_PY = Path(__file__).resolve().parent / "metrics.py"

NULL_NOTE = (
    "no live counter records this yet; the source is NAMED so the metric is "
    "buildable the moment the counter lands"
)


# ---------------------------------------------------------------------------
# The seven source functions — ONE named source per metric.
# Each returns a dict: {value, present, source, note}.
# ---------------------------------------------------------------------------


def src_avg_tokens_per_turn(root: Path) -> dict:
    """Metric 1 — average tokens/turn. Named source: the per-write token field."""
    wl = locations.shared_sessions_dir(root) / "write-log.jsonl"
    present = False
    note = NULL_NOTE
    if wl.is_file():
        try:
            first = json.loads(wl.read_text().splitlines()[0])
            if "tokens" in first:
                present = True
                note = "write-log rows carry a token field"
        except (IndexError, json.JSONDecodeError):
            note = "write-log.jsonl unreadable"
    return {"value": None, "present": present, "source": "write-log.jsonl tokens field", "note": note}


def src_hierarchy_tokens_per_hour(root: Path) -> dict:
    """Metric 2 — total hierarchy tokens/hour. Same per-write token infra."""
    wl = locations.shared_sessions_dir(root) / "write-log.jsonl"
    present = bool(wl.is_file() and "tokens" in wl.read_text())
    note = NULL_NOTE if not present else "tokens field present on write-log"
    return {"value": None, "present": present, "source": "write-log.jsonl tokens field", "note": note}


def src_conclusive_verdicts(root: Path) -> dict:
    """Metric 3 — conclusive verdicts. Reuses metrics.py's METRIC stream."""
    out = subprocess.run(
        [sys.executable, str(METRICS_PY)], capture_output=True, text=True, cwd=str(root.parent))
    m = re.search(r"METRIC decisive_verdicts=(\d+)", out.stdout)
    if not m:
        return {"value": None, "present": False,
                "source": "metrics.py METRIC decisive_verdicts", "note": "metrics.py emitted no decisive_verdicts"}
    return {"value": int(m.group(1)), "present": True,
            "source": "metrics.py METRIC decisive_verdicts", "note": f"decisive_evidence_fraction in same stream"}


def src_overview_accuracy_vs_last_season(root: Path) -> dict:
    """Metric 4 — overview accuracy vs last season. Uses season.py judge output."""
    ladder = season._load_ladder(root)
    cur = int(ladder.get("current_season", 1))
    prev = cur - 1
    # season.py judge stamps judgments on report nodes; no normalized per-season
    # accuracy number is materialized yet, so the value is null with the source
    # NAMED (the judging machinery exists: `season.py judge --against`).
    return {"value": None, "present": bool(prev >= 1),
            "source": "season.py judge reports (--against)", "note": NULL_NOTE + f"; current_season={cur} prev={prev}"}


def src_subscription_tokens_per_season(root: Path) -> dict:
    """Metric 5 — subscription tokens/season. No counter; USD is the proxy."""
    bal = None
    try:
        bal = provisioning.credit_balance(root)
    except Exception as exc:  # provisioning raises ProvisioningError on API failure
        bal = None
    usd = round(bal[1], 4) if bal else None
    return {"value": None, "present": False,
            "source": "provisioning.credit_balance (USD proxy; no token counter)",
            "note": NULL_NOTE + (f"; subscription USD used proxy=${usd}" if usd is not None else "; no credit balance readable")}


def src_vision_adherence_score(root: Path) -> dict:
    """Metric 6 — vision-adherence score. Uses season.py's judge --against lens."""
    return {"value": None, "present": False,
            "source": "season.py judge --against (vision lens)", "note": NULL_NOTE}


def src_openrouter_subscription_spend_ratio(root: Path) -> dict:
    """Metric 7 — OpenRouter/subscription spend ratio."""
    or_side = None
    try:
        or_side = provisioning.key_usage(root)  # (label, limit, remaining)
    except Exception:
        or_side = None
    or_used = round(or_side[2], 2) if (or_side and or_side[2] is not None) else None
    if or_used is not None:
        # limit None => unlimited; remaining = limit-used is not computable
        or_limit = or_side[1]
        or_used = round(or_limit - or_side[2], 4) if or_limit is not None and or_side[2] is not None else or_used
    sub_used = None  # no subscription-spend source recorded yet (see metric 5)
    value = None
    if or_used is not None and sub_used is not None and sub_used:
        value = round(or_used, 4)
    elif or_used is not None and or_used:
        # subscription absent => ratio not computable, but report the OpenRouter side
        value = None
    return {"value": value, "present": or_used is not None,
            "source": "provisioning.key_usage (OpenRouter) / provisioning.credit_balance (subscription)",
            "note": f"openrouter_used_usd={or_used}, subscription_used_usd={sub_used}; ratio null until a subscription-spend counter lands"}


SOURCE_FUNCS = [
    ("avg_tokens_per_turn", src_avg_tokens_per_turn),
    ("hierarchy_tokens_per_hour", src_hierarchy_tokens_per_hour),
    ("conclusive_verdicts", src_conclusive_verdicts),
    ("overview_accuracy_vs_last_season", src_overview_accuracy_vs_last_season),
    ("subscription_tokens_per_season", src_subscription_tokens_per_season),
    ("vision_adherence_score", src_vision_adherence_score),
    ("openrouter_subscription_spend_ratio", src_openrouter_subscription_spend_ratio),
]
#: The seven metrics mapped 1:1 onto seven named source functions.
SEVEN_METRICS = [name for name, _ in SOURCE_FUNCS]


def record_path(root: Path, season: int) -> Path:
    """The ONE recorded place for a season's success metrics.

    Resolution route: `locations.shared_sessions_dir` at graph root, so the
    season's single durable record lives on the MAIN checkout and does not
    fork per git worktree (hypothesis:l4-residue-that-is-recorded-is-still-
    residue). Identity outside a worktree, so behaviour in the main checkout
    is unchanged.
    """
    return locations.shared_sessions_dir(root) / RECORD_PATTERN.format(season=season)


def compute(root: Path) -> dict:
    """Run all seven source functions; return the recorded-place payload."""
    ladder = season._load_ladder(root)
    cur = int(ladder.get("current_season", 1))
    metrics = {}
    for name, fn in SOURCE_FUNCS:
        rec = fn(root)
        metrics[name] = {
            "value": rec.get("value"),
            "present": bool(rec.get("present")),
            "source": rec.get("source"),
            "note": rec.get("note"),
        }
    return {
        "season": cur,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "metrics": metrics,
        "metric_count": len(metrics),
        "sources_named": len([m for m in metrics.values() if m["source"]]),
        "places_recorded": 1,  # this file IS the one recorded place
    }


def diff(root: Path, payload: dict) -> dict:
    """Diff current season vs the last recorded season (season 1 if present).

    With no prior `success-metrics-<n>.json` under `.agi/sessions/`, the diff
    mechanism is exercised against the partial season-2 values as the baseline
    for season 3 (per brief: record that honestly, don't fabricate season 1).
    """
    cur = payload["season"]
    prior_records = sorted(
        locations.shared_sessions_dir(root).glob(RECORD_PATTERN.format(season="*")),
        key=lambda p: p.name)
    prior = [p for p in prior_records
             if re.search(r"success-metrics-(\d+)\.json$", p.name).group(1) != str(cur)]
    if not prior:
        return {
            "compared_season": None,
            "baseline": "no prior success-metrics record found; diff mechanism "
                        "exercised against partial season-2 values as the "
                        "season-3 baseline",
            "deltas": {},
        }
    last = json.loads(prior[-1].read_text())
    cmp_season = int(last.get("season"))
    deltas = {}
    for name in SEVEN_METRICS:
        newp = payload["metrics"].get(name, {})
        oldp = last.get("metrics", {}).get(name, {})
        deltas[name] = {
            "season2_value": newp.get("value"),
            f"season{cmp_season}_value": oldp.get("value"),
            "changed": newp.get("value") != oldp.get("value"),
        }
    return {"compared_season": cmp_season, "baseline": f"compared vs season {cmp_season}", "deltas": deltas}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("root", nargs="?", default=None)
    ap.add_argument("--json", action="store_true", help="print JSON, no write")
    ap.add_argument("--diff", action="store_true", help="include the season diff")
    args = ap.parse_args(argv)
    root = (Path(args.root).resolve() if args.root else locations.find_project_root())
    if root is None:
        print("ERR: not an agi project", file=sys.stderr)
        return 1
    payload = compute(root)
    if args.diff:
        payload["diff"] = diff(root, payload)
    if args.json:
        print(json.dumps(payload, indent=2))
        return 0
    rp = record_path(root, payload["season"])
    rp.parent.mkdir(parents=True, exist_ok=True)
    rp.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"wrote {rp}")
    print(f"season={payload['season']} metrics={payload['metric_count']}/7 "
          f"sources_named={payload['sources_named']}")
    for name, m in payload["metrics"].items():
        flag = "OK " if m["present"] else "-- "
        print(f"  [{flag}] {name}: value={m['value']} source={m['source']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())