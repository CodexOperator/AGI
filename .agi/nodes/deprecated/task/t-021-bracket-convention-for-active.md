---
id: task:t-021
mint_id: f258500609c5417490cc8efeb9d2a2ce
type: task
parents:
  - hyp:schema-registry-r2
acceptance_criteria:
  - R2.1 (bracketed file is in active set)
  - R2.2 (no brackets → loaded but inactive
  - excluded from auto-discovery)
  - R2.3 (activating = renaming to add brackets)
  - R2.4 (two bracketed schemas claiming same name → load failure naming both)
blocked_by:
  - task:t-019
cavekit_req: schema-registry/R2
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
title: "T-021: Bracket convention for active schemas"
---
**Description:** Implement `is_active = filename.startswith('[') and filename.endswith(']')`. Track active vs inactive sets separately. On collision among active schemas, raise `DuplicateActiveSchemaError(names=[path1, path2])`.

**Files:** `agi-tree/src/schema_registry/active_set.py`, `agi-tree/tests/schema_registry/test_brackets.py`

**Test Strategy:** Tests for each of the four criteria, including renaming an inactive file mid-test and reloading.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `schema-registry/R2` under `hyp:schema-registry-r2`, whose disposition is already closed by `verdict:schema-registry-r2` before this pass; deprecated with its domain (`idea:domain-schema-registry`).
<!-- THOUGHT:END -->