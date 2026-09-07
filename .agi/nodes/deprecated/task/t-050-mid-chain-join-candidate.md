---
id: task:t-050
mint_id: 98ecccd6ca3547b291333693c52e0495
type: task
parents:
  - hyp:chain-engine-r4
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
edited_by: season.py
effort: M
origin: build-site
season: 1
status: deprecated
tags:
  - M
  - tier--1
thought_session: season
tier: -1
title: "T-050: Mid-chain join candidate sampling"
---
**Description:** Implement `mid_chain_candidates(chains, config, rng)`. Filter chains shorter than `chain_min_join_length`. With probability `mid_chain_join_prob`, sample a non-tail position; else return the tail. Use a seedable rng for determinism.

**Files:** `agi-tree/src/chain_engine/join.py`, `agi-tree/tests/chain_engine/test_mid_chain_join.py`

**Test Strategy:** With prob=1.0, assert no tails. With prob=0.0, assert all tails. With min_length=5, chains of length 4 are excluded.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `chain-engine/R4` under `hyp:chain-engine-r4`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:chain-engine-r4-by-citation` citing `build:src-chain-engine-mid-chain`: `mid_chain.py`'s docstring enumerates R4.1-R4.4 and implements each (`MidChainConfig`: join probability, minimum chain length).
<!-- THOUGHT:END -->