#!/usr/bin/env python3
"""failures.py — derive an idempotent per-agent failure ledger from session
artifacts and report failure rates by seat/model/role/harness.

**goal:g16 / hypothesis:l3w4-agent-failure-ledger.** Master Sensei's first
reader: a measured table of how often each agent fails, so the Sensei homes
in on improvement targets from data rather than recollection.

Closed failure categories (one row per event, per agent):

- died               status `failed` | `hung-unhealed` on agent.json
- demoted            agent.json carries `demoted_from` / `demote_reason`
- rejected           output.log contains `EVIDENCE-GATE REJECTED` (exit 2,
                     nothing written)
- overclaim          `iter-*/review/results.json` reports `overclaims>0`
- broken_frontmatter write-log.jsonl `operation=="repair-frontmatter"`
- session_limit      output.log's last line is a subscription-limit result
- wrong_file         output.log shows a `write_guard` `WARN unsanctioned
                     write:` — the agent hand-edited a node instead of
                     routing the edit through the sanctioned writer
- no_build_probe_only agent.json `verdict=="pending"` at done

`unadmitted` slots never count — no agent ran, there is no dir to read.

Rows are keyed `sha256(agent_id + category + detail)` for idempotent
append: `ledger` derives rows from the artifacts and appends only the
ones whose key is not already in the ledger file, so an immediate rerun
appends zero rows. `rates` reads the ledger file and groups per axis;
per-axis counts must sum to the total row count.

Usage:
    python3 failures.py ledger <root> [--since ITER] [--out PATH] [--write-node ID]
    python3 failures.py rates  <root> --by model|role|harness [--in PATH]

`--write-node` lands the merged table as a build node's payload via
`write.py`, the only sanctioned writer (this module never calls
node_writer itself). The target build node (build:g16-failure-ledger,
parents [mvp:g16-failure-ledger]) is minted by the mvp job — until it
exists, `--write-node` reports that it is absent and does not fail on
the file landing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402

# Closed failure categories.
CATEGORIES = (
    "died",
    "demoted",
    "rejected",
    "overclaim",
    "broken_frontmatter",
    "session_limit",
    "wrong_file",
    "no_build_probe_only",
)

#: agent.json statuses that count as a died agent.
DIED_STATUSES = {"failed", "hung-unhealed"}

#: Default ledger file, relative to a project root's sessions dir.
DEFAULT_LEDGER = "failure-ledger.json"

#: Aggregated rate table (`sensei.pick_worst` shape), written by `sensei`.
DEFAULT_RATES = "failure-rates.json"

_ERR_MSG = re.compile(r"EVIDENCE-GATE REJECTED")
_WARN_MSG = re.compile(r"WARN unsanctioned write:\s+(\S+)")
_MODEL_RE = re.compile(r"--model\s+['\"]?([^'\"\s]+)")
_ROLE_RE = re.compile(r"You are (PARENT|parent|KID|kid|agent)\b", re.IGNORECASE)


def _row_key(agent_id: str, category: str, detail: str) -> str:
    blob = f"{agent_id}\u0000{category}\u0000{detail}"
    return hashlib.sha256(blob.encode("utf-8", "replace")).hexdigest()


def _iter_sortable(iter_id) -> tuple:
    """Numeric iterations sort before dotted-season ones; both among
    themselves numerically."""
    if isinstance(iter_id, int):
        return (0, iter_id)
    m = re.search(r"(\d+)", str(iter_id))
    # iter-L3.28 -> L3.28-like; use a stable numeric-ish key.
    parts = re.findall(r"\d+", str(iter_id))
    return (1, [int(p) for p in parts], str(iter_id))


def _derive_model(rec: dict) -> str:
    m = _MODEL_RE.search(str(rec.get("command", "")))
    return m.group(1) if m else ""


def _derive_role(rec: dict) -> str:
    m = _ROLE_RE.search(str(rec.get("command", "")))
    if m:
        return m.group(1).lower()
    return str(rec.get("tier") or "")


def _iteration_rows(root: Path, iter_id) -> list[dict]:
    """Rows for one iteration directory, from its per-agent json/artifacts."""
    itdir = locations.iteration_dir(root, iter_id)
    if not itdir.is_dir():
        return []
    out: list[dict] = []
    iter_str = str(iter_id)

    # Per-agent dirs: agent.json is the authoritative record; skip manifest,
    # logs, review, `.lock` and anything without an agent record.
    for adir in sorted(itdir.iterdir()):
        if not adir.is_dir():
            continue
        if adir.name.startswith(".") or adir.name.startswith("p-"):
            continue
        aj = adir / "agent.json"
        if not aj.exists():
            continue
        try:
            rec = json.loads(aj.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if not isinstance(rec, dict):
            continue
        # unadmitted / bare scaffold: no id or never got a terminal status
        # and no node record -> no failure evidence to count.
        aid = str(rec.get("id") or "")
        status = str(rec.get("status") or "")
        base = {
            "agent_id": aid,
            "iter": iter_str,
            "tier": str(rec.get("tier") or ""),
            "role": _derive_role(rec),
            "model": _derive_model(rec),
            "harness": str(rec.get("harness") or ""),
            "target": str(rec.get("target") or ""),
            "node_id": str(rec.get("node_id") or ""),
            "source_path": str(aj),
            "ts": int(rec.get("started_at") or rec.get("finished_at") or time.time()),
        }

        def emit(category: str, detail: str) -> None:
            row = dict(base)
            row["category"] = category
            row["detail"] = detail
            row["_key"] = _row_key(aid, category, detail)
            out.append(row)

        # died
        if status in DIED_STATUSES:
            emit("died", status)
        # demoted
        if rec.get("demoted_from") or rec.get("demote_reason"):
            emit("demoted", str(rec.get("demote_reason") or rec.get("demoted_from") or ""))
        # no_build_probe_only
        if str(rec.get("verdict") or "").strip().lower() == "pending":
            emit("no_build_probe_only", "verdict pending at done")

        # rejected / wrong_file / session_limit from output.log
        olog = adir / "output.log"
        if olog.exists():
            text = olog.read_text(encoding="utf-8", errors="replace")
            if _ERR_MSG.search(text):
                emit("rejected", "EVIDENCE-GATE REJECTED")
            for m in _WARN_MSG.finditer(text):
                emit("wrong_file", m.group(1))
            lim = _scan_session_limit(olog)
            if lim:
                emit("session_limit", lim)

    # overclaim from the iteration-level review results.json
    rsum = _scan_overclaims(itdir)
    if rsum:
        out.append({
            "agent_id": "",
            "iter": iter_str, "tier": "", "role": "", "model": "",
            "harness": "", "target": "",
            "node_id": "",
            "category": "overclaim",
            "detail": rsum,
            "source_path": str(itdir / "review" / "results.json"),
            "ts": int(time.time()),
            "_key": _row_key("overclaim", "overclaim", rsum),
        })
    return out


def _scan_session_limit(olog: Path) -> str | None:
    """output.log's last non-empty line is a `session_limit` result."""
    try:
        lines = [l for l in olog.read_text(encoding="utf-8", errors="replace")
                 .splitlines() if l.strip()]
    except OSError:
        return None
    if not lines:
        return None
    last = lines[-1]
    low = last.lower()
    if "session_limit" in low:
        return "session_limit"
    try:
        ev = json.loads(last)
    except json.JSONDecodeError:
        return None
    if isinstance(ev, dict) and ev.get("subtype") == "session_limit":
        return "session_limit"
    if isinstance(ev, dict) and ev.get("type") == "result" and "limit" in low:
        return str(ev.get("reset_time") or "session_limit")
    return None


