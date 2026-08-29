---
id: "outcome:graph-core-r1"
mint_id: 2cda138a563241bd850f03a56178653d
next_edges:
  - bigger_outcome:graph-core-r1
parents:
  - mvp:graph-core-r1
subgraph: false
tags:
  - graph-core
  - R1
title: "graph-core/R1: Outcome"
type: outcome
---

**Input:** Node id strings, type strings, optional body text

**Output:** Graph with nodes + edges, DAG-validated

**Behavior:**
- Node(id=..., type=...) creates a node record
- Edge(source_id=..., target_id=..., relation=...) creates edge
- Graph.add_node() / add_edge() update graph state
- DAG invariant enforced: no cycles, no self-loops
- Frontmatter persistence: nodes stored as YAML-frontmatter .md files

**Edge cases:**
- Duplicate node ids → Graph.add_node is idempotent (last-write-wins by id)
- Self-loop edges → rejected by DAG invariant
- Cycle-creating edges → rejected by DAG invariant
