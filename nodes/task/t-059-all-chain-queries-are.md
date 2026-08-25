---
acceptance_criteria:
  - R9.4 (all chain queries read-only
  - never mutate the graph)
blocked_by:
  - task:t-056
  - task:t-057
  - task:t-058
cavekit_req: chain-engine/R9
effort: S
id: "task:t-059"
mint_id: e6d9ffe1a7344a7689cf6e4cbe9de3b5
origin: build-site
parents:
  - hyp:chain-engine-r9
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-059: All chain queries are read-only"
type: task
---

**Description:** Wrap each query call site in a guard that snapshots the graph before and asserts equality after. Add a test asserting graph equality before/after each query.

**Files:** `agi-tree/tests/chain_engine/test_query_purity.py`

**Test Strategy:** Snapshot-comparison test for each of the three queries.
