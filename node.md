---
id: outcome:embeddings-r3
mint_id: 403d44e63ac847a7ab0cf8c682c31059
type: outcome
parents:
  - mvp:embeddings-r3
next_edges:
  - bigger_outcome:embeddings-r3
edited_by: ubuntu
judged_against: goal:g11.2
lens: unknown
season: 1
subgraph: false
tags:
  - embeddings
  - R3
testable_claim: Coordinate Isomorphism with Renderers
thought_session: season
title: "embeddings/R3: Outcome"
---
**Input:** UMAP-projected 2D coordinates `{node_id: (x, y)}` from `project()`, and a `Representation` with default x=0.0, y=0.0 tokens.

**Output:** `Representation` where every token has x, y equal to the projected coordinates — spatial layout now driven by the embeddings layer.

**Behavior:**
- `apply_umap_coords(repr, coords)` updates `RenderToken.x` and `RenderToken.y` in-place
- Tokens without entries in `coords` retain their prior values (typically 0.0)
- Idempotent: calling twice with same `coords` produces identical token state

**Edge cases:**
- `coords` dict has fewer than 2 dims for a node → `ValueError`
- `coords` dict is empty → all tokens retain their prior x, y values
- Token not found in `coords` → no-op (x, y unchanged)

**Validation:** 181/181 tokens in the live graph receive non-default UMAP coordinates.