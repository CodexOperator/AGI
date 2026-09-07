---
id: task:t-019
mint_id: 2f0dbbd4acfd45faa1da5371a2583242
type: task
parents:
  - hyp:schema-registry-r1
acceptance_criteria:
  - R1.1 (schema lives at known context path with documented naming)
  - R1.2 (adding new schema file makes node type available without code changes/restart)
  - R1.4 (Markdown-with-frontmatter or structured-data file accepted)
blocked_by:
  - task:t-006
cavekit_req: schema-registry/R1
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
title: "T-019: Schema as file with naming convention"
---
**Description:** Schemas live under `context/schemas/`. Naming: `name.md` for inactive, `[name].md` for active (R2 covers brackets). Loader iterates the directory; reuses T-006 frontmatter reader. Both `.md` and `.json` accepted.

**Files:** `agi-tree/src/schema_registry/loader.py`, `agi-tree/tests/schema_registry/test_schema_files.py`, `agi-tree/tests/fixtures/schemas/example.md`, `agi-tree/tests/fixtures/schemas/example.json`

**Test Strategy:** Drop a new schema file into a fixture and assert it appears in the registry on next load without code changes.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `schema-registry/R1` under `hyp:schema-registry-r1`, whose disposition is already closed by `verdict:schema-registry-r1` before this pass; deprecated with its domain (`idea:domain-schema-registry`).
<!-- THOUGHT:END -->