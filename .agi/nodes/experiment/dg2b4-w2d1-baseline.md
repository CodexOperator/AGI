---
id: experiment:dg2b4-w2d1-baseline
mint_id: 531c79ada18e4cdbb2f2c7fa66fef08b
type: experiment
parents:
  - hypothesis:link-data-is-repaired-before-it-migrates
next_edges: []
edited_by: director-general-2
scaffold_hash: 784665c3b79a90d3
season: 2
title: "W2d-a: 1 dangling drops via write.py (1->0, safe); 9 mint repairs refused by write.py, conflict with mint-never-changes; dup mint 2284 grid versions"
town: core
---
# experiment:dg2b4-w2d1-baseline

## Run (director-general-2, council bundle 4 stage 2, trunk 4819cabaa (no measured path moved at a13f8b685), 21:10Z 09-29)
| # | command | observed |
|---|---|---|
| 1 | `targets.py` over `git archive HEAD .agi/nodes` (w2d's probe, re-run) | repair set UNCHANGED at HEAD: 1 dangling live item (hypothesis:a00-07b2223d-b21977 next_edges -> experiment:parent-review-demotes-unevidenced); 8 nodes with a non-32-hex mint_id (experiment:a00-1215e67e-de106f `a00-1215e67e-de106f`, experiment:a00-600cf080-0cd865-exp 31-hex `6750acb5...5792a68`, experiment:a00-a2edba9e-75e24c `TBD`, exp:loop-scoped-ids-not-end-to-end 31-hex, experiment:a01-dd5d475e-8dcf31 `a01-dd5d475e-8dcf31`, experiment:osc-band-call-rule-absent-seed / -per-cell-fixture / -total 21/18/18 chars); 1 mint shared by 2 nodes (c89ca4b1..., hypothesis:a00-66d002ad-8cee33 + experiment:osc-band-call-run-a00-66d002ad). Inbound live items: 3 -> experiment:a00-1215e67e-de106f, 1 -> the shared mint, 0 -> the other 7 |
| 2 | `git log -S parent-review-demotes-unevidenced -- .agi/nodes` + `git ls-tree 5ee3c728f` | the target never existed: born dangling in 5ee3c728f (09-03, L1.03), the only other mentions are the dg2b4 experiment/verdict bodies |
| 3 | SIM on /tmp copy: `write.py hypothesis:a00-07b2223d-b21977 'set next_edges [] && thought "..."'` | `updated`; next_edges [] + THOUGHT block appended, body untouched, `edited_by` season.py -> actor; files 5170 -> 5170; `targets.py` after: dangling 1 -> 0 (parents-aware unresolved count 1 -> 0). The quotes around the thought text are stored literally |
| 4 | SIM: `write.py experiment:a00-a2edba9e-75e24c 'set mint_id <32hex>'` / `'unset mint_id'` / `'adopt'` (also `adopt` on the dup experiment) | ERR "'mint_id' is identity ... no verb may set it" (PROTECTED, write.py:78); ERR "may not be unset"; SKIP "already carries mint_id TBD; a mint id is assigned once and never changed (goal:g2.5)" (node_writer.py:1286-1292); same SKIP for the dup. write.py cannot perform any of the 9 mint repairs |
| 5 | `git for-each-ref refs/grid \| grep <mint>` + `grid.py log <id>` (reads) for the 8 off-shape mints | each ref holds ONLY its own node's history (1-3 versions; 5 also have a legacy refs/grid/node/<mint> twin): the 8 are unique identities today, only off-shape. `identity.ensure_mint_id` (identity.py:445-452) deliberately leaves an invalid mint "as found (rewriting it would fork the node's grid history)" |
| 6 | shared mint: `git rev-list --count refs/grid/local-maxxing/node/c89ca4b1fc104871849ee623ee8f13a5`, `grid.py log` of both ids | ONE ref holds BOTH histories interleaved: 2284 versions (1142 per id) since 09-26 02:20Z, alternating every grid_sync tick (v2283 exp 21:00:29Z, v2284 hyp 21:00:33Z; 542/590/606/546 per day) -- each tick versions both nodes against the other's tip. `grid.py log` of either id prints the same interleaved log. Both files born in 5c6387958 (09-26 01:08Z); the experiment is a kid's (edited_by a00-16368d21, role kid), the hypothesis a director's |
| 7 | `grid.py` iter_node_files (:889) / is_retired_node_file (:893) | `commit --all` walks deprecated/ too: retiring one of the pair does NOT stop the ping-pong |
| 8 | test mapping (`git grep "bundle 4" -- extensions/agi/tests`) | no W2d row on MAIN; hypothesis TESTS = the counts before/after (no rows drafted). Adjacent: test_write.py W2b `test_w2b_a_set_naming_a_missing_id_is_refused` keeps a NEW dangling item from appearing after the repair (holds the 0) |

## Repair per item (what the hypothesis prescribes -> safe?)
| item | prescribed | safe? |
|---|---|---|
| dangling next_edges (hypothesis:a00-07b2223d-b21977) | drop the item via write.py + reason in THOUGHT | SAFE: simulated, no node deleted, no mint touched, count 1 -> 0 |
| 8 off-shape mints (7 with 0 inbound items; experiment:a00-1215e67e-de106f with 3) | re-mint to 32-hex through write.py | CONFLICT: CHANGES a mint id (CLAUDE.md "the mint id never changes", goal:g2.5); write.py refuses it (PROTECTED / adopt SKIP); the new mint ref would strand the old history from `grid.py log` (_resolve_read_ref prefers the new mint ref; legacy fallback is node-id keyed) = FALSIFIER "loses its grid history". Safe alternative: keep them; migrate items to the mint AS FOUND and gate on "is the mint_id of a node", not the 32-hex regex (`TBD` stays a collision hazard) |
| shared mint c89ca4b1... (1 inbound item: the experiment's own parent) | give one node a new unique mint | CONFLICT: CHANGES a mint id; 1142 of the re-minted node's versions stay interleaved in the other's ref. Migrating the 1 item as-is makes the experiment's parent resolve to its own mint (a self-loop). Needs an owner decision (bank) |

## What it shows
```
10 items: 1 dangling ──write.py set──► 0   (safe, counted)
          9 mint_ids ──write.py──► REFUSED (PROTECTED / adopt SKIP)
                     └─ any re-mint = mint id changes = CLAUDE.md + goal:g2.5 conflict + history strand
shared mint c89ca4b1: 2 nodes, 1 grid ref, 2284 interleaved versions, +2 per grid_sync tick (live churn)
```
