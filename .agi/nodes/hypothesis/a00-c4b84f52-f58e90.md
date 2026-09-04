---
id: hypothesis:a00-c4b84f52-f58e90
mint_id: 81a28cbe8cc14632a42f1628ed2a5ea7
type: hypothesis
parents:
  - goal:s32
next_edges: []
confidence: 0.0
scaffold_hash: 50180a5690634f72
testable_claim: "Given a graph with embedded + projected nodes (via `embed_graph` + `project`), a scatter renderer that reads `Representation.tokens[].x/.y` (already populated by the embeddings layer overwriting the defaults) can produce a bounded ASCII scatter grid where:"
title: A00 c4b84f52 f58e90
verdict: pending
---
# hypothesis:a00-c4b84f52-f58e90

## Hypothesis

A scatter renderer can be added that renders the 2D UMAP projection of embeddings through the same `Representation` that `ascii.py` and `mermaid.py` consume, producing bounded ASCII output where each node is placed at its `(x, y)` coordinate projected from its embedding vector.

### Testable Claim

Given a graph with embedded + projected nodes (via `embed_graph` + `project`), a scatter renderer that reads `Representation.tokens[].x/.y` (already populated by the embeddings layer overwriting the defaults) can produce a bounded ASCII scatter grid where:

- Each node appears at the cell closest to its `(x, y)` after normalising all coords into a bounded grid (≤200×200 chars, same as ASCII renderer bounds)
- Overlapping nodes show an overlap marker (e.g. `@` or count)
- Two runs over the same graph produce byte-identical output

### Proved by

1. A `scatter.py` module exists under `src/renderers/`, registered in `__init__.py`, taking a `Representation` and returning a string
2. Overlapping nodes at the same cell are resolved with a documented marker
3. The output respects the 200×200 bound and degrades gracefully when exceeded
4. Two runs over the same graph with the same projection coords produce identical output
5. Test suite passes

### Disproved by

1. The scatter output cannot be made deterministic across runs (e.g. floating-point rounding produces different cell assignments)
2. The 200×200 bound cannot be respected without dropping nodes in a way that loses the scatter structure
3. The overlap resolution has no acceptable degenerate behaviour (e.g. three nodes at same cell → ambiguous) that cannot be documented
4. The scatter view does not add information beyond what the ASCII tree view already shows (i.e. layout correlation is too low to be useful)


## Agent Notes
Hypothesis for scatter renderer — renders 2D UMAP projection through the same Representation that ascii.py consumes. Covers the scatter renderer gap from goal:s32 (was hyp:embeddings-r6, deprecated). No experiment run yet.