---
id: task:t-030
mint_id: b30bb820136b42f79abec81a2bd40d12
type: task
parents:
  - hyp:schema-registry-r7
acceptance_criteria:
  - R7.1 (hook-generated file written without brackets; not added to active set this load)
  - R7.2 (subsequent load after user adds brackets → active)
  - {"R7.3 (provenance metadata": "timestamp"}
  - source dir
  - hook target in frontmatter)
blocked_by:
  - task:t-027
cavekit_req: schema-registry/R7
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
title: "T-030: Generated schemas land inactive with provenance"
---
**Description:** Generated schema files are named `<name>.md` (no brackets). Frontmatter includes `provenance: {generated_at, source_dir, hook_target}`. Idempotency check: hash the source-dir fingerprint and skip writing if a file with the same hash already exists.

**Files:** `agi-tree/src/schema_registry/generation.py`, `agi-tree/tests/schema_registry/test_schema_generation.py`

**Test Strategy:** Run cascade twice with the same input; assert one file written and second run is a no-op. Verify provenance fields. Rename to bracketed and reload; assert active.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `schema-registry/R7` under `hyp:schema-registry-r7`, whose disposition is disposition GENUINELY-OPEN, not run: no generation/provenance-writing module was found under `schema_registry/` (not exhaustively ruled out inside `cascade.py`/`hooks/cascade_step.py`); no existing goal obviously covers it (`goal:s17` is spawn-time enforcement, the opposite direction), so this THOUGHT is the record.
<!-- THOUGHT:END -->