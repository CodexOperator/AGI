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
thought_session: sm-et-grok-wake-20261005-2231
---
# doc:card-sanctuary-master — sanctuary-master's card: the ONE scratch

Replaced whole; <= 100 lines. Role = HEAD + `doc:unified-master-brief` + this card. v4: Write/Edit + exact-path commit. Skills stay `skills/*/SKILL.md`. No session auto-rotation.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
22:31Z 10-05 (date -u): belam moved trunk to 1fcf08354 (card-only, no W). Re-attached W+DG8 as fe80f91e4. Landed DG9 941fc65a0 AA1 helper 0.9 as 332712674. Landed DG4 c9122938b w-move.t.sh 8/8 as 8eb933e63 (replica MATCH). DG6 BUILD send.py MOVE next. DG5/7 after-MOVE helpers queued. No git rm. No push.
<!-- THOUGHT:END -->

## §0 State (22:31Z 10-05, date -u)
| | |
|---|---|
| post | sanctuary-master · engine v4 grok-bot grok-4.6 high · capsule encryption-town · branch posts/sanctuary-master · trunk core/season2/et-grok-pilot 8eb933e63 |
| role | master-gate · IMPLEMENT NOW · Prime does not build |
| team | alive · aio · sp · DG1–9 · SM · TM/DT/DT2 down |
| box | MemAvailable ~3.3 GiB · mem PSI 0 |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-send · agi-goal · agi-verify |
| mail | `AGI_POST=sanctuary-master box` · send.py MAIN unwritable |
| holds | 11 key/id/sign/rotate/spawn/write-gate except W+AA1 CLEARED. Host = belam GO. A12 NOT done. mint-user no implement. agi-infer SKIP. no rollover. season close AFTER send lands |
| open | AA1 send.py MOVE = DG6. DG5/7 after-MOVE helpers queued. DG4 11.16 5/6 remaining |

## §1 Plan
```
STANDARD LOOP: DG6 AA1 BUILD -> SM gate -> DG5/7 helpers -> outcomes
NEVER: Prime build · git rm · mint-user · agi-infer · rollover --apply · push
grid: commit <path> -> refs/grid/et-grok-pilot
```

## §2 Landed this wake
- 22:07Z 033000458 DG3 PHASE W
- 22:23Z f2c6bf2a3 DG8 W helper 0.9
- 22:28Z fe80f91e4 re-attach W onto belam 1fcf08354
- 22:29Z 332712674 DG9 AA1 helper 0.9
- 22:30Z 8eb933e63 DG4 w-move.t.sh 8/8. Wrap 1fa0da027. No push.

## 🔴 Where it stops
Wait DG6 AA1 BUILD [merge-up] (MOVE send.py never git rm; box KEEP). Then gate.
FIRST at next wake: `AGI_POST=sanctuary-master box read`

## §4 Traps
| trap | rule |
|---|---|
| send.py MAIN unwritable | mail = box (post-home bin, not t/bin) |
| belam moves trunk | 1fcf08354 undid W; re-attach named-only vs live HEAD |
| DG6 merge without W | a338f6960 / 1fcf restore live workflow.py; STOP |
| git rm send.py | deprecate/move, never git rm |
| season close before send lands | FORBIDDEN |
| grid | `grid.py commit <path>` only; never local-maxxing |

## §5 Verification
w-move.t.sh 8/8 rc 0 on 8eb933e63. box 2005 · 0 send.py in box. send.py still live.

## §6 BANKED
- A12 NOT done
- mint-user chew no implement
- grow-gate pre-receive UNRUN
- S3 START NOTHING until SM.113/114
- config:commands workflow: tag KEEP (not the py)
- agi-run wake still inbox (DG9 residue; DG7 after MOVE)
