---
id: task:t-025
mint_id: 83e494dc8ff246688fe2db34e16363f0
type: task
parents:
  - hyp:schema-registry-r5
acceptance_criteria:
  - R5.1 (bracketed schema matches by name → selected
  - later steps skipped)
blocked_by:
  - task:t-021
cavekit_req: schema-registry/R5
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
title: "T-025: Auto-discovery cascade — bracket name match (step 1)"
---
**Description:** Implement step 1 of the cascade. Given a directory name `foo`, look up `[foo].md` in the active set. On match, return that schema and short-circuit.

**Files:** `agi-tree/src/schema_registry/cascade.py`, `agi-tree/tests/schema_registry/test_cascade_step_1.py`

**Test Strategy:** Place `[idea].md` in the schemas dir; load directory `idea/` and assert the matching schema is selected.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `schema-registry/R5` under `hyp:schema-registry-r5`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:schema-registry-r5-by-citation` citing `build:src-schema-registry-cascade`, `build:src-schema-registry-fingerprint`, `build:tests-schema-registry-test-cascade-step-1`, `build:tests-schema-registry-test-cascade-step-2`: `cascade.py` (`cascade_step_1`, `discover_schema`, `register_extra_step`) and `fingerprint.py` (`cascade_step_2`) are the auto-discovery cascade, with a test per step.
<!-- THOUGHT:END -->