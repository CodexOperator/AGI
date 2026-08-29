---
id: "exp:schema-registry-r2"
mint_id: cd52087324ad409b85cabc72350ebd64
next_edges:
  - verdict:schema-registry-r2
parents:
  - hyp:schema-registry-r2
tags:
  - schema-registry
  - R2
title: "schema-registry R2 chain: exp:schema-registry-r2"
type: experiment
---

**experiment** node for schema-registry R2: Bracket Convention.

## Acceptance Criteria
- R2.1 Bracketed → active
- R2.2 Non-bracketed → inactive
- R2.3 Rename to add brackets = activate
- R2.4 Duplicate active → DuplicateActiveSchemaError
