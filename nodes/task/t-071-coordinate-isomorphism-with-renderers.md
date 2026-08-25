---
acceptance_criteria:
  - R3.1 (renderer's shared representation derives x/y per token from embedding output for same node id)
  - R3.2 (when embeddings recomputed
  - renderer coordinates change accordingly without separate update)
  - R3.3 (no alternative coordinate source permitted for nodes that have an embedding)
  - R3.4 (integration check confirms renderer-side and embedding-side coordinates equal per node)
blocked_by:
  - task:t-070
  - task:t-060
cavekit_req: embeddings/R3
effort: M
id: "task:t-071"
mint_id: cf82bda7bf7d446986c4861706977517
origin: build-site
parents:
  - hyp:embeddings-r3
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-071: Coordinate isomorphism with renderers"
type: task
---

**Description:** Modify `build_representation(graph)` (T-060) to consult the embeddings cache for each node id and use those coordinates when present. Forbid setting `RenderToken.x` or `.y` from any other source when an embedding exists (assertion at construction). Provide an integration test fixture.

**Files:** `agi-tree/src/renderers/representation.py`, `agi-tree/src/embeddings/coordinates.py`, `agi-tree/tests/embeddings/test_isomorphism.py`

**Test Strategy:** Integration test loads graph, runs embed+project, builds representation, asserts each token's (x, y) equals the projection result for that id.
