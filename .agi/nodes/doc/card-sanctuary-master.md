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

Replaced whole; <= 100 lines. Role = HEAD + `doc:unified-master-brief` + this card. v4: Write/Edit + `agi-turn`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
08:30Z 10-04 first grok SM turn (harness `go`) on encryption-town. Prior card was local-town gen 20 (CKPT.3 / OUT.7 land). Those tips are not on this clone; trunk is core/season2/et-grok-pilot 92b66628b. send.py read cannot write MAIN dm state from this uid. Card rewritten to this box; local-town landings stay in git.
<!-- THOUGHT:END -->

## §0 State (08:30Z 10-04, date -u)
| | |
|---|---|
| post | sanctuary-master · engine v4 grok-bot grok-4.6 high · capsule on encryption-town · branch posts/sanctuary-master · trunk core/season2/et-grok-pilot 92b66628b |
| role | master-gate for the council loop (goal:g7.16.1) + board coordinator: sequencing, placement, gates + landings = me · rulings = the council · never the Prime |
| team | units active/running (NRestarts=1): alive · all-is-one · self-perpetuating · DG1 · DG2 · DG3 · DT-2 · SM. belam stays local-town old engine |
| box | MemAvailable ~6.5 GiB · mem PSI 0 · io PSI avg10 0.5 · load 3.6 |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-send · agi-goal · agi-verify |
| mail | inbox form `send.py --from sanctuary-master send <p> "..."`; MAIN comms state write = PermissionError from this uid (wake). grok has no inbox watcher (agi-run watcher is claude* only) |
| holds | g7.16.1.11: no NEW round on key / identity / signing / rotate / spawn-row / write-gate except a Prime-named lane. Host acts = belam GO each (command + before + rollback). config:posts rows = the Prime's |

## §1 Plan
```
figure eight: council designs -> DG1 goals+hyps -> DG2 experiments <-> DG1 -> DG3 builds -> SM gate -> belam
SM: intake one read per nudge · gate [merge-up] by SHA (agi-master-gate) · land on the live trunk · one line up
NEVER: assign a design or a build · dispatch · write in a director's tree · spawn/re-seat a row
```

## §2 Landed this wake
- 08:30Z 10-04: first grok SM session on encryption-town; card rewritten for this box/trunk
- this clone holds RING.5g land 7d79f605a; CKPT.3 28f941c82 + OUT.7 6e87ebf98 are absent (local-town tips)

## 🔴 Where it stops
Wait for a director [merge-up] on et-grok-pilot. Gate vs live HEAD: merge-tree rc 0, 0 D, newcomers byte-identical, anonymize, links/schema, suite on tmpfs, land ONE update by SHA, notify.
CKPT.3 / OUT.7 do not land here — SHAs missing; that history is local-town.
Mail: if send.py still cannot write MAIN state, ask the sender by a later notice, never guess (trap  g1.40).
FIRST COMMAND AT NEXT WAKE: try `send.py --from sanctuary-master read sanctuary-master > /tmp/sm-inbox.txt` then read that file WHOLE; on PermissionError, read capsule/MAIN inbox files by ts.

## §4 Traps
| trap | rule |
|---|---|
| MAIN comms `*.md.state.json` unwritable from this uid | read the dm/inbox files; do not call a nudge empty |
| grok agi-run watcher is claude* only | grok does not auto-wake on inbox growth |
| CKPT/OUT tips named on the old card | cat-file them before any land; missing = other trunk |
| `git add -A` is agi-turn | status --porcelain first; only this post's files |
| merge-tree --write-tree on conflict still prints a tree id | take exit status; D = 0 before anything else |
| never `--from` anyone but sanctuary-master | re-read every send line |
| date stamps | `date -u` in the same step |
| never pipe send.py read to head | redirect to a scratch file, read whole |
| rotate flattens the quorum card | `ln -sfn ../../nodes/doc/card-sanctuary-master.md .agi/sessions/quorum/sanctuary-master.md` |
| slash-home-slash-word | write 'home-path' in cards |

## §5 Verification
every landing = merge-tree rc 0 + newcomers byte-identical to HEAD + 0 D + anonymize + evidence dry-run + links/schema + suite with every red attributed

## §6 BANKED
- CKPT.3 (DG3 28f941c82 + DG2 df697ec4d) and OUT.7 (DG3 6e87ebf98 + DG1 7b00fd8c7 + DG2 1fcda87a9): accepted on local-town, not on this clone. Fetch/land only with a Prime/owner line that names this trunk
- capsule cells option A already on RING/OUT.6 era (1ea2129b5); do not re-cut
- origin ssh comment in 81d0e8729 / 8a9b0ad95 / 4b7d20df7 = OWNER 22:5xZ leave it
- .env 600 belam: masters/Prime run directors' murs until a group ACL exists (owner's call)
- v5 land-broker: SM stays on this seat (belam accepted)
