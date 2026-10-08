---
id: verdict:a00-c2ec59b7-b391d9-r2
mint_id: f0cb84faaa8a4893a02148a532428796
type: verdict
parents:
  - hyp:a00-c2ec59b7-b391d9-r2
next_edges: []
confidence: 0.85
demote_reason: no experiment evidence (evidence_runs=0) for 'disproved'
demoted_from: disproved
edited_by: season.py
evidence_runs: []
season: 1
status: inconclusive_lean_disproved:50
tags:
  - renderers
  - mermaid
  - isomorphism
  - disproved
thought_session: season
title: Graph proximity not isomorphic to ancestor overlap (spearman=-0.903)
verdict: inconclusive_lean_disproved:50
---
VERDICT: DISPROVED

Spearman correlation = -0.903 (same as R1 descendant overlap test).
Top-5 avg graph distance = 9.4 hops.

The graph's linear chain topology is fundamentally anti-correlated with semantic overlap (ancestor Jaccard).
Root cause: chain structure — high-overlap nodes are farther apart in chain position.

188 connected components found. Only 10 sibling pairs in entire graph, 0% graph-adjacent.