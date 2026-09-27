---
id: goal:g7.31.3.3
mint_id: 819815f42d0947259caa1c53807a29a1
type: goal
parents:
  - goal:g7.31.3
next_edges: []
confidence: 0.7
edited_by: belam
goal_id: G7.31.3.3
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: d179db52abe5b582
season: 2
seeds: []
status: active
tags:
  - engine
  - spawn
  - rotate
thought_session: belam-S2-L5-XI
title: "G7.31.3.3: SPAWN AND ROTATE ARE ONE GRAPH WRITE -- parent slots pre-set under each post in .geometry, kid rows dynamic under their parent slot, rotate a spawn option (needs-rotate: true), the reaper/heal loop carries out what the graph says (assigned: director-engine)"
town: core
---
# goal:g7.31.3.3

## OWNER 2026-09-27 00:38Z + 00:45Z (belam-S2-L5-X's pane), verbatim -- the spawn/rotate part
"One thing that bothered me is that parents get a different spawn route than posts. I want parents and posts to share the same spawn route so spawn/rotate becomes one and uses individual post info and/or generic templates to decide who gets what messages. And also it creates the parent seats in-graph under the post seat that spawned them in the .geometry directory, and get removed as part of the reaper routine. So the concurrency limit and the parallel limit together become the amount of pre-set parent post slots each post has under it, and each kid also becomes a row entry in the parent slot “kid*” row. Rows added dynamically on each kid spawn and removed on kid exit. All using the unified spawn route. Rotate just becomes an option for spawn and parents can be rotated in place instead of re dispatched. Everything is still just a unified write/mint of nodes with a new version. The reaper/heal routine just then executes actions as put into the graph via post updates and linked templates. If a post needs rotation  just set the needs-rotate: true and wait on the loop to do it. So everything becomes a graph write even spawn/rotation commands. Parents just spawn kids but all it does is write the rows and points to where in the graph that kid needs to put its next node."

"One addition to 3: a refusal also activated the message send reply route to update the relevant sending post which can be found via graph of what failed and for whom."

(The same 00:38Z message opens with the parents-on-the-message-system question; that half is goal:g7.32.5.)

## The design as the owner confirmed it (gen 10's reading, pasted into the Prime's pane, confirmed 00:5xZ 09-27; the owner's words above win)
Unify spawn and rotate as graph writes. Parents become rows under the post that spawned them in .geometry, with pre-set parent slots per post. Kids become dynamic kid rows under their parent's slot. Rotate becomes a spawn option (needs-rotate: true), and the reaper/heal loop carries out whatever the graph says. Refinements:
1. Slot definitions are committed; live occupancy lives in a local runtime file.
2. Only the box hosting the post acts (checked via AGI_BOX), and the loop clears the flag.
3. A refusal is written into the row by name AND sent to the requesting post through the reply route, found via the graph. Cap it at one reply per failed request.
4. Gate who may write which rows: parents write only their own kid rows, kids write none.

## Invariants
- GUARD BY PLACEMENT (Prime 03:2xZ 09-27, on the owner's question 'Will the guard work with the new spawn/rotate unified redesign?'): every spawn -- post, parent, kid, and rotate as a spawn option -- is a `systemd-run --user` transient SERVICE named `agi-<town>-<post>[-<slot>]`; tmux is only a view attached to it. The sanctuary guard caps by systemd placement (user@1000 high/max 12618/14021M; `agi-*.service` -> agi-work.slice 9302M), so a unit so named is guarded with no guard change. Measured 03:2xZ: 25 claude processes of the tmux-spawned seats sit in session-73.scope, OUTSIDE user@1000 (uncapped); dispatch.py parents are --scope units in app.slice (user@ cap only).
- Near miss: unifying on today's post route (tmux) would move parents OUT of the cap too -- a silent regression nothing refuses.
- Kid worktrees follow hypothesis:kid-worktrees-resolve-from-one-cell-and-can-live-in-ram (paths.<town>.worktrees_root; the guard-owned RAM disk; reaper eviction).

## Relations
- parent goal:g7.31.3 -- the rotate|spawn route of the five unified engine routes; this makes it one graph write.
- goal:g7.32.5 -- the parents' dm-append push grant, the messaging half of the same owner message.
- goal:g4.18.1 -- one mint route: slot and kid rows go through the same write flow.
- goal:send-is-hub-only-dm-file-versions-synced-every-30s -- the reply route refinement 3 uses; its (default)-box note (46d1d17e1): refinement 2 acts only on the box a row names.

## Routing
assigned: director-engine. THIRD of the three graph redesigns, after node spawn/mint (goal:g4.18.1) and the send hub-only work (OWNER 01:0xZ 09-27: "Would the mint write design be first? Um send pieces depend on it, and rotate depends on send"): refinement 3's refusal rides send's reply route.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
2026-09-27 03:2xZ belam-S2-L5-XII: an Invariants section -- the guard by placement. (1) Owner 03:2xZ: 'Will the guard work with the new spawn/rotate unified redesign?' (2) The guard caps by cgroup placement (guard-init.sh:295-305, the agi-.service.d drop-in Slice=agi-work.slice); measured seats in session-73.scope outside user@1000. (3) Near miss: one route that is the tmux route unifies the protection DOWN. (4) Previous thought (routing third in the owner's dependency order) is in the grid.
<!-- THOUGHT:END -->
