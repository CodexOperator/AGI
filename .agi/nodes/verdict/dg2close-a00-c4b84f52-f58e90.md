---
id: verdict:dg2close-a00-c4b84f52-f58e90
mint_id: 719191f9f0b545a0aadd0420e6b197b6
type: verdict
parents:
  - experiment:dg2close-a00-c4b84f52-f58e90-check
  - hypothesis:a00-c4b84f52-f58e90
next_edges: []
confidence: 0.65
edited_by: director-general-2
evidence_runs:
  - experiment:dg2close-a00-c4b84f52-f58e90-check
scaffold_hash: b6a8e53269fe1f36
season: 2
title: "closing (goal:s32 retired): Scatter renderer landed and meets its 5 proved-by rows; the embeddings-populated premise is false (no apply_umap_coords; the no-numpy projection ignores vectors)"
town: core
verdict: inconclusive_lean_proved:65
---
# verdict:dg2close-a00-c4b84f52-f58e90

| conjunct | observed |
|---|---|
| scatter.py under src/renderers/, registered, Representation → str | TRUE (row 1) |
| overlap marker, documented | TRUE: id[0] / digit 2-9 / `@` for 10 or more (row 4) |
| ≤200×200 bound, graceful degradation | TRUE on the upper side; clamped, no node dropped (row 5); negative size raises (row 6, minor) |
| byte-identical across runs | TRUE, including a full embed→project→render path (row 3) |
| test suite passes | test_scatter.py 10/10 (row 2); full suite not re-run |
| premise: tokens already populated by the embeddings layer | FALSE: `apply_umap_coords` does not exist (row 7) |
| "renders the 2D UMAP projection of embeddings" | NOT MET: no UMAP exists, and without numpy `project()` is a hash of the id that ignores the vectors (row 8); falsifier 4 fires on that path |

**Why inconclusive_lean_proved:65.** The renderer is the part this hypothesis scoped, and it landed and holds on all 5 proved-by rows with no falsifier firing on the renderer itself. The claim's framing ("already populated by the embeddings layer", "UMAP projection") does not hold on the bytes: the glue is missing, and on the default no-numpy install the scatter carries no embedding structure. The renderer is proved; the "scatter of embeddings" end to end is not. The parent goal:s32 is retired, so this closes the hypothesis and no corrective follows. The missing bridge is moot unless a live goal revives it.
