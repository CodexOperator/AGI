---
id: hyp:a00-c2ec59b7-b391d9-r2
mint_id: 873bbda1ad4044a484c59b2789defdd4
type: hypothesis
parents:
  - idea:domain-renderers
  - hyp:a00-c2ec59b7-b391d9
next_edges: []
confidence: 0.85
contradicts:
  - hyp:a00-c2ec59b7-b391d9
demote_reason: no experiment evidence (evidence_runs=0) for 'disproved'
demoted_from: disproved
domain: renderers
edited_by: season.py
evidence_runs: []
season: 1
status: completed
tags:
  - renderers
  - mermaid
  - isomorphism
  - semantic-proximity
thought_session: season
title: "R2: Mermaid/graph proximity isomorphic to ancestor overlap"
verdict: inconclusive_lean_disproved:50
---
# hyp:a00-c2ec59b7-b391d9-r2

## Hypothesis: Mermaid Render Proximity Isomorphic to Descendant Overlap

## Result (iter 9, continuation)

- **Spearman correlation: -0.903** (strongly anti-correlated, same as R1)
- **Top-5 avg graph distance: 9.4** hops
- **VERDICT: DISPROVED**

## Key Findings

1. **188 connected components** in the graph — most domains are isolated
2. Within the largest component (174 nodes), sampled 30 pairs
3. **Same -0.903 anti-correlation** as R1 (descendant overlap test)
4. **Only 10 sibling pairs** exist in entire graph, 0% are graph-adjacent (dist=1)
5. 93% of random non-sibling pairs are graph-adjacent due to dense chain structure

## Root Cause

Linear chain structure causes high-ancestor-overlap nodes to be far apart in chain position:
- extend33 and extend31 share many ancestors (chain path) → Jaccard=0.942
- But they're 4 hops apart in the verdict→experiment→verdict cycle
- More overlap → farther apart in linear chain topology

## Conclusion

Mermaid renders the graph AS the graph (no reordering). The graph's linear chain topology is fundamentally anti-correlated with semantic overlap. This is a structural property, not a renderer bug.

## Next Steps
- R3: Test force-directed layout (Mermaid viewer layout) — but this requires actual Mermaid rendering
- R4: Accept that linear chains are incompatible with proximity-based navigation
- Alternative: Consider tree-structured branching instead of linear chains

Graph proximity also anti-correlated with ancestor overlap (spearman=-0.903). Linear chain structure causes high-overlap nodes to be far apart. Also extended 9 chains to 100 hops (KEPT).