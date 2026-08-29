---
acceptance_criteria:
  - R1.3 (removing schema makes type unavailable next load; existing nodes of that type fall back to generic with warning)
blocked_by:
  - task:t-019
cavekit_req: schema-registry/R1
effort: S
id: "task:t-091"
mint_id: f982fb4971014102b9e715cc24ffb2c8
origin: build-site
parents:
  - hyp:schema-registry-r1
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-091: Schema removal handling with generic fallback warning"
type: task
---

**Description:** When a previously-loaded schema is no longer present, mark its type as removed. Nodes that referenced it on next load fall through to the generic schema and emit a single warning per missing schema name.

**Files:** `agi-tree/src/schema_registry/loader.py`, `agi-tree/tests/schema_registry/test_schema_removal.py`

**Test Strategy:** Load fixture with `[t].md`, then delete it, then reload; assert nodes of type `t` map to generic and a warning is emitted naming `t`.
