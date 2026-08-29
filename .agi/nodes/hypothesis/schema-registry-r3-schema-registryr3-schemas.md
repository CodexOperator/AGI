---
confidence: 0.5
id: "hyp:schema-registry-r3"
mint_id: 515c3ad16ae94d5aae60aa4b62151e4a
origin: build-site
parents:
  - idea:domain-schema-registry
subgraph: false
tags:
  - schema-registry
  - R3
testable_claim: Schemas as Meta-Nodes
title: "schema-registry/R3: Schemas as Meta-Nodes"
type: hypothesis
---

**Description:** Every registered schema appears in the graph as a node of type `meta_node` so the graph can describe its own structure.

**Acceptance Criteria:**
- [ ] After load, the graph contains one `meta_node` per registered schema and its id is derived from the schema's name
- [ ] A meta-node's frontmatter exposes the schema's declared fields, defaults, and validation rules
- [ ] Edges from `meta_node` instances to ordinary nodes record which schema validated which node
- [ ] Removing a schema removes its meta-node and the validating edges on next load

**Dependencies:** graph-core (R1 nodes, R2 edges)
