---
id: task:t-027
mint_id: afa429da4db44224a045e4a46a032890
type: task
parents:
  - hyp:schema-registry-r5
acceptance_criteria:
  - R5.3 (similarity < threshold and hook available → hook proposes schema
  - written without brackets pending review)
blocked_by:
  - task:t-026
  - task:t-028
cavekit_req: schema-registry/R5
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-027: Auto-discovery cascade — language-model fallback (step 3)"
---
**Description:** Step 3: invoke the configured LM hook with the directory's frontmatter samples. The hook returns proposed schema YAML. Validate the proposal (via T-028 hook output validation), write to `context/schemas/<name>.md` (no brackets), and use generic fallback for the current load.

**Files:** `agi-tree/src/schema_registry/cascade.py`, `agi-tree/tests/schema_registry/test_cascade_step_3.py`

**Test Strategy:** Stub hook returning a known YAML; assert file is written without brackets and the directory falls back to generic for this load.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `schema-registry/R5` under `hyp:schema-registry-r5`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:schema-registry-r5-by-citation` citing `build:src-schema-registry-cascade`, `build:src-schema-registry-fingerprint`, `build:tests-schema-registry-test-cascade-step-1`, `build:tests-schema-registry-test-cascade-step-2`: `cascade.py` (`cascade_step_1`, `discover_schema`, `register_extra_step`) and `fingerprint.py` (`cascade_step_2`) are the auto-discovery cascade, with a test per step.
<!-- THOUGHT:END -->
