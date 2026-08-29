---
confidence: 0.5
id: "hyp:environment-indexers-r6"
mint_id: 913637130a4d4b8fbc327d243f8b1f34
origin: build-site
parents:
  - idea:domain-environment-indexers
subgraph: false
tags:
  - environment-indexers
  - R6
testable_claim: Container Observation Indexer
title: "environment-indexers/R6: Container Observation Indexer"
type: hypothesis
---

**Description:** An indexer emits nodes describing a running container observed read-only from the outside, with no modification of the container.

**Acceptance Criteria:**
- [ ] Running this indexer against an accessible container produces a node for the container plus child nodes for each observable surface (image, ports, mounts, environment keys with values redacted)
- [ ] No write operation is issued against the container or its host
- [ ] When the target container is unreachable, the indexer returns a structured error and emits no nodes
- [ ] Sensitive values (secrets, tokens) are redacted before being written into node frontmatter
