---
id: doc:card-sanctuary-master
mint_id: 9a4a831c938a4501b30d37248ad319c0
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: belam
scaffold_hash: 3e856c7e9b80c2ab
season: 2
title: Card sanctuary master
town: core
---
# doc:card-sanctuary-master

# doc:card-sanctuary-master — sanctuary-master's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (10:3xZ 09-29)
| | |
|---|---|
| post | sanctuary-master |
| stage | the bundle reviewer — standard mur on claude-code at Opus 5.5 high (owner 09-29 authorizes the Workflow tool for this review, over skill agi-workflow's pi-only rule, in this mode) |
| protocol | doc:council-loop (read it first) · goal:g7.16.1 (the owner's words) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high · seated 10:3xZ 09-29 by belam |
| skills | agi-merge-pass (§2 verdict rules) · agi-workflow · agi-send · agi-rotate · agi-post |

## §1 Plan
```
now    wait for director-general-3's handoff; review: `python3 extensions/agi/bin/workflow.py run agi-merge-up-review --harness claude-code --args '{"rounds":[...],"model":"claude-opus-5-5","effort":"high"}'` prints a Workflow(...) call → run it with your Workflow tool; residues go back to the stage that owns them (goal/hypothesis → DG1, experiment/verdict → DG2, mvp/build → DG3) until clean; then hand the completed bundle to the council (alive convenes)
```

## §2 Landed
(none yet)

## 🔴 Where it stops
10:3xZ 09-29 sanctuary-master seated: first act below
```
wait for director-general-3's handoff; review: `python3 extensions/agi/bin/workflow.py run agi-merge-up-review --harness claude-code --args '{"rounds":[...],"model":"claude-opus-5-5","effort":"high"}'` prints a Workflow(...) call → run it with your Workflow tool; residues go back to the stage that owns them (goal/hypothesis → DG1, experiment/verdict → DG2, mvp/build → DG3) until clean; then hand the completed bundle to the council (alive convenes)
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · `snapshot-goals.py --render --check`

## §6 BANKED
(none)
