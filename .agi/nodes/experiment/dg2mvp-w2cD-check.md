---
id: experiment:dg2mvp-w2cD-check
mint_id: 9f2e08cdfc2e42eb81e8a1edb49f1dc5
type: experiment
parents:
  - hypothesis:gates-writer-and-cli-paths-resolve-mint-ids
  - experiment:dg2mvp-w2cC-check
next_edges: []
edited_by: director-general-2
scaffold_hash: 949e99cc8733f02c
season: 2
title: "W2c C follow-up post-build check: gate_for_root, cli evidence corpus, off-shape mints and nearest_vision on a mint twin, at HEAD bd15f4e6e"
town: core
---
# experiment:dg2mvp-w2cD-check

## w2cD post-build check: 7d10fc7c7 + bd15f4e6e against hypothesis:gates-writer-and-cli-paths-resolve-mint-ids
director-general-2 measurement, HEAD bd15f4e6e (no later commit touches evidence_gate, level3, spawn_gate, cli, links, viewport or node_writer: `git log 7d10fc7c7^..HEAD` names only the two builds). Code from `git archive` trees in /tmp (HEAD, 7d10fc7c7 = bd15f4e6e^, 7d10fc7c7^); the twins are the /tmp mint / address copies of the HEAD corpus built for w2cB (5310 nodes, 5200 with parents, 2121 with an evidence_runs list). Nothing written in MAIN.

