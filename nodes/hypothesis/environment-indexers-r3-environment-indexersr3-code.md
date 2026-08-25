---
confidence: 0.5
id: "hyp:environment-indexers-r3"
mint_id: 26068eb634be4e21865cabe7c651049a
origin: build-site
parents:
  - idea:domain-environment-indexers
subgraph: false
tags:
  - environment-indexers
  - R3
testable_claim: Code Symbol Indexer
title: "environment-indexers/R3: Code Symbol Indexer"
type: hypothesis
---

**Description:** An indexer emits nodes for code symbols (functions, classes, methods, modules) and edges for the relationships between them. The internals carry forward the lessons of the predecessor project (warm-load caching, tag-based bridging edges, precomputed traversal paths) but are re-implemented against this kit's contracts rather than copied.

**Acceptance Criteria:**
- [ ] Running this indexer on a code repository emits at minimum function, class, method, and module nodes for the supported language
- [ ] The emitted graph contains relationship edges sufficient to answer "callers of X" and "callees of X" queries
- [ ] The indexer warm-loads in time indistinguishable from a no-op on a previously-indexed unchanged repository
- [ ] Inline comments inside the indexer's source flag at least one upgrade point per major parsing stage (for example "this regex parser could be replaced by a tree-based parser later")
