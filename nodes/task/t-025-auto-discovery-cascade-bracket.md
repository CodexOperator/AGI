---
acceptance_criteria:
  - R5.1 (bracketed schema matches by name → selected
  - later steps skipped)
blocked_by:
  - task:t-021
cavekit_req: schema-registry/R5
effort: S
id: "task:t-025"
mint_id: 83e494dc8ff246688fe2db34e16363f0
origin: build-site
parents:
  - hyp:schema-registry-r5
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-025: Auto-discovery cascade — bracket name match (step 1)"
type: task
---

**Description:** Implement step 1 of the cascade. Given a directory name `foo`, look up `[foo].md` in the active set. On match, return that schema and short-circuit.

**Files:** `agi-tree/src/schema_registry/cascade.py`, `agi-tree/tests/schema_registry/test_cascade_step_1.py`

**Test Strategy:** Place `[idea].md` in the schemas dir; load directory `idea/` and assert the matching schema is selected.
