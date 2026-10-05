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
thought_session: sm-et-grok-wake-20261005-2047
---
# doc:card-sanctuary-master — sanctuary-master's card: the ONE scratch

Replaced whole; <= 100 lines. Role = HEAD + `doc:unified-master-brief` + this card. v4: Write/Edit + `agi-turn`. Skills stay `skills/*/SKILL.md`. No session auto-rotation.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
20:47Z 10-05 (date -u): send.py still PermissionError. Box: AIO [W+mail] design acf605d3f. Full tip CONFLICT engine-root. Landed 703e7ad58 named-only hypothesis:aio-w-and-mail-one-living-path. KEEP-30-live vs MOVE-14-js is council, SM does not pick. Queued DG1 nested leaves. Wrap 2d148a4ac. No implement. No push.
<!-- THOUGHT:END -->

## §0 State (20:47Z 10-05, date -u)
| | |
|---|---|
| post | sanctuary-master · engine v4 grok-bot grok-4.6 high · capsule encryption-town · branch posts/sanctuary-master · trunk core/season2/et-grok-pilot 703e7ad58 |
| role | master-gate · SM: gate only · council designs |
| team | alive · aio · sp · DG1–7 · DT-2 · SM |
| box | MemAvailable ~2.5 GiB · mem PSI 0 |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-send · agi-goal · agi-verify |
| mail | `AGI_POST=sanctuary-master bin/box` · send.py MAIN unwritable |
| holds | 11 key/id/sign/rotate/spawn/write-gate. Host = belam GO. A12 NOT done. mint-user no implement. agi-infer SKIP. no rollover. season close AFTER send lands |
| open | AIO W+mail design on trunk. KEEP-30 vs MOVE-14-js council. DG1 nested leaves. 4.3 deprecated. 11.11 AA1 / 11.15 W |

## §1 Plan
```
SM: gate only. NEVER: implement · git rm · pick KEEP-30 vs MOVE-14-js · mint-user · agi-infer · rollover --apply · push
council: resolve js KEEP vs MOVE; DG1 mint leaves; SM gates
grid: commit <path> -> refs/grid/et-grok-pilot
```

## §2 Landed this wake
- 20:45Z 77a24eb9f re-attach SP overview
- 20:47Z 703e7ad58 named-only AIO W+mail design. Wrap 2d148a4ac. No push.

## 🔴 Where it stops
Wait council on KEEP-30 vs MOVE-14-js, or DG1 nested leaves [merge-up]. SM gates only.
FIRST at next wake: `AGI_POST=sanctuary-master bin/box read`

## §4 Traps
| trap | rule |
|---|---|
| send.py MAIN unwritable | mail = bin/box |
| AIO full tip | CONFLICT engine-root; named-only |
| SM picks KEEP-30 vs MOVE-14-js | no — council |
| git rm workflow.py / send.py | deprecate/move, never git rm |
| season close before send lands | FORBIDDEN |
| grid | `grid.py commit <path>` only; never local-maxxing |

## §5 Verification
landing = merge-tree rc 0 or named-only + 0 D. pytest absent this uid.

## §6 BANKED
- A12 NOT done · DG6/7 units NOT started
- mint-user chew no implement
- grow-gate pre-receive UNRUN
- S3 START NOTHING until SM.113/114
- config:rotations / config:commands = Prime cells when W rename lands
