---
acceptance_criteria:
  - R1.1 (schema lives at known context path with documented naming)
  - R1.2 (adding new schema file makes node type available without code changes/restart)
  - R1.4 (Markdown-with-frontmatter or structured-data file accepted)
blocked_by:
  - task:t-006
cavekit_req: schema-registry/R1
effort: M
id: "task:t-019"
origin: build-site
parents:
  - hyp:schema-registry-r1
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-019: Schema as file with naming convention"
type: task
---

**Description:** Schemas live under `context/schemas/`. Naming: `name.md` for inactive, `[name].md` for active (R2 covers brackets). Loader iterates the directory; reuses T-006 frontmatter reader. Both `.md` and `.json` accepted.

**Files:** `agi-tree/src/schema_registry/loader.py`, `agi-tree/tests/schema_registry/test_schema_files.py`, `agi-tree/tests/fixtures/schemas/example.md`, `agi-tree/tests/fixtures/schemas/example.json`

**Test Strategy:** Drop a new schema file into a fixture and assert it appears in the registry on next load without code changes.
