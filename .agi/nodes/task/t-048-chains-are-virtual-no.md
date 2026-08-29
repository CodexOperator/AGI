---
acceptance_criteria:
  - R2.1 (no chain object written to disk during normal operation)
  - R2.2 (adding node that completes new chain → queryable without rebuild)
  - R2.3 (removing node that participated in chain → chain disappears next traversal)
  - R2.4 (chain query result independent of earlier queries in same session)
blocked_by:
  - task:t-047
cavekit_req: chain-engine/R2
effort: S
id: "task:t-048"
mint_id: 7829db7186554f59a1461375bb135fcd
origin: build-site
parents:
  - hyp:chain-engine-r2
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-048: Chains are virtual (no on-disk chain objects)"
type: task
---

**Description:** Audit code path: ensure `find_chains` is pure over the live graph, never persists. Add tests for the four criteria.

**Files:** `agi-tree/src/chain_engine/chains.py`, `agi-tree/tests/chain_engine/test_virtual.py`

**Test Strategy:** Run query, mutate graph, run again; assert difference. Audit that no file in `context/.cache/chains/` is created during a query.
