---
acceptance_criteria:
  - R7.1 (file declares chain_min_join_length
  - mid_chain_join_prob
  - fresh_start_prob
  - big_idea_vs_small_idea_split
  - attractiveness_weights with length/depth/recency/mvp_count)
blocked_by:
  - task:t-018
cavekit_req: chain-engine/R7
effort: M
id: "task:t-053"
mint_id: 91c29d22637e45b7a7228ada6ec7e79b
origin: build-site
parents:
  - hyp:chain-engine-r7
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-053: Chain configuration file (`chain-config.toml`)"
type: task
---

**Description:** Implement `ChainConfig.load(path)` reading `context/config/chain-engine.toml`. Pydantic-style validators reject out-of-range values. Defaults documented inline. Bootstrap (T-018) lays down a default file.

**Files:** `agi-tree/src/chain_engine/config.py`, `agi-tree/src/graph_core/templates/chain-engine.toml`, `agi-tree/tests/chain_engine/test_config.py`

**Test Strategy:** Tests for missing file (defaults + warning), missing key (structured error), out-of-range value (structured error), editable behavior (modify file, reload, observe difference).
