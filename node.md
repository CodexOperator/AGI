---
id: hyp:a01-5c29f2e6-f5104d
mint_id: 50d67ef9b05844faa5cc6d188f4bc5ef
type: hypothesis
parents:
  - idea:domain-graph-core
confidence: 0.5
edited_by: season.py
season: 1
subgraph: false
tags:
  - graph-core
  - R11
testable_claim: Query and Filter API
thought_session: season
title: "graph-core/R11: Query and Filter API"
verdict: pending
---
# hyp:a01-5c29f2e6-f5104d
## Hypothesis

**testable_claim:** graph-core/R11: Query and Filter API

**Claim:** A typed query API — filter by node type, tags, edge relation, and structural predicates (depth range, breadth) — plus built-in BFS/DFS traversal methods, delivers consistent sub-100ms response on graphs up to 500 nodes without index precomputation.

**Prove it:** Write a self-contained benchmark script that loads a 500-node graph, runs all query variants (type filter, tag filter, relation filter, depth-range, BFS from root, DFS from root) and reports each latency. All runs ≤ 100ms.

**Disprove it:** Any single query variant exceeds 100ms on the same graph.

**Dependencies:** graph-core-R1 (node primitive), graph-core-R3 (identity scheme), graph-core-R7 (warm-load caching)

**Out of scope:** Rich predicate languages (regex on body text), recursive subgraph queries, cross-backend queries. These belong to environment-indexers or future R12+.


Hypothesis R11: Query and Filter API — typed filter by type/tag/relation/depth + BFS/DFS traversal, sub-100ms on 500 nodes