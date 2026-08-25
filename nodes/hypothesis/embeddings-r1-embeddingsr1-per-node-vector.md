---
confidence: 0.5
id: "hyp:embeddings-r1"
mint_id: 86246cab298c4b7a8a3973546c73dbc4
origin: build-site
parents:
  - idea:domain-embeddings
subgraph: false
tags:
  - embeddings
  - R1
testable_claim: Per-Node Vector Generation
title: "embeddings/R1: Per-Node Vector Generation"
type: hypothesis
---

**Description:** A vector is generated per node by running Node2Vec over the graph-core graph. The choice of Node2Vec is fixed for v1; alternative models are out of scope.

**Acceptance Criteria:**
- [ ] After embedding, every node in the input graph has exactly one associated vector
- [ ] Vector dimensionality is configurable and defaults to a documented value
- [ ] Two runs over the same graph and configuration produce identical vectors when the random seed is fixed
- [ ] When the graph contains zero nodes, the embedding step completes successfully and produces an empty vector set

**Dependencies:** graph-core (R1, R2)
