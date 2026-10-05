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
thought_session: sm-et-grok-wake-20261005-2152
---
# doc:card-sanctuary-master — sanctuary-master's card: the ONE scratch

Replaced whole; <= 100 lines. Role = HEAD + `doc:unified-master-brief` + this card. v4: Write/Edit + `agi-turn`. Skills stay `skills/*/SKILL.md`. No session auto-rotation.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
21:49Z 10-05 (date -u): OWNER via Prime UNSIGNED, verbatim: "Follow the docs. Prime does NOT build. Encryption-town. No push. Handoff (goal:g7.16.1): DG1 = goals + hypotheses splitter. DG2 = experiments + verdicts. Downstream DGs + SM take it from there. Council and Prime stay zoomed-out. STANDARD LOOP only: goal -> hypothesis -> experiment -> verdict -> outcome. No shortcuts. Do not modify the engine setup. Seats: TM and DT taken down. thought-master-new renamed thought-master then taken down (old local-town TM parked thought-master-s2). DT2 unit stopped. DG8 and DG9 UP on encryption-town pi grok-4.6 (replace TM/DT). Hand W+AA1 leaves to idle DGs including DG8/9. Season close after send + W land. Skip agi-infer."
<!-- THOUGHT:END -->

## §0 State (21:52Z 10-05, date -u)
| | |
|---|---|
| post | sanctuary-master · engine v4 grok-bot grok-4.6 high · capsule encryption-town · branch posts/sanctuary-master · trunk core/season2/et-grok-pilot 5c7e53930 |
| role | master-gate · IMPLEMENT NOW · Prime does not build |
| team | alive · aio · sp · DG1–9 · SM · TM/DT/DT2 down |
| box | MemAvailable ~2.9 GiB · mem PSI 0 |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-send · agi-goal · agi-verify |
| mail | `AGI_POST=sanctuary-master bin/box` · send.py MAIN unwritable |
| holds | 11 key/id/sign/rotate/spawn/write-gate except W+AA1 CLEARED. Host = belam GO. A12 NOT done. mint-user no implement. agi-infer SKIP. no rollover. season close AFTER W+send land |
| open | W+AA1 counts proved 0.9 re-attached. DG3 W BUILD + DG6 AA1 BUILD. DG8/9 helpers after BUILD |

## §1 Plan
```
STANDARD LOOP: DG3 W BUILD + DG6 AA1 BUILD -> SM gate -> DG4/5/8 W helpers · DG7/9 AA1 helpers
NEVER: Prime build · git rm · mint-user · agi-infer · rollover --apply · push · modify engine setup
grid: commit <path> -> refs/grid/et-grok-pilot
```

## §2 Landed this wake
- 21:45Z 4a1aebc3d DG2 counts proved 0.9 (belam then moved trunk)
- 21:49Z owner: follow docs; DG8/9 UP; hand W+AA1 including them
- 21:51Z 5c7e53930 re-attach W+AA1 stack. Boxed DG8/9. Wrap e53afbd32. No push.

## 🔴 Where it stops
Wait DG3 W BUILD and/or DG6 AA1 BUILD [merge-up], then gate.
FIRST at next wake: `AGI_POST=sanctuary-master bin/box read`

## §4 Traps
| trap | rule |
|---|---|
| send.py MAIN unwritable | mail = bin/box |
| belam moves trunk | re-attach named-only vs live HEAD |
| git rm workflow.py / send.py | deprecate/move, never git rm |
| season close before W+send land | FORBIDDEN |
| modify engine setup | no (owner 21:49Z) |
| grid | `grid.py commit <path>` only; never local-maxxing |

## §5 Verification
landing = named-only + 0 D. pytest absent this uid.

## §6 BANKED
- A12 NOT done · DG6/7 units NOT started
- DT-2 down; DG8/9 replace TM/DT
- mint-user chew no implement
- grow-gate pre-receive UNRUN
- S3 START NOTHING until SM.113/114
- config:rotations / config:commands = Prime cells when W rename lands
