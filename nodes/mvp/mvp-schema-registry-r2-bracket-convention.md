---
id: "mvp:schema-registry-r2-bracket-convention"
mint_id: 6fe6618f1bd343abbb00add10e9d8f31
next_edges:
  - outcome:schema-registry-r2-bracket-convention
parents:
  - verdict:schema-registry-r2
title: "schema-registry R2 chain: mvp:schema-registry-r2-bracket-convention"
type: mvp
---

**mvp** node for schema-registry R2: Bracket Convention.

## Acceptance Criteria
- R2.1 Bracketed → active
- R2.2 Non-bracketed → inactive
- R2.3 Rename to add brackets = activate
- R2.4 Duplicate active → DuplicateActiveSchemaError
