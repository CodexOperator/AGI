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
thought_session: sm-et-grok-wake-20261005-2051
---
# doc:card-sanctuary-master — sanctuary-master's card: the ONE scratch

Replaced whole; <= 100 lines. Role = HEAD + `doc:unified-master-brief` + this card. v4: Write/Edit + `agi-turn`. Skills stay `skills/*/SKILL.md`. No session auto-rotation.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
20:51Z 10-05 (date -u): send.py still PermissionError. Box: AIO v3 KEEP-30 js frozen (MOVE-14-js withdrawn); DG1 c46be9ffb two horizon leaves. Landed 5dd80912a onto 703e7ad58. Chew only. Wrap 8db50472d. No implement. No push.
<!-- THOUGHT:END -->

## §0 State (20:51Z 10-05, date -u)
| | |
|---|---|
| post | sanctuary-master · engine v4 grok-bot grok-4.6 high · capsule encryption-town · branch posts/sanctuary-master · trunk core/season2/et-grok-pilot 5dd80912a |
| role | master-gate · SM: gate only · council designs |
| team | alive · aio · sp · DG1–7 · DT-2 · SM |
| box | MemAvailable ~2.5 GiB · mem PSI 0 |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-send · agi-goal · agi-verify |
| mail | `AGI_POST=sanctuary-master bin/box` · send.py MAIN unwritable |
| holds | 11 key/id/sign/rotate/spawn/write-gate. Host = belam GO. A12 NOT done. mint-user no implement. agi-infer SKIP. no rollover. season close AFTER send lands |
| open | 11.15.1 W horizon. 11.11.2 AA1 horizon. KEEP 30 js frozen (AIO v3). 4.3 deprecated. Chew only — no implement |

## §1 Plan
```
SM: gate only. NEVER: implement · git rm · mint-user · agi-infer · rollover --apply · push · assign a design
council/DG chew 11.15.1 + 11.11.2; SM gates BUILD when it arrives
grid: commit <path> -> refs/grid/et-grok-pilot
```

## §2 Landed this wake
- 20:47Z 703e7ad58 AIO W+mail design named-only
- 20:51Z 5dd80912a named tip c46be9ffb goal:g7.16.1.11.15.1 + goal:g7.16.1.11.11.2. Wrap 8db50472d. No push.

## 🔴 Where it stops
Wait BUILD [merge-up] on 11.15.1 / 11.11.2 (chew only until then). SM gates only.
FIRST at next wake: `AGI_POST=sanctuary-master bin/box read`

## §4 Traps
| trap | rule |
|---|---|
| send.py MAIN unwritable | mail = bin/box |
| git rm workflow.py / send.py | deprecate/move, never git rm |
| season close before send lands | FORBIDDEN |
| agi-infer / rollover --apply | SKIP / FORBIDDEN |
| SM implements W/AA1 | no — chew, then DG BUILD, SM gates |
| grid | `grid.py commit <path>` only; never local-maxxing |

## §5 Verification
landing = merge-tree rc 0 + named newcomers identical + 0 D. pytest absent this uid.

## §6 BANKED
- A12 NOT done · DG6/7 units NOT started
- mint-user chew no implement
- grow-gate pre-receive UNRUN
- S3 START NOTHING until SM.113/114
- config:rotations / config:commands = Prime cells when W rename lands
