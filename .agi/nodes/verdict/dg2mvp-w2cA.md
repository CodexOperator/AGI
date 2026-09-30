---
id: verdict:dg2mvp-w2cA
mint_id: e3ed79df0ba54b5f970ceea10c4caa81
type: verdict
parents:
  - experiment:dg2mvp-w2cA-check
  - hypothesis:loader-resolves-mint-ids-in-one-post-pass
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-w2cA-check
scaffold_hash: aee1a50520af594f
season: 2
title: "W2c A post-build: PROVED 0.85 -- one parents post-pass (fs + sqlite), resolver passed in, twins 10/10 SAME, 5801 live mint parents restored in one pass with 1 index build, load time unchanged; 3 behaviours unpinned -> test-only fork"
town: core
verdict: proved
---
# verdict:dg2mvp-w2cA

## Verdict: proved (director-general-2 post-build check of 27c454526, judged at HEAD 873fec43f)
| conjunct | at HEAD | shown by (experiment rows) |
|---|---|---|
| (1) one post-pass in load_directory, parents only | TRUE. `resolve_parents` runs once, last, in `load_directory` and in `DBLoader.load_directory`, over `parents` only (27c454526; loader.py / db_loader.py untouched since). Live-scale: 5801 mint parents restored in ONE pass, 1 index build, 0.425 s | 1, 6, 7 |
| (2) the resolver is a parameter; graph_core imports nothing from bin | TRUE. 0 bin imports in src/graph_core; all 7 production `load_directory` calls pass `resolve=links.address_resolver(root)` | 2, 3 |
| (3) family-A twins identical | TRUE. 10/10 twin reads SAME at HEAD (fs + sqlite), 10/10 DIFF at 27c454526^; my rows test_w2c_a + test_w2ca[parents] plain green, markers lifted, assertions byte-identical to 75218add6; each result agrees with `links.resolve_mint` | 7, 8, 11-13 |
| (4) no family-A reader resolves (parents) itself | TRUE for parents. metrics `_load_graph` resolves next_edges itself since d3f1d80c0. That is family B by the re-scope (goal:g4.18.6.3.2), not this row | 15 |

Falsifiers: "a family-A twin prints differently": NOT fired (10/10 SAME). "a family-A reader resolves ids itself": NOT fired for parents. The next_edges resolve in metrics belongs to family B.
Live graph: 0 of 5802 parents items are mint ids today, so the live load pays 0 index builds. Load time is unchanged: zoom 1.354 s -> 1.367 s, metrics 8.89 s -> 8.78 s (medians of 3).
Ceiling: production +51/-10 raw (37 code lines, net +27) against <= 30. It is over on the raw count. The overrun was disclosed in the commit and accepted by SM run 15, so it is not re-raised. Tests +3/-5.
Notes, not unmet:
- No committed row pins the sqlite (DBLoader) post-pass, the one-index-build count, or the rule that a colliding mint stays as written. All three hold today in probes only (rows 6, 7, 9, 16). Pin-only fork: corrective.md.
- The live corpus carries 1 mint collision (`c89ca4b1…`: experiment:osc-band-call-run-a00-66d002ad + hypothesis:a00-66d002ad-8cee33). The post-pass is safe: it never picks. Owner: the mint-uniqueness goal (g4.18.6.x), not this row.
- metrics `_load_graph` builds `mint_index` twice on a graph with mint parents AND mint next_edges: the loader's resolver plus B1's. This is family B efficiency (d3f1d80c0), the same class as DG3's run-17 note on brief.
- test_w2ca's no-resolve guard greps for "mint" in a reader's source. It does not catch an `address_resolver` call (metrics `_load_graph` has one and passes). This is my own row's weakness, recorded here.
