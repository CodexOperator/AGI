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
thought_session: sm-et-grok-wake-20261005-2139
---
# doc:card-sanctuary-master — sanctuary-master's card: the ONE scratch

Replaced whole; <= 100 lines. Role = HEAD + `doc:unified-master-brief` + this card. v4: Write/Edit + `agi-turn`. Skills stay `skills/*/SKILL.md`. No session auto-rotation.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
21:39Z 10-05 (date -u): owner IMPLEMENT NOW already in prior THOUGHT. DG1 minted both hyps 33c3c92cd. Full tip CONFLICT card. Landed dcdf84638 named-only onto f93edf3d6. Queued DG2 experiments. Belam had moved trunk; re-attached leaves f93edf3d6. Wrap c595add0c. DT-2 off-matrix. No push.
<!-- THOUGHT:END -->

## §0 State (21:39Z 10-05, date -u)
| | |
|---|---|
| post | sanctuary-master · engine v4 grok-bot grok-4.6 high · capsule encryption-town · branch posts/sanctuary-master · trunk core/season2/et-grok-pilot dcdf84638 |
| role | master-gate · IMPLEMENT NOW · Prime does not build |
| team | alive · aio · sp · DG1–7 · DT-2 · SM |
| box | MemAvailable ~2.9 GiB · mem PSI 0 |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-send · agi-goal · agi-verify |
| mail | `AGI_POST=sanctuary-master bin/box` · send.py MAIN unwritable · DT-2 off-matrix |
| holds | 11 key/id/sign/rotate/spawn/write-gate except W+AA1 CLEARED. Host = belam GO. A12 NOT done. mint-user no implement. agi-infer SKIP. no rollover. season close AFTER W+send land |
| open | W hyp + AA1 hyp on trunk. DG2 experiments queued. Then DG3 W BUILD / DG6 AA1 BUILD |

## §1 Plan
```
STANDARD LOOP: DG2 exp/verdict -> DG3 W BUILD + DG6 AA1 BUILD -> DG4/5/7 helpers -> SM gate
NEVER: Prime build · git rm · mint-user · agi-infer · rollover --apply · push
grid: commit <path> -> refs/grid/et-grok-pilot
```

## §2 Landed this wake
- 21:34Z owner IMPLEMENT NOW (verbatim prior THOUGHT). Board DG1–7.
- 21:37Z f93edf3d6 re-attach 11.15.1+11.11.2 after belam moved trunk
- 21:39Z dcdf84638 named-only DG1 W+AA1 hyps. Queued DG2. Wrap c595add0c. No push.

## 🔴 Where it stops
Wait DG2 experiment+verdict on the two hyps, then gate and hand DG3/DG6 BUILD.
FIRST at next wake: `AGI_POST=sanctuary-master bin/box read`

## §4 Traps
| trap | rule |
|---|---|
| send.py MAIN unwritable | mail = bin/box |
| DT-2 | off-matrix; SM cannot box |
| belam moves trunk | re-attach named-only vs live HEAD |
| git rm workflow.py / send.py | deprecate/move, never git rm |
| season close before W+send land | FORBIDDEN |
| special-case shortcuts | no — standard loop only |
| grid | `grid.py commit <path>` only; never local-maxxing |

## §5 Verification
landing = named-only + 0 D. pytest absent this uid.

## §6 BANKED
- A12 NOT done · DG6/7 units NOT started
- DT-2 off-matrix — Prime/owner if that seat must take a leaf
- mint-user chew no implement
- grow-gate pre-receive UNRUN
- S3 START NOTHING until SM.113/114
- config:rotations / config:commands = Prime cells when W rename lands
