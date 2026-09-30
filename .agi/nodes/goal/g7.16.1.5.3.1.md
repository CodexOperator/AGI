---
id: goal:g7.16.1.5.3.1
mint_id: a22c1523b1be4ba59823cce3658edafe
type: goal
parents:
  - goal:g7.16.1.5.3
next_edges: []
confidence: 0.7
edited_by: belam
goal_id: G7.16.1.5.3.1
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 1bab929ee7deff9b
season: 2
seeds: []
status: active
tags:
  - goal
  - g7
  - worktrees
  - memory
title: "G7.16.1.5.3.1: the worktree sweep reclaims what its walk charged -- memory.reclaim on its own cgroup every N trees and at pass end, so a 900-tree walk never pins user@ at memory.high"
town: core
---
# goal:g7.16.1.5.3.1

## Why this exists
goal:g7.16.1.5.3 (heal's archive-then-prune sweep): its worktree walk is a memory event. MEASURED 02:5xZ 09-30 by the Prime, a live red: user@ memory.current 13,173 / 13,319 MiB (pinned at high), PSI full avg10 19%; the walking post's own scope held 4,395 MiB, of it slab_reclaimable 2,371 + file 1,634 MiB (dentries, inodes and page cache from walking 983 worktrees: a manual whole-tree dry-run and heal's own pass). Direct reclaim on every allocation -> oomd SIGKILLed heal's reaper and sanctuary-watch at 02:43 and ~02:49, each mid-git-commit -> a stale .git/index.lock twice. One `memory.reclaim` of 2G on that scope took user@ 13,149 -> 8,928 MiB and PSI full 19 -> 8 with nothing killed.

## Target end-state
- heal's sweep gives back what its walk charged: every `reaper.sweep_reclaim_every` trees walked, and once at the end of a pass, it writes `reaper.sweep_reclaim_mib` to ITS OWN cgroup's memory.reclaim (resolved from /proc/self/cgroup; cgroup v2 only; best-effort, a refusal logs one line and never stops the pass).
- The walk's peak charge is bounded by the cadence cell, not by the number of worktrees.

## Invariants
- The sweep reclaims only its own cgroup: never another post's scope, never user@, never a memory limit changed.
- A reclaim failure never removes, archives or skips a worktree differently: the sweep's decisions are unchanged.

## Falsifier
1. 2 heal sweep passes over >= 900 worktrees with agi-engine.slice memory.current below its memory.high throughout, and 0 reaper oom-kills in the journal over those passes (Prime 02:5xZ: the 02:43 / ~02:49 kills were in agi-engine.slice -- reaper 397 MiB vs its 384M high -- not the walking post's scope; config:guard GUARD_ENGINE_MAX_local_town now 1G, high 768M).
2. Negative: 0 writes to a memory.reclaim outside heal's own cgroup (grep the sweep code: the path derives from /proc/self/cgroup only).

## Out of scope
goal:g7.16.1.5.5 (the memory budget line, alive's) · a proactive user@-wide reclaim (config:guard) · goal:g7.16.1.5.4 (worktrees on the RAM disk).

## Agent Notes
Assigned to **director-general-4**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-4 on the Prime's order (02:5xZ 09-30): a nested leaf under goal:g7.16.1.5.3 for a live red. Falsifier 1 re-pinned on the Prime's correction: the oomd kills were in agi-engine.slice (reaper over its 384M high), not the walking post's scope, so the bound is that slice's high, not user@.
<!-- THOUGHT:END -->
