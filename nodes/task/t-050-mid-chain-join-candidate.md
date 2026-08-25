---
acceptance_criteria:
  - R4.1 (join candidates returned from anywhere along candidate chains
  - not only tails)
  - R4.2 (engine applies configured mid-chain join probability when sampling)
  - R4.3 (minimum-chain-length parameter prevents joining chains shorter than threshold)
  - R4.4 (probability=0 → only tail nodes returned)
blocked_by:
  - task:t-049
  - task:t-053
cavekit_req: chain-engine/R4
effort: M
id: "task:t-050"
mint_id: 98ecccd6ca3547b291333693c52e0495
origin: build-site
parents:
  - hyp:chain-engine-r4
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-050: Mid-chain join candidate sampling"
type: task
---

**Description:** Implement `mid_chain_candidates(chains, config, rng)`. Filter chains shorter than `chain_min_join_length`. With probability `mid_chain_join_prob`, sample a non-tail position; else return the tail. Use a seedable rng for determinism.

**Files:** `agi-tree/src/chain_engine/join.py`, `agi-tree/tests/chain_engine/test_mid_chain_join.py`

**Test Strategy:** With prob=1.0, assert no tails. With prob=0.0, assert all tails. With min_length=5, chains of length 4 are excluded.
