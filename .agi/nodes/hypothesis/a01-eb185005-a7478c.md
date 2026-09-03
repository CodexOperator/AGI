---
id: hypothesis:a01-eb185005-a7478c
mint_id: 41ca83dcac23457da5c177edc7d6ea90
type: hypothesis
parents:
  - idea:domain-graph-core
confidence: 0.5
evidence_runs: 0
title: A01 eb185005 a7478c
verdict: pending
wired_at: 1788198005
wired_from: a01-eb185005
---


# hypothesis:a01-eb185005-a7478c

## Hypothesis

**Claim:** graph-core's directory-walk auto-discovery can serve zoom (subtree) queries at O(subtree) cost instead of O(total nodes) by maintaining a derived, content-hash-keyed subtree index — without changing the node file format, without a second source of truth, and with staleness detected entirely by the per-node `mint_id` + body hash the grid already computes.

**Rationale:** The zoom path (`zoom.py`) walks the full node set to collect a 2-hop subtree every time (47 nodes at `idea:domain-graph-core`; ~800+ live). Read-time recursive-body resolution and query/filter R11 both sit on the same full-walk cost. If the walk dominates, that cost scales linearly with the whole graph for a query proportional to the subtree.

**Proves if:** a test builds N≥1000 nodes with an attached subtree, queries the 2-hop subtree via the indexed path, and (a) returns results byte-identical to a full-walk baseline, (b) touches only files under the subtree plus the index, verified by read-instrumentation or fs-usage, (c) detects a stale index after an out-of-band node edit and rebuilds it correctly.

**Disproves if:** index maintenance itself costs O(total nodes) per query or per subtree-local write (no win over the plain walk), or staleness detection produces a wrong subtree (missing/extra node) in any of: node add, node retag (address change), node deprecate (directory move), edge retarget.


Hypothesis: content-hash-keyed subtree index makes zoom/2-hop queries O(subtree) instead of O(total nodes), staleness via mint_id+body hash, no format change.