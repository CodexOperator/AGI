---
id: "verdict:schema-registry-r2"
mint_id: 869027c3fa19487c823868c87019539e
next_edges:
  - exp:schema-registry-r2-extend
  - mvp:schema-registry-r2-bracket-convention
parents:
  - exp:schema-registry-r2
title: "schema-registry R2 chain: verdict:schema-registry-r2"
type: verdict
---

**verdict** node for schema-registry R2: Bracket Convention.

## Acceptance Criteria
- R2.1 Bracketed → active
- R2.2 Non-bracketed → inactive
- R2.3 Rename to add brackets = activate
- R2.4 Duplicate active → DuplicateActiveSchemaError
