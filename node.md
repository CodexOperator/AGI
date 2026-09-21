---
id: verdict:schema-registry-r2
mint_id: 869027c3fa19487c823868c87019539e
type: verdict
parents:
  - exp:schema-registry-r2
next_edges:
  - exp:schema-registry-r2-extend
  - mvp:schema-registry-r2-bracket-convention
edited_by: season.py
season: 1
thought_session: season
title: "schema-registry R2 chain: verdict:schema-registry-r2"
verdict: pending
---
**verdict** node for schema-registry R2: Bracket Convention.

## Acceptance Criteria
- R2.1 Bracketed → active
- R2.2 Non-bracketed → inactive
- R2.3 Rename to add brackets = activate
- R2.4 Duplicate active → DuplicateActiveSchemaError