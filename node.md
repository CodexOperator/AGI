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
thought_session: sm-et-grok-wake-20261005-2045
---
# doc:card-sanctuary-master — sanctuary-master's card: the ONE scratch

Replaced whole; <= 100 lines. Role = HEAD + `doc:unified-master-brief` + this card. v4: Write/Edit + `agi-turn`. Skills stay `skills/*/SKILL.md`. No session auto-rotation.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
20:45Z 10-05 (date -u): send.py still PermissionError. Box: SP chew (4.3 retired et@9eb2af142). Belam moved trunk cbed6e651 off 0ed36866f. 4.3 now deprecated on LIVE. Re-attached 77a24eb9f named-only SP overview onto that. Owner 20:42Z still: finish send then season close. Wrap 48dd3736c. No push.
<!-- THOUGHT:END -->

## §0 State (20:45Z 10-05, date -u)
| | |
|---|---|
| post | sanctuary-master · engine v4 grok-bot grok-4.6 high · capsule encryption-town · branch posts/sanctuary-master · trunk core/season2/et-grok-pilot 77a24eb9f |
| role | master-gate · SM: gate only · council designs |
| team | alive · aio · sp · DG1–7 · DT-2 · SM |
| box | MemAvailable ~2.5 GiB · mem PSI 0 |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-send · agi-goal · agi-verify |
| mail | `AGI_POST=sanctuary-master bin/box` · send.py MAIN unwritable |
| holds | 11 key/id/sign/rotate/spawn/write-gate. Host = belam GO. A12 NOT done. mint-user no implement. agi-infer SKIP. no rollover. season close AFTER send lands |
| open | 11.11 AA1 send.py retire (council). 11.15 Phase W. g1.40 may fold into AA1. 4.3 deprecated 9eb2af142. W3 remaining write/render |

## §1 Plan
```
SM: gate only. NEVER: implement · git rm send.py/workflow.py · mint-user · agi-infer · rollover --apply · push · assign a design
council chew: hypothesis:phase-w-and-messaging + bundle 4 W3
THEN SM places leaves; DGs build; SM gates
grid: commit <path> -> refs/grid/et-grok-pilot
```

## §2 Landed this wake
- 20:42Z owner: finish send then season close; 4.3 MOOT
- 20:45Z 77a24eb9f re-attach SP overview onto cbed6e651 (4.3 deprecate kept). Wrap 48dd3736c. No push.

## 🔴 Where it stops
Wait council design [merge-up] on AA1/W. SM gates only.
FIRST at next wake: `AGI_POST=sanctuary-master bin/box read`

## §4 Traps
| trap | rule |
|---|---|
| send.py MAIN unwritable | mail = bin/box |
| belam moves trunk | re-attach named-only vs live HEAD |
| git rm send.py / workflow.py | deprecate/move, never git rm |
| season close before send lands | FORBIDDEN |
| agi-infer / rollover --apply | SKIP / FORBIDDEN |
| grid | `grid.py commit <path>` only; never local-maxxing |

## §5 Verification
landing = merge-tree rc 0 + named newcomers identical + 0 D. pytest absent this uid.

## §6 BANKED
- A12 NOT done · DG6/7 units NOT started
- mint-user chew no implement
- grow-gate pre-receive UNRUN
- S3 START NOTHING until SM.113/114
- config:rotations / config:commands = Prime cells when W rename lands
