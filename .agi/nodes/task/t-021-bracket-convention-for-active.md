---
acceptance_criteria:
  - R2.1 (bracketed file is in active set)
  - R2.2 (no brackets → loaded but inactive
  - excluded from auto-discovery)
  - R2.3 (activating = renaming to add brackets)
  - R2.4 (two bracketed schemas claiming same name → load failure naming both)
blocked_by:
  - task:t-019
cavekit_req: schema-registry/R2
effort: M
id: "task:t-021"
mint_id: f258500609c5417490cc8efeb9d2a2ce
origin: build-site
parents:
  - hyp:schema-registry-r2
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-021: Bracket convention for active schemas"
type: task
---

**Description:** Implement `is_active = filename.startswith('[') and filename.endswith(']')`. Track active vs inactive sets separately. On collision among active schemas, raise `DuplicateActiveSchemaError(names=[path1, path2])`.

**Files:** `agi-tree/src/schema_registry/active_set.py`, `agi-tree/tests/schema_registry/test_brackets.py`

**Test Strategy:** Tests for each of the four criteria, including renaming an inactive file mid-test and reloading.
