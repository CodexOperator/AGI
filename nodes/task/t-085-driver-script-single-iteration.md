---
acceptance_criteria:
  - R7.1 (single command runs at least one full iteration end-to-end)
  - R7.4 (driver respects config without code changes)
blocked_by:
  - task:t-077
  - task:t-078
  - task:t-080
  - task:t-081
  - task:t-084
cavekit_req: autoresearch-tree-skill/R7
effort: M
id: "task:t-085"
mint_id: 491cfbb6665d4046857050adf8f27535
origin: build-site
parents:
  - hyp:autoresearch-tree-skill-r7
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-085: Driver script — single iteration end-to-end"
type: task
---

**Description:** Implement `agi-tree run` CLI invoking decision → dispatch → verdict-emission → benchmark → record, all reading `context/config/`.

**Files:** `agi-tree/src/skill/driver.py`, `agi-tree/src/skill/cli.py`, `agi-tree/tests/skill/test_driver_iteration.py`

**Test Strategy:** End-to-end fixture with stub builder; assert the iteration completes, records exist, and editing config affects behavior.
