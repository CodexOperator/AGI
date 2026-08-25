---
acceptance_criteria:
  - R9.2 (branching_factor returns avg + per-node count of out-edges across chain participants)
blocked_by:
  - task:t-051
cavekit_req: chain-engine/R9
effort: S
id: "task:t-057"
mint_id: 1a19457b9c034e79bb442638ba5415cd
origin: build-site
parents:
  - hyp:chain-engine-r9
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-057: branching_factor query"
type: task
---

**Description:** Implement `branching_factor(graph)` returning `{avg: float, per_node: {id: count}}`.

**Files:** `agi-tree/src/chain_engine/queries.py`, `agi-tree/tests/chain_engine/test_query_branching.py`

**Test Strategy:** Fixture chain participants with known fork counts; assert avg and per-node values.
