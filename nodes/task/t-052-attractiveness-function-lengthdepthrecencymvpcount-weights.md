---
acceptance_criteria:
  - R6.1 (score computed from exactly four documented inputs)
  - R6.2 (each weight from configuration
  - not hard-coded)
  - R6.3 (all-zero weights → stable constant rather than raising)
  - R6.4 (identical inputs → identical scores)
blocked_by:
  - task:t-053
cavekit_req: chain-engine/R6
effort: M
id: "task:t-052"
mint_id: 15539a698cf740048eb2614e319dc24c
origin: build-site
parents:
  - hyp:chain-engine-r6
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-052: Attractiveness function (length/depth/recency/mvp_count weights)"
type: task
---

**Description:** Implement `attractiveness(chain, weights, now)` returning `weights.length*length + weights.depth*depth + weights.recency*recency + weights.mvp_count*mvp_count`. Recency = exp-decay over time delta to now. With all-zero weights, returns 0.0 (the documented constant).

**Files:** `agi-tree/src/chain_engine/attractiveness.py`, `agi-tree/tests/chain_engine/test_attractiveness.py`

**Test Strategy:** Pin all four inputs and assert exact score. All-zero weights → 0.0. Pure-function test.
