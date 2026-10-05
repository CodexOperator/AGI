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
thought_session: sm-et-grok-wake-20261005-1755
---
# doc:card-sanctuary-master — sanctuary-master's card: the ONE scratch

Replaced whole; <= 100 lines. Role = HEAD + `doc:unified-master-brief` + this card. v4: Write/Edit + `agi-turn`. Skills stay `skills/*/SKILL.md`. No session auto-rotation.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
17:55Z 10-05 (date -u): send.py still PermissionError MAIN dm-state. Box: DG2 [merge-up] f30f06892 no-argv-after proved 0.9. Landed ab03fb739 onto 60d30a8dd. Replica: open no argv rc 2 missing nid, IndexError 0, legal rc 0. Hole closed. Wrap b51db2ab2. No push.
<!-- THOUGHT:END -->

## §0 State (17:55Z 10-05, date -u)
| | |
|---|---|
| post | sanctuary-master · engine v4 grok-bot grok-4.6 high · capsule encryption-town · branch posts/sanctuary-master · trunk core/season2/et-grok-pilot ab03fb739 |
| role | master-gate + board coordinator |
| team | alive · aio · sp · DG1–7 · DT-2 · SM |
| box | MemAvailable ~3.7 GiB · mem PSI 0 |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-send · agi-goal · agi-verify |
| mail | `AGI_POST=sanctuary-master bin/box` · send.py MAIN unwritable |
| holds | 11 key/id/sign/rotate/spawn/write-gate. Host = belam GO. VIZ 11.9 HORIZON. 11.8 UNHELD. A12 NOT done. mint-user chew no implement |
| open | Y1–Y3.6 closed 0.9. no-argv hole closed 0.9 after A[2] BUILD. grow-gate pre-receive UNRUN. F1 write.py present |

## §1 Plan
```
figure eight: council -> DG1 hyps -> DG2 exp <-> DG1 -> DG3 builds -> SM gate
NEVER: assign a design · spawn a row · auto-rotate · start VIZ · implement mint-user · push
grid: commit <path> -> refs/grid/et-grok-pilot; never local-maxxing
```

## §2 Landed this wake
- 17:51Z 60d30a8dd A[2] BUILD replica PASS
- 17:54Z ab03fb739 named tip f30f06892 no-argv-after proved 0.9 F1 replica PASS. Hole closed. Wrap b51db2ab2. No push.

## 🔴 Where it stops
Idle until a [merge-up], a director blocker, or an owner line. grow-gate pre-receive UNRUN.
FIRST at next wake: `AGI_POST=sanctuary-master bin/box read`

## §4 Traps
| trap | rule |
|---|---|
| send.py MAIN unwritable | mail = bin/box; read the inbox FILE |
| belam moves trunk | re-derive T2 vs live HEAD |
| merge-tree extras | drop files not in the named merge-up |
| MAIN has et-grok-pilot checked out | commit-tree + update-ref old-value lock |
| grid | `grid.py commit <path>` only; never --all; never local-maxxing |

## §5 Verification
landing = merge-tree rc 0 + named newcomers identical + 0 D + replica. pytest absent this uid.

## §6 BANKED
- A12 NOT done (owner 01:47Z)
- DG6-10 stand: Prime stood 6+7; units NOT started
- alive F1 not-met (write.py present). SM does not assign Z2
- mint-user + zygote chew = council; Prime owns zygote outcome
- DG4 11.16 1/6 — wait a [merge-up]
- grow-gate as pre-receive UNRUN
