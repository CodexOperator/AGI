---
id: verdict:a00-c2ec59b7-b391d9
mint_id: 632f60af2e3a4910871a02eba4f73c74
type: verdict
parents:
  - exp:a00-c2ec59b7-b391d9
  - hyp:a00-c2ec59b7-b391d9
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
  - ascii
  - isomorphism
  - disproved
thought_session: season
title: ASCII render proximity not isomorphic to descendant overlap
verdict: inconclusive_lean_disproved:50
---
VERDICT: DISPROVED

Spearman correlation = -0.903 (strongly anti-correlated).
Top-5 overlapping pairs avg order diff = 280.2 (out of 983 tokens).

The ASCII renderer's proximity ordering does NOT cluster semantically related nodes.
Nodes with high descendant overlap are rendered FARTHER apart, not closer.

Root cause: ASCII renderer orders by type grouping + alphabetical sort, not by graph topology.