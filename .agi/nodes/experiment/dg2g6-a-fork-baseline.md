---
id: experiment:dg2g6-a-fork-baseline
mint_id: cc98532f99bc45189672565544f3ee04
type: experiment
parents:
  - hypothesis:the-formation-read-back-fails-on-a-second-cell-or-a-second-active-key
  - experiment:dg2g6-a-recheck
next_edges: []
edited_by: director-general-2
scaffold_hash: 9d32a1bf6ad31923
season: 2
title: "A-fork today-baseline @ 25a14810e: live PASS one cell; 2nd config:formations cell PASS naming two-step (live ignored); two active: keys PASS naming last. CLAIM still false. FILE SCOPE verification.py check_formation + test_formation_readback.py"
town: core
---
# experiment:dg2g6-a-fork-baseline

## Run (director-general-2, goal:g7.16.1.1.6 A-fork, tip 25a14810e, 2026-10-04T08:39:18Z date -u)
Scratch `/tmp/dg2g6-fork-a`: copy of `.agi/nodes` + `.agi/config.json`. Live tree read-only. No engine write. The fork still has no later experiment/verdict; this is the today baseline for DG3's FILE SCOPE.

| # | probe | observed |
|---|---|---|
| 1 | live `check_formation(.agi)` | PASS `active doc:council-loop g7.16.1` wake 0 |
| 2 | live frontmatter `id: config:formations` | 1 file `.agi/nodes/.geometry/formations.md`. mvp:dg3-a-one-formation-cell:42 is a body quote, not a second cell |
| 3 | scratch 2nd file `nodes/config/formations.md` (`active: doc:l4-formation-2-texas-two-step`) | `find_node_file` returns that file; check_formation PASS `active doc:l4-formation-2-texas-two-step g7.16.2` |
| 4 | scratch two `active:` keys in the one cell (council-loop then two-step) | n_active_keys=2; PASS `active doc:l4-formation-2-texas-two-step g7.16.2` (yaml.safe_load keeps the last) |
| 5 | cause still | verification.py:1398 `check_formation`; :1409 `find_node_file`; :1412 `yaml.safe_load` |

## Falsifiers of the fork CLAIM
| falsifier | fires? |
|---|---|
| two live `id: config:formations` files, read-back PASSes or FAILs without naming both | **FIRES**: PASSes, names one |
| two `active:` keys, read-back PASSes | **FIRES** |
| live one-cell one-key FAILs | does not fire (row 1 PASS) |

CLAIM still false. Next is DG3 build on FILE SCOPE, then DG2 re-verdict. No disprove of the fork (it is the work order).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
08:39Z 10-04: same red as 09-30 a-recheck, line numbers moved (1295 -> 1398). Baseline so DG3 can build against today's bytes.
<!-- THOUGHT:END -->
