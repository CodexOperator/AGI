---
id: task:t-070
mint_id: 28a6c6ab26ab46969030a837d7f34e8c
type: task
parents:
  - hyp:embeddings-r2
acceptance_criteria:
  - R2.1 (every embedded node has (x
  - y) coordinate pair after projection)
  - R2.2 (projection dim configurable to 2 or 3
  - default 2)
  - R2.3 (two runs over same vectors + config + seed → identical coords)
blocked_by:
  - task:t-069
cavekit_req: embeddings/R2
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-070: UMAP projection to 2D (with 3D toggle)"
---
**Description:** Implement `project(vectors, dim=2, seed) -> dict[node_id, (x, y)]` using `umap-learn` or a stdlib alternative. With <2 nodes, return zero-coordinates with a warning. Configurable to 3D for future use; tests assert defaults.

**Files:** `agi-tree/src/embeddings/projection.py`, `agi-tree/tests/embeddings/test_projection.py`

**Test Strategy:** Tests for each criterion, including fewer-than-two-nodes degenerate path.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `embeddings/R2` under `hyp:embeddings-r2`, whose disposition is already closed by `verdict:embeddings-r2` before this pass; deprecated with its domain (`idea:domain-embeddings`).
<!-- THOUGHT:END -->
