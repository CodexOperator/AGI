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
thought_session: sm-et-grok-wake-20261005-2136
---
# doc:card-sanctuary-master — sanctuary-master's card: the ONE scratch

Replaced whole; <= 100 lines. Role = HEAD + `doc:unified-master-brief` + this card. v4: Write/Edit + `agi-turn`. Skills stay `skills/*/SKILL.md`. No session auto-rotation.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
21:34Z 10-05 (date -u): OWNER via Prime UNSIGNED, verbatim: "IMPLEMENT NOW. Prime does NOT build. Encryption-town. No push. Send (goal:g7.16.1.11.11 AA1 boxes; send.py deprecate/move, never git rm) and phase W (goal:g7.16.1.11.15) are CLEARED. Wind-down no-implement does not cover them. STANDARD LOOP only: goals -> hypotheses -> experiments -> verdicts -> outcomes -> bigger_outcomes -> overviews. No special-case shortcuts. DG/SM inner loops as usual. SM: hand the build sub-goals to idle DGs now: DG2 DG3 DG4 DG5 DG6 DG7 DT2. Place leaves on the town board. Council design is settled. Season close AFTER both land. Manifest count: council already settling 30 vs 16+14. Skip agi-infer. Graph: hypothesis:phase-w-and-messaging-council-designs-then-dg-sm. Questions for Shael go belam then Grok Bot."
<!-- THOUGHT:END -->

## §0 State (21:36Z 10-05, date -u)
| | |
|---|---|
| post | sanctuary-master · engine v4 grok-bot grok-4.6 high · capsule encryption-town · branch posts/sanctuary-master · trunk core/season2/et-grok-pilot 8edae1766 |
| role | master-gate · IMPLEMENT NOW · Prime does not build |
| team | alive · aio · sp · DG1–7 · DT-2 · SM |
| box | MemAvailable ~2.9 GiB · mem PSI 0 · load ~12 |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-send · agi-goal · agi-verify |
| mail | `AGI_POST=sanctuary-master bin/box` · send.py MAIN unwritable · DT-2 off-matrix |
| holds | 11 key/id/sign/rotate/spawn/write-gate except W+AA1 CLEARED. Host = belam GO. A12 NOT done. mint-user no implement. agi-infer SKIP. no rollover. season close AFTER W+send land |
| open | 11.15.1 living-16 / MOVE-14-js. 11.11.2 send.py MOVE. Board: DG1 hyps → DG2 exp → DG3 W BUILD → DG4 tests → DG5 skill re-point → DG6 AA1 BUILD → DG7 helper |

## §1 Plan
```
STANDARD LOOP: goals (landed) -> DG1 hyps -> DG2 exp/verdict -> DG3/DG6 BUILD -> SM gate
NEVER: Prime build · git rm · mint-user · agi-infer · rollover --apply · push
grid: commit <path> -> refs/grid/et-grok-pilot
```

## §2 Landed this wake
- 21:07Z 8edae1766 11.15.1 SETTLE
- 21:34Z owner IMPLEMENT NOW (verbatim THOUGHT). Board DG1–7. DT-2 off-matrix (banked). No push.

## 🔴 Where it stops
Wait DG1 hyps [merge-up] on 11.15.1 + 11.11.2, then queue DG2.
FIRST at next wake: `AGI_POST=sanctuary-master bin/box read`

## §4 Traps
| trap | rule |
|---|---|
| send.py MAIN unwritable | mail = bin/box |
| DT-2 | off-matrix; SM cannot box; bank |
| git rm workflow.py / send.py | deprecate/move, never git rm |
| season close before W+send land | FORBIDDEN |
| special-case shortcuts | no — standard loop only (owner 21:34Z) |
| grid | `grid.py commit <path>` only; never local-maxxing |

## §5 Verification
landing = merge-tree rc 0 or named-only + 0 D. pytest absent this uid.

## §6 BANKED
- A12 NOT done · DG6/7 units NOT started
- DT-2 off-matrix — Prime/owner if that seat must take a leaf
- mint-user chew no implement
- grow-gate pre-receive UNRUN
- S3 START NOTHING until SM.113/114
- config:rotations / config:commands = Prime cells when W rename lands
