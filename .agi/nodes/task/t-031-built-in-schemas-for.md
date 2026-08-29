---
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
effort: L
id: "task:t-031"
mint_id: e6d3ab06ca844b14a73088bc623aa40c
origin: build-site
parents:
  - hyp:schema-registry-r8
status: pending
tags:
  - L
  - tier--1
tier: -1
title: "T-031: Built-in schemas for autoresearch types"
type: task
---

**Description:** Ship eight bracketed schema files in `agi-tree/src/graph_core/templates/builtin_schemas/`. Bootstrap copies them into `context/schemas/`. Verdict schema declares `state`, `confidence`, `evidence_runs`, `contradicts`, `supports`. User override mechanism: any user-placed `[<same-name>].md` shadows the built-in (built-in skipped on copy). Downstream callers of missing built-ins receive `MissingBuiltinSchemaError`.

**Files:** `agi-tree/src/graph_core/templates/builtin_schemas/[idea].md`, `[hypothesis].md`, `[experiment].md`, `[verdict].md`, `[mvp].md`, `[outcome].md`, `[bigger_outcome].md`, `[app_purpose].md`, `agi-tree/src/schema_registry/builtins.py`, `agi-tree/tests/schema_registry/test_builtins.py`

**Test Strategy:** Bootstrap test asserts all eight schemas present and active. Override test places `[verdict].md` and asserts user version is used. Removal test asserts a `MissingBuiltinSchemaError` is surfaced rather than crashing.
