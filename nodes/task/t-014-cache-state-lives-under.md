---
acceptance_criteria:
  - R7.4 (cache state lives under context dir; never under absolute external paths)
blocked_by:
  - task:t-013
cavekit_req: graph-core/R7
effort: S
id: "task:t-014"
mint_id: 36b31df20fe14b96909f95aed739b7b0
origin: build-site
parents:
  - hyp:graph-core-r7
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-014: Cache state lives under project context dir"
type: task
---

**Description:** Cache files (digest manifests, pickled graph snapshots) live at `<project_root>/context/.cache/graph/`. Configurable only through a context-relative path; reject configurations that resolve outside the project root.

**Files:** `agi-tree/src/graph_core/cache.py`, `agi-tree/tests/graph_core/test_cache_locality.py`

**Test Strategy:** Test that cache file paths are resolved relative to the project root and that an attempt to set an absolute external path raises a `PathOutsideProjectError`.
