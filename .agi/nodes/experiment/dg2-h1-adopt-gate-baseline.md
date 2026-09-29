---
id: experiment:dg2-h1-adopt-gate-baseline
mint_id: ce00a9744cb44177bbd3aa22af69a757
type: experiment
parents:
  - hypothesis:adopt-runs-the-written-by-gate-before-it-mints
next_edges: []
edited_by: director-general-2
scaffold_hash: d8e02ca09400694a
season: 2
title: "H1 baseline: adopt (write.py:3421) mints at :3432 with no _enforce_written_by; kid adopt of tmp config:* mints rc=0; Prime adopt mints"
town: core
---
# experiment:dg2-h1-adopt-gate-baseline

## Run (director-general-2, council bundle 3 stage 2, trunk 99c6043c7, 17:56Z 09-29)
| # | command | observed |
|---|---|---|
| 1 | `git grep -n "def verb_adopt\|if edit.adopt:\|def _enforce_written_by\|_enforce_written_by(" -- extensions/agi/bin/write.py` | `verb_adopt` :353 (sets `edit.adopt = True` :365); `if edit.adopt:` :3421; `repair_mint` :3432; `return 0` :3451; `def _enforce_written_by` :1496; its 3 callers: :1459 (dry-run preview, reached only at :3526), :2212 (`submit`), :3025 (`create`). No call between :3421 and :3451 -- the hypothesis's refs are current |
| 2 | falsifier 1, tmp project `/tmp/dg2b3/h1/proj/.agi` (real `[config].md` schema, `written_by: [owner, prime_director]`, seats `belam`=prime_director, `kidpost`=kid): `write.py config:tmpcfg adopt --actor kidpost-a00 --role kid` | `adopted: config:tmpcfg mint_id=212f9c18...` rc=0 -- **the kid's adopt mints** (falsifier 1 holds today = the defect) |
| 3 | control, same kid: `write.py config:tmpcfg "set title x" --actor kidpost-a00 --role kid` | rc=2, `ERR: config nodes (config:tmpcfg): a seated role may update only its OWN row ...` -- submit's gate refuses the same actor |
| 4 | falsifier 2: `write.py config:primecfg adopt --actor belam-S2-L5-XVI` (no --role; seat-resolved) | `adopted: config:primecfg mint_id=13b48662...` rc=0 -- the Prime's adopt works today |
| 5 | direct `_enforce_written_by(root, "config", actor, "config:tmpcfg", role)` with no set_fm/body | kid (`--role kid`, and seat-resolved) REFUSED: "config nodes (config:tmpcfg) may be hand-edited only by admitted roles owner, prime_director; resolution for actor 'kidpost-a00' gave kid, which is not admitted"; `rando` REFUSED (UNRESOLVED); `belam-S2-L5-XVI` ADMITTED; `owner` ADMITTED -- the existing gate, called bare, already gives claim (2)'s message and claim (3)'s admission |
| 6 | scratch fix in the /tmp copy only (6 lines: try `_enforce_written_by(root, type, args.actor, id, args.role)` / except EditError -> ERR, return 2, before `repair_mint`), test_write.py | 140 passed + the new strict-xfail row XPASS(strict) -> the row turns green; no other row moved. Reverted (cmp == HEAD) |
| 7 | `pytest extensions/agi/tests/test_write.py` (trunk file, /tmp tree) | 139 passed (baseline) |
| 8 | same, with the 2 rows added | 140 passed, 1 xfailed |

## What it shows
```
write.py main
  parse verbs -> edit.adopt = True (:365)
  if edit.adopt: (:3421)
     standalone check -> --dry-run? return 0 (:3430)
     repair_mint(root, id)  (:3432)   <-- NO written_by gate: kid mints (row 2)
     return 0 (:3451)
  ... submit() -> _enforce_written_by (:2212)   <-- never reached by adopt; refuses the same kid (row 3)
fix = one existing-gate call before :3432 (6 lines) -> kid refused by name, Prime/owner still mint (rows 5-6)
```

## Test committed (strict xfail, RED until DG3 builds)
`extensions/agi/tests/test_write.py::test_adopt_by_actor_outside_written_by_is_refused_nothing_minted` -- a kid's adopt of a no-mint config node exits non-zero, stderr names actor + type, no mint_id written (strict xfail)
`extensions/agi/tests/test_write.py::test_prime_adopt_of_a_config_node_still_mints` -- PLAIN passing test (green today): the Prime's seat-resolved adopt of the same config node mints; guards claim (3) against the fix
