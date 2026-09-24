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

# goal:g7.33.11

| | |
|---|---|
| goal | grid.py stores a town's grid in ONE named branch (the owner's example: the local-maxxing branch) -- commit writes there, log / diff / versions / payload read from there, and a push is one ref |
| origin | the owner 17:57Z 09-24 (verbatim on town:local-maxxing's board) |
| measured | 18:0xZ 09-24: the grid_sync cron commits every 5 min into refs/grid/local-maxxing/ (4,293 refs, newest 17:55:42Z), but its push of refs/grid/local-maxxing/* has failed 967 times -- GitHub rejects each ref "Timed out validating rule, please try again" -> the remote holds 0 of the 4,293 (its 4,204 refs/grid refs are all outside that namespace) -> the town's grid history lives on this box's disk alone · the cron log is 775 MB of those rejection lines |
| where | the branch name = a config cell per town, never a literal · the cron line = config:crons (.agi/nodes/.geometry/crons.md) |
| done | every node's version count in = out across the move (the 4,293 ref histories migrated or archived, 0 lost) · git ls-remote shows the grid branch on origin carrying the latest versions · grid.py log / diff / versions / payload read it · the cron's push is one ref and logs one summary line per run, never one line per ref · tests pin it |
| who | director-engine, batched by thought-master (TMM.128) |
