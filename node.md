---
id: hyp:a00-b43be286-f3ca7b
mint_id: 0c46891cf89e4183a3fa7802d9fbb160
type: hypothesis
parents: []
next_edges: []
domain: graph-topology
edited_by: season.py
season: 1
tags:
  - topology
  - chain-completion
  - attractor-regions
  - density
  - statistical-test
thought_session: season
title: Topology attractor regions predict chain completion
---
# hyp:a00-b43be286-f3ca7b

**Domain:** graph-topology
**Type:** hypothesis

# hyp:a00-b43be286-f3ca7b
## Hypothesis

The autoresearch DAG's topological structure (branching density, convergence zones, attractor regions) is a statistically significant predictor of chain completion — chains that fall within high-density attractor regions (many incoming edges, high fan-in) are disproportionately likely to reach verdict status, while isolated or sparse-region chains are disproportionately likely to remain as pending tasks.

## Test

1. Compute topological metrics per node: fan-in, fan-out, clustering coefficient, betweenness centrality approximation (BFS depth from hubs).
2. Label each task node as `completed` (verdict exists) or `pending` (no verdict).
3. Bin task nodes by their topological region density (dense / medium / sparse).
4. Compute completion rate per bin. Chi-square or Fisher exact test for significance at α=0.05.

## Would prove it

Completion rate in dense regions ≥ 2× completion rate in sparse regions, with p < 0.05.

## Would disprove it

No significant difference in completion rates across density bins (p ≥ 0.05), OR sparse-region chains complete at higher rates.

## Evidence

- Script: `python3 - <<'EOF'` computing BFS-based fan-in/fan-out per task node, density binning, Fisher exact test.
- Input: graph built from existing nodes on disk.
- Output: table of density-bins vs completed/pending counts, p-value.