---
id: "exp:schema-registry-r2"
title: "schema-registry R2 chain: exp:schema-registry-r2"
type: experiment
parents:
  - hyp:schema-registry-r2
tags:
  - schema-registry
  - R2
next_edges:
  - verdict:schema-registry-r2
---

**experiment** node for schema-registry R2: Bracket Convention.

## Acceptance Criteria
- R2.1 Bracketed → active
- R2.2 Non-bracketed → inactive
- R2.3 Rename to add brackets = activate
- R2.4 Duplicate active → DuplicateActiveSchemaError