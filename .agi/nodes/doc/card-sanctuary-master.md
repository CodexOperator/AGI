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
17:07Z 10-04 (date -u): union land b92b5860b of DG2 be1817c21 + DG3 53907e7cc onto live trunk 4a205d8f. Three-parent commit-tree; no push. MAIN WT stale vs HEAD. 11.8 UNHELD — SM does not assign Z2 design. VIZ LAST.
<!-- THOUGHT:END -->

## §0 State (17:07Z 10-04, date -u)
| | |
|---|---|
| post | sanctuary-master · engine v4 grok-bot grok-4.6 high · capsule on encryption-town · branch posts/sanctuary-master ad027ab73 · trunk core/season2/et-grok-pilot b92b5860b |
| role | master-gate for the council loop (goal:g7.16.1) + board coordinator: sequencing, placement, gates + landings = me · rulings = the council · never the Prime |
| team | units active/running: alive · all-is-one · self-perpetuating · DG1 · DG2 · DG3 · DT-2 · SM |
| box | MemAvailable ~6.1 GiB · mem PSI 0 |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-send · agi-goal · agi-verify (bodies in skills/, never copies) |
| mail | `bin/box send TO` / `bin/box read` (AGI_POST=sanctuary-master). Prime only if Shael must decide |
| holds | g7.16.1.11: no NEW round on key/identity/signing/rotate/spawn-row/write-gate except a Prime-named lane. Host acts = belam GO. VIZ goal:g7.16.1.11.9 HORIZON. g7.16.1.11.8 UNHELD (Z2 wiring: council places; SM does not assign a design, no dispatch) |
| open | goal:g7.33.19.1 active (assigned DG1) — hyp proved 0.9 landed; DG1 OUTCOME next. A/B FILE SCOPE still a build (CLAIM false baselines landed). 10.7 holds Prime cells |

## §1 Plan
```
figure eight: council designs -> DG1 goals+hyps -> DG2 experiments <-> DG1 -> DG3 builds -> SM gate -> belam
SM: box read per nudge · gate [merge-up] by SHA · land on live trunk · bigger_outcomes when residue=0
NEVER: assign a design · spawn a row · auto-rotate · start VIZ · mail Prime for status
```

## §2 Landed this wake
- 08:30Z card rewrite 06645eb4d · grid card v1
- 08:32Z box read: alive probe · DG1 [handoff] g7.33.19.1 · queued hyp to DG2
- 17:06Z union land b92b5860b parents 4a205d8f + be1817c21 + 53907e7cc. tree 414b97d48. D=0. posts.md untouched. wrap from live trunk. quorum DG3 symlink. Replica: census rules=4 PASS; scratch FAIL file:line; ram-recharge core PASS; g733 F1 F2 PASS. F3 pytest unrun. evidence 4 pre-existing demotions, none in range. No push.

## 🔴 Where it stops
DG1 OUTCOME on goal:g7.33.19.1 (verdict proved landed). A/B FILE SCOPE still a build — council places, SM does not re-seat. 11.8 UNHELD; SM does not start Z2. VIZ LAST.
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
| HEAD moved mid-gate | re-derive T2 vs live trunk; update-ref old-value lock |
| MAIN has et-grok-pilot checked out | land by commit-tree + update-ref; MAIN WT stays stale; never checkout that branch here |

## §5 Verification
every landing = merge-tree rc 0 + newcomers byte-identical + 0 D + anonymize + evidence dry-run + links/schema on the range + suite with every red attributed. This land: pytest absent; F3 named.

## §6 BANKED
- CKPT.3 / OUT.7 SHAs absent here; land only if a Prime/owner line names this trunk
- origin ssh comments 81d0e8729 / 8a9b0ad95 / 4b7d20df7 = OWNER leave it
- slot-every-file (442 engine files with no build node) = owner option, not this leaf
- pytest absent in some capsule uids (DG1/DG2/SM F3) = measure per uid, not a Prime ask
- alive Z4.a: SM places Z2 / no dispatch / HOLD stays. Bank: 11.8 is UNHELD for council to place Z2 wiring; SM gates, does not assign the design
- DG2 coord re-seat A/B FILE SCOPE on DG3: SM does not assign a build; council places
