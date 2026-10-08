---
id: task:t-083
mint_id: 816bc1db97d14d1e96ff5be0c253a79c
type: task
parents:
  - hyp:autoresearch-tree-skill-r6
acceptance_criteria:
  - R6.2 (outcome_coverage = fraction of bigger_outcome nodes traceable to at least one mvp node
  - in [0.0
  - 1.0])
blocked_by:
  - task:t-082
cavekit_req: autoresearch-tree-skill/R6
edited_by: season.py
effort: S
origin: build-site
season: 1
status: deprecated
tags:
  - S
  - tier--1
thought_session: season
tier: -1
title: "T-083: Benchmark harness — outcome_coverage definition"
---
**Description:** Implement `outcome_coverage(graph)` per definition. BFS from each `bigger_outcome` node backward; count those with at least one `mvp` ancestor. Returns `count/total` in [0.0, 1.0].

**Files:** `agi-tree/src/skill/bench.py`, `agi-tree/tests/skill/test_outcome_coverage.py`

**Test Strategy:** Three fixtures: 0/3 covered → 0.0; 2/3 → 0.667; 3/3 → 1.0.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `autoresearch-tree-skill/R6` under `hyp:autoresearch-tree-skill-r6`, whose disposition is disposition CLOSE-BY-SMALL-EXPERIMENT, not run: `bin/benchmark.py` exists (`idea:engine-benchmark`) but was not confirmed to emit these five metric names; the small experiment is diffing its output fields against the criteria.
<!-- THOUGHT:END -->