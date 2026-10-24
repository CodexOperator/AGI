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
import os
import re
import subprocess
import sys
import time
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


def _write_log_has_tokens_field(wl: Path) -> bool:
    """goal:g3.8 R1: True when a write-log ROW carries a `tokens` FIELD. The rows are
    parsed, never substring-searched: a node-id slug such as `...first-prose-tokens`
    or a note value naming the word is not a counter."""
    try:
        with wl.open(encoding="utf-8", errors="replace") as fh:
            for ln in fh:
                try:
                    row = json.loads(ln)
                except ValueError:
                    continue
                if isinstance(row, dict) and "tokens" in row:
                    return True
    except OSError:
        return False
    return False


def src_hierarchy_tokens_per_hour(root: Path) -> dict:
    """Metric 2 — total hierarchy tokens/hour. Same per-write token infra."""
    wl = locations.shared_sessions_dir(root) / "write-log.jsonl"
    present = bool(wl.is_file() and _write_log_has_tokens_field(wl))
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


#: The graph counters metrics.py prints as `METRIC k=v`, in the order the line carries them.
LINE_GRAPH_KEYS = (
    "node_count", "active_node_count", "deprecated_node_count", "edge_count",
    "evidence_fraction", "decisive_verdicts", "decisive_evidence_fraction",
    "broken_links", "thought_coverage", "longest_chain_length", "outcome_coverage")


def _reason(exc: BaseException | str) -> str:
    """A FIXED code that can sit inside UNMEASURED(...) on one line, never exception text: an exception's text can
    hold an absolute box path, and the line is pushed. The exception class, plus errno / exit code where there is
    one; anything that is not an exception is never echoed."""
    if not isinstance(exc, BaseException):
        return "unknown"
    name = type(exc).__name__
    code = getattr(exc, "errno", None) if not isinstance(exc, SystemExit) else exc.code
    return f"{name} {code}" if isinstance(code, int) and not isinstance(code, bool) else name


