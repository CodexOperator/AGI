---
acceptance_criteria:
  - R7.1 (hook-generated file written without brackets; not added to active set this load)
  - R7.2 (subsequent load after user adds brackets → active)
  - R7.3 (provenance metadata: timestamp
  - source dir
  - hook target in frontmatter)
blocked_by:
  - task:t-027
cavekit_req: schema-registry/R7
effort: M
id: "task:t-030"
mint_id: b30bb820136b42f79abec81a2bd40d12
origin: build-site
parents:
  - hyp:schema-registry-r7
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-030: Generated schemas land inactive with provenance"
type: task
---

**Description:** Generated schema files are named `<name>.md` (no brackets). Frontmatter includes `provenance: {generated_at, source_dir, hook_target}`. Idempotency check: hash the source-dir fingerprint and skip writing if a file with the same hash already exists.

**Files:** `agi-tree/src/schema_registry/generation.py`, `agi-tree/tests/schema_registry/test_schema_generation.py`

**Test Strategy:** Run cascade twice with the same input; assert one file written and second run is a no-op. Verify provenance fields. Rename to bracketed and reload; assert active.