def _scan_overclaims(itdir: Path) -> str | None:
    """Check `iter-*/review/results.json` (bug-master output) for overclaims>0."""
    rj = itdir / "review" / "results.json"
    if not rj.exists():
        return None
    try:
        data = json.loads(rj.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    total = 0
    if isinstance(data, list):
        for entry in data:
            oc = _oc_of(entry)
            if oc:
                total += oc
    elif isinstance(data, dict):
        # may wrap {"reviews":[...]} or carry a top-level overclaims summary
        for entry in data.get("reviews", [data]):
            oc = _oc_of(entry)
            if oc:
                total += oc
        oc = _oc_of(data)
        if oc and not data.get("reviews"):
            total = max(total, oc)
    return f"overclaims={total}" if total else None


def _oc_of(entry: dict) -> int:
    try:
        return int(entry.get("overclaims") or 0)
    except (TypeError, ValueError):
        return 0


def _broken_frontmatter_rows(root: Path, since) -> list[dict]:
    """Rows from sessions/write-log.jsonl for `repair-frontmatter` ops."""
    wl = Path(root) / locations.SESSIONS_DIR_NAME / "write-log.jsonl"
    if not wl.exists():
        return []
    out: list[dict] = []
    agent_by_node: dict[str, dict] = {}
    # Index agent records across iterations by node_id and by agent id so the
    # repair row can be attributed to the agent that caused it.
    for iid in locations.list_iterations(root):
        itdir = locations.iteration_dir(root, iid)
        for adir in itdir.glob("*/agent.json"):
            try:
                rec = json.loads(adir.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            if isinstance(rec, dict) and rec.get("node_id"):
                agent_by_node[str(rec["node_id"])] = rec
                if rec.get("id"):
                    agent_by_node[str(rec["id"])] = rec
    with wl.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(ev, dict) or ev.get("operation") != "repair-frontmatter":
                continue
            node_id = str(ev.get("node_id") or "")
            rec = agent_by_node.get(node_id)
            aid = str(rec.get("id") or "") if rec else (node_id or "unknown")
            detail = str(ev.get("path") or node_id)
            out.append({
                "agent_id": aid,
                "iter": "",
                "tier": str(rec.get("tier") or "") if rec else "",
                "role": _derive_role(rec) if rec else "",
                "model": _derive_model(rec) if rec else "",
                "harness": str(rec.get("harness") or "") if rec else "",
                "target": str(rec.get("target") or "") if rec else "",
                "node_id": node_id,
                "category": "broken_frontmatter",
                "detail": detail,
                "source_path": str(wl),
                "ts": int(time.time()),
                "_key": _row_key(aid, "broken_frontmatter", detail),
            })
    return out


def derive_rows(root: Path, since: str | None = None) -> list[dict]:
    """All derived failure rows for a project root, newest iteration first.

    `since` is an inclusive iteration id that narrows the walk to that
    iteration and newer. The write-log (broken_frontmatter rows) is not
    iteration-scoped, so `since` applies to it only as a soft floor: an
    absent or unknown `since` includes it unconditionally. The key is what
    makes the whole exercise idempotent, so the walk order is cosmetic.
    """
    rows: list[dict] = []
    iters = locations.list_iterations(root)
    iters.sort(key=_iter_sortable, reverse=True)
    for iid in iters:
        if since and str(since) != str(iid):
            continue
        rows.extend(_iteration_rows(root, iid))
    rows.extend(_broken_frontmatter_rows(root, since))
    return rows


def _load_ledger(path: Path) -> tuple[list[dict], set[str]]:
    if not path.exists():
        return [], set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return [], set()
    if not isinstance(data, list):
        return [], set()
    keys = {str(r.get("_key", "")) for r in data if isinstance(r, dict) and r.get("_key")}
    return [r for r in data if isinstance(r, dict)], keys


def ledger(root: Path, since=None, out_path: Path | None = None,
           write_node: str | None = None) -> tuple[list[dict], int, int]:
    """Append only new rows to the ledger file. Returns (new_rows, total, appended)."""
    session_dir = Path(root) / locations.SESSIONS_DIR_NAME
    out = out_path or (session_dir / DEFAULT_LEDGER)
    existing, keys = _load_ledger(out)
    new = [r for r in derive_rows(root, since) if r.get("_key") not in keys]
    existing.extend(new)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    if write_node:
        _land_via_write(root, write_node, new, out)
    return new, len(existing), len(new)


def _land_via_write(root: Path, write_node: str, new_rows: list[dict],
                    out_path: Path) -> None:
    """Land the merged table as a build node's payload via the sanctioned
    writer. The build node is minted by the mvp job; absent it, we report."""
    # Re-read the full merged ledger so `payload -` carries the whole table.
    merged, _ = _load_ledger(out_path)
    text = json.dumps(merged, indent=2)
    cmd = [sys.executable, str(Path(__file__).resolve().parent / "write.py"),
           write_node, "payload -"]
    try:
        proc = subprocess.run(cmd, cwd=str(root), input=text,
                              capture_output=True, text=True, timeout=60)
    except (subprocess.SubprocessError, OSError) as exc:
        print(f"WARN: --write-node land failed ({write_node}): {exc}",
              file=sys.stderr)
        return
    if proc.returncode != 0:
        print(f"WARN: write.py could not land payload on {write_node} "
              f"(not yet minted by the mvp job?): {proc.stderr.strip()}",
              file=sys.stderr)


def aggregate(rows: list[dict], by: str = "role") -> list[dict]:
    """Compress raw per-event failure rows into the rate-table shape that
    `sensei.pick_worst` groups on.

    Every ledger row *is* a failure event, so there is no separate run count
    to divide by here; `failed` is the count of failure rows in a group and
    `fail_rate` is that group's share of all failure rows. Each output row
    carries `seat_or_role` (the grouped axis value), `model`, `failed` and
    `fail_rate` — the exact four keys pick_worst reads.
    """
    from collections import defaultdict
    groups: dict[tuple[str, str], int] = defaultdict(int)
    for r in rows:
        seat = str(r.get(by) or r.get("role") or r.get("agent_id") or "?")
        model = str(r.get("model") or "")
        groups[(seat, model)] += 1
    total = sum(groups.values()) or 1
    out: list[dict] = []
    for (seat, model), cnt in sorted(groups.items()):
        out.append({
            "seat_or_role": seat,
            "model": model,
            "failed": cnt,
            "fail_rate": round(cnt / total, 4),
        })
    return out


def rates(root: Path, by: str, in_path: Path | None = None) -> tuple[dict[str, int], int, bool]:
    """Group ledger rows by axis; return (counts, total, sum_matches)."""
    session_dir = Path(root) / locations.SESSIONS_DIR_NAME
    src = in_path or (session_dir / DEFAULT_LEDGER)
    rows, _ = _load_ledger(src)
    counts: dict[str, int] = {}
    total = 0
    for r in rows:
        val = str(r.get(by, "") or "?")
        counts[val] = counts.get(val, 0) + 1
        total += 1
    ok = sum(counts.values()) == total and (counts or not rows)
    return counts, total, ok


def _cmd_ledger(args) -> int:
    root = Path(args.root).resolve()
    out = Path(args.out) if args.out else None
    new, total, appended = ledger(root, args.since, out, args.write_node)
    print(f"{appended} rows appended ({len(new)} new of {total} total)")
    return 0 if appended >= 0 else 1


def _cmd_sensei(args) -> int:
    """Aggregate the raw ledger into the rate table sensei.pick_worst reads,
    written as a JSON array to `<sessions>/failure-rates.json` by default.
    """
    root = Path(args.root).resolve()
    session_dir = Path(root) / locations.SESSIONS_DIR_NAME
    src = Path(args.in_path) if args.in_path else (session_dir / DEFAULT_LEDGER)
    rows, _ = _load_ledger(src)
    table = aggregate(rows, args.by)
    out = Path(args.out) if args.out else (session_dir / DEFAULT_RATES)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(table, indent=2), encoding="utf-8")
    print(f"wrote {len(table)} rate rows ({sum(r['failed'] for r in table)} "
          f"failure events) -> {out}")
    return 0 if table else 2


def _cmd_rates(args) -> int:
    root = Path(args.root).resolve()
    in_path = Path(args.in_path) if args.in_path else None
    counts, total, ok = rates(root, args.by, in_path)
    for k in sorted(counts):
        print(f"{k}: {counts[k]}")
    print(f"TOTAL: {total}")
    if not ok:
        print(f"ERR: per-axis counts do not sum to total ({total})",
              file=sys.stderr)
        return 2
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="failures.py", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("ledger", help="derive and append new failure rows")
    pl.add_argument("root")
    pl.add_argument("--since", default=None)
    pl.add_argument("--out", default=None)
    pl.add_argument("--write-node", default=None)
    pl.set_defaults(fn=_cmd_ledger)

    pr = sub.add_parser("rates", help="per-axis failure counts")
    pr.add_argument("root")
    pr.add_argument("--by", choices=("model", "role", "harness"), required=True)
    pr.add_argument("--in", dest="in_path", default=None)
    pr.set_defaults(fn=_cmd_rates)

    ps = sub.add_parser("sensei", help="write the rate table pick_worst reads")
    ps.add_argument("root")
    ps.add_argument("--by", choices=("role", "model", "harness", "agent_id"),
                    default="role")
    ps.add_argument("--in", dest="in_path", default=None)
    ps.add_argument("--out", default=None)
    ps.set_defaults(fn=_cmd_sensei)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())