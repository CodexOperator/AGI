---
id: "app-purpose:graph-core-storage-traversal-layer"
mint_id: c00f7c79da1a4e7b88d51ec53e496a6b
next_edges: []
parents:
  - bigger-outcome:graph-core-r1
subgraph: false
tags:
  - graph-core
  - root
title: "App Purpose: graph-core storage and traversal layer"
type: app_purpose
---

**App Purpose:** graph-core is the foundational storage and traversal layer for the capillary DAG memory. Nodes are files with YAML frontmatter, edges are relations, and the Graph class enforces DAG invariants. Every other module—chain_engine, renderers, embeddings, schema_registry—builds on these primitives. A fresh git clone can bootstrap itself from the node files alone.

> Disambiguated 2026-08-25 from an id collision on `app-purpose:graph-core` (G7.2); the other file at `nodes/app-purpose/app-purpose-graph-core.md` retains that id.
