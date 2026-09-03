---
id: task:t-014
mint_id: 36b31df20fe14b96909f95aed739b7b0
type: task
parents:
  - hyp:graph-core-r7
acceptance_criteria:
  - R7.4 (cache state lives under context dir; never under absolute external paths)
blocked_by:
  - task:t-013
cavekit_req: graph-core/R7
edited_by: l1.09-execution-parent
effort: S
origin: build-site
status: deprecated
tags:
  - S
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-014: Cache state lives under project context dir"
---
**Description:** Cache files (digest manifests, pickled graph snapshots) live at `<project_root>/context/.cache/graph/`. Configurable only through a context-relative path; reject configurations that resolve outside the project root.

**Files:** `agi-tree/src/graph_core/cache.py`, `agi-tree/tests/graph_core/test_cache_locality.py`

**Test Strategy:** Test that cache file paths are resolved relative to the project root and that an attempt to set an absolute external path raises a `PathOutsideProjectError`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `graph-core/R7` under `hyp:graph-core-r7`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:graph-core-r7-by-citation` citing `build:src-graph-core-cache`, `build:tests-graph-core-test-warm-load`: `cache.py` is the digest-keyed warm-load cache with invalidation and `test_warm_load.py` is its suite.
<!-- THOUGHT:END -->
