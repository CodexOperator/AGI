#!/usr/bin/env python3
"""telemetry_rollup.py — walk a report node's parent chain, sum descendant
kid/experiment telemetry fields, and attach the sums.

**goal:g16 / hypothesis:l2w6-telemetry-rollup.**

For a given report node (outcome, bigger_outcome, or overview), this script
walks the parent chain to find descendant experiment/kid nodes that carry
telemetry stamps (tokens_in, tokens_out, cost_usd, accepted_bytes), sums
their values, and writes the aggregate onto the report node via write.py.

Walk rules:
- outcome: parents -> verdict -> experiment -> hypothesis -> goal
  Collects telemetry from experiment nodes.
- bigger_outcome: parents -> outcome -> verdict -> experiment
  Collects from experiment nodes reachable through its outcome parents.
- overview: parents -> bigger_outcome -> outcome -> verdict -> experiment
  Collects from experiment nodes reachable through its bigger_outcome parents.

Usage:
    python3 telemetry_rollup.py <report-node-id> [--dry-run] [--root PATH]

    python3 telemetry_rollup.py outcome:a00-c8365a0c-85a6d1
    python3 telemetry_rollup.py --dry-run outcome:a00-c8365a0c-85a6d1
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import locations  # noqa: E402
import node_writer  # noqa: E402
from graph_core.persistence import frontmatter as fm_reader  # noqa: E402

# Cache of graph data per project root: {root_str: (nodes_by_id, children_map)}
_GRAPH_CACHE: dict[str, tuple[dict[str, dict], dict[str, list[str]]]] = {}

#: Telemetry fields this rollup looks for on experiment nodes.
TELEMETRY_FIELDS = ("tokens_in", "tokens_out", "cost_usd", "accepted_bytes")

#: Aggregate fields written back to report nodes.
SUMMARY_FIELDS = (
    "tokens_in_total",
    "tokens_out_total",
    "cost_usd_total",
    "accepted_bytes_total",
    "telemetry_nodes_summed",
    "telemetry_nodes_skipped",
)


def count_aligned_outcomes(root: Path, node_id: str) -> int:
    """Walk the graph from node_id and count outcome nodes with alignment=aligned."""
    nodes_by_id, children_map = _graph_data(root)
    if node_id not in nodes_by_id:
        return 0

    visited: set[str] = set()
    queue: deque[str] = deque([node_id])
    aligned_count = 0

    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)

        fm = nodes_by_id.get(current)
        if fm is None:
            continue

        if fm.get("type") == "outcome" and fm.get("alignment") == "aligned":
            aligned_count += 1

        for parent in _ensure_list(fm.get("parents", [])):
            if parent not in visited:
                queue.append(parent)
        for child in children_map.get(current, []):
            if child not in visited:
                queue.append(child)

    return aligned_count


def _ensure_list(val) -> list[str]:
    """Normalize a parents field into a list of strings."""
    if not val:
        return []
    if isinstance(val, str):
        return [val]
    return [str(item) for item in val]


def _build_graph_index(root: Path) -> tuple[dict[str, dict], dict[str, list[str]]]:
    """Load every node's frontmatter and a parent->children map for traversal."""
    nodes_by_id: dict[str, dict] = {}
    children: dict[str, list[str]] = defaultdict(list)
    nodes_dir = root / "nodes"
    if not nodes_dir.exists():
        return nodes_by_id, children

    for fpath in nodes_dir.rglob("*.md"):
        try:
            nf = fm_reader.load_node_file(fpath, body=False)
        except Exception:
            continue
        fm = nf.frontmatter
        node_id = fm.get("id")
        if not node_id:
            continue
        nodes_by_id[node_id] = fm
        for parent in _ensure_list(fm.get("parents", [])):
            children[parent].append(node_id)
    return nodes_by_id, children


