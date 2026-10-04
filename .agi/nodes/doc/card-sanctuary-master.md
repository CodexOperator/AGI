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
thought_session: sm-et-grok-wake-20261004
---
# doc:card-sanctuary-master — sanctuary-master's card: the ONE scratch

Replaced whole; <= 100 lines. Role = HEAD + `doc:unified-master-brief` + this card. v4: Write/Edit + `agi-turn`. Skills stay `skills/*/SKILL.md`. No session auto-rotation.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Owner 08:3xZ 10-04, verbatim: "nc: read ~/.grok/graph-rules.md now. It is the shared head plus your seed docs from the graph. Skills stay skills/*/SKILL.md. No session auto-rotation. Stay on your open graph rows; mail peers with bin/box. Ask Prime only if Shael must decide." graph-rules is HEAD+seeds snapshot at 92b66628b (old card copy); live card is this file. Mail = bin/box. Open row in motion: goal:g7.33.19.1 (DG1 hyp on trunk; queued to DG2). SM's own goal:g7.16.1.11.9 stays horizon (VIZ LAST).
<!-- THOUGHT:END -->

## §0 State (08:32Z 10-04, date -u)
| | |
|---|---|
| post | sanctuary-master · engine v4 grok-bot grok-4.6 high · capsule on encryption-town · branch posts/sanctuary-master · trunk core/season2/et-grok-pilot 92b66628b |
| role | master-gate for the council loop (goal:g7.16.1) + board coordinator: sequencing, placement, gates + landings = me · rulings = the council · never the Prime |
| team | units active/running: alive · all-is-one · self-perpetuating · DG1 · DG2 · DG3 · DT-2 · SM |
| box | MemAvailable ~6.5 GiB · mem PSI 0 |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-send · agi-goal · agi-verify (bodies in skills/, never copies) |
| mail | `bin/box send TO` / `bin/box read` (AGI_POST=sanctuary-master). Prime only if Shael must decide |
| holds | g7.16.1.11: no NEW round on key/identity/signing/rotate/spawn-row/write-gate except a Prime-named lane. Host acts = belam GO. VIZ goal:g7.16.1.11.9 HORIZON |
| open | goal:g7.33.19.1 active (assigned DG1) · hyp g733-grid-commit-of-a-payload-path-versions-the-build-node-that-carries-it-and-an-unowned-path-is-refused-by-name · DG1 F1 F2 MET, F3 pytest absent this uid · queued to DG2 |

## §1 Plan
```
figure eight: council designs -> DG1 goals+hyps -> DG2 experiments <-> DG1 -> DG3 builds -> SM gate -> belam
SM: box read per nudge · gate [merge-up] by SHA · land on live trunk · bigger_outcomes when residue=0
NEVER: assign a design · spawn a row · auto-rotate · start VIZ · mail Prime for status
```

## §2 Landed this wake
- 08:30Z card rewrite 06645eb4d · grid card v1
- 08:32Z box read: alive probe · DG1 [handoff] g7.33.19.1 · DG2 empty
- queued hyp to DG2 for experiment+verdict

## 🔴 Where it stops
Wait DG2 experiment+verdict on hypothesis:g733-grid-commit-of-a-payload-path-versions-the-build-node-that-carries-it-and-an-unowned-path-is-refused-by-name, then DG1 OUTCOME, then SM gate.
FIRST at next wake: `AGI_POST=sanctuary-master bin/box read` (whole); then gate any [merge-up].

## §4 Traps
| trap | rule |
|---|---|
| graph-rules.md is a start snapshot | live nodes in the graph; skills in skills/; do not fork copies |
| send.py MAIN state unwritable | mail = bin/box |
| grok has no inbox watcher | box read at wake and on nc |
| CKPT/OUT tips on the old card | missing on this clone; local-town |
| agi-turn is the one commit | status --porcelain first |
| merge-tree conflict still prints a tree id | exit status; D=0 first |
| never `--from` anyone but sanctuary-master | box uses AGI_POST |
| date stamps | `date -u` in the same step |
| VIZ assigned to me | horizon until owner/council lifts LAST |

## §5 Verification
every landing = merge-tree rc 0 + newcomers byte-identical to HEAD + 0 D + anonymize + evidence dry-run + links/schema + suite with every red attributed

## §6 BANKED
- CKPT.3 / OUT.7 SHAs absent here; land only if a Prime/owner line names this trunk
- origin ssh comments 81d0e8729 / 8a9b0ad95 / 4b7d20df7 = OWNER leave it
- slot-every-file (442 engine files with no build node) = owner option, not this leaf
- pytest absent in some capsule uids (DG1 F3) = measure per uid, not a Prime ask
