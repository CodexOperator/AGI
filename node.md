---
id: bigger_outcome:graph-core-primitives-r1-r10
mint_id: d4682171bf004e9f807055b13cf77b76
type: bigger_outcome
parents:
  - outcome:graph-core-r1
next_edges:
  - vision:graph-core
edited_by: season.py
judged_against: goal:g1
season: 1
subgraph: false
tags:
  - graph-core
  - R1
thought_session: season
title: "graph-core/R1: Bigger Outcome"
---
**Broader outcome:** graph-core provides the foundational primitives (Node, Edge, Graph) for the entire capillary DAG memory system. All other modules (chain_engine, renderers, embeddings, schema_registry, environment_indexers) depend on these primitives. The DAG invariant ensures the graph never forms cycles, making find_chains() termination guaranteed.

**Properties achieved:**
- Generic Node Primitive (R1): id + type + optional body
- Generic Edge Primitive (R2): source + target + relation triple
- Identity Scheme (R3): slug-based collision resistance
- Frontmatter File Persistence (R4): YAML frontmatter storage
- Recursive Node Bodies (R5): arbitrary content per node
- Directory-Walking Auto-Discovery (R6): load entire graph from disk
- Warm-Load Caching (R7): LRU cache on GraphBuilder
- Pluggable Persistence Layer (R8): abstracted backend contract
- Portability Contract (R9): relative paths for repo portability
- Bootstrap Command (R10): CLI to initialize new graph context

> Disambiguated 2026-08-25 from an id collision on `bigger-outcome:graph-core-r1` (G7.2); the other file kept that id. Renamed 2026-08-26 (S17): it is now `bigger_outcome:graph-core-r1` at `nodes/bigger_outcome/graph-core-r1.md`, on the canonical underscore spelling.