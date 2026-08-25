---
confidence: 0.5
id: "hyp:graph-core-r2"
mint_id: 53c8000206f24232ae89ed74b0e927dd
origin: build-site
parents:
  - idea:domain-graph-core
subgraph: false
tags:
  - graph-core
  - R2
testable_claim: Generic Edge Primitive
title: "graph-core/R2: Generic Edge Primitive"
type: hypothesis
---

**Description:** Edges connect a parent node to a child node, carry a relation type, and may carry tag metadata. The graph is a DAG; cycles are rejected at insert time.

**Acceptance Criteria:**
- [ ] Inserting an edge that would create a cycle returns a structured error and leaves the graph unchanged
- [ ] An edge exposes `source_id`, `target_id`, `relation`, and an optional `tags` set
- [ ] Two edges with the same `(source_id, target_id, relation)` are treated as one (idempotent insert)
- [ ] Removing a node removes all incident edges and leaves no dangling references
