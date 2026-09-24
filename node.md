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
| goal | the grid stays git refs (the owner withdrew the subdirectory shape at 18:3xZ: refs are the leaner database) -- each branch's namespace (grid.storage_trunk) holds and uploads ONLY what changed after its split from its parent; pushes go <= 200 refs at a time and only for tips origin lacks, so a backlog never forms; merges carry the rest, and origin/season2/main + origin/main keep the coarse history |
| origin | the owner 17:57Z + 18:17Z + 18:21Z + 18:35Z 09-24 (verbatim on town:local-maxxing's board): the fix NOW, worked by the director; the 0.7 GB of failure logs cleaned up; the subdirectory shape WITHDRAWN -- refs stay, only post-split refs are uploaded, a couple hundred per push |
| measured | 18:0xZ 09-24: the grid_sync cron commits every 5 min into refs/grid/local-maxxing/ (4,293 refs, newest 17:55:42Z), but its push of refs/grid/local-maxxing/* has failed 967 times -- GitHub rejects each ref "Timed out validating rule, please try again" -> the remote holds 0 of the 4,293 (its 4,204 refs/grid refs are all outside that namespace) -> the town's grid history lives on this box's disk alone · the cron log is 775 MB of those rejection lines · 18:2xZ: what exists = grid.storage_trunk (goal:g14.14.7; config value refs/grid/local-maxxing), a per-trunk ref NAMESPACE -- still one ref per node; no verb stores or pushes the grid as one branch (core/season2/main's grid.py is unchanged since the 09-23 merge-base; ours is newer) · 18:4xZ: of the namespace's 4,298 refs, 3,773 were born in ONE split pass (v1 at 09-21 01:48-01:49Z; the first local-only trunk commit 01:54Z) -> 2,430 split-only v1 snapshots (unchanged since) + 1,343 changed since + 525 born after = a POST-SPLIT set of 1,868 refs carrying 3,449 versions · the pre-split namespace refs/grid/node/* (3,807 local) shares 3,779 names with origin's but 0 identical tips: two boxes wrote the same names (the cross-branch race per-branch namespaces avoid) |
| where | the namespace = grid.storage_trunk (a config cell per branch), never a literal · the cron line = config:crons (.agi/nodes/.geometry/crons.md) |
| done | origin's ref count for the namespace = the local post-split count (1,868 at 18:4xZ, plus any newer) · the 2,430 split-only snapshots never pushed and never deleted (0 local refs deleted) · every push <= 200 refs, only tips origin lacks · 0 rejected in 3 consecutive cron runs · a new branch's namespace cross-populated from its parent's tips at the split (no fresh v1 roots) · the push-rejection lines stripped from the cron log once those 3 runs are clean (before / after bytes reported) · tests pin the batching and the post-split filter |
| who | director-engine NOW (the owner 18:17Z: "let the director work it"), batched by thought-master (TMM.128 -> TMM.129 -> TMM.130 void -> TMM.132) |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 17 18:3xZ: the owner withdrew the subdirectory shape -- the grid stays refs; each namespace uploads only its post-split refs (1,868 of 4,298 measured), <= 200 per push; TMM.132 (TMM.130 void)
<!-- THOUGHT:END -->
