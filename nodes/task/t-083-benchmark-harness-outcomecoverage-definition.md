---
acceptance_criteria:
  - R6.2 (outcome_coverage = fraction of bigger_outcome nodes traceable to at least one mvp node
  - in [0.0
  - 1.0])
blocked_by:
  - task:t-082
cavekit_req: autoresearch-tree-skill/R6
effort: S
id: "task:t-083"
mint_id: 816bc1db97d14d1e96ff5be0c253a79c
origin: build-site
parents:
  - hyp:autoresearch-tree-skill-r6
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-083: Benchmark harness — outcome_coverage definition"
type: task
---

**Description:** Implement `outcome_coverage(graph)` per definition. BFS from each `bigger_outcome` node backward; count those with at least one `mvp` ancestor. Returns `count/total` in [0.0, 1.0].

**Files:** `agi-tree/src/skill/bench.py`, `agi-tree/tests/skill/test_outcome_coverage.py`

**Test Strategy:** Three fixtures: 0/3 covered → 0.0; 2/3 → 0.667; 3/3 → 1.0.