def _run_metrics_once(root: Path) -> tuple[dict, str | None]:
    """ONE metrics.py run (about a minute live): (METRIC map, why it is dead or None)."""
    try:
        out = subprocess.run([sys.executable, str(METRICS_PY), str(root)],
                             capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return {}, "metrics.py timeout"
    except OSError as exc:
        return {}, f"metrics.py unrunnable {_reason(exc)}"
    if out.returncode != 0:
        return {}, f"metrics.py rc={out.returncode}"
    found = {}
    for ln in out.stdout.splitlines():
        if ln.startswith("METRIC ") and "=" in ln:
            k, _, v = ln[7:].strip().partition("=")
            found[k] = v.split()[0] if v.split() else ""
    return found, None


#: goal:g3.8 R4: these two sources ask OpenRouter (provisioning.credit_balance /
#: key_usage, up to two authenticated 30 s GETs) and their value is always null, so the
#: hourly --line names them statically instead of calling out and discarding the answer.
LINE_NO_NETWORK = ("subscription_tokens_per_season", "openrouter_subscription_spend_ratio")


# ---------------------------------------------------------------------------
# goal:g7.16.1.11.46.5 (M4): the intake segment and the TRAJECTORY line, read from
# the cards' §7 ATOMS rows -- the ONE writer of metrics_line stays this --line.
# ---------------------------------------------------------------------------

LAP_SECONDS = 14400   # one lap = 4 h, the cadence of the Prime's digest / CHECK (agi-atom stamps lap<n> with the same unit)
_S7 = re.compile(r"^## (?:\S+ )?§7(?!\d)")
_ATOM_ID = re.compile(r"^(a\d+|\d+\.\d+)$")
_BOLD = re.compile(r"^\*\*(.+?)\*\*\s*$")   # a card's `**throw 1 (10-22) -- ...**` line names the section the rows below it belong to


def current_lap() -> int:
    """The lap number now (AGI_LAP overrides, as it does for agi-atom)."""
    env = os.environ.get("AGI_LAP", "")
    return int(env) if env.isdigit() else int(time.time() // LAP_SECONDS)


def card_atoms(card: Path) -> list[tuple[str, str, int | None, str]]:
    """(id, state, lap, section) for every §7 row of a card (section = the text of the last
    standalone `**...**` line above the row, "" before any): the agi-atom form
    `| a<n> | "<slice>" | src:<..> | <state> | lap<n> |` and the legacy
    `| 1.1 | <text> | <state> |` (no lap: its age is unknown, never red, counted apart as `?`)."""
    try:
        text = card.read_text(encoding="utf-8")
    except OSError:
        return []
    rows, in7, sect = [], False, ""
    for ln in text.splitlines():
        if ln.startswith("## "):
            in7, sect = bool(_S7.match(ln)), ""
            continue
        if in7 and (b := _BOLD.match(ln)):
            sect = b.group(1)
            continue
        if not in7 or not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if not cells or not _ATOM_ID.match(cells[0]):
            continue
        m = re.fullmatch(r"lap(\d+)", cells[-1]) if len(cells) == 5 else None
        if len(cells) == 5 and m and cells[2].startswith("src:"):
            rows.append((cells[0], cells[3], int(m.group(1)), sect))
        elif len(cells) >= 3:
            rows.append((cells[0], cells[-1], None, sect))
    return rows


def _cards(root: Path) -> list[tuple[str, Path]]:
    """(post, card) for each quorum card with a §7, one per resolved file."""
    q, seen, out = root / "sessions" / "quorum", set(), []
    for f in sorted(q.glob("*.md")) if q.is_dir() else []:
        real = f.resolve()
        if real in seen or not real.is_file():
            continue
        seen.add(real)
        out.append((f.stem, real))
    return out


def intake_counts(rows: list[tuple[str, str, int | None, str]], lap: int) -> tuple[int, int, int, int]:
    """(open, placed, red, unknown): open = state target:..., placed = any other state,
    red = open and older than one lap (stamped lap n with lap - n > 1), unknown = open with
    NO lap (a legacy row: its age cannot be told, so it is never red and never hidden)."""
    op = sum(1 for _, st, _, _ in rows if st.startswith("target:"))
    red = sum(1 for _, st, lp, _ in rows if st.startswith("target:") and lp is not None and lap - lp > 1)
    unk = sum(1 for _, st, lp, _ in rows if st.startswith("target:") and lp is None)
    return op, len(rows) - op, red, unk


def intake_segment(root: Path) -> str:
    """`intake: <post>=<open>/<placed>/<red>[/?<unknown-age open>] ...` for every post whose card has a §7;
    no quorum dir = UNMEASURED (a wrong root is named, never "none")."""
    if not (root / "sessions" / "quorum").is_dir():
        return "intake: UNMEASURED(no quorum dir)"
    lap = current_lap()
    parts = []
    for post, card in _cards(root):
        rows = card_atoms(card)
        if rows:
            op, placed, red, unk = intake_counts(rows, lap)
            parts.append(f"{post}={op}/{placed}/{red}" + (f"/?{unk}" if unk else ""))
    return "intake: " + (" ".join(parts) if parts else "none")


_LEAF_STATE = re.compile(r"^leaf:(?:goal:)?(g[0-9][0-9.]*)")


def trajectory_line(root: Path, post: str, label: str, throws: str = "") -> str:
    """One TRAJECTORY line for a throw ingested into <post>'s card §7:
    `<label> atoms=<n> placed=<k> -> <leaf ids>`. THROWS is a section-heading prefix: only the rows
    under the card's `**<prefix>...**` lines are the throw's (a later ask has its own line); empty = every row."""
    rows = [r for r in card_atoms(root / "sessions" / "quorum" / f"{post}.md") if r[3].startswith(throws)]
    placed = intake_counts(rows, current_lap())[1]
    leaves = sorted({m.group(1) for _, st, _, _ in rows if (m := _LEAF_STATE.match(st))})
    return f"{label} atoms={len(rows)} placed={placed} \u2192 {' '.join(leaves) if leaves else 'none'}"


def trajectory_segment(root: Path) -> str:
    """goal:g7.16.1.11.46.5 T2: one `| trajectory: <line>` per throw REGISTERED in the town node's
    `trajectory_throws` cell (`  - {"post": .., "label": .., "throws": <heading prefix>}`), re-rendered by this
    ONE writer on every cell write, never pasted. No cell = no segment; an unreadable one is NAMED."""
    node = root / "nodes" / "town" / "local-maxxing.md"
    try:
        text = node.read_text(encoding="utf-8")
    except OSError:
        return ""
    head = text.split("\n---", 1)[0] if text.startswith("---") else ""
    lines, on, regs = head.splitlines(), False, []
    try:
        for ln in lines:
            if ln.startswith("trajectory_throws:"):
                on = True
                continue
            if on and ln.startswith("  - {"):
                regs.append(json.loads(ln[4:]))
            elif on:
                break
        return " ".join(f"| trajectory: {trajectory_line(root, r['post'], r['label'], r.get('throws', ''))}" for r in regs)
    except Exception as exc:  # noqa: BLE001 -- a metrics line is never fatal
        return f"| trajectory: UNMEASURED(registered throws unreadable: {_reason(exc)})"


def p1_segment(root: Path) -> str:
    """goal:g7.16.1.11.46.9 Q3: the `| p1: <model> $/landed=.. s/landed=.. red=<r>/<n>` segments, one per arm in
    the committed results file (p1_ab.py writes the file and never this line).

    `root` is the REPO root or the graph dir `<repo>/.agi` (the CLI's find_project_root returns the latter): the
    repo is resolved ONCE and used for the config AND the repo-relative results path. No `.agi/config.json`, no
    `p1` cell (another project) or no results file yet = NO segment; a file that exists and cannot be read or
    rendered is NAMED, not dropped."""
    repo = locations.repo_root(Path(root))
    cfg_path = repo / ".agi" / "config.json"
    if not cfg_path.is_file():
        return ""
    try:
        import json  # noqa: PLC0415
        import p1_ab  # noqa: PLC0415
        cfg = json.loads(cfg_path.read_text())
        if not isinstance(cfg.get("p1"), dict):
            return ""
        results = p1_ab.read_results(repo, cfg)
        return "" if results is None else p1_ab.render_segment(results, cfg)
    except Exception as exc:  # noqa: BLE001 -- a metrics line is never fatal
        return f"| p1: UNMEASURED(results unreadable: {_reason(exc)})"


def make_line(root: Path) -> str:
    """goal:g3.8 -- ONE line: a UTC minute, the graph counters and the seven success
    metrics. A null is NAMED (UNMEASURED(reason)), never a number the engine does not
    have; an absent counter is named, not dropped; a dead metrics.py is named with its
    rc in every key. metrics.py runs ONCE; conclusive_verdicts is read from that stream."""
    found, dead = _run_metrics_once(root)

    def graph(k: str) -> str:
        if dead:
            return f"UNMEASURED({dead})"
        return found[k] if found.get(k) else "UNMEASURED(absent from metrics.py)"

    parts = []
    for name, fn in SOURCE_FUNCS:
        if name == "conclusive_verdicts":
            parts.append(f"{name}={graph('decisive_verdicts')}")
            continue
        if name in LINE_NO_NETWORK:
            parts.append(f"{name}=UNMEASURED(no source yet)")
            continue
        try:
            rec = fn(root)
        except (Exception, SystemExit) as exc:   # a source that cannot run is named, not fatal
            parts.append(f"{name}=UNMEASURED(source failed: {_reason(exc)})")
            continue
        if rec.get("value") is not None:
            parts.append(f"{name}={rec['value']}")
        else:
            parts.append(f"{name}=UNMEASURED("
                         f"{'no live counter' if rec.get('present') else 'no source yet'})")
    when = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    g = " ".join(f"{k}={graph(k)}" for k in LINE_GRAPH_KEYS)
    line = f"{when} graph: {g} | success: {' '.join(parts)}"
    seg = p1_segment(root)
    line = f"{line} {seg}" if seg else line
    seg = trajectory_segment(root)
    line = f"{line} {seg}" if seg else line
    return f"{line} | {intake_segment(root)}"   # intake stays LAST: goal:g7.16.1.11.46.5 "ends `| intake:`"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("root", nargs="?", default=None)
    ap.add_argument("--line", action="store_true",
                    help="print ONE line for the town node's graph_metrics cell, no write")
    ap.add_argument("--trajectory", nargs=2, metavar=("POST", "LABEL"),
                    help="print ONE TRAJECTORY line for the throw ingested into POST's card §7, no write")
    ap.add_argument("--throws", default="", metavar="HEADING_PREFIX",
                    help="with --trajectory: count only the rows under the card's **<prefix>...** sections")
    ap.add_argument("--json", action="store_true", help="print JSON, no write")
    ap.add_argument("--diff", action="store_true", help="include the season diff")
    args = ap.parse_args(argv)
    root = (Path(args.root).resolve() if args.root else locations.find_project_root())
    if root is None:
        print("ERR: not an agi project", file=sys.stderr)
        return 1
    if args.line:
        print(make_line(root))
        return 0
    if args.trajectory:
        print(trajectory_line(root, *args.trajectory, throws=args.throws))
        return 0
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