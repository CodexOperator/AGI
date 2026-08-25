---
confidence: 0.5
id: "hyp:chain-engine-r7"
mint_id: 2efa24ebc4b6441aa9ec578d5e3271af
origin: build-site
parents:
  - idea:domain-chain-engine
subgraph: false
tags:
  - chain-engine
  - R7
testable_claim: Configuration File
title: "chain-engine/R7: Configuration File"
type: hypothesis
---

**Description:** Tunable parameters live in a single chain-configuration file at a documented path inside the project context. The file declares the join, fork, fresh-start, idea-split, and weight parameters.

**Acceptance Criteria:**
- [ ] The configuration file declares the keys `chain_min_join_length`, `mid_chain_join_prob`, `fresh_start_prob`, `big_idea_vs_small_idea_split`, and `attractiveness_weights` with the four documented sub-keys (`length`, `depth`, `recency`, `mvp_count`)
- [ ] When the file is missing, documented defaults apply and a warning identifies the absent file
- [ ] When a key is missing or out of range, the engine raises a structured error naming the offending key
- [ ] Editing the file changes engine behavior on next run without code changes
