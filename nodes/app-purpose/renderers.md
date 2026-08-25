---
id: "app-purpose:renderers"
mint_id: d6dc4cb497374032a8f7c19414219244
next_edges: []
parents:
  - bigger-outcome:renderers-r1
subgraph: false
tags:
  - renderers
  - root
title: "App Purpose: renderers"
type: app_purpose
---

**App Purpose:** Renderers convert the graph into human-readable formats (ASCII DAG, Mermaid flowchart, Git-tree, Git-diff) all sharing a common RenderToken representation. The same representation feeds the embeddings coordinate isomorphism. Agents can switch between render formats without changing the underlying graph.
