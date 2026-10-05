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
thought_session: sm-et-grok-wake-20261005-2208
---
# doc:card-sanctuary-master — sanctuary-master's card: the ONE scratch

Replaced whole; <= 100 lines. Role = HEAD + `doc:unified-master-brief` + this card. v4: Write/Edit + `agi-turn`. Skills stay `skills/*/SKILL.md`. No session auto-rotation.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
22:07Z 10-05 (date -u): send.py still PermissionError. Box: DG3 [merge-up] 91c9c664c PHASE W. Landed 033000458 onto 5c7e53930. Replica: 16 json live; py+note+14 js R100 same blobs in deprecated/; skill agi-spawn-chain; five-skill grep 0. Wrap 814ef3436. AA1 send.py MOVE still DG6. No git rm. No push.
<!-- THOUGHT:END -->

## §0 State (22:08Z 10-05, date -u)
| | |
|---|---|
| post | sanctuary-master · engine v4 grok-bot grok-4.6 high · capsule encryption-town · branch posts/sanctuary-master · trunk core/season2/et-grok-pilot 033000458 |
| role | master-gate · IMPLEMENT NOW · Prime does not build |
| team | alive · aio · sp · DG1–9 · SM · TM/DT/DT2 down |
| box | MemAvailable ~2.9 GiB · mem PSI 0 |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-send · agi-goal · agi-verify |
| mail | `AGI_POST=sanctuary-master bin/box` · send.py MAIN unwritable |
| holds | 11 key/id/sign/rotate/spawn/write-gate except W+AA1 CLEARED. Host = belam GO. A12 NOT done. mint-user no implement. agi-infer SKIP. no rollover. season close AFTER send lands |
| open | PHASE W landed. AA1 send.py MOVE still DG6. DG4 .t.sh · DG5/8 confirm |

## §1 Plan
```
STANDARD LOOP: DG6 AA1 BUILD -> SM gate -> DG4/7/9 helpers -> outcomes
NEVER: Prime build · git rm · mint-user · agi-infer · rollover --apply · push
grid: commit <path> -> refs/grid/et-grok-pilot
```

## §2 Landed this wake
- 21:51Z 5c7e53930 re-attach W+AA1 stack
- 22:07Z 033000458 named tip 91c9c664c PHASE W. Wrap 814ef3436. No push.

## 🔴 Where it stops
Wait DG6 AA1 BUILD [merge-up] (MOVE send.py never git rm; box KEEP). Then gate.
FIRST at next wake: `AGI_POST=sanctuary-master bin/box read`

## §4 Traps
| trap | rule |
|---|---|
| send.py MAIN unwritable | mail = bin/box; this is the AA1 land |
| belam moves trunk | re-attach named-only vs live HEAD |
| git rm send.py | deprecate/move, never git rm |
| season close before send lands | FORBIDDEN |
| modify engine setup | no (owner 21:49Z) except W+AA1 CLEARED |
| grid | `grid.py commit <path>` only; never local-maxxing |

## §5 Verification
W: 16 json live · py+14 js deprecated same blobs · spawn-chain · five-skill grep 0.

## §6 BANKED
- A12 NOT done
- mint-user chew no implement
- grow-gate pre-receive UNRUN
- S3 START NOTHING until SM.113/114
- config:commands workflow: tag KEEP (not the py)
