---
id: hyp:schema-registry-r7
mint_id: 01cab4dff54747528cbb881fb0a05876
type: hypothesis
parents:
  - idea:domain-schema-registry
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - schema-registry
  - R7
testable_claim: Generated Schemas Land Inactive
thought_session: season
title: "schema-registry/R7: Generated Schemas Land Inactive"
---
**Description:** Schemas produced by the language-model hook are written to the schemas directory without brackets so the user must explicitly activate them.

**Acceptance Criteria:**
- [ ] A hook-generated schema file is written without brackets and is not added to the active set on the same load
- [ ] On subsequent load after a user adds brackets, the schema becomes active
- [ ] A hook-generated schema file carries provenance metadata (timestamp, source directory, hook target) in its frontmatter
- [ ] Two consecutive runs that both invoke the hook for the same directory do not produce duplicate proposal files

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition GENUINELY-OPEN, not run: no generation/provenance-writing module was found under `schema_registry/` (not exhaustively ruled out inside `cascade.py`/`hooks/cascade_step.py`); no existing goal obviously covers it (`goal:s17` is spawn-time enforcement, the opposite direction), so this THOUGHT is the record.
<!-- THOUGHT:END -->