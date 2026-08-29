---
acceptance_criteria:
  - R2.1 (every embedded node has (x
  - y) coordinate pair after projection)
  - R2.2 (projection dim configurable to 2 or 3
  - default 2)
  - R2.3 (two runs over same vectors + config + seed → identical coords)
blocked_by:
  - task:t-069
cavekit_req: embeddings/R2
effort: M
id: "task:t-070"
mint_id: 28a6c6ab26ab46969030a837d7f34e8c
origin: build-site
parents:
  - hyp:embeddings-r2
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-070: UMAP projection to 2D (with 3D toggle)"
type: task
---

**Description:** Implement `project(vectors, dim=2, seed) -> dict[node_id, (x, y)]` using `umap-learn` or a stdlib alternative. With <2 nodes, return zero-coordinates with a warning. Configurable to 3D for future use; tests assert defaults.

**Files:** `agi-tree/src/embeddings/projection.py`, `agi-tree/tests/embeddings/test_projection.py`

**Test Strategy:** Tests for each criterion, including fewer-than-two-nodes degenerate path.
