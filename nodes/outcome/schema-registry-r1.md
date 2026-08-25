---
id: "outcome:schema-registry-r1"
mint_id: 031e7c79958f4f8abf8e95146b557109
next_edges:
  - bigger-outcome:schema-registry-r1
parents:
  - mvp:schema-registry-r1
subgraph: false
tags:
  - schema-registry
  - R1
title: "schema-registry/R1: Outcome"
type: outcome
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
