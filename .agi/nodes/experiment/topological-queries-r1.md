---
id: exp:topological-queries-r1
mint_id: 7b86e35c43104608adf670651ea92ba6
type: experiment
parents:
  - hyp:a00-c2d7dbcc-3987c7
next_edges:
  - verdict:topological-queries-r1
confidence: 0.65
edited_by: season.py
season: 1
spawns: []
status: completed
tags:
  - experiment
  - topology
  - query-api
thought_session: season
title: exp:topological-queries-r1
---
# exp:topological-queries-r1

**Hypothesis:** `hyp:a00-c2d7dbcc-3987c7`
**Status:** completed
**Date:** 2026-05-01

## Method

1. Load 999-node graph (reconstruct_next_edges=True)
2. Implement 4 topological ranking functions in `src/graph_core/topological_queries.py`:
   - `completion_ratio()` — proved verdict nodes / verifiable nodes
   - `unresolved_density()` — unresolved hypotheses / total hypotheses
   - `chain_length_score()` — BFS longest path via 'next' edges
   - `cycle_depth_max()` — max verdict→experiment→verdict cycles
3. `rank_ideas()` composite score = unresolved×0.4 + (1-completion)×0.3 + norm_chain×0.3
4. Compare topological ranking vs 13-item expert ground truth

## Results

- Graph: 999 nodes, 821 edges
- Match@7 = 100% (all 7 expert domains in topological top-7)
- Match@5 = 40% (2/5 top-K match)
- Spearman ρ = 0.604 (moderate positive)
- top5_avg_order_diff = 3.4

## Verdict

`inconclusive_lean_proved:65` — topology works as coarse filter, insufficient for fine-grained priority.