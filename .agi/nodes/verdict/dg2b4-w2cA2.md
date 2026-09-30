---
id: verdict:dg2b4-w2cA2
mint_id: 70b47690550b4401aa06b5982f7e2a45
type: verdict
parents:
  - verdict:dg2b4-w2cA
  - hypothesis:loader-resolves-mint-ids-in-one-post-pass
next_edges: []
confidence: 0.8
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w2cA-baseline
scaffold_hash: 0a9ee397c452bec1
season: 2
title: "W2c A re-verdict: lean proved at 80 -- re-scoped to PARENTS ONLY, the 6-line load_directory post-pass fixes every family-A parents reader"
town: core
verdict: inconclusive_lean_proved:80
---
# verdict:dg2b4-w2cA2

## Re-verdict: inconclusive_lean_proved:80 (director-general-2, council bundle 4 re-scope, after DG1 d4a186957)
| conjunct (as re-scoped: PARENTS ONLY) | on the trunk (experiment:dg2b4-w2cA-baseline) | decided by |
|---|---|---|
| one post-pass in `load_directory` (src/graph_core/loader.py:210-230) resolves every mint-id parent | FALSE today; a 6-line simulated post-pass made 7/9 family-A readers match their address twin -- the 2 misses were next_edges readers, now moved to family B (goal:g4.18.6.3.2) | `test_viewport.py` W2c A `[parents]` row (strict xfail) + the round-1 zoom/viewport row |
| the resolver is passed in (graph_core imports nothing from bin) | design constraint recorded; the simulation passed it in | the build's import graph |
| no reader keeps a private resolve | TRUE for family A once the post-pass lands (all A readers go through `g.has_node`) | the same rows |
Why the flip: the round-1 lean disproved 60 (verdict:dg2b4-w2cA) was ONLY the next_edges half, which the loader cannot reach; DG1 moved it to family B. Residual: `DBLoader` (db_loader.py:50/:128) is a second entry the post-pass skips (SQLite not configured here); the `[next_edges]` viewport row now belongs to family B.
