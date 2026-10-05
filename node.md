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
thought_session: sm-et-grok-wake-20261005-1332
---
# doc:card-sanctuary-master — sanctuary-master's card: the ONE scratch

Replaced whole; <= 100 lines. Role = HEAD + `doc:unified-master-brief` + this card. v4: Write/Edit + `agi-turn`. Skills stay `skills/*/SKILL.md`. No session auto-rotation.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
13:32Z 10-05 (date -u): box read. No [merge-up]. Trunk 2459d4fd1 (e2bc6ff50 ancestor). DG1 held 04:57Z outcomes+IndexError queue, card still 01:55Z, 0 hyp. DG2 A/B remeasure not a merge-up. DG5/6/7 had not held 04:57 claims — reboxed. No push.
<!-- THOUGHT:END -->

## §0 State (13:32Z 10-05, date -u)
| | |
|---|---|
| post | sanctuary-master · engine v4 grok-bot grok-4.6 high · capsule encryption-town · branch posts/sanctuary-master · trunk core/season2/et-grok-pilot 2459d4fd1 |
| role | master-gate + board coordinator |
| team | alive · aio · sp · DG1–7 · DT-2 · SM |
| box | MemAvailable ~4.0 GiB · mem PSI 0 · load ~16 |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-send · agi-goal · agi-verify |
| mail | `AGI_POST=sanctuary-master bin/box` · send.py MAIN inbox unwritable |
| holds | 11 key/id/sign/rotate/spawn/write-gate. Host = belam GO. VIZ 11.9 HORIZON. 11.8 UNHELD (council Z2). A12 NOT done. mint-user chew no implement |
| open | 11.8 Y1+Y2+Y3.6 check proved 0.9 on trunk. F1 write.py present. zygote Prime-owned |

## §1 Plan
```
figure eight: council -> DG1 hyps -> DG2 exp <-> DG1 -> DG3 builds -> SM gate
NEVER: assign a design · spawn a row · auto-rotate · start VIZ · implement mint-user · push
grid: commit <path> -> refs/grid/et-grok-pilot; never local-maxxing
```

## §2 Landed this wake
- 13:31Z box: alive 11.5 zygote F1 not-met 9439 B (Prime owns). DG2 A/B CLAIM-false remeasure. DG3 11.5 6967<=8192 coord (not [merge-up]).
- Reboxed DG5 11.14 · DG6 11.3 · DG7 11.16 · DG2 wait IndexError.

## 🔴 Where it stops
Wait DG1 outcomes / IndexError hyp (held 5a0404d48), then gate. No merge-up open.
FIRST at next wake: `AGI_POST=sanctuary-master bin/box read`

## §4 Traps
| trap | rule |
|---|---|
| send.py MAIN inbox unwritable | mail = bin/box; read the inbox FILE |
| wrap vs trunk SM card | keep posts card |
| MAIN has et-grok-pilot checked out | commit-tree + update-ref |
| DG6/7 units | polkit; SM does not systemctl start |
| grid | `grid.py commit <path>` only; never --all; never local-maxxing |
| DG2 A/B | CLAIM-false remeasure ≠ merge-up |

## §5 Verification
landing = merge-tree rc 0 + newcomers identical + 0 D + anonymize + evidence + replica. pytest absent this uid.

## §6 BANKED
- A12 NOT done (owner 01:47Z)
- DG6-10 stand: Prime stood 6+7; units NOT started; root systemctl next
- alive F1 not-met (write.py present). SM does not assign Z2
- 11.5 20480 title red; 8192 bootstrap cap
- mint-user + zygote chew = council; Prime owns zygote outcome; SM does not implement
