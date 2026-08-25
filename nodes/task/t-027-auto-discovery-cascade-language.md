---
acceptance_criteria:
  - R5.3 (similarity < threshold and hook available → hook proposes schema
  - written without brackets pending review)
blocked_by:
  - task:t-026
  - task:t-028
cavekit_req: schema-registry/R5
effort: M
id: "task:t-027"
mint_id: afa429da4db44224a045e4a46a032890
origin: build-site
parents:
  - hyp:schema-registry-r5
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-027: Auto-discovery cascade — language-model fallback (step 3)"
type: task
---

**Description:** Step 3: invoke the configured LM hook with the directory's frontmatter samples. The hook returns proposed schema YAML. Validate the proposal (via T-028 hook output validation), write to `context/schemas/<name>.md` (no brackets), and use generic fallback for the current load.

**Files:** `agi-tree/src/schema_registry/cascade.py`, `agi-tree/tests/schema_registry/test_cascade_step_3.py`

**Test Strategy:** Stub hook returning a known YAML; assert file is written without brackets and the directory falls back to generic for this load.
