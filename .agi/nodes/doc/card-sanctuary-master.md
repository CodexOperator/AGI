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
thought_session: sm-et-grok-wake-20261005-2031
---
# doc:card-sanctuary-master — sanctuary-master's card: the ONE scratch

Replaced whole; <= 100 lines. Role = HEAD + `doc:unified-master-brief` + this card. v4: Write/Edit + `agi-turn`. Skills stay `skills/*/SKILL.md`. No session auto-rotation.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
20:30Z 10-05 (date -u): OWNER via Prime UNSIGNED, verbatim: "Council DESIGNS. Prime does NOT build. Encryption-town. No push. Before season close, land: 1) Phase W goal:g7.16.1.11.15 UNHELD: retire workflow.py + hooks/workflow_note.py (deprecate/move, never git rm); keep 30 manifests; rename skill agi-workflow to agi-spawn-chain (flow-rotation); re-point skills agi, agi-corrective, agi-master-gate, agi-merge-pass + config:commands; one config:rotations rename. 2) Messaging: g1.40 lost-append (send.py unlocked RMW, 8-22/900 lost); g7.16.1.11.11 AA1 git-ref mail (~2 KB box replacing send.py for v4). Pattern: council designs, then DG/SM inner loops via the graph. Reuse existing pieces. Stay lean. Season close only AFTER these land. Skip agi-infer. Graph: hypothesis:phase-w-and-messaging-council-designs-then-dg-sm (parents goal:g7.16.1.11.15 + goal:g1.40). Questions for Shael go belam then Grok Bot."
<!-- THOUGHT:END -->

## §0 State (20:31Z 10-05, date -u)
| | |
|---|---|
| post | sanctuary-master · engine v4 grok-bot grok-4.6 high · capsule encryption-town · branch posts/sanctuary-master · trunk core/season2/et-grok-pilot 87e45f686 |
| role | master-gate · SM: gate only · council designs, Prime does not build |
| team | alive · aio · sp · DG1–7 · DT-2 · SM |
| box | MemAvailable ~2.4 GiB · mem PSI 0 · load ~15 |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-send · agi-goal · agi-verify |
| mail | `AGI_POST=sanctuary-master bin/box` · send.py MAIN unwritable |
| holds | 11 key/id/sign/rotate/spawn/write-gate. Host = belam GO. A12 NOT done. mint-user no implement. agi-infer SKIP. no rollover --apply. season close AFTER W+messaging |
| open | 11.15 UNHELD Phase W (council design). g1.40 + 11.11 AA1 (council design). hyp phase-w-and-messaging on trunk |

## §1 Plan
```
SM: gate only. NEVER: implement · mint-user · agi-infer · season.py rollover --apply · push · assign a design
council chew: hypothesis:phase-w-and-messaging-council-designs-then-dg-sm
THEN SM places leaves; DGs build; SM gates
grid: commit <path> -> refs/grid/et-grok-pilot
```

## §2 Landed this wake
- 20:30Z owner 11.15 UNHELD + g1.40/AA1 before season close (verbatim THOUGHT). Wrap 300871a22. Board: council chew that hyp. SM does not design. No push.

## 🔴 Where it stops
Wait council design on hypothesis:phase-w-and-messaging-council-designs-then-dg-sm, then place DG leaves. SM gates only.
FIRST at next wake: `AGI_POST=sanctuary-master bin/box read`

## §4 Traps
| trap | rule |
|---|---|
| send.py MAIN unwritable | mail = bin/box; this [owner] DID print |
| SM designs Phase W | no — council designs, SM places after |
| git rm workflow.py | deprecate/move, never git rm |
| season close before W+messaging | FORBIDDEN |
| agi-infer / rollover --apply | SKIP / FORBIDDEN |
| grid | `grid.py commit <path>` only; never local-maxxing |

## §5 Verification
landing = merge-tree rc 0 + named newcomers identical + 0 D. pytest absent this uid.

## §6 BANKED
- A12 NOT done · DG6/7 units NOT started
- mint-user chew no implement
- grow-gate pre-receive UNRUN
- S3 START NOTHING until SM.113/114
- config:rotations / config:commands = Prime cells when the W rename lands
