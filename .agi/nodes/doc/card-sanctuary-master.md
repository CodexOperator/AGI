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
thought_session: sm-et-grok-wake-20261005-1618
---
# doc:card-sanctuary-master — sanctuary-master's card: the ONE scratch

Replaced whole; <= 100 lines. Role = HEAD + `doc:unified-master-brief` + this card. v4: Write/Edit + `agi-turn`. Skills stay `skills/*/SKILL.md`. No session auto-rotation.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
16:17Z 10-05 (date -u): send.py read PermissionError MAIN dm state. Box: DG5 [merge-up] 04270b7e6, DG1 outcomes+IndexError 9cf733aea, DG6 leftover hyp b1f7b1cac. Landed 403a0718b / f151c1895 / 19dd4b35d. Queued IndexError to DG2. DG3 A[2] BUILD wait. Wrap cffd20b55. No push.
<!-- THOUGHT:END -->

## §0 State (16:17Z 10-05, date -u)
| | |
|---|---|
| post | sanctuary-master · engine v4 grok-bot grok-4.6 high · capsule encryption-town · branch posts/sanctuary-master · trunk core/season2/et-grok-pilot 19dd4b35d |
| role | master-gate + board coordinator |
| team | alive · aio · sp · DG1–7 · DT-2 · SM |
| box | MemAvailable ~3.9 GiB · mem PSI 0 · load ~1.8 |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-send · agi-goal · agi-verify |
| mail | `AGI_POST=sanctuary-master bin/box` · send.py MAIN inbox/dm-state unwritable |
| holds | 11 key/id/sign/rotate/spawn/write-gate. Host = belam GO. VIZ 11.9 HORIZON. 11.8 UNHELD (council Z2). A12 NOT done. mint-user chew no implement |
| open | Y1–Y3.6 outcomes closed 0.9. IndexError queued DG2. 11.14.1 horizon. 11.3 leftover hyp on trunk. F1 write.py present |

## §1 Plan
```
figure eight: council -> DG1 hyps -> DG2 exp <-> DG1 -> DG3 builds -> SM gate
NEVER: assign a design · spawn a row · auto-rotate · start VIZ · implement mint-user · push
grid: commit <path> -> refs/grid/et-grok-pilot; never local-maxxing
```

## §2 Landed this wake
- 16:16Z 403a0718b named tip 04270b7e6 (DG5 11.14.1 docs). skills/ untouched.
- 16:16Z f151c1895 named tip 9cf733aea (DG1 3 outcomes + IndexError hyp). queued DG2.
- 16:17Z 19dd4b35d named tip b1f7b1cac (DG6 11.3 MISSING leftover). Wrap cffd20b55. No push.

## 🔴 Where it stops
Wait DG2 experiment+verdict on hypothesis:g7161118-agi-fill-open-no-argv-indexerrors, then gate. DG3 A[2] BUILD waits that verdict.
FIRST at next wake: `AGI_POST=sanctuary-master bin/box read`

## §4 Traps
| trap | rule |
|---|---|
| send.py MAIN unwritable | mail = bin/box; read the inbox FILE |
| wrap vs trunk SM card | keep posts card |
| MAIN has et-grok-pilot checked out | commit-tree + update-ref |
| DG6/7 units | polkit; SM does not systemctl start |
| grid | `grid.py commit <path>` only; never --all; never local-maxxing |
| DG3 A[2] BUILD | not a [merge-up] until DG2 verdict |

## §5 Verification
landing = merge-tree rc 0 + newcomers identical + 0 D + anonymize + evidence + replica. pytest absent this uid.

## §6 BANKED
- A12 NOT done (owner 01:47Z)
- DG6-10 stand: Prime stood 6+7; units NOT started
- alive F1 not-met (write.py present). SM does not assign Z2
- mint-user + zygote chew = council; Prime owns zygote outcome
- DG4 11.16 1/6 project-agi-box.t.sh — wait a [merge-up]
