---
confidence: 0.95
contrasts: []
evidence_runs:
  - exp:embeddings-r3
id: "verdict:embeddings-r3"
mint_id: 44c5461f749c41ba9551e38d9785eb97
next_edges:
  - exp:embeddings-r3-extend
  - mvp:embeddings-r3
parents:
  - exp:embeddings-r3
status: proved
subgraph: false
supports:
  - verdict:embeddings-r2
tags:
  - embeddings
  - R3
title: "embeddings/R3: Verdict"
type: verdict
verdict: "proved"
---

**Verdict:** PROVED

**Evidence:**
- 5/5 R3 acceptance criteria tests passed
- 241/241 total test suite passes (no regressions)
- Full pipeline verified: graph → embed_graph() → project() → apply_umap_coords() → Representation
- 181/181 tokens in live graph receive non-default UMAP coordinates
- Implementation: `src/embeddings/projection.py::apply_umap_coords()` + `__init__.py` export
- Documented in `src/renderers/representation.py` docstring (updated "may be" → "are ... overwritten by")

**Acceptance Criteria (R3):**
- R3.1: every node_id in coords → token.x, token.y updated in-place ✓
- R3.2: nodes not in coords → x, y remain unchanged (0.0 default) ✓
- R3.3: coords with < 2 dims → ValueError ✓
- R3.4: idempotent — same coords produce same state ✓
- R3.5: full pipeline correct (graph→embedding→UMAP→apply→repr) ✓
