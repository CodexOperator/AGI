---
acceptance_criteria:
  - R9.3 (mid_chain_candidates accepts min chain length and max recency
  - returns join targets matching both)
blocked_by:
  - task:t-050
cavekit_req: chain-engine/R9
effort: S
id: "task:t-058"
mint_id: 1c286c886c784be9befcfb940bdb83b6
origin: build-site
parents:
  - hyp:chain-engine-r9
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-058: mid_chain_candidates query"
type: task
---

**Description:** Implement `mid_chain_candidates(graph, min_length, max_recency)` returning a list of `(node_id, chain, position)` triples meeting both filters.

**Files:** `agi-tree/src/chain_engine/queries.py`, `agi-tree/tests/chain_engine/test_query_mid_chain.py`

**Test Strategy:** Fixture with chains of varying length and recency; assert filter intersection is correct.
