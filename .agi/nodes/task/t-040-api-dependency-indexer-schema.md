---
acceptance_criteria:
  - R5.3 (edges record which endpoints share schemas or reference each other)
blocked_by:
  - task:t-039
cavekit_req: environment-indexers/R5
effort: S
id: "task:t-040"
mint_id: 6fac3fd125a8443994a427c369cb66d2
origin: build-site
parents:
  - hyp:environment-indexers-r5
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-040: API dependency indexer — schema reuse edges"
type: task
---

**Description:** Scan `$ref` and inline schema reuse. For every shared component, emit `shares_schema` edges between the affected endpoint nodes.

**Files:** `agi-tree/src/environment_indexers/api_deps.py`, `agi-tree/tests/environment_indexers/test_api_deps_shared_schemas.py`

**Test Strategy:** Fixture with two endpoints sharing a `User` schema; assert one `shares_schema` edge between them.
