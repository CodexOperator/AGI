---
confidence: 0.5
id: "hyp:graph-core-r5"
mint_id: 2c8b63ef7b3845fd93578cfbae98aac6
origin: build-site
parents:
  - idea:domain-graph-core
subgraph: false
tags:
  - graph-core
  - R5
testable_claim: Recursive Node Bodies
title: "graph-core/R5: Recursive Node Bodies"
type: hypothesis
---

**Description:** A node body may itself contain a subgraph. The same primitives and the same renderers handle top-level and recursive subgraphs.

**Acceptance Criteria:**
- [ ] A node whose frontmatter declares `subgraph: true` is treated as a container; its body is parsed as a graph using the same loader
- [ ] Recursive subgraphs may nest at least three levels deep without special-case code paths
- [ ] Renderers are invoked uniformly on a top-level graph and on a nested subgraph using the same input contract
- [ ] Querying a parent node exposes both its outer-graph children and an opaque handle to its inner subgraph
