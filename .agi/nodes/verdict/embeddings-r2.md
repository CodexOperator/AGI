---
confidence: 0.85
contrasts: []
evidence_runs:
  - exp:embeddings-r2
id: "verdict:embeddings-r2"
mint_id: 27b471797af0471f855fec186605594a
next_edges:
  - exp:embeddings-r2-extend
  - mvp:embeddings-r2
parents:
  - exp:embeddings-r2
status: proved
subgraph: false
supports: []
tags:
  - embeddings
  - R2
title: "embeddings/R2: Verdict"
type: verdict
verdict: "proved"
---

**Verdict:** PROVED

**Evidence:**
- 8/8 projection tests passed (tests/embeddings/test_projection.py)
- R2.1: every embedded node has exactly one (x, y) coordinate pair
- R2.2: projection dim configurable to 2 or 3, default 2
- R2.3: same vectors + config + seed → identical coords (deterministic)
- R2.4: <2 nodes → zero-coord with UserWarning, no exception
- Falls back to hash-based deterministic projection when numpy unavailable
- PCA-based projection when numpy is available
