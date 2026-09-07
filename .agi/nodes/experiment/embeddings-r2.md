---
id: exp:embeddings-r2
mint_id: 5b9d32fccd8a44dd87f4f05e8d9fa237
type: experiment
parents:
  - hyp:embeddings-r2
next_edges:
  - verdict:embeddings-r2
edited_by: season.py
season: 1
subgraph: false
tags:
  - embeddings
  - R2
testable_claim: UMAP Projection to 2D
thought_session: season
title: "embeddings/R2: Experiment"
---
**Description:** Run embeddings projection test suite to validate UMAP 2D projection acceptance criteria.

**Method:**
- Run pytest tests/embeddings/test_projection.py (8 tests)
- Validate R2.1–R2.4 programmatically
- 8/8 tests passed (commit b9b3078)

**Results:**
- R2.1: every embedded node gets (x, y) coordinate pair ✓
- R2.2: dim configurable to 2 or 3, default 2 ✓
- R2.3: seeded runs identical ✓
- R2.4: <2 nodes degenerate case with warning, no raise ✓