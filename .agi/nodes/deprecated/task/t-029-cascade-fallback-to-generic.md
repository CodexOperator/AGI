---
id: task:t-029
mint_id: 353c493fb7fa4b9aa61075b0986ce2d9
type: task
parents:
  - hyp:schema-registry-r5
acceptance_criteria:
  - R5.4 (all earlier steps fail → generic schema with warning listing each unmatched file)
blocked_by:
  - task:t-027
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
title: "T-029: Cascade fallback to generic with unmatched-files warning (step 4)"
---
**Description:** Final cascade step. Load all files under the unmatched directory as generic nodes. Emit one aggregated warning listing every unmatched file.

**Files:** `agi-tree/src/schema_registry/cascade.py`, `agi-tree/tests/schema_registry/test_cascade_step_4.py`

**Test Strategy:** Fixture directory with no matching schema and no hook; assert generic loading and warning content.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `schema-registry/R5` under `hyp:schema-registry-r5`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:schema-registry-r5-by-citation` citing `build:src-schema-registry-cascade`, `build:src-schema-registry-fingerprint`, `build:tests-schema-registry-test-cascade-step-1`, `build:tests-schema-registry-test-cascade-step-2`: `cascade.py` (`cascade_step_1`, `discover_schema`, `register_extra_step`) and `fingerprint.py` (`cascade_step_2`) are the auto-discovery cascade, with a test per step.
<!-- THOUGHT:END -->