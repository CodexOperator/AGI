---
id: outcome:schema-registry-r1
mint_id: 031e7c79958f4f8abf8e95146b557109
type: outcome
parents:
  - mvp:schema-registry-r1
next_edges:
  - bigger_outcome:schema-registry-r1
edited_by: ubuntu
judged_against: goal:g3.2
lens: unknown
season: 1
subgraph: false
tags:
  - schema-registry
  - R1
thought_session: season
title: "schema-registry/R1: Outcome"
---
**Input:** Directory of schema files (`schemas/[name].md` or `schemas/name.md`)

**Output:** SchemaRegistry with `schemas: dict[str, Schema]`, ActiveSet with `active/inactive` partitioning

**Behavior:**
- `load_schemas_from_dir()` iterates directory, parses frontmatter/JSON
- Bracketed filename `[name]` → active=True; unbracketed → active=False
- Multiple formats: `.md` (YAML frontmatter) and `.json`
- Schema removal → generic fallback with one-shot warning

**Edge cases:**
- Duplicate active schemas → DuplicateActiveSchemaError
- Missing schema → generic fallback with UserWarning
- Malformed frontmatter → logged as error, skipped gracefully