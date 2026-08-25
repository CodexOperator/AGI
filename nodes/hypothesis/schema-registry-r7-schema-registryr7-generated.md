---
confidence: 0.5
id: "hyp:schema-registry-r7"
mint_id: 01cab4dff54747528cbb881fb0a05876
origin: build-site
parents:
  - idea:domain-schema-registry
subgraph: false
tags:
  - schema-registry
  - R7
testable_claim: Generated Schemas Land Inactive
title: "schema-registry/R7: Generated Schemas Land Inactive"
type: hypothesis
---

**Description:** Schemas produced by the language-model hook are written to the schemas directory without brackets so the user must explicitly activate them.

**Acceptance Criteria:**
- [ ] A hook-generated schema file is written without brackets and is not added to the active set on the same load
- [ ] On subsequent load after a user adds brackets, the schema becomes active
- [ ] A hook-generated schema file carries provenance metadata (timestamp, source directory, hook target) in its frontmatter
- [ ] Two consecutive runs that both invoke the hook for the same directory do not produce duplicate proposal files
