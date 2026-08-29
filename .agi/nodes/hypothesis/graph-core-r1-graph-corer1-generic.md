---
confidence: 0.5
id: "hyp:graph-core-r1"
mint_id: 4959ba1d6e9f409ebd87fa3ee7dddb54
next_edges:
  - exp:graph-core-r1
origin: build-site
parents:
  - idea:domain-graph-core
subgraph: false
tags:
  - graph-core
  - R1
testable_claim: Generic Node Primitive
title: "graph-core/R1: Generic Node Primitive"
type: hypothesis
---

**Description:** A node is a typed, identified record with an optional payload reference, parent and child links, and free-form tags. Node type does not constrain payload; payload meaning is delegated to the schema-registry.

**Acceptance Criteria:**
- [ ] A node exposes the fields `id`, `type`, `payload_ref`, `parents`, `children`, `tags` and nothing in graph-core requires additional mandatory fields
- [ ] A node with no parents is accepted as a valid root and a node with no children is accepted as a valid leaf
- [ ] `parents` and `children` are sets of node ids (no duplicates) and self-loops are rejected with a clear error
- [ ] `tags` is a set of strings and is independent of the typed parent/child links

**Dependencies:** none
