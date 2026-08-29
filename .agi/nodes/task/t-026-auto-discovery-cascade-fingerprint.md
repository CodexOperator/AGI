---
acceptance_criteria:
  - R5.2 (no name match → compare observed frontmatter shape against schemas; pick best match if similarity >= 0.7)
blocked_by:
  - task:t-025
cavekit_req: schema-registry/R5
effort: M
id: "task:t-026"
mint_id: 68f78a50d33148bc8cca18076624dfc4
origin: build-site
parents:
  - hyp:schema-registry-r5
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-026: Auto-discovery cascade — fingerprint similarity (step 2)"
type: task
---

**Description:** Step 2: compute a fingerprint (set of frontmatter keys) for files in the directory and the union over all registered schemas. Score = Jaccard similarity. Pick the schema with the highest score >= 0.7.

**Files:** `agi-tree/src/schema_registry/fingerprint.py`, `agi-tree/tests/schema_registry/test_cascade_step_2.py`

**Test Strategy:** Fixture with directory whose files share 70% of fields with one schema; assert that schema is selected.
