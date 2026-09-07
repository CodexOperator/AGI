---
id: verdict:graph-core-r1
mint_id: 490712112f6d494b8fa146158470ba6b
type: verdict
parents:
  - exp:graph-core-r1
next_edges:
  - exp:graph-core-r1-extend
confidence: 1.0
contrasts:
edited_by: season.py
evidence_runs:
  - exp:graph-core-r1
season: 1
status: proved
subgraph: false
supports:
tags:
  - graph-core
  - R1
thought_session: season
title: "graph-core/R1: Verdict"
verdict: proved
---
**Verdict:** PROVED

**Evidence:**
- 16 graph-core test files covering node, edge, graph, DAG, identity, lazy_body, warm_load, walk_determinism, recursive_bodies, uniform_contract, backend_swap, frontmatter_errors, paths, node_invariants
- R1.1: Node with id + type created correctly
- R1.2: Node body is optional
- R1.3: Edge stores source/target/relation triple
- R1.4: Graph add_node/add_edge work correctly
- R1.5: Valid DAG (no cycles) accepted
- R1.6: No self-loop allowed by DAG invariant