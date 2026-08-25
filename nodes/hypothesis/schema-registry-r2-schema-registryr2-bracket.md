---
confidence: 0.5
id: "hyp:schema-registry-r2"
mint_id: f4fe8309d4234e0cb9ead0d658186cca
next_edges:
  - exp:schema-registry-r2
origin: build-site
parents:
  - idea:domain-schema-registry
subgraph: false
tags:
  - schema-registry
  - R2
testable_claim: Bracket Convention for Active Schemas
title: "schema-registry/R2: Bracket Convention for Active Schemas"
type: hypothesis
---

**Description:** A schema file whose name is wrapped in brackets is treated as the active schema for the directory tree it lives in. Bracketing is the user's signal of approval.

**Acceptance Criteria:**
- [ ] A schema file whose name is wrapped in brackets is loaded into the active set
- [ ] A schema file without brackets is loaded into the registry but marked inactive and excluded from auto-discovery matching
- [ ] Activating a schema is achieved by renaming the file to add brackets; no other action is required
- [ ] When two bracketed schemas claim the same name, loading fails with a structured error naming both files
