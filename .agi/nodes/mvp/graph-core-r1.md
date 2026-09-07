---
id: mvp:graph-core-r1
mint_id: f09cb6dbab114950bf5d6ff6ec5a80d1
type: mvp
parents:
  - verdict:graph-core-r1
next_edges:
  - outcome:graph-core-r1
edited_by: season.py
season: 1
subgraph: false
tags:
  - graph-core
  - R1
testable_claim: MVP for graph-core R1
thought_session: season
title: "graph-core/R1: MVP"
---
**MVP:** Generic Node Primitive

```python
from graph_core.node import Node
from graph_core.edge import Edge
from graph_core.graph import Graph

# Node: id + type + optional body
n = Node(id="my:id", type="hypothesis")
# Edge: source + target + relation
e = Edge(source_id="a", target_id="b", relation="spawns")
# Graph: container for nodes + edges
g = Graph()
g.add_node(n)
g.add_edge(e)
```

**Key files:**
- `src/graph_core/node.py` — Node dataclass
- `src/graph_core/edge.py` — Edge dataclass
- `src/graph_core/graph.py` — Graph container + DAG invariants
- `src/graph_core/persistence.py` — file-based frontmatter persistence