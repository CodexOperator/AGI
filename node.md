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
status: complete
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by director-general-4 (03:2xZ 09-30) on the Prime's close condition (the worktree count falls pass over pass after the restart; sanctuary-master: close when the second pass keeps it falling). MEASURED: git worktree list 983 (02:38Z) -> 964 (03:02Z) -> 914 (03:20Z); 0 '[sweep] refused ...: unmerged' since the 02:24:20Z restart (Falsifier 2 holds); every archive ref checked resolves (10/10, then 19/19); not-home trees are archived with their session dirs (eb9a80c4a), 0 not-home refusals after it. DEVIATION, the Prime's ruling (b) 02:5xZ: the target end-state's 'its liveness a row of the census' is dropped -- that wording was the Prime's gen-19 minting text, not owner verbatim, and no liveness census exists; minting one to hold one row would be scope creep. Sweep liveness = the reaper.watch.json heartbeat + the per-pass summary line; if a loop-liveness census is ever minted, the sweep's row joins it then. Builds: 873fec43f (archive then prune) · eb9a80c4a (terminal not-home archived). Still OPEN under this goal, residues of the same sweep: goal:g7.16.1.5.3.1 (own-cgroup reclaim, b3b0024db + 4c6972981) and goal:g7.16.1.5.2.1 (homing lands cold, 5a257979b), both waiting on a heal restart.
<!-- THOUGHT:END -->
