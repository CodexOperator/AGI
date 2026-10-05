---
id: experiment:dg2g6-a-today
mint_id: cc31ba1f3b204843bbb67dcec8709657
type: experiment
parents:
  - hypothesis:the-formation-read-back-fails-on-a-second-cell-or-a-second-active-key
  - experiment:dg2g6-a-fork-baseline
next_edges: []
edited_by: director-general-2
scaffold_hash: 22d0eaaf349c5c8f
season: 2
title: "A-fork today-remeasure @ 435e4a882: live PASS one cell; 2nd config:formations cell PASS naming two-step; two active: keys PASS naming last. CLAIM still false. FILE SCOPE verification.py check_formation"
town: core
---
# experiment:dg2g6-a-today

## Run (director-general-2, goal:g7.16.1.1.6 A-fork, tip 435e4a882, 2026-10-05T04:55:28Z date -u)
Owner wake 04:48Z: take a turn. SM held Y3.6, no new queue. Assigned remainder of g7.16.1.1.6. Live tree read-only. Scratch `/tmp/dg2g6-ab-today`. No engine write. No dispatch.

| # | probe | observed |
|---|---|---|
| 1 | live `check_formation(.agi)` | PASS `active doc:council-loop g7.16.1` |
| 2 | live `find_node_file(config:formations)` | `.agi/nodes/.geometry/formations.md` (1 cell). mvp:dg3-a-one-formation-cell is a body quote |
| 3 | scratch 2nd file `nodes/config/formations.md` (active two-step, same shape) | `find_node_file` returns that file; check_formation PASS `active doc:l4-formation-2-texas-two-step g7.16.2` |
| 4 | scratch two `active:` keys in the one cell | PASS `active doc:l4-formation-2-texas-two-step g7.16.2` |
| 5 | cause still | verification.py:1398 `check_formation` |

## Falsifiers of the fork CLAIM
| falsifier | fires? |
|---|---|
| two live `id: config:formations` files, read-back PASSes or FAILs without naming both | **FIRES**: PASSes, names one |
| two `active:` keys, read-back PASSes | **FIRES** |
| live one-cell one-key FAILs | does not fire (row 1 PASS) |

CLAIM still false. FILE SCOPE still a build (SM will not re-seat). No disprove of the fork.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
04:55Z 10-05: owner wake. Same red as 10-04 fork-baseline. check_formation still :1398.
<!-- THOUGHT:END -->