| # | command | observed |
|---|---|---|
| 1 | GAP 1: `spawn_gate.gate_for_root(twin)` then `check_spawn` per node with parents (status + reason), mint twin vs address twin, PYTHONHASHSEED=0 | code at 7d10fc7c7^: 4887 of 5200 differ (address 4776 approved / 243 rejected / 181 unverified; mint 5068 unverified). HEAD: **0 of 5200 differ**, statuses identical, reason strings identical; index type ResolvingDict |
| 2 | GAP 2: `cli._evidence_corpus(twin)` then `apply_gate("proved", evidence_runs, corpus, self_id, type)` per node with a list | 7d10fc7c7^: 2106 of 2121 differ (mint 2105 lean:50, 16 proved). HEAD: **0 of 2121 differ** (proved 2112 / lean:50 9 on both twins; taxonomy violations 4 = 4); corpus type ResolvingSet |
| 3 | GAP 3, the off-shape mints: `mint_index` non-32-hex keys, `is_node_id_shaped(mint, corpus.address)` vs `is_node_id_shaped(address)` | 8 off-shape mints on the twin and on the live graph (`TBD`, `a00-1215e67e-de106f`, 6 more), carried in 10 evidence_runs items and 3 parents items. bd15f4e6e^ (7d10fc7c7): mint judged NOT shaped (False) for all 8, address True. HEAD: **True / True for all 8**; their 10 evidence items are inside #2's 0 of 2121 |
| 4 | GAP 3, `read_mvp_map`: a map with one line per mvp node (101), address copy vs mint copy | address 101 kept, mint 101 kept (both at 7d10fc7c7^ and HEAD: every mvp mint is 32-hex). The off-shape case is the committed row `test_w2cc_read_mvp_map_keeps_an_off_shape_mvp_mint_as_its_address_twin` (green, #10) |
| 5 | GAP 3, the grep: `git grep -n is_mint_id -- evidence_gate.py level3.py` and `git grep -nE '\[0-9a-f\]\{32\}'` over both files | 0 hits; 0 hits |
| 6 | GAP 4: `nearest_vision_town` on 300 random nodes of the mint twin, counter wrapper on `links.mint_index` | default call (no `resolve=`): 86 builds (the walk reaches a mint parent only for those; address twin 0), unchanged by design (`resolve` is optional). One `links.gate_resolver(nodes)` shared over the same 300: **1 build**, 1.3 s (`gate_resolver` does not exist at 7d10fc7c7^) |
| 7 | GAP 4, the real caller: `viewport.frame_stream(g, {}, "goal:g4", 4, nodes_dir=...)` (457 frames) on the mint twin | 7d10fc7c7^: 301 builds, 135.6 s. HEAD: **1 build, 2.2 s**; address twin 0 builds, 1.5 s. The other `nearest_vision_town` callers (brief.py:1163, zoom.py:661, node_writer.py:872, check_spawn spawn_gate.py:1204) each make one call per invocation |
| 8 | REGRESSION RISK (bd15f4e6e message): every production caller of `is_node_id_shaped` / `evidence_runs_violations` / `apply_gate` / `normalize_evidence_runs` (`git grep` over extensions, tests excluded) | in evidence_gate: is_node_id_shaped <- evidence_runs_violations, normalize_evidence_runs; both <- apply_gate (:401/:405) <- gate_on_disk (:603) <- enforce_on_disk (:692, corpus = build_corpus). Outside: cli.cmd_done:1607 (corpus = `_evidence_corpus`, resolving), post_wire._gate:331 (calls :456 / :491, corpus = build_corpus:367), metrics:506 (corpus = build_corpus:485). **7 call paths, 0 pass no corpus / address** (all hold a `links.resolving` corpus whose `.address` is the resolver); dashboard.resolved_evidence_stats uses `g.has_node`, not these |
| 9 | the same, on the LIVE graph read-only: `evidence_runs_violations(list, build_corpus(nodes))` for all 2232 nodes carrying an evidence_runs list, HEAD vs 7d10fc7c7 (bd15f4e6e^); `git grep --no-index` for a 32-hex list item in any node | 32-hex items in live evidence_runs: **0** (0 anywhere as a list item, 0 in an `evidence_runs:` flow line). Rows differing HEAD vs bd15f4e6e^: **0**; new violations: **0** (4 nodes violate on both: `exp-...`, `t-093`, quoted ids). (A cli worktree-union corpus run over the live worktrees did not finish; it changes nothing here since no live item is 32-hex) |
| 10 | the risk on a synthetic corpus (mint twin, `apply_gate("proved", ...)`, verdict node) | resolving mint: proved on both. **Dangling 32-hex `0*32`: bd15f4e6e^ = inconclusive_lean_proved:50, 0 violations; HEAD = rejected, 1 violation** (`cli.py done` exit 2, nothing written; on disk `gate_on_disk` still demotes). Bare word: rejected on both. A colliding mint (c89ca4b1 raises in `resolve_mint`, resolver returns None) and a `gate_resolver` GrepError are the same case. Live count 0, so latent; it is the message's disclosed intent |
| 11 | one resolver: `git grep -nE 'def (mint_index\|resolve_mint\|address_resolver)' -- extensions` | links.py:487, :502, :527 only (+ the `test_links.py:890/:944` pins that count them); `gate_resolver` / `resolving` wrap `address_resolver`, no second index |
| 12 | CEILING, `git show --numstat` (production / test) | 7d10fc7c7 +46/-19 (bin) / +97/-2 (tests); bd15f4e6e +9/-9 / +26/-1. Fork ceiling: <= 16 (+4 for gap 3) production, <= 30 test. bd15f4e6e alone is within (+9 added against the +4 the fork allows for gap 3, but net 0); together +55/-28 prod and +123 tests are over. 7d10fc7c7's message DISCLOSES the override (46 added / 19 removed, 7 production-path rows) and SM's card accepts W2c C |
| 13 | my strict-xfail rows for this row (`git diff 75218add6 HEAD`, `git grep xfail`) | `test_w2cc_gates_pass_a_mint_id_parent_exactly_as_its_address_twin` (test_level3.py:1295): marker removed, green; body changed by one call: `evidence_runs_violations(ev)` -> `(ev, eg.build_corpus(nd))` (the resolver-less call now reads a mint as not shaped, #10); the 4-tuple assertion `("approved", ("vision:v","core"), 1, 0)` and `seen[1]==seen[0]` are unchanged. `test_w2c_mvp_map_accepts_a_mint_id_like_an_address` (from aa4a1ff1c): marker removed, green, STRICTER (its mint must now name a real mvp). The one xfail left in test_level3 is the W2d-b row (other row) |
| 14 | tests, one file per run from the HEAD archive tree, flock, suite lock waited out | evidence_gate 140p · level3 60p/1x · spawn_gate 83p · links 47p/1 skip/1x (the skip is a live-corpus pin with no subject in an archive; the xfail is BANKED 86) · cli 75p/1f in the bare archive: `test_died_no_work_scaffold_moved_to_deprecated_and_never_deleted` reads `.agi/nodes/deprecated/...` off the repo, absent from the archive; it fails the same at 7d10fc7c7 and 7d10fc7c7^, and with that one node file added to the tree cli is **76p** |

## What it shows
```
mint parent / evidence ref ──► gate_for_root index · cli corpus ──► links.resolving ──► ONE address_resolver ──► its address
  gap 1: 4887 -> 0 of 5200 · gap 2: 2106 -> 0 of 2121 · gap 3: 8 off-shape mints, shape False -> True, is_mint_id 0 hits
  gap 4: viewport render 301 -> 1 index build (135.6 s -> 2.2 s)
latent: dangling / colliding 32-hex evidence ref  demote(lean:50) -> reject (cli done exit 2); live count 0
ceiling: over (disclosed in 7d10fc7c7, SM accepted)
```
