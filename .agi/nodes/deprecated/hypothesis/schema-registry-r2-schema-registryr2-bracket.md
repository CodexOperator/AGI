---
id: hyp:schema-registry-r2
mint_id: f4fe8309d4234e0cb9ead0d658186cca
type: hypothesis
parents:
  - idea:domain-schema-registry
next_edges:
  - exp:schema-registry-r2
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - schema-registry
  - R2
testable_claim: Bracket Convention for Active Schemas
thought_session: L1.09
title: "schema-registry/R2: Bracket Convention for Active Schemas"
---
**Description:** A schema file whose name is wrapped in brackets is treated as the active schema for the directory tree it lives in. Bracketing is the user's signal of approval.

**Acceptance Criteria:**
- [ ] A schema file whose name is wrapped in brackets is loaded into the active set
- [ ] A schema file without brackets is loaded into the registry but marked inactive and excluded from auto-discovery matching
- [ ] Activating a schema is achieved by renaming the file to add brackets; no other action is required
- [ ] When two bracketed schemas claim the same name, loading fails with a structured error naming both files

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); already closed by `verdict:schema-registry-r2` before this pass; deprecated with its domain (`idea:domain-schema-registry`).
<!-- THOUGHT:END -->
