---
id: task:t-031
mint_id: e6d3ab06ca844b14a73088bc623aa40c
type: task
parents:
  - hyp:schema-registry-r8
acceptance_criteria:
  - R8.1 (after bootstrap
  - registry has active schemas idea/hypothesis/experiment/verdict/mvp/outcome/bigger_outcome/app_purpose)
  - R8.2 (each declares required fields
  - including verdict taxonomy fields where applicable)
  - R8.3 (overridable by user-supplied bracketed schema of same name without code changes)
blocked_by:
  - task:t-021
  - task:t-024
  - task:t-018
cavekit_req: schema-registry/R8
edited_by: l1.09-execution-parent
effort: L
origin: build-site
status: deprecated
tags:
  - L
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-031: Built-in schemas for autoresearch types"
---
**Description:** Ship eight bracketed schema files in `agi-tree/src/graph_core/templates/builtin_schemas/`. Bootstrap copies them into `context/schemas/`. Verdict schema declares `state`, `confidence`, `evidence_runs`, `contradicts`, `supports`. User override mechanism: any user-placed `[<same-name>].md` shadows the built-in (built-in skipped on copy). Downstream callers of missing built-ins receive `MissingBuiltinSchemaError`.

**Files:** `agi-tree/src/graph_core/templates/builtin_schemas/[idea].md`, `[hypothesis].md`, `[experiment].md`, `[verdict].md`, `[mvp].md`, `[outcome].md`, `[bigger_outcome].md`, `[app_purpose].md`, `agi-tree/src/schema_registry/builtins.py`, `agi-tree/tests/schema_registry/test_builtins.py`

**Test Strategy:** Bootstrap test asserts all eight schemas present and active. Override test places `[verdict].md` and asserts user version is used. Removal test asserts a `MissingBuiltinSchemaError` is surfaced rather than crashing.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `schema-registry/R8` under `hyp:schema-registry-r8`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:schema-registry-r8-by-citation` citing `build:src-schema-registry-active-set`, `build:src-schema-registry-loader`, `build:tests-schema-registry-test-brackets`, `build:tests-schema-registry-test-schema-files`: `.agi/context/schemas/[*].md` is the real built-in schema set (a superset of the fictional eight, adapted to this project's taxonomy); bracket override is `active_set.py` and `loader.py::_generic_schema()` is the fallback for a missing schema.
<!-- THOUGHT:END -->
