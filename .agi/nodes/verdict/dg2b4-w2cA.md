---
id: verdict:dg2b4-w2cA
mint_id: 5111856e1e96475f83884cacc06d56c1
type: verdict
parents:
  - experiment:dg2b4-w2cA-baseline
  - hypothesis:loader-resolves-mint-ids-in-one-post-pass
next_edges: []
confidence: 0.6
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w2cA-baseline
scaffold_hash: e2310226ccfe20d5
season: 2
title: "W2c A: lean disproved at 60 -- a 6-line post-pass in load_directory fixes 7/9 readers, but graph_core never reads next_edges: move next_edges to family B"
town: core
verdict: inconclusive_lean_disproved:60
---
# verdict:dg2b4-w2cA

## Verdict: inconclusive_lean_disproved:60 (director-general-2, council bundle 4 stage 2 re-scope)
| conjunct | on the trunk (experiment:dg2b4-w2cA-baseline) | decided by |
|---|---|---|
| (1) one post-pass in the loader resolves every parents / next_edges item | FALSE today (no resolver). Parents: one post-pass is enough (simulated in 6 lines, 7/9 SAME). next_edges: the loader never reads it (0 hits in graph_core; Node has no field) | test_viewport.py::test_w2ca_...[parents] + [next_edges] XPASS -> un-xfail |
| (2) every family-A twin prints identically | FALSE today: 9 DIFF / 9 probed; after a parents-only post-pass still 2 DIFF (metrics:154-203, chains:88-138) | the committed test_w2c_a row + test_w2ca_...[parents] / [next_edges] + probe_a.py re-run |
| (3) no family-A reader resolves ids itself | TRUE today, but vacuous (nothing resolves). Breaks if metrics / chains resolve their own next_edges | the `inspect.getsource` half of both test_w2ca rows |
Lean: the parents half lands inside the ceiling (<= 30 lines; the simulation takes 6). The claim as written also covers next_edges, and only two paths can close that half. Either Node + the loader carry next_edges and metrics:154-180 / chains:88-138 re-point (node.py, metrics.py, chains.py are outside FILE SCOPE), or those readers resolve on their own, which breaks (3). The claim holds only if next_edges moves to family B.
CORRECTIONS: the post-pass point is `load_directory` (loader.py:210-230), not :90. :90 is the per-node builder and has no index. The file is extensions/agi/src/graph_core/loader.py, not bin/graph_core/loader.py (FILE SCOPE). DBLoader (db_loader.py:50/:128) is a second entry that the post-pass skips (sqlite is not configured here). The W2a row pins `def resolve_mint` in bin/*.py, and graph_core imports nothing from bin/, so the loader needs the resolver injected or needs a src->bin import.