def _graph_data(root: Path) -> tuple[dict[str, dict], dict[str, list[str]]]:
    """Return cached (nodes_by_id, children_map) for the project root."""
    key = str(root.resolve())
    cached = _GRAPH_CACHE.get(key)
    if cached is None:
        cached = _build_graph_index(root)
        _GRAPH_CACHE[key] = cached
    return cached


def _load_node_fm(root: Path, node_id: str) -> dict | None:
    """Load a node's frontmatter from the cached graph index."""
    nodes_by_id, _ = _graph_data(root)
    return nodes_by_id.get(node_id)


def walk_experiments(
    root: Path,
    node_id: str,
) -> list[dict]:
    """Traverse the graph around `node_id` and collect experiment nodes.

    Walks both up (parents) and down (children) so that all experiment nodes
    participating in the plan judged by the report are collected, including
    siblings that share the same parent nodes.
    """
    nodes_by_id, children_map = _graph_data(root)
    if node_id not in nodes_by_id:
        return []

    experiments: list[dict] = []
    visited: set[str] = set()
    queue: deque[str] = deque([node_id])

    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)

        fm = nodes_by_id.get(current)
        if fm is None:
            continue

        if fm.get("type") == "experiment":
            experiments.append(fm)

        for parent in _ensure_list(fm.get("parents", [])):
            if parent not in visited:
                queue.append(parent)
        for child in children_map.get(current, []):
            if child not in visited:
                queue.append(child)

    return experiments


def collect_telemetry(
    experiment_fms: list[dict],
) -> tuple[dict[str, int | float], int, int]:
    """Sum telemetry fields across experiment frontmatter dicts.

    Returns (sums, nodes_summed, nodes_skipped).
    - sums: {tokens_in_total: X, tokens_out_total: Y, cost_usd_total: Z,
             accepted_bytes_total: W}
    - nodes_summed: count of experiment nodes that had at least one telemetry field
    - nodes_skipped: count of experiment nodes that had ALL telemetry fields absent
    """
    telemetry_keys = {"tokens_in", "tokens_out", "cost_usd", "accepted_bytes"}
    sums: dict[str, int | float] = {
        "tokens_in_total": 0,
        "tokens_out_total": 0,
        "cost_usd_total": 0,
        "accepted_bytes_total": 0,
    }
    nodes_summed = 0
    nodes_skipped = 0

    for fm in experiment_fms:
        has_any = False
        for key in telemetry_keys:
            val = fm.get(key)
            if val is not None:
                if key == "cost_usd":
                    sums["cost_usd_total"] += float(val)
                elif key == "accepted_bytes":
                    sums["accepted_bytes_total"] += int(val)
                elif key == "tokens_in":
                    sums["tokens_in_total"] += int(val)
                elif key == "tokens_out":
                    sums["tokens_out_total"] += int(val)
                has_any = True
        if has_any:
            nodes_summed += 1
        else:
            nodes_skipped += 1

    return sums, nodes_summed, nodes_skipped


def format_ratios(sums: dict[str, int | float]) -> str:
    """Format ratio metrics for display.

    - bytes_per_token = accepted_bytes_total / (tokens_in_total + tokens_out_total) when nonzero
    - bytes_per_dollar = accepted_bytes_total / cost_usd_total when nonzero
    """
    tokens_total = sums.get("tokens_in_total", 0) + sums.get("tokens_out_total", 0)
    bytes_total = sums.get("accepted_bytes_total", 0)
    cost_total = sums.get("cost_usd_total", 0)

    parts = []
    if tokens_total and bytes_total:
        parts.append(f"bytes_per_token={bytes_total / tokens_total:.4f}")
    if cost_total and bytes_total:
        parts.append(f"bytes_per_dollar={bytes_total / cost_total:.4f}")

    return ", ".join(parts) if parts else "no ratios computable"


