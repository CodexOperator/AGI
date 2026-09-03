---
id: exp:exp:a00-204c9d9e-1d958f
mint_id: 046c80b309264adf83950e4470413c23
type: experiment
parents:
  - hyp:a00-204c9d9e-1d958f
next_edges:
  - verdict:verdict:a00-204c9d9e-1d958f
title: Exp:a00 204c9d9e 1d958f
---
# exp:exp:a00-204c9d9e-1d958f

## What Was Run

`exp-query-api-r1.py` — tests all 4 Query API functions against the live 933-node graph.

## Implementation

`src/chain_engine/query_api.py` — new module with 4 functions:
1. `task_attractiveness(task_id)` — scores tasks based on parent hypothesis chain signal
2. `chain_gaps(domain)` — finds hypotheses in a domain with no verdict yet
3. `next_best_hypothesis(graph, weights, n)` — top-N hypotheses ranked by chain-progress
4. `coverage_report(graph)` — per-domain node-type counts

Key fixes:
- `_build_outgoing(graph)` builds outgoing edges map from graph.edges (not node.children which is always empty)
- Handles `hyp:` prefix in hypothesis IDs for chain_gaps regex
- Handles `exp:` prefix in experiment_child detection
- Uses frontmatter `parents` field for task→hypothesis parent links

## Results

- Graph loaded: 933 nodes, 923 edges
- Q1 task_attractiveness: 94 tasks scored, 1 non-zero (most raw hypotheses have no graph edges — expected)
- Q2 chain_gaps: 44 total gaps across 5 domains (hypotheses without verdict children)
- Q3 next_best_hypothesis: 5 top hypotheses returned with scores
- Q4 coverage_report: 9 domains, 933 nodes (82.2% coverage)

## Metrics

- coverage_pct: 82.2
- domains_covered: 9
- hypotheses_scored: 94
- total_gaps: 44

## Outcome

All 4 queries operational. No crashes. 272 tests pass.