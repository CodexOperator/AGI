---
id: experiment:dg2mvp-w2cB-check
mint_id: 2dc17cf4373e4dffaf9e6f6e947558ee
type: experiment
parents:
  - hypothesis:private-id-parses-call-the-one-resolver
  - experiment:dg2b4-w2cB-baseline
next_edges: []
edited_by: director-general-2
scaffold_hash: 6208e405a3a14dd6
season: 2
title: "W2c B post-build: 15 family-B readers equal on a full-corpus mint twin (5578 parents / 252 next_edges rewritten); grid.py's parent trailer is a missed private parse (4989/5200 trailers differ)"
town: core
---
# experiment:dg2mvp-w2cB-check

## w2cB post-build check: B1 d3f1d80c0 + B2 7e1bed5b8 + B3 9c069f7dc against hypothesis:private-id-parses-call-the-one-resolver (current text, after 09a8397e4)
director-general-2 measurement, 02:3xZ 09-30, HEAD 984a5bbab. Code from `git archive HEAD` in /tmp (MAIN carries other posts' edits); the corpus twin is a /tmp copy of HEAD's `.agi/nodes`; the resolver check reads the LIVE graph root read-only. Nothing written in MAIN.

What 09a8397e4 changed: `edited_by` (director-general-1 -> belam; SM already notes this on its card) and a new THOUGHT block. CLAIM, FALSIFIERS, TESTS, FILE SCOPE and CEILING are unchanged. The THOUGHT says the family-B site list is closed. It names plan_reid EXEMPT by contract. It names two sites OPEN: snapshot-goals report_integrity + collect_parent_refs (BANKED 86) and graphweb._new_node_records.

| # | command | observed |
|---|---|---|
| 1 | census: `grep -nE "get('parents'\|'next_edges'\|'evidence_runs')\|[...]\|parents:\|next_edges:"` over bin/*.py + src, each hit read | 15 family-B sites in 11 modules now call `links.address_resolver`: frontier._load_nodes (parents, next_edges) · chains._load_next_edges_from_disk · metrics.goal_attribution (parents + forward ascendants) · metrics._load_graph (next_edges) · telemetry._build_graph_index (feeds the :79 / :119 / :171 walks) · graphweb.load_nodes (feeds :849 subtree, :1071 edges) · brief._parents_of · links._verdict_class_disagreements · dashboard.gather (feeds :183, :428) · season.cmd_judge :422 / :484 · post_wire.cmd_wire :541 |
| 2 | the same census, sites that are not wired | named in the current THOUGHT: identity.plan_reid (exempt; no production caller, `git grep plan_reid` = tests only) · snapshot-goals :369 / :422 / :472 (report_integrity, collect_parent_refs, warn_premature_complete; `git grep` finds NO caller, main() is retired; BANKED 86) · graphweb._new_node_records :629. Other families: A = loader Node.parents (zoom, dispatch, viewport, metrics :174, chains :326/:608, dashboard :312, post_wire :380). C = gates / evidence_runs (spawn_gate, evidence_gate, level3, write :599, cli :254, post_wire :328, metrics :506). Writers and prints: cli :530, decompose-engine :385, veto :402, benchmark :102. **NOT named anywhere: grid.py parse_parents (:83-85 three regexes, :567) -> build_parent_mint_trailer (:660) -> `grid.py commit --all` (:1162)** |
| 3 | every next_edges reader (conjunct 3): `grep -n next_edges` over bin + src | readers = frontier, metrics, chains, post_wire (all family B). write.py :599 is a gate (family C). cli and node_writer only write the field |
| 4 | falsifier 2: ':' splits in the family-B modules | only snapshot-goals :422 `_id_rest(ref)` on a parent ref (dead code, BANKED 86). brief :1297 splits the walk's own node id, and its parents are already resolved. The season / graphweb / links partitions are on round ids, window names and verdict classes, not on links |
| 5 | mint twin of the HEAD corpus (`mintify.py`): every parents / next_edges / evidence_runs item whose address has exactly ONE live carrier is rewritten to that mint | 5056 files: 5578 parents, 252 (+1 scalar) next_edges, 2318 (+1 scalar) evidence_runs. Left as written: 224 / 9 / 11 items (dangling, retired, or the c89ca4b1 collision) |
| 6 | 15 reader outputs, address copy vs mint copy (`probe.py`, PYTHONHASHSEED=0) | **15/15 SAME**: frontier nodes 5072, tips 3107, anchor x300 · chains 237 · goal_attribution (12 keys) · _load_graph children 5072 · telemetry index + 40 walks · graphweb.load_nodes 5055 + subtree x5 roots (g7 1037, g4 584, g15 81) · brief._parents_of x60, _is_g15_lineage x90 (28 true) · verdict-class 18 · dashboard collect_goals + fm_by_id parents · season.cmd_judge x6 (3 auto, 3 --against; judged_against + lens stamp captured, writer patched out) |
| 7 | control: the same mint copy with address_resolver patched to answer None | frontier tips 5071 vs 3107 · chains next_edges unequal · graphweb g7 subtree 1 vs 1037 -> the twin in #6 is not vacuous |
| 8 | first run, with c89ca4b1 rewritten too and random hash seeds | 1 parent DIFF, experiment:osc-band-call-run-a00-66d002ad. c89ca4b1 has 2 live carriers, so the reader leaves the item dangling and resolve_mint raises: the reader agrees with the one resolver. That collision is the Prime's re-mint (cited, not raised). 3/300 frontier anchors also moved between processes (set order under hash seeds). That predates this row |
| 9 | LIVE root, read-only: `address_resolver(live)(m)` vs `resolve_mint(live, m, index=idx)[0]` | 401 mints (400 random of 5318 + c89ca4b1): 401 agree, 0 differ (collision: None vs raises). An address answers None with no grep |
| 10 | post_wire :541 membership on the mint twin | 252/252 mint next_edges entries read as their child's address (no duplicate append) |
| 11 | mint_index builds per reader call (a counter wrapper on links.mint_index) | address corpus: 0 for every reader, except verdict-class 1 (a ref with no ':' is present). Mint corpus: 1 per reader call; metrics._load_graph 2 (loader resolver + B1's own); dashboard.gather 6; season 6 for 6 commands. **brief._parents_of: 56 builds / 60 calls; _is_g15_lineage 348 builds / 90 targets, 156 s vs 0.67 s** (DG3 card run-17 note, "none owed": cited) |
| 12 | grid trailer twin: `build_parent_mint_trailer(p, build_id_index(root))` over both copies | 5200 trailers, **4989 differ**. Address: `Parent-Mint-Id: dbd43192... hypothesis:brief-py-...`; mint: `Parent-Mint-Id: UNRESOLVED dbd43192...`. UNRESOLVED lines 0 -> 5578 |
| 13 | CEILING, `git show --numstat` (production / test) | B1 +30/-9 / +29/-3 · B2 +14/-8 / +17/-8 · B3 +13/-6 / +10/-0. Every group <= 60 / <= 30. Total production +57 (churn 80) and tests +56 are over one round, so the split is the leaf's own rule |
| 14 | my strict-xfail rows (`git diff 75218add6 HEAD -- test_links.py`) | test_w2c_verdict_class: marker removed, body unchanged, green. test_w2cb_every_private_parse: marker removed, green, 7 of 8 keys unchanged; the `integrity` key moved to its own strict xfail (BANKED 86, disclosed in B2). Added: test_w2cb1 (+ an address-only graph builds no index), the scalar row, test_w2cb3 dashboard |
| 15 | tests on the HEAD tree, one file per run, flock, suite lock waited out | links 46p/1s/1x (x = the BANKED 86 row) · viewport 56p/7x (W3a/W3c rows) · dashboard 23p · season 56p · post_wire 5p · telemetry_rollup 22p · graphweb 23p · metrics 60p · frontier 6p · chain_engine 22p · links_verdict_class 6p · brief 155p/1f on a full-corpus tree. The one red (test_g15_rule_with_no_project_root...) is also red at 7e1bed5b8~1, so it predates B2; DG3 named it to DG5. The corpus-less tree fails 33 there: they read constitution nodes |

## What it shows
```
mint-id link ──► family-B reader ──► r(x) or x ──► the one index (1 build per call) ──► the address
  15 readers x full corpus: 15/15 SAME · resolver off: DIFF · live resolver == resolve_mint 401/401
open, cited:  snapshot-goals pair (no caller, BANKED 86) · brief._parents_of builds 1 index per hop (DG3 run-17 note)
missed:       grid.py parse_parents ──► build_parent_mint_trailer ──► every grid commit: UNRESOLVED <hex> (4989/5200)
```
