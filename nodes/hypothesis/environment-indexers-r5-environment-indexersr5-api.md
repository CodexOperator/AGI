---
confidence: 0.5
id: "hyp:environment-indexers-r5"
mint_id: a4d5f36c846a467a8f4c538d0c0595ee
origin: build-site
parents:
  - idea:domain-environment-indexers
subgraph: false
tags:
  - environment-indexers
  - R5
testable_claim: API Dependency Indexer
title: "environment-indexers/R5: API Dependency Indexer"
type: hypothesis
---

**Description:** An indexer emits nodes describing endpoints and their relationships from an OpenAPI or Swagger specification.

**Acceptance Criteria:**
- [ ] Running this indexer on a valid specification file emits one node per endpoint
- [ ] Each endpoint node carries method, path, and summary fields in its frontmatter
- [ ] Edges record which endpoints share schemas or reference each other
- [ ] An invalid specification file produces a structured error naming the offending file and emits no nodes
