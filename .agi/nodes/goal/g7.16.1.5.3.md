---
id: goal:g7.16.1.5.3
mint_id: e573f55567864ca08baec01c652e4cc1
type: goal
parents:
  - goal:g7.16.1.5
next_edges: []
confidence: 0.8
edited_by: belam
goal_id: G7.16.1.5.3
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 23ca6f1fe6e9ac58
season: 2
seeds: []
status: active
tags:
  - goal
  - g7
  - worktrees
  - ram-disk
title: "G7.16.1.5.3: heal's worktree sweep archives then prunes -- 'refused: unmerged' is never terminal; every removed worktree keeps an archive ref"
town: core
---
# goal:g7.16.1.5.3

# goal:g7.16.1.5.3

## Why this exists
goal:g7.16.1.5 line C, made the FIRST priority by the owner (02:0xZ 09-30, verbatim below). MEASURED 02:15Z 09-30 on the now-timestamped heal log (goal:g6.41.2): heal's worktree sweep refuses nearly every worktree ("[sweep] refused a00-...: unmerged" / "dirty (N paths)"), because landings are fresh commits and "merged" is never provable by ancestry (0 of 1021 at 09-29). The Prime's off-graph prune tool archived 7/881 by hand; this leaf puts that rule in the engine.

## Target end-state
- heal's sweep ARCHIVES then removes: a worktree past its round (no live agent, harvested or older than a config cell's age) gets refs/archive/worktrees/<name> (HEAD pinned; a dirty tree first committed onto <name>-dirty, objects shared), then `git worktree remove`; "refused: unmerged" is no longer a terminal state.
- Gated on io + memory pressure (config:guard cells), resumable pass by pass, its liveness a row of the census.

## Invariants
- A worktree with uncommitted state is never removed before its archive ref exists; no byte is lost; a live round's worktree is never touched.

## Falsifier
1. `git worktree list | wc -l` falls to the live rounds only; every removed worktree has a refs/archive/worktrees/<name> ref.
2. Negative: zero "[sweep] refused ...: unmerged" lines in the heal log after the change lands.

## Out of scope
goal:g7.16.1.5.4 (new worktrees on the RAM disk) · goal:g7.16.1.5.2 (session sweep).

## OWNER 2026-09-30 01:5xZ, verbatim
"we need to make sure and prioritize the build nodes or the goals and chains that will go into the build nodes that will give us proper work tree cleanup because that RAM disk usage is feeling a little high for how little stuff we're really actually trying to load on it."

## Agent Notes
Assigned to **director-general-4**.
