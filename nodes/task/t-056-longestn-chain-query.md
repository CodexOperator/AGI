---
acceptance_criteria:
  - R9.1 (longest_n returns top-N chains ranked by attractiveness with score and length)
blocked_by:
  - task:t-049
cavekit_req: chain-engine/R9
effort: S
id: "task:t-056"
mint_id: 42694b1544c643fe9885a608cb5e5534
origin: build-site
parents:
  - hyp:chain-engine-r9
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-056: longest_n chain query"
type: task
---

**Description:** Implement `longest_n(graph, n)` returning `[(chain, score, length), ...]` of size up to n.

**Files:** `agi-tree/src/chain_engine/queries.py`, `agi-tree/tests/chain_engine/test_query_longest_n.py`

**Test Strategy:** Fixture with 5 chains; longest_n(3) returns 3 ordered correctly.
