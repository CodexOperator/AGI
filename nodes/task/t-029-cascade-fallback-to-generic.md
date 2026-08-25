---
acceptance_criteria:
  - R5.4 (all earlier steps fail → generic schema with warning listing each unmatched file)
blocked_by:
  - task:t-027
cavekit_req: schema-registry/R5
effort: S
id: "task:t-029"
mint_id: 353c493fb7fa4b9aa61075b0986ce2d9
origin: build-site
parents:
  - hyp:schema-registry-r5
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-029: Cascade fallback to generic with unmatched-files warning (step 4)"
type: task
---

**Description:** Final cascade step. Load all files under the unmatched directory as generic nodes. Emit one aggregated warning listing every unmatched file.

**Files:** `agi-tree/src/schema_registry/cascade.py`, `agi-tree/tests/schema_registry/test_cascade_step_4.py`

**Test Strategy:** Fixture directory with no matching schema and no hook; assert generic loading and warning content.
