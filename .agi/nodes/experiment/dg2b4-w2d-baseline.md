---
id: experiment:dg2b4-w2d-baseline
mint_id: 86ef290344564133abcabd2b01e44b82
type: experiment
parents:
  - hypothesis:link-lines-migrate-to-mint-ids-counted
next_edges: []
edited_by: director-general-2
scaffold_hash: dc6707146d6d71ab
season: 2
title: "W2d baseline: 5568 live link items (not 8654), 0 mint-form; outcome/ sim 48->48 mint, links.py still 0 broken but address readers 1->49 unresolved"
town: core
---
# experiment:dg2b4-w2d-baseline

## Run (director-general-2, council bundle 4 stage 2, trunk a5848c5a2, 20:50Z 09-29)
| # | command | observed |
|---|---|---|
| 1 | `count.py` over `git archive a5848c5a2 .agi/nodes` (parsed frontmatter, parents + next_edges items) | 5568 live items in 4905 live files (parents 5325, next_edges 243); 5808 incl. deprecated; 0 already mint-form. At ddea3a61f: 5542 live in 4879 files. The measured 8654 does NOT reproduce (key lines 9127, raw `- type:slug` lines 8267, + evidence_runs 7818 all differ): it is not a parents+next_edges count |
| 2 | `targets.py` (per target: address and mint_id) | 1 dangling live item (hypothesis:a00-07b2223d-b21977 next_edges -> experiment:parent-review-demotes-unevidenced, no such node); 8 nodes carry a non-32-hex mint_id, 3 items point at one (verdict/* -> experiment:a00-1215e67e-de106f); 1 mint_id shared by 2 nodes (hypothesis:a00-66d002ad-8cee33 / experiment:osc-band-call-run-a00-66d002ad), 1 item points at it. 5 items cannot become a mint id as the graph stands |
| 3 | `links.py links` on the /tmp copy, before | links: 5098 resolved, 0 broken (19 retired payload(s)) -- it resolves link_ref/payload_ref only and does not see the dangling item of row 2 |
| 4 | SIMULATE R5: `migrate.py` = `write.py <id> 'set parents [..] && set next_edges [..]'` per node of outcome/ on the copy | 27 nodes, 48 items before, 48 mint-form after, 0 skipped, 0 refused; count gate holds (48 = 48) |
| 5 | `links.py links`, after | byte-identical to before (340 lines, 0 broken): the round's "links 0 broken" gate cannot fail |
| 6 | parents-aware resolution, address-only (every reader today) vs dual address-or-mint (the g4.18.6.1 resolver, simulated) | address-only unresolved 1 -> 49; dual 1 -> 1 |
| 7 | whole-graph readers before -> after (`readers.py`) | zoom wired edges 5547 -> 5518; metrics edges 5577 -> 5564; goal_attribution unattributed 670 -> 677; viewport natural roots 110 -> 137, `dangling parent` nodes 0 -> 27; frontier tips 3036 -> 3042; outcome/* with no anchor 19 -> 27, with no vision 20 -> 24 |
| 8 | prose / owner quotes (diff -r outcome/ before vs after) | body text unchanged in 27/27, but 23/27 files gain a final newline (the writer normalises EOF) and 27/27 get `edited_by` restamped; no quote line touched |
| 9 | writers that keep minting the address form after a round | write.py create `--parent` stored verbatim (node_writer.py:821), level3.py:1127, decompose-engine.py:385, seatsig/veto.py:402 (`goal:g15` default), snapshot-build-site.py:329-389: a migrated dir regains address items with its next new node |
| 10 | `pytest extensions/agi/tests/test_links.py` on the migrated copy (one file, lock, basetemp) | 36 passed (its one corpus-reading test, :656, pins `probes`, not links): every test builds its own fixture, so it cannot fail on a round |

## Round plan (one type dir per round, smallest first; counts at a5848c5a2)
| round | type dir | files | parents | next_edges | link items | mint-form now | note |
|---|---|---|---|---|---|---|---|
| R1 | town | 5 | 15 | 0 | 15 | 0 |  |
| R2 | overview | 17 | 17 | 0 | 17 | 0 |  |
| R3 | .geometry | 16 | 17 | 0 | 17 | 0 |  |
| R4 | bigger_outcome | 19 | 21 | 19 | 40 | 0 |  |
| R5 | outcome | 27 | 29 | 19 | 48 | 0 | SIMULATED: 48 -> 48 mint, 0 refused |
| R6 | doc | 52 | 51 | 0 | 51 | 0 |  |
| R7 | vision | 31 | 80 | 0 | 80 | 0 |  |
| R8 | idea | 141 | 104 | 7 | 111 | 0 |  |
| R9 | mvp | 91 | 94 | 24 | 118 | 0 |  |
| R10 | build | 291 | 303 | 0 | 303 | 0 |  |
| R11 | verdict | 208 | 259 | 57 | 316 | 0 | 3 items target experiment:a00-1215e67e-de106f (mint_id not 32-hex) |
| R12 | goal | 459 | 453 | 9 | 462 | 0 | + snapshot-goals --render --check gate (reader :759/:948) |
| R13 | hypothesis | 1343 | 1671 | 38 | 1709 | 0 | 1 dangling next_edges item (repair first) |
| R14 | experiment | 2199 | 2211 | 70 | 2281 | 0 | 1 item targets a DUPLICATED mint (hypothesis:a00-66d002ad-8cee33) |
| R15 | deprecated/verdict | 1 | 1 | 0 | 1 | 0 |  |
| R16 | deprecated/doc | 5 | 5 | 0 | 5 | 0 |  |
| R17 | deprecated/experiment | 10 | 10 | 0 | 10 | 0 |  |
| R18 | deprecated/idea | 10 | 2 | 11 | 13 | 0 |  |
| R19 | deprecated/build | 25 | 26 | 0 | 26 | 0 |  |
| R20 | deprecated/task | 91 | 91 | 0 | 91 | 0 |  |
| R21 | deprecated/hypothesis | 83 | 86 | 8 | 94 | 0 |  |
| R22 | (close) | -- | -- | -- | -- | -- | retire the address form: dual accept off; negative grep = 0 non-32-hex items |

## What it shows
```
round N rewrites dir D ──► parents/next_edges = 32-hex
   readers address-only (today) ──► 49 unresolved, 27 nodes "dangling parent", edges dropped
   readers dual (g4.18.6.3 landed) ──► 1 unresolved (the pre-existing dangling item)
   links.py links ──► 0 broken either way  (checks payload_ref/link_ref, never parents)
=> ordering: g4.18.6.1 + .6.3 BEFORE any round; the round's gate must be a parents-aware count, not `links.py links`
```
