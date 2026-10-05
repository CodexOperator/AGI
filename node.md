---
id: doc:card-director-general-4
mint_id: 64d78a63a98f45cca1deb5a9e3362c1b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-4
scaffold_hash: 83e9e4c0ac970627
season: 2
tags:
  - card
  - director
  - director-general-4
title: Card director general 4
town: core
thought_session: dg4-et-grok-wake-20261005
---
ET 2026-10-05: encryption-town pi seat, grok-4.6 high, splits DG3 BUILD with DG5. Graph routes. Mint ids stay.
# doc:card-director-general-4

Role = director template + HEAD. Scratch only; skills in skills/; progress on the board.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
01:57Z 10-05 (date -u): belam [rule] 01:53Z (owner 01:36+01:47Z). Merged trunk ea29cd8f1. storage_trunk now refs/grid/et-grok-pilot. Pre-rule grid v1 of this card is on refs/grid/local-maxxing (163991f01) -- BANK, never write that ns again.
<!-- THOUGHT:END -->

## §0 State (01:57Z 10-05, date -u)
| | |
|---|---|
| post | director-general-4 · BUILD split of DG3 · engine.v4 grok-4.6 high · capsule encryption-town |
| branch | posts/director-general-4 @ ea29cd8f1 · trunk core/season2/et-grok-pilot @ 71b08aa48 |
| master | sanctuary-master · Prime off-matrix (Shael only) |
| mail | `AGI_POST=director-general-4 AGI_TRUNK=core/season2/et-grok-pilot box` · send.py MAIN inbox EACCES |
| skills | agi-goal · agi-verify · agi-send · agi-rotate · agi-corrective · agi-master-gate · agi-post · agi-workflow · agi-dispatch · agi-memory-guard · v4: Write/Edit + exact-path commit |

## §1 Plan
```
now    wait SM place of one BUILDABLE leaf
rule   grid.py commit PATH -> refs/grid/et-grok-pilot · NEVER refs/grid/local-maxxing · no push (grid_sync+branch_push OFF)
not    11.3-11.7/11.10 (DG3) · 11.11-17 (DG1) · 11.8 (council) · 11.18 (all-is-one) · 11.9 (SM/horizon)
never  invent a top · push · write.py · sudo · host acts · parent/kid dispatch · agi-turn (add -A)
```

## §2 Landed
- boxed SM [wake] a125ed11c
- [rule] belam 01:53Z applied: merged trunk ea29cd8f1; storage_trunk et-grok-pilot

## 🔴 Where it stops
Wait SM BUILDABLE leaf. Next: `AGI_POST=director-general-4 AGI_TRUNK=core/season2/et-grok-pilot box n` then `box read`

## §4 Traps
| trap | rule |
|---|---|
| grid.storage_trunk | refs/grid/et-grok-pilot; NEVER write refs/grid/local-maxxing from this checkout |
| MAIN inbox EACCES | send.py read prints then fails mark; mail = bin/box; file is MAIN `.agi/sessions/inbox/<post>.md` |
| MAIN / this tree is shared | commit by exact path; never switch branches, stash or reset |
| agi-turn is git add -A | leave only what should land; commit exact paths |
| user.name empty | `git -c user.name=director-general-4 commit -- <paths>` |
| no push | SM lands; grid_sync + branch_push OFF (52af4a8f6) |
| host acts | belam GO each |
| no kid dispatch | AA2/AA3 unbuilt; build directly |
| grep -r / find over .agi | io storm; git grep -- paths |
| pytest absent this uid | scratch / in-process replica |

## §5 Verification
box send rc 0 · verify-commit Good · merge-tree rc 0 · storage_trunk refs/grid/et-grok-pilot · grid_sync/branch_push enabled:false

## §6 BANKED
- pre-rule grid v1 of this card: refs/grid/local-maxxing/node/64d78a63a98f45cca1deb5a9e3362c1b @ 163991f01 (00:53Z). Do not rewrite that ns.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
