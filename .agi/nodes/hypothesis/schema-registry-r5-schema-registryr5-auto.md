---
confidence: 0.5
id: "hyp:schema-registry-r5"
mint_id: fefc3c46128c41068cd11c2990a27beb
origin: build-site
parents:
  - idea:domain-schema-registry
subgraph: false
tags:
  - schema-registry
  - R5
testable_claim: Auto-Discovery Cascade
title: "schema-registry/R5: Auto-Discovery Cascade"
type: hypothesis
---

**Description:** When a directory of files is encountered, the registry resolves its node type using a documented cascade: bracketed schema match, then fingerprint similarity against registered schemas, then language-model fallback to propose a new schema, then a generic fallback with a warning.

**Acceptance Criteria:**
- [ ] When a bracketed schema matches the directory by name, that schema is selected and later steps are skipped
- [ ] When no name match exists, the registry compares observed frontmatter shape against registered schemas and selects the best match if its similarity score is at least 0.7
- [ ] When similarity is below the threshold and a language-model hook is available, the hook proposes a schema and the proposal is written without brackets pending user review
- [ ] When all earlier steps fail, the directory is loaded under a generic schema and a warning lists each unmatched file
