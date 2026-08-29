---
acceptance_criteria:
  - R8.1 (state ∈ {proved
  - disproved
  - inconclusive_lean_proved:N
  - inconclusive_lean_disproved:N
  - pending})
blocked_by:
  - task:t-031
cavekit_req: chain-engine/R8
effort: M
id: "task:t-054"
mint_id: f65f475493de4aa8b0745dc7f5f1e88e
origin: build-site
parents:
  - hyp:chain-engine-r8
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-054: Verdict taxonomy state validation"
type: task
---

**Description:** Implement `Verdict.validate(state, n)` and a parser for the colon-suffixed forms. Insert hook in graph that intercepts verdict-typed nodes and runs validation; raises `VerdictTaxonomyError` on violation.

**Files:** `agi-tree/src/chain_engine/verdict.py`, `agi-tree/tests/chain_engine/test_verdict_state.py`

**Test Strategy:** Test each of the five forms; reject `inconclusive_lean_proved:101`; reject `proved:50`; reject unknown state.
