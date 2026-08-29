---
confidence: 0.5
id: "hyp:schema-registry-r4"
mint_id: c964ce4786844df0b614553a17d880d6
origin: build-site
parents:
  - idea:domain-schema-registry
subgraph: false
tags:
  - schema-registry
  - R4
testable_claim: Optional Validation Hooks
title: "schema-registry/R4: Optional Validation Hooks"
type: hypothesis
---

**Description:** A schema may declare a validation rule. When set, the rule checks node frontmatter on load.

**Acceptance Criteria:**
- [ ] A schema without a validation rule loads its nodes without per-field checks
- [ ] A schema with a validation rule rejects nodes whose frontmatter violates the rule and emits a structured error per offending node
- [ ] Validation errors do not abort the rest of the load
- [ ] The set of validation results is queryable after load (for example, count of failures per schema)
