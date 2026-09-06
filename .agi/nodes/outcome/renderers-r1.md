---
id: outcome:renderers-r1
mint_id: ebf4d73f723a4b4fa5204be534cd3ce2
type: outcome
parents:
  - mvp:renderers-r1
next_edges:
  - bigger_outcome:renderers-r1
edited_by: season.py
judged_against: goal:g9.4
lens: goal:g9
season: 1
subgraph: false
tags:
  - renderers
  - R1
thought_session: season
title: "renderers/R1: Outcome"
---
**Input:** Graph with nodes + edges

**Output:** Sequence of RenderToken objects

**Behavior:**
- build_representation(graph) → list[RenderToken]
- Each token: id, label, type, depth (BFS from roots), x/y (0.0 by default), edges
- Deterministic: same graph → same token sequence (sorted by id)
- Empty graph → empty representation
- Token edges mirror graph edges

**Edge cases:**
- No nodes → empty list
- Single node → one token with empty edges list
- Disconnected nodes → separate subgraphs in representation