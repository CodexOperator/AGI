---
id: task:t-011
mint_id: f09d3eb3c1814a2b9747541bc7bb7dea
type: task
parents:
  - hyp:graph-core-r6
acceptance_criteria:
  - R6.1 (point loader at directory; nodes correspond to files)
  - R6.4 (deterministic walk order; identical node set and id order across runs)
blocked_by:
  - task:t-006
  - task:t-005
cavekit_req: graph-core/R6
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
title: "T-011: Directory-walking loader (deterministic)"
---
**Description:** Walk a directory using `os.walk` with explicit sort on entries at every level. For each file, mint an id via T-005 and load via T-006. Add a fixed seed mechanism to break ties.

**Files:** `agi-tree/src/graph_core/loader.py`, `agi-tree/tests/graph_core/test_walk_determinism.py`

**Test Strategy:** Walk the same fixture directory twice; assert id sequences are byte-equal.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `graph-core/R6` under `hyp:graph-core-r6`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:graph-core-r6-by-citation` citing `build:src-graph-core-loader`, `build:tests-graph-core-test-loader`, `build:tests-graph-core-test-walk-determinism`: `loader.py` is the directory walk with schema-resolved subgraphs and `test_walk_determinism.py` pins the walk order.
<!-- THOUGHT:END -->