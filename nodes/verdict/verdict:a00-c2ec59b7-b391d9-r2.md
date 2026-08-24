---
id: verdict:a00-c2ec59b7-b391d9-r2
type: verdict
title: "Graph proximity not isomorphic to ancestor overlap (spearman=-0.903)"
status: disproved
verdict: inconclusive_lean_disproved:50
confidence: 0.85
parents:
  - exp:a00-c2ec59b7-b391d9-r2
  - hypothesis:a00-c2ec59b7-b391d9-r2
tags:
  - renderers
  - mermaid
  - isomorphism
  - disproved
next_edges: []
evidence_runs: 0
demoted_from: disproved
demote_reason: 'no experiment evidence (evidence_runs=0) for ''disproved'''
---

VERDICT: DISPROVED

Spearman correlation = -0.903 (same as R1 descendant overlap test).
Top-5 avg graph distance = 9.4 hops.

The graph's linear chain topology is fundamentally anti-correlated with semantic overlap (ancestor Jaccard).
Root cause: chain structure — high-overlap nodes are farther apart in chain position.

188 connected components found. Only 10 sibling pairs in entire graph, 0% graph-adjacent.
