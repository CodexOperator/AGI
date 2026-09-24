---
id: goal:g7.33.11
mint_id: 6a2604e630444966a595be177e770b5c
type: goal
parents:
  - goal:g7.33
next_edges: []
confidence: 0.9
edited_by: director-engine
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
title: "G7.33.11: THE GRID STAYS refs/grid/* -- push only the post-split set, batched, so the remote finally holds it"
town: core
---
# goal:g7.33.11

| | |
|---|---|
| goal | the grid stays git refs (the owner withdrew the subdirectory shape at 18:3xZ: refs are the leaner database) -- each branch's namespace (grid.storage_trunk) holds and uploads ONLY what changed after its split from its parent; pushes go <= 200 refs at a time and only for tips origin lacks, so a backlog never forms; merges carry the rest, and origin/season2/main + origin/main keep the coarse history |
| origin | the owner 17:57Z + 18:17Z + 18:21Z + 18:35Z 09-24 (verbatim on town:local-maxxing's board, relayed to director-engine via thought-master TMM.128 -> TMM.129 -> TMM.130 -> **TMM.132, which WITHDRAWS TMM.130**): TMM.129's "one branch" and TMM.130's "subdirectory per branch" shapes are BOTH dead -- refs/grid/* stays exactly what it was, only the push's ref selection changes; the 0.7 GB of failure logs get cleaned up once the new push is proven |
| measured | 18:0xZ 09-24: the grid_sync cron commits every 5 min into refs/grid/local-maxxing/ (4,293 refs, newest 17:55:42Z), but its push of refs/grid/local-maxxing/* has failed 967 times -- GitHub rejects each ref "Timed out validating rule, please try again" -> the remote holds 0 of the 4,293 (its 4,204 refs/grid refs are all outside that namespace) -> the town's grid history lives on this box's disk alone · the cron log is 775 MB of those rejection lines · 18:2xZ: what exists = grid.storage_trunk (goal:g14.14.7; config value refs/grid/local-maxxing), a per-trunk ref NAMESPACE -- still one ref per node; no verb stores or pushes the grid as one branch (core/season2/main's grid.py is unchanged since the 09-23 merge-base; ours is newer) · 18:4xZ: of the namespace's 4,298 refs, 3,773 were born in ONE split pass (v1 at 09-21 01:48-01:49Z; the first local-only trunk commit 01:54Z, see commit 2a761ecd71) -> 2,430 split-only v1 snapshots (unchanged since) + 1,343 changed since + 525 born after = a POST-SPLIT set of 1,868 refs carrying 3,449 versions · the pre-split namespace refs/grid/node/* (3,807 local) shares 3,779 names with origin's but 0 identical tips: two boxes wrote the same names (the cross-branch race per-branch namespaces avoid) · the push itself is ONE `git push` with grid.py:171's single wildcard refspec, issued by extensions/agi/bin/crons.py:554-559 -- that call site is what becomes the batched/filtered loop |
| where | the namespace = grid.storage_trunk (a config cell per branch), never a literal · the push builds in extensions/agi/bin/crons.py:554-559, the refspec in extensions/agi/bin/grid.py:171 (`push_spec_for`) · the cron line = cron:crons (NOT `config:crons` -- that id does not resolve, verified) · .agi/nodes/.geometry/crons.md |
| done | origin's ref count for the namespace = the local post-split count (1,868 at 18:4xZ, plus any newer) · the 2,430 split-only snapshots never pushed and never deleted (0 local refs deleted, ever) · every push <= 200 refs, only tips origin lacks · 0 rejected in 3 consecutive cron runs · a new branch's namespace cross-populated from its parent's tips at the split (no fresh v1 roots) · the push-rejection lines stripped from the cron log once those 3 runs are clean (before / after bytes reported) · tests pin the batching and the post-split filter · ONE `[merge-up]` as soon as round A is done |
| who | director-engine NOW (the owner 18:17Z: "let the director work it"), batched by thought-master (TMM.128 -> TMM.129 -> TMM.130 void -> TMM.132) |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 17/18 18:3x-18:37Z: the owner WITHDRAWS TMM.130's subdirectory-per-branch shape (TMM.132) -- the grid stays refs/grid/*, mechanism unchanged; the real fix is the push's ref SELECTION (skip the 2,430 unchanged split-only v1 snapshots core already carries, push only the ~1,868 post-split refs, batched <=200) plus a going-forward rule (push only tips not yet on origin) and a cross-population rule so future splits never need a catch-up batch. Also measured: the pre-split refs/grid/node/* namespace collides on 3,779 names between local and origin with 0 identical tips -- two boxes wrote the same names, exactly the cross-branch race per-branch namespaces are meant to avoid. DH.290 (a live pi-free parent + kid already deep in branch-local migration code for the now-void subdirectory design, chasing 7 failing grid tests) was CUT, not rebriefed, by director-engine: the two designs differ in kind (ref-namespace filtering vs. tree-content restructuring), so patching DH.290's context in place would be less reliable than a fresh pi-free parent (DH.292) carrying TMM.132's orders cleanly. Verified TMM.132 against the real dm log (director-engine--thought-master.md:796) before acting -- it arrived first as a cross-session message from agi-5c, matched word for word once checked. This version reconciles a concurrent independent edit from thought-master: same TMM.132, same conclusion; thought-master's measurement had the ref-name-collision fact this side lacked, this side had the DH.290-cut operational fact and the exact push call-site (crons.py:554-559 / grid.py:171).
<!-- THOUGHT:END -->
