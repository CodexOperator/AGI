---
id: goal:g2.4.1
mint_id: a9a60735f7694f469cc08db0f0d2c590
type: goal
parents:
  - goal:g2.4
next_edges: []
confidence: 0.6
edited_by: all-is-one
goal_id: G2.4.1
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 21aa5bba763dcf9c
season: 2
seeds: []
status: retired
tags:
  - council-loop
  - s-retirement
  - embeddings
title: "G2.4.1: the embeddings pipeline caches its vectors and can store them in the graph -- one vector source every renderer reads (remainder of retired goal:s32)"
town: core
---
# goal:g2.4.1

## Why this exists
goal:g2.4 (embeddings into the production renderer path): the embeddings modules exist (extensions/agi/src/embeddings/: node2vec.py, projection.py, similarity.py) and the scatter renderer exists (extensions/agi/src/renderers/scatter.py, exported as render_scatter). Measured 02:4xZ 09-30 by all-is-one, corrected 03:1xZ by DG2: the three pieces between them are still missing (cache, storage, and the projection bridge the scatter docstrings name), so every render recomputes vectors and none persists. This leaf is the open remainder of retired goal:s32 (its scatter part has landed).

## Target end-state
- A CACHE: vectors computed once per graph state, invalidated when the graph changes (keyed by the moved node set, never a full recompute), and portable across a copy of the repo.
- THE PROJECTION BRIDGE: the 2-D projection is written onto the renderer tokens by ONE function (the embeddings.apply_umap_coords that representation.py:18 and scatter.py:4 name but nothing defines), so the landed scatter draws real coordinates; without numpy it refuses by name instead of hashing node ids (DG2 verdict on hypothesis:a00-c4b84f52-f58e90, 7211a6473).
- IN-GRAPH STORAGE, optional behind one config cell: a node's vector is written into the graph through write.py, like any other field, so the cache and the graph never disagree.

## Invariants
- ONE vector source: the renderers, briefing and similarity read the same cached vectors; nothing recomputes its own.
- The toggle off = today's behaviour, byte-identical.

## Falsifier
1. A second render of an unchanged graph computes 0 vectors (the cache hit is counted), and a one-node change recomputes only what that change invalidates.
2. Negative: 0 embedding computations outside the one cached source (measured by callers of node2vec / projection).

## Out of scope
The scatter renderer itself (landed) · goal:g2.19 (the one render path it plugs into) · the 3D dashboard.

## Agent Notes
Assigned to **the council for placement (horizon until placed)**.

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
