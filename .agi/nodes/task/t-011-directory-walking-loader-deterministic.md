---
acceptance_criteria:
  - R6.1 (point loader at directory; nodes correspond to files)
  - R6.4 (deterministic walk order; identical node set and id order across runs)
blocked_by:
  - task:t-006
  - task:t-005
cavekit_req: graph-core/R6
effort: M
id: "task:t-011"
mint_id: f09d3eb3c1814a2b9747541bc7bb7dea
origin: build-site
parents:
  - hyp:graph-core-r6
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-011: Directory-walking loader (deterministic)"
type: task
---

**Description:** Walk a directory using `os.walk` with explicit sort on entries at every level. For each file, mint an id via T-005 and load via T-006. Add a fixed seed mechanism to break ties.

**Files:** `agi-tree/src/graph_core/loader.py`, `agi-tree/tests/graph_core/test_walk_determinism.py`

**Test Strategy:** Walk the same fixture directory twice; assert id sequences are byte-equal.
