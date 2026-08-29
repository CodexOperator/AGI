---
acceptance_criteria:
  - R9.1 (no node/cache/config file references absolute path outside project root)
  - R9.2 (copying context dir to fresh checkout reproduces graph)
  - R9.3 (loads with no env vars beyond optional model selector)
blocked_by:
  - task:t-014
  - task:t-015
cavekit_req: graph-core/R9
effort: M
id: "task:t-016"
mint_id: 93615883194d4ea393a45d53e6fc3854
origin: build-site
parents:
  - hyp:graph-core-r9
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-016: Portability contract — relative paths only"
type: task
---

**Description:** Audit every path-handling site to use `Path(project_root) / relative`. Reject configuration values containing absolute paths outside the project root. Document the optional model-selector env var as the only permitted environment dependency.

**Files:** `agi-tree/src/graph_core/paths.py`, `agi-tree/tests/graph_core/test_portability.py`

**Test Strategy:** Copy fixture context dir to `/tmp/<random>/`, load, assert node count and id list match the original site.
