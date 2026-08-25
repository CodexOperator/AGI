---
acceptance_criteria:
  - R4.2 (edges record which internal module imports which other internal module)
blocked_by:
  - task:t-037
  - task:t-034
cavekit_req: environment-indexers/R4
effort: M
id: "task:t-038"
mint_id: 373c74d7badb443fa96ca812a06fa187
origin: build-site
parents:
  - hyp:environment-indexers-r4
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-038: Python dependency indexer — internal-import edges"
type: task
---

**Description:** Walk Python files, parse `import`/`from ... import` statements. For modules that resolve within the project, emit `imports` edges between module nodes (reuse module nodes from T-034 if present, otherwise emit lightweight stand-ins).

**Files:** `agi-tree/src/environment_indexers/python_deps.py`, `agi-tree/tests/environment_indexers/test_python_deps_imports.py`

**Test Strategy:** Fixture with two internal modules; assert one `imports` edge in the right direction.
