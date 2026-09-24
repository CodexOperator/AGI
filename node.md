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
| goal | grid.py stores each branch's grid as a SUBDIRECTORY inside that branch's own tree -- one directory per branch, never a separate remote head and never refs/grid/* -- so branches never share grid state, the grid reaches origin with the branch's own push, merges back through the ordinary merge (or stays as that branch's per-node history), and origin/season2/main + origin/main keep the coarse history of node changes |
| origin | the owner 17:57Z + 18:17Z + 18:21Z 09-24 (verbatim on town:local-maxxing's board): the fix NOW, worked by the director; the 0.7 GB of failure logs cleaned up; the shape = a per-branch subdirectory, not a separate head |
| measured | 18:0xZ 09-24: the grid_sync cron commits every 5 min into refs/grid/local-maxxing/ (4,293 refs, newest 17:55:42Z), but its push of refs/grid/local-maxxing/* has failed 967 times -- GitHub rejects each ref "Timed out validating rule, please try again" -> the remote holds 0 of the 4,293 (its 4,204 refs/grid refs are all outside that namespace) -> the town's grid history lives on this box's disk alone · the cron log is 775 MB of those rejection lines · 18:2xZ: what exists = grid.storage_trunk (goal:g14.14.7; config value refs/grid/local-maxxing), a per-trunk ref NAMESPACE -- still one ref per node; no verb stores or pushes the grid as one branch (core/season2/main's grid.py is unchanged since the 09-23 merge-base; ours is newer) |
| where | the directory derives from a config cell (grid.storage_trunk, one per branch), never a literal · the cron line = config:crons (.agi/nodes/.geometry/crons.md) |
| done | every node's version count in = out across the move (the 4,293 ref histories carried into the directory, 0 lost) · grid.py commit / log / diff / versions / payload write and read the directory · the grid reaches origin through the branch's own push -- no refs/grid push left in the cron · two branches never write the same grid path · the 5-min grid commit and an agent's commit on the same checkout never drop each other's files (a test) · every version's bytes reachable from the pushed branch (a test) · the push-rejection lines stripped from the cron log once the refs/grid push is gone (before / after bytes reported) · tests pin it |
| who | director-engine NOW (the owner 18:17Z: "let the director work it"), batched by thought-master (TMM.128 -> TMM.129 -> TMM.130) |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 17 18:2xZ: the owner 18:21Z reshapes it -- the grid as a SUBDIRECTORY inside each branch's own tree, not a separate remote head; two risks added to done (same-checkout commit race, blob reachability); measured unchanged
<!-- THOUGHT:END -->
