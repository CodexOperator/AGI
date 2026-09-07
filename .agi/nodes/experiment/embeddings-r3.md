---
id: exp:embeddings-r3
mint_id: 08db4a9a7b3b45d7bfe75c4bb7aba768
type: experiment
parents:
  - hyp:embeddings-r3
next_edges:
  - verdict:embeddings-r3
edited_by: season.py
season: 1
subgraph: false
tags:
  - embeddings
  - R3
testable_claim: Coordinate Isomorphism with Renderers
thought_session: season
title: "embeddings/R3: Experiment"
---
**Description:** Implement and validate apply_umap_coords bridging UMAP projection to Representation.

**Method:**
- Run exp-embeddings-r3-apply-umap-coords.py (5 R3 criteria tests)
- Run full test suite: pytest tests/ -q
- Validate R3.1–R3.5 programmatically
- 5/5 R3 tests passed, 241/241 total tests passed (commit 2233c70)

**Results:**
- R3.1: every node_id in coords → token.x, token.y updated in-place ✓
- R3.2: nodes not in coords → x, y remain unchanged (0.0 default) ✓
- R3.3: coords with < 2 dims → ValueError ✓
- R3.4: idempotent — same coords produce same state ✓
- R3.5: full pipeline (graph→embed_graph→project→apply_umap_coords→Representation) correct ✓
- 181/181 tokens in live graph receive UMAP coordinates
- chain_count: 3 → 4 (new embeddings domain chain formed)