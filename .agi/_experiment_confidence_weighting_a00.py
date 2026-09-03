#!/usr/bin/env python3
"""Compute confidence-weighted goal fulfillment vs. binary outcome_coverage.

Goal: test hypothesis:a00-ee08875d-df7a60 claims:
1. At least one active goal has confidence_weighted_score >0.2 lower
   than per_goal_outcome_coverage (binary mvps/hypotheses).
2. At least one goal has M/G > 0 but confidence_weighted_score < 0.05.
3. Global confidence_weighted_outcome_coverage strictly lower than
   global outcome_coverage by at least 0.05.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path


def safe_yaml_load(text: str) -> dict:
    try:
        import yaml
        return yaml.safe_load(text) or {}
    except Exception:
        return {}


def load_nodes(nodes_dir: Path) -> dict:
    """Return {node_id: {type, parents, confidence, status, verdict}}."""
    nodes = {}
    for nf in sorted(nodes_dir.rglob("*.md")):
        text = nf.read_text()
        if not text.startswith("---"):
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        fm = safe_yaml_load(parts[1])
        if not isinstance(fm, dict):
            continue
        nid = fm.get("id", "")
        if not isinstance(nid, str) or not nid.strip():
            continue
        parents = fm.get("parents", [])
        parents = [p.strip() for p in parents if isinstance(p, str) and p.strip()]
        nodes[nid] = {
            "type": fm.get("type", ""),
            "parents": parents,
            "confidence": fm.get("confidence", 0.5),
            "status": (fm.get("status") or "").strip(),
            "verdict": (fm.get("verdict") or "").strip(),
        }
    return nodes


def walk_to_goal(nid: str, nodes: dict) -> set:
    """Walk parent chain upward to find all reachable goal ids."""
    seen = {nid}
    stack = list(nodes.get(nid, {}).get("parents", []))
    goals = set()
    while stack:
        cur = stack.pop()
        if cur in seen:
            continue
        seen.add(cur)
        nd = nodes.get(cur)
        if nd is None:
            continue
        if nd["type"] == "goal":
            goals.add(cur)
            continue
        stack.extend(nd.get("parents", []))
    return goals


def find_hyp_ancestor(nid: str, nodes: dict) -> tuple[str | None, float]:
    """Find the nearest hypothesis ancestor and its confidence.

    BFS along parent chain. Returns (hypothesis_id, confidence).
    """
    seen = {nid}
    stack = list(nodes.get(nid, {}).get("parents", []))
    while stack:
        cur = stack.pop()
        if cur in seen:
            continue
        seen.add(cur)
        nd = nodes.get(cur)
        if nd is None:
            continue
        if nd["type"] == "hypothesis":
            c = nd.get("confidence")
            return cur, c if c is not None else 0.5
        stack.extend(nd.get("parents", []))
    return None, 0.5


SCORING_STATUSES = frozenset({"active", "horizon", "complete"})
RETIRED_STATUSES = frozenset({"retired", "phasing-out"})


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    nodes_dir = root / ".agi" / "nodes"
    if not nodes_dir.is_dir():
        nodes_dir = root / "nodes"
    if not nodes_dir.is_dir():
        print(f"ERR: no nodes/ dir under {root}", file=sys.stderr)
        sys.exit(1)

    nodes = load_nodes(nodes_dir)

    # === Build goal index ===
    goal_status = {}
    for nid, nd in nodes.items():
        if nd["type"] == "goal":
            goal_status[nid] = nd.get("status", "active") or "active"

    # For the scoring-compatible version, replicate goal_attribution logic:
    # hypotheses and mvps attributed to each goal by parent-chain walking.
    # A hypothesis belongs to a goal if walking its parents reaches that goal.

    # Step 1: Map each non-goal node to all goals reachable via parents
    node_to_goals = {}
    for nid, nd in nodes.items():
        if nd["type"] == "goal":
            continue
        node_to_goals[nid] = walk_to_goal(nid, nodes)

    # Step 2: Group hypotheses and mvps by goal
    hyp_by_goal = defaultdict(set)  # goal -> {hypothesis ids}
    mvp_by_goal = defaultdict(set)  # goal -> {mvp ids}
    unattributed_hyps = 0
    unattributed_mvps = 0

    for nid, nd in nodes.items():
        if nd["type"] == "hypothesis":
            gs = node_to_goals.get(nid, set())
            # Per metrics.py scoring: a node with no goals keeps scoring
            # (conservative). Also skip retired-only attribution.
            if not gs:
                unattributed_hyps += 1
            for g in gs:
                if goal_status.get(g) in SCORING_STATUSES:
                    hyp_by_goal[g].add(nid)
        elif nd["type"] == "mvp":
            gs = node_to_goals.get(nid, set())
            if not gs:
                unattributed_mvps += 1
            for g in gs:
                if goal_status.get(g) in SCORING_STATUSES:
                    mvp_by_goal[g].add(nid)

    # Orphan mvps: mvps with no goal attribution at all
    orphan_mvp_ids = {
        nid for nid, nd in nodes.items()
        if nd["type"] == "mvp" and not node_to_goals.get(nid, set())
    }
    orphan_mvp_hypothesis_chains = {}
    for mid in orphan_mvp_ids:
        h, c = find_hyp_ancestor(mid, nodes)
        if h:
            orphan_mvp_hypothesis_chains[mid] = (h, c)

    # === Compute per-goal scores ===
    goals_with_hyps = sorted(
        [(g, hyps) for g, hyps in hyp_by_goal.items() if len(hyps) > 0],
        key=lambda x: -len(x[1]),
    )

    results = []
    global_mvps = 0
    global_hyps = 0
    global_conf_weight = 0.0

    for gid, hyps in goals_with_hyps:
        mvps = mvp_by_goal.get(gid, set())

        # Find hypotheses that actually have mvp descendants in this goal
        mvped_hyps = set()
        hyp_conf_sum = 0.0
        for m in mvps:
            h_id, conf = find_hyp_ancestor(m, nodes)
            if h_id and h_id in hyps:
                mvped_hyps.add(h_id)
                hyp_conf_sum += conf

        hyp_count = len(hyps)
        mvp_count = len(mvps)
        binary_ratio = mvp_count / max(hyp_count, 1)
        # confidence_weighted_score(G) = sum(confidence(h) for each mvp-linked hyp) / |H_G|
        weighted_score = hyp_conf_sum / max(hyp_count, 1)
        gap = binary_ratio - weighted_score
        gap_pct = gap / max(binary_ratio, 0.001) if binary_ratio > 0 else 0.0

        results.append({
            "goal": gid,
            "status": goal_status.get(gid, "?"),
            "hyp_count": hyp_count,
            "mvp_count": mvp_count,
            "binary_ratio": round(binary_ratio, 4),
            "conf_weighted_score": round(weighted_score, 4),
            "gap": round(gap, 4),
            "gap_pct": round(gap_pct * 100, 1),
            "mvped_hyp_count": len(mvped_hyps),
            "mvped_conf_sum": round(hyp_conf_sum, 3),
            "mvp_ids": sorted(mvps),
        })

        global_mvps += mvp_count
        global_hyps += hyp_count
        global_conf_weight += hyp_conf_sum

    # Global scores
    global_binary = global_mvps / max(global_hyps, 1)
    global_weighted = global_conf_weight / max(global_hyps, 1)
    global_gap = global_binary - global_weighted

    # === Orphan mvps (no goal attribution) ===
    orphan_mvps_with_hyp = []
    orphan_mvps_no_hyp = []
    for mid in orphan_mvp_ids:
        h, c = find_hyp_ancestor(mid, nodes)
        if h:
            orphan_mvps_with_hyp.append((mid, h, c))
        else:
            orphan_mvps_no_hyp.append(mid)

    # === REPORT ===
    print("=" * 72)
    print("CONFIDENCE-WEIGHTED GOAL FULFILLMENT ANALYSIS")
    print("=" * 72)
    print(f"Total goals: {len(goal_status)}")
    print(f"  active: {sum(1 for s in goal_status.values() if s == 'active')}")
    print(f"  horizon: {sum(1 for s in goal_status.values() if s == 'horizon')}")
    print(f"  complete: {sum(1 for s in goal_status.values() if s == 'complete')}")
    print(f"  retired: {sum(1 for s in goal_status.values() if s in RETIRED_STATUSES)}")
    print(f"Total hypotheses: {len([n for n,nd in nodes.items() if nd['type'] == 'hypothesis'])}")
    print(f"Total mvps: {len([n for n,nd in nodes.items() if nd['type'] == 'mvp'])}")
    print()
    print(f"Attributed hypotheses (scoring goals): {global_hyps}")
    print(f"  unattributed (no goal in chain): {unattributed_hyps}")
    print(f"Attributed mvps (scoring goals): {global_mvps}")
    print(f"  unattributed (no goal in chain): {unattributed_mvps}")
    print(f"  unattributed but with hyp chain: {len(orphan_mvps_with_hyp)}")
    print(f"  unattributed no hyp chain: {len(orphan_mvps_no_hyp)}")
    print()

    print("GLOBAL SCORES:")
    print(f"  outcome_coverage (binary): {round(global_binary, 4)}")
    print(f"  confidence_weighted_score: {round(global_weighted, 4)}")
    print(f"  gap: {round(global_gap, 4)}")
    print()

    print("PER-GOAL SCORES (sorted by gap descending):")
    print(f"{'Goal':20s} {'Status':12s} {'Hyps':6s} {'Mvps':6s} {'Binary':8s} "
          f"{'ConfWt':8s} {'Gap':8s} {'Gap%':7s} {'MvpdHyp':7s}")
    print("-" * 88)
    for r in sorted(results, key=lambda x: -x["gap"]):
        print(f"{r['goal']:20s} {r['status']:12s} {r['hyp_count']:6d} {r['mvp_count']:6d} "
              f"{r['binary_ratio']:8.4f} {r['conf_weighted_score']:8.4f} "
              f"{r['gap']:8.4f} {r['gap_pct']:6.1f}% {r['mvped_hyp_count']:7d}")
    print()

    # === HYPOTHESIS CLAIMS ===
    print("=" * 72)
    print("CLAIM CHECK")
    print("=" * 72)

    # Claim 1: at least one active goal has gap > 0.2
    claim1 = False
    claim1_detail = []
    for r in results:
        if r["status"] == "active" and r["gap"] > 0.2:
            claim1 = True
            claim1_detail.append(r)
    print(f"\nClaim 1: active goal with conf_weighted >0.2 below binary?")
    if claim1:
        print(f"  ✓ PASS — {len(claim1_detail)} active goal(s) exceed 0.2 gap")
        for r in claim1_detail:
            print(f"    {r['goal']}: binary={r['binary_ratio']:.4f}, "
                  f"conf_wt={r['conf_weighted_score']:.4f}, gap={r['gap']:.4f}")
    else:
        max_gap_active = max((r["gap"] for r in results if r["status"] == "active"), default=0)
        print(f"  ✗ FAIL — max gap among active goals: {max_gap_active:.4f}")

    # Claim 2: at least one goal with M/G > 0 but conf_weighted < 0.05
    claim2 = False
    for r in results:
        if r["mvp_count"] > 0 and r["conf_weighted_score"] < 0.05:
            claim2 = True
            print(f"\nClaim 2: goal with mvps>0 but conf_weighted <0.05?")
            print(f"  ✓ PASS — {r['goal']}: mvps={r['mvp_count']}, "
                  f"binary={r['binary_ratio']:.4f}, conf_wt={r['conf_weighted_score']:.4f}")
            break
    if not claim2:
        print(f"\nClaim 2: goal with mvps>0 but conf_weighted <0.05?")
        print(f"  ✗ FAIL — no such goal found")

    # Claim 3: global weighted < global binary by at least 0.05
    claim3 = global_gap >= 0.05
    print(f"\nClaim 3: global gap ≥ 0.05?")
    if claim3:
        print(f"  ✓ PASS — gap={round(global_gap, 4)}")
    else:
        print(f"  ✗ FAIL — gap={round(global_gap, 4)}")

    print()

    # === ORPHAN MVP ANALYSIS ===
    if orphan_mvps_with_hyp:
        print(f"Orphan mvps WITH hypothesis chain (would contribute to conf_weighted if goal-attributed):")
        for mid, h, c in orphan_mvps_with_hyp:
            print(f"  {mid}: hyp={h}, conf={c}")
    print()

    print(f"METRIC primary_metric=global_gap")
    print(f"METRIC primary_value={round(global_gap, 4)}")
    print(f"METRIC global_binary={round(global_binary, 4)}")
    print(f"METRIC global_confidence_weighted={round(global_weighted, 4)}")


if __name__ == "__main__":
    main()