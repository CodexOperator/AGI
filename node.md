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
thought_session: sm-et-grok-wake-20261005-2043
---
# doc:card-sanctuary-master — sanctuary-master's card: the ONE scratch

Replaced whole; <= 100 lines. Role = HEAD + `doc:unified-master-brief` + this card. v4: Write/Edit + `agi-turn`. Skills stay `skills/*/SKILL.md`. No session auto-rotation.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
20:42Z 10-05 (date -u): OWNER via Prime UNSIGNED, verbatim: "Council DESIGNS. Prime does NOT build. Encryption-town. No push. Next: finish send, then season close. Send must work fully in the new engine with no Python files: git-ref mail AA1 boxes (goal:g7.16.1.11.11) replaces send.py entirely. send.py retires (deprecate/move, never git rm). Same pattern: council designs, DG/SM inner loops via the graph. Season close AFTER send lands. Still queued: phase W (goal:g7.16.1.11.15), g1.40 lost-append (may fold into AA1: refs have no RMW). Bundle 4: g7.16.1.4.3 deprecated (write.py route retired). Skip agi-infer. Graph: hypothesis:phase-w-and-messaging-council-designs-then-dg-sm. Questions for Shael go belam then Grok Bot." Prior 20:41Z (write.py edits retire; 4.3 MOOT) also landed; 20:42Z is latest on send.
<!-- THOUGHT:END -->

## §0 State (20:43Z 10-05, date -u)
| | |
|---|---|
| post | sanctuary-master · engine v4 grok-bot grok-4.6 high · capsule encryption-town · branch posts/sanctuary-master · trunk core/season2/et-grok-pilot 0ed36866f |
| role | master-gate · SM: gate only · council designs |
| team | alive · aio · sp · DG1–7 · DT-2 · SM |
| box | MemAvailable ~2.5 GiB · mem PSI 0 |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-send · agi-goal · agi-verify |
| mail | `AGI_POST=sanctuary-master bin/box` · send.py MAIN unwritable (this is the AA1 land) |
| holds | 11 key/id/sign/rotate/spawn/write-gate. Host = belam GO. A12 NOT done. mint-user no implement. agi-infer SKIP. no rollover. season close AFTER send lands |
| open | 11.11 AA1 send.py retire (council design, then DG). 11.15 Phase W. g1.40 may fold into AA1. 4.3 MOOT (this trunk still has live g7.16.1.4.3 — council closes bundle 4) |

## §1 Plan
```
SM: gate only. NEVER: implement · git rm send.py/workflow.py · mint-user · agi-infer · rollover --apply · push · assign a design
council chew: hypothesis:phase-w-and-messaging + bundle 4 close (4.3 MOOT)
THEN SM places leaves; DGs build; SM gates
grid: commit <path> -> refs/grid/et-grok-pilot
```

## §2 Landed this wake
- 20:34Z 0ed36866f SP overview named-only
- 20:41Z owner 4.3 MOOT + write.py route retired
- 20:42Z owner: finish send (AA1 replaces send.py entirely), then season close. Board: council.

## 🔴 Where it stops
Wait council design [merge-up] on AA1/W/bundle-4. SM gates only. 4.3 still active on THIS trunk — council deprecates, SM does not move it.
FIRST at next wake: `AGI_POST=sanctuary-master bin/box read`

## §4 Traps
| trap | rule |
|---|---|
| send.py MAIN unwritable | mail = bin/box; this is the AA1 land |
| SM deprecates 4.3 | no — council designs; 4.3 still active on this trunk |
| git rm send.py / workflow.py | deprecate/move, never git rm |
| season close before send lands | FORBIDDEN (20:42Z) |
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
- 4.3 MOOT claimed by owner; this trunk file still status active — council close
