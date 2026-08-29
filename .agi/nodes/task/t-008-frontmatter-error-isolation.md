---
acceptance_criteria:
  - R4.4 (malformed frontmatter produces structured error naming the offending file; rest of load proceeds)
blocked_by:
  - task:t-006
cavekit_req: graph-core/R4
effort: S
id: "task:t-008"
mint_id: ffd971fb5b2e428fac8e9201d2d3584c
origin: build-site
parents:
  - hyp:graph-core-r4
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-008: Frontmatter error isolation"
type: task
---

**Description:** Wrap each per-file load in a try/except that emits a `FrontmatterError(path, reason)` into a structured error list and skips the offending file. Graph load returns both the loaded node set and the error list.

**Files:** `agi-tree/src/graph_core/persistence/frontmatter.py`, `agi-tree/src/graph_core/errors.py`, `agi-tree/tests/graph_core/test_frontmatter_errors.py`

**Test Strategy:** Load directory containing one valid and one malformed node file; assert one node loaded and one error reported with the correct path.
