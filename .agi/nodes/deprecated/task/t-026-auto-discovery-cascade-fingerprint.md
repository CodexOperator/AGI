---
id: task:t-026
mint_id: 68f78a50d33148bc8cca18076624dfc4
type: task
parents:
  - hyp:schema-registry-r5
acceptance_criteria:
  - R5.2 (no name match → compare observed frontmatter shape against schemas; pick best match if similarity >= 0.7)
blocked_by:
  - task:t-025
cavekit_req: schema-registry/R5
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
title: "T-026: Auto-discovery cascade — fingerprint similarity (step 2)"
---
**Description:** Step 2: compute a fingerprint (set of frontmatter keys) for files in the directory and the union over all registered schemas. Score = Jaccard similarity. Pick the schema with the highest score >= 0.7.

**Files:** `agi-tree/src/schema_registry/fingerprint.py`, `agi-tree/tests/schema_registry/test_cascade_step_2.py`

**Test Strategy:** Fixture with directory whose files share 70% of fields with one schema; assert that schema is selected.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `schema-registry/R5` under `hyp:schema-registry-r5`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:schema-registry-r5-by-citation` citing `build:src-schema-registry-cascade`, `build:src-schema-registry-fingerprint`, `build:tests-schema-registry-test-cascade-step-1`, `build:tests-schema-registry-test-cascade-step-2`: `cascade.py` (`cascade_step_1`, `discover_schema`, `register_extra_step`) and `fingerprint.py` (`cascade_step_2`) are the auto-discovery cascade, with a test per step.
<!-- THOUGHT:END -->