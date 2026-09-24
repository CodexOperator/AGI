---
id: goal:g7.33.11
mint_id: 6a2604e630444966a595be177e770b5c
type: goal
parents:
  - goal:g7.33
next_edges: []
confidence: 0.9
edited_by: thought-master
goal_id: G7.33.11
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 7ab1948628cacc0b
season: 2
seeds: []
status: active
tags:
  - local-maxxing
  - engine
  - grid
title: "G7.33.11: THE GRID IN ONE BRANCH -- grid.py stores a town's grid in one named branch, so a push is one ref and the remote finally holds it"
town: core
---
# goal:g7.33.11

| | |
|---|---|
| goal | grid.py stores a town's grid in ONE named branch (the owner's example: the local-maxxing branch) -- commit writes there, log / diff / versions / payload read from there, and a push is one ref |
| origin | the owner 17:57Z + 18:17Z 09-24 (verbatim on town:local-maxxing's board): the fix NOW, worked by the director, and the 0.7 GB of failure logs cleaned up |
| measured | 18:0xZ 09-24: the grid_sync cron commits every 5 min into refs/grid/local-maxxing/ (4,293 refs, newest 17:55:42Z), but its push of refs/grid/local-maxxing/* has failed 967 times -- GitHub rejects each ref "Timed out validating rule, please try again" -> the remote holds 0 of the 4,293 (its 4,204 refs/grid refs are all outside that namespace) -> the town's grid history lives on this box's disk alone · the cron log is 775 MB of those rejection lines · 18:2xZ: what exists = grid.storage_trunk (goal:g14.14.7; config value refs/grid/local-maxxing), a per-trunk ref NAMESPACE -- still one ref per node; no verb stores or pushes the grid as one branch (core/season2/main's grid.py is unchanged since the 09-23 merge-base; ours is newer) |
| where | the branch name = a config cell per town, never a literal · the cron line = config:crons (.agi/nodes/.geometry/crons.md) |
| done | every node's version count in = out across the move (the 4,293 ref histories migrated or archived, 0 lost) · git ls-remote shows the grid branch on origin carrying the latest versions · grid.py log / diff / versions / payload read it · the cron's push is one ref and logs one summary line per run, never one line per ref · the push-rejection lines stripped from the cron log once the new push is live (before / after bytes reported) · tests pin it |
| who | director-engine NOW (the owner 18:17Z: "let the director work it"), batched by thought-master (TMM.128 -> TMM.129) |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 17 18:2xZ: the owner 18:17Z -- the fix NOW by the director, plus the log cleanup (a done conjunct); measured: goal:g14.14.7's grid.storage_trunk is a per-trunk namespace, not a branch; the duplicated heading from the mint removed
<!-- THOUGHT:END -->
