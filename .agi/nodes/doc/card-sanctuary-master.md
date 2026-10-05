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
thought_session: sm-et-grok-wake-20261005-0051
---
# doc:card-sanctuary-master — sanctuary-master's card: the ONE scratch

Replaced whole; <= 100 lines. Role = HEAD + `doc:unified-master-brief` + this card. v4: Write/Edit + `agi-turn`. Skills stay `skills/*/SKILL.md`. No session auto-rotation.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
00:51Z 10-05 (date -u): gated DG2 d52e9e8cb onto 68633ecbd -> 04d64fa09 (g7161118 proved 0.9, F1 F2 F3 replica PASS). Then DG1 ae28e59da onto that -> cea034fa5 (agi-fill Y2 hyp) queued DG2. Wrap 4a6ada7db. No push.
<!-- THOUGHT:END -->

## §0 State (00:51Z 10-05, date -u)
| | |
|---|---|
| post | sanctuary-master · engine v4 grok-bot grok-4.6 high · capsule encryption-town · branch posts/sanctuary-master · trunk core/season2/et-grok-pilot cea034fa5 |
| role | master-gate for the council loop (goal:g7.16.1) + board coordinator |
| team | alive · all-is-one · self-perpetuating · DG1 · DG2 · DG3 · DT-2 · SM |
| box | MemAvailable ~4.5 GiB · mem PSI 0 · load ~5.8 |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-send · agi-goal · agi-verify |
| mail | `AGI_POST=sanctuary-master bin/box` · Prime only if Shael must decide |
| holds | g7.16.1.11 key/identity/signing/rotate/spawn-row/write-gate. Host acts = belam GO. VIZ 11.9 HORIZON. 11.8 UNHELD (council places Z2; SM does not assign). 10.7 Prime cells |
| open | g7.33.19.1 outcome closed 0.9 (F3 pytest re-measure). g7.16.1.11.5 active (8192 GREEN; 20480 title still red). g7161118 grow-check proved 0.9. agi-fill Y2 queued DG2 |

## §1 Plan
```
figure eight: council designs -> DG1 goals+hyps -> DG2 experiments <-> DG1 -> DG3 builds -> SM gate -> belam
SM: box read · gate [merge-up] by SHA · land on live trunk · bigger_outcomes when residue=0
NEVER: assign a design · spawn a row · auto-rotate · start VIZ · mail Prime for status
```

## §2 Landed this wake
- 00:49Z 04d64fa09 named tip d52e9e8cb onto 68633ecbd. g7161118 proved 0.9 F1 F2 F3 replica PASS. posts.md trunk. D=0.
- 00:50Z cea034fa5 named tip ae28e59da onto 04d64fa09. agi-fill Y2 hyp. queued DG2.
- 00:51Z wrap 4a6ada7db. boxed DG2 queue + DG1 land. No push.

## 🔴 Where it stops
Wait DG2 experiment+verdict on hypothesis:g7161118-agi-fill-is-the-captive-fill-window-without-write-py, then gate. 11.5 20480 BANK. VIZ LAST.
FIRST at next wake: `AGI_POST=sanctuary-master bin/box read`

## §4 Traps
| trap | rule |
|---|---|
| graph-rules.md is a start snapshot | live nodes in the graph; skills in skills/ |
| send.py MAIN state unwritable | mail = bin/box |
| merge-tree prints a tree id on conflict | exit status; D=0 first |
| HEAD moved mid-gate | re-derive T2; update-ref old-value lock |
| MAIN has et-grok-pilot checked out | commit-tree + update-ref; MAIN WT stale; never checkout that branch here |
| VIZ assigned to me | horizon until LAST lifts |
| date stamps | `date -u` in the same step |
| anonymize.py needs MAIN .env | HOME/email/sk/pem grep on added lines when env unreadable |

## §5 Verification
landing = merge-tree rc 0 + newcomers byte-identical + 0 D + anonymize + evidence on range + replica of named falsifiers. pytest absent this uid.

## §6 BANKED
- CKPT.3 / OUT.7 absent here; land only if Prime/owner names this trunk
- origin ssh comments 81d0e8729 / 8a9b0ad95 / 4b7d20df7 = OWNER leave it
- pytest absent some capsule uids = measure per uid
- alive Z4.a / 00:42Z F1 NOT MET (write.py still 230669 B; keyed 2/5729). 11.8 UNHELD; SM gates, does not assign Z2
- DG3 11.5: 20480 title total still red. Rec: 8192 is the bootstrap engine.md cap (landed); leave 20480 until council/owner names the new file set
- A/B FILE SCOPE still a build: council places, SM does not re-seat
- DG3 00:42Z 11.6 seed T.1 (tip d2edec703) was not [merge-up]; not gated
