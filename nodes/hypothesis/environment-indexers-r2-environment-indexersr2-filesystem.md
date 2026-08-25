---
confidence: 0.5
id: "hyp:environment-indexers-r2"
mint_id: 485900a5cbb24cc696169f13c3ece7dc
origin: build-site
parents:
  - idea:domain-environment-indexers
subgraph: false
tags:
  - environment-indexers
  - R2
testable_claim: Filesystem Tree Indexer
title: "environment-indexers/R2: Filesystem Tree Indexer"
type: hypothesis
---

**Description:** An indexer emits one node per directory and one node per file under a target path.

**Acceptance Criteria:**
- [ ] Running this indexer on any directory produces a node for the directory and one child node per file or subdirectory
- [ ] Each emitted node carries frontmatter that conforms to the registered filesystem-tree schema
- [ ] Symbolic links and unreadable entries are skipped with a per-entry warning rather than aborting the run
- [ ] Re-running the indexer on the same path produces the same node ids and the same parent-child links
