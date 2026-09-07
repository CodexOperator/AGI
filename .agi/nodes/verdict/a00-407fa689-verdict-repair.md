---
id: verdict:a00-407fa689-verdict-repair
mint_id: 2d78d95e879f43188ee27c83e514c5d4
type: verdict
parents:
  - hyp:a00-407fa689-verdict-repair
confidence: 0.6
contradicts: []
edited_by: season.py
evidence_runs:
  - exp-a00-407fa689-verdict-repair
season: 1
supports:
  - verdict:a00-407fa689-verdict-pareto
tags:
  - chain-extension
  - repair
  - structural-bias
thought_session: season
title: A00 407fa689 verdict repair
verdict: inconclusive_lean_proved:60
---
# verdict:a00-407fa689-verdict-repair

## Summary

| Metric | Before | After (simulated) |
|---|---|---|
| Orphaned verdicts | 1473 (99.7%) | 1127 (76.3%) |
| Linked to hypothesis | 5 (0.3%) | 351 (23.7%) |
| Repair reduction | — | 23.5% |

## Repair Strategies Used

| Strategy | Count |
|---|---|
| experiment_parent (via next_edges) | 0 |
| domain_match (from verdict ID) | 346 |
| unrepairable | 6 |

## Key Finding

The `experiment_parent` repair strategy failed entirely (0 repairs) because the extend-to-300hop.py script does NOT populate `next_edges` from verdict nodes to their spawning experiments. This confirms the structural bias: synthetic verdict nodes lack both parent hypotheses AND next_edges to their chain context.

The `domain_match` strategy recovers 23.5% by tracing domain names from verdict IDs to base hypotheses (e.g., `verdict:graph-core-extend42` → `hypothesis:graph-core-r1`). However, this is a coarse approximation — extend verdicts should link to specific hypotheses, not always r1.

## Implications

1. **Partial repair is possible but coarse**: domain_match strategy is better than nothing but loses hypothesis granularity.
2. **The experiment_parent strategy requires fixing the extend script**: if extend-to-300hop.py populated `next_edges: ["exp:{domain}-extend{cycle}"]`, repair would be exact.
3. **6 verdicts are unrepairable**: orphan outliers from non-standard naming.
4. **The capillary DAG's parent-child integrity is recoverable** but requires both fixing existing nodes AND fixing the script that creates new ones.

## Verdict

**inconclusive_lean_proved:60** — partial repair works (23.5% orphan reduction) but is too coarse. Full repair requires fixing the extend script to populate parents and next_edges.