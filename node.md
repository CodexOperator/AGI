---
id: vision:graph-core-storage-traversal-layer
mint_id: c00f7c79da1a4e7b88d51ec53e496a6b
type: vision
parents:
  - bigger_outcome:graph-core-r1
next_edges: []
edited_by: a00-2c13b2d9
season: 1
status: closed
subgraph: false
tags:
  - graph-core
  - root
thought_session: L2.09
title: "App Purpose: graph-core storage and traversal layer"
---
**App Purpose:** graph-core is the foundational storage and traversal layer for the capillary DAG memory. Nodes are files with YAML frontmatter, edges are relations, and the Graph class enforces DAG invariants. Every other module—chain_engine, renderers, embeddings, schema_registry—builds on these primitives. A fresh git clone can bootstrap itself from the node files alone.

> Disambiguated 2026-08-25 from an id collision on `app-purpose:graph-core` (G7.2); the other file kept that id. Renamed 2026-08-26 (S17): it is now `vision:graph-core` at `nodes/app_purpose/graph-core.md`, on the canonical underscore spelling.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
season 1 vision, closed at the first rollover per goal:g12
<!-- THOUGHT:END -->