def do_rollup(root: Path, report_id: str, *, dry_run: bool = False) -> dict:
    """Run one telemetry rollup and return the results.

    Returns a dict with keys: node_id, type, sums, nodes_summed, nodes_skipped,
    ratios, write_results (None if dry_run).
    """
    fm = _load_node_fm(root, report_id)
    if fm is None:
        return {"error": f"report node {report_id} not found"}

    node_type = fm.get("type", "")
    if node_type not in ("outcome", "bigger_outcome", "overview"):
        return {"error": f"{report_id} is type={node_type!r}, expected outcome|bigger_outcome|overview"}

    experiments = walk_experiments(root, report_id)

    # De-duplicate by node id.
    seen: set[str] = set()
    unique_experiments: list[dict] = []
    for efm in experiments:
        nid = efm.get("id", "")
        if nid not in seen:
            seen.add(nid)
            unique_experiments.append(efm)

    sums, nodes_summed, nodes_skipped = collect_telemetry(unique_experiments)

    aligned_outcomes_count = count_aligned_outcomes(root, report_id)
    cost_total = sums.get("cost_usd_total", 0)
    cost_per_aligned: float | None = None
    if cost_total and aligned_outcomes_count:
        cost_per_aligned = cost_total / aligned_outcomes_count

    result = {
        "node_id": report_id,
        "type": node_type,
        "experiments_found": len(unique_experiments),
        "nodes_summed": nodes_summed,
        "nodes_skipped": nodes_skipped,
        "aligned_outcomes_count": aligned_outcomes_count,
        "cost_per_aligned_outcome": cost_per_aligned,
        "sums": sums,
        "ratios": format_ratios(sums),
    }

    if dry_run:
        result["write_results"] = None
        result["dry_run"] = True
        return result

    # Attach the sums to the report node via node_writer.
    set_fm = {
        "tokens_in_total": sums["tokens_in_total"],
        "tokens_out_total": sums["tokens_out_total"],
        "cost_usd_total": sums["cost_usd_total"],
        "accepted_bytes_total": sums["accepted_bytes_total"],
        "telemetry_nodes_summed": nodes_summed,
        "telemetry_nodes_skipped": nodes_skipped,
    }

    write_res = node_writer.update_node(root, report_id, set_fm=set_fm)
    status = write_res.status.upper() if isinstance(write_res.status, str) else write_res.status
    result["write_results"] = {
        "status": status,
        "reason": write_res.reason,
    }

    return result


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    import argparse

    ap = argparse.ArgumentParser(
        description="Telemetry roll-up: sum descendant experiment telemetry "
                    "onto a report node.")
    ap.add_argument("report_id", help="node id of the report node (outcome|bigger_outcome|overview)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print what would be written without writing")
    ap.add_argument("--root", default=".",
                    help="any path inside the project (default: cwd)")
    ap.add_argument("--json", action="store_true",
                    help="output as JSON for machine consumption")
    args = ap.parse_args(argv)

    root = locations.find_project_root(Path(args.root).resolve())
    if root is None:
        print(f"ERR: not an agi project: {args.root}", file=sys.stderr)
        return 1

    result = do_rollup(root, args.report_id, dry_run=args.dry_run)

    error = result.get("error")
    if error:
        print(f"ERR: {error}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print(f"Report: {result['node_id']} (type={result['type']})")
    print(f"  experiment nodes found: {result['experiments_found']}")
    print(f"  nodes summed:           {result['nodes_summed']}")
    print(f"  nodes skipped (no data):{result['nodes_skipped']}")
    print(f"  sums:")
    for k, v in result['sums'].items():
        print(f"    {k}: {v}")
    print(f"  ratios: {result['ratios']}")
    cpa = result.get('cost_per_aligned_outcome')
    aligned_count = result.get('aligned_outcomes_count', 0)
    print(f"  aligned outcomes:     {aligned_count}")
    if cpa is not None:
        print(f"  cost_per_aligned_outcome: ${cpa:.6f}")
    else:
        print(f"  cost_per_aligned_outcome: n/a")
    if args.dry_run:
        print(f"  (dry run — nothing written)")
    elif result.get("write_results"):
        wr = result["write_results"]
        print(f"  write: {wr['status']} — {wr['reason']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())