---
id: doc:card-sanctuary-master
mint_id: 9a4a831c938a4501b30d37248ad319c0
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 3e856c7e9b80c2ab
season: 2
tags:
  - card
  - master
title: Card sanctuary master
town: core
thought_session: sm-et-grok-wake-20261005-2345
---
# doc:card-sanctuary-master — sanctuary-master's card: the ONE scratch

Replaced whole; <= 100 lines. Role = HEAD + `doc:unified-master-brief` + this card. v4: Write/Edit + exact-path commit. Skills stay `skills/*/SKILL.md`. No session auto-rotation.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
23:45Z 10-05 (date -u): owner finish-send. DG6 aa030dc83 R100 send.py -> deprecated/bin/ 317680 B. Landed fa8fd991f onto 8eb933e63. Never git rm. box KEEP. Card on tip stale (said BUILD next). DG5/7/8 after-MOVE helpers queued. Season close AFTER helpers. No push.
<!-- THOUGHT:END -->

## §0 State (23:45Z 10-05, date -u)
| | |
|---|---|
| post | sanctuary-master · engine v4 grok-bot grok-4.6 high · capsule encryption-town · branch posts/sanctuary-master · trunk core/season2/et-grok-pilot fa8fd991f |
| role | master-gate · IMPLEMENT NOW · Prime does not build |
| team | alive · aio · sp · DG1–9 · SM · TM/DT/DT2 down |
| box | MemAvailable ~3.4 GiB · mem PSI 0 |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-send · agi-goal · agi-verify |
| mail | `AGI_POST=sanctuary-master box` · send.py MAIN unwritable (MOVED) |
| holds | 11 key/id/sign/rotate/spawn/write-gate except W+AA1 CLEARED. Host = belam GO. A12 NOT done. mint-user no implement. agi-infer SKIP. no rollover until helpers then close |
| open | W+AA1 on trunk. DG5/7/8 after-MOVE helpers. Then season close (outcomes → overviews). DG4 11.16 |

## §1 Plan
```
NOW: DG5/7/8 after-MOVE helpers -> SM gate
THEN season close (owner 23:3xZ): leaf outcomes → bigger_outcomes → 1 overview/vision
NEVER: Prime build · git rm · mint-user · agi-infer · rollover --apply before close · push
grid: commit <path> -> refs/grid/et-grok-pilot
```

## §2 Landed this wake
- 22:07Z 033000458 DG3 PHASE W
- 22:23Z f2c6bf2a3 DG8 W helper 0.9
- 22:28Z fe80f91e4 re-attach W onto belam 1fcf08354
- 22:29Z 332712674 DG9 AA1 helper 0.9
- 22:30Z 8eb933e63 DG4 w-move.t.sh 8/8
- 23:45Z fa8fd991f DG6 aa030dc83 AA1 MOVE send.py R100. Wrap 91da628f1. No push.

## 🔴 Where it stops
Wait DG5/7/8 after-MOVE [merge-up] (live send.py gone + deprecated 317680 + box 2005; agi-run wake residue). Then season close.
FIRST at next wake: `AGI_POST=sanctuary-master box read`

## §4 Traps
| trap | rule |
|---|---|
| send.py MAIN unwritable | mail = box; send.py MOVED never git rm |
| belam moves trunk | 1fcf08354 undid W; re-attach named-only vs live HEAD |
| git rm send.py | deprecate/move, never git rm |
| season close before helpers | wait after-MOVE then close |
| grid | `grid.py commit <path>` only; never local-maxxing |

## §5 Verification
send.py live gone · deprecated 317680 · workflow.py still dep · box 2005 · w-move.t.sh 8/8.

## §6 BANKED
- A12 NOT done
- mint-user chew no implement
- grow-gate pre-receive UNRUN
- S3 START NOTHING until SM.113/114; owner 23:3xZ: season3/main this close only AFTER send+helpers
- config:commands workflow: tag KEEP (not the py)
- agi-run wake still inbox (DG7 after-MOVE)
