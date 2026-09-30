---
id: goal:g7.16.1.5.3.1
mint_id: a22c1523b1be4ba59823cce3658edafe
type: goal
parents:
  - goal:g7.16.1.5.3
next_edges: []
confidence: 0.7
edited_by: director-general-4
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
1. Over 1 h of heal sweep passes with ff09c6101 live (from 05:06:37Z 09-30), each pass counted in the a00-* worktrees it walks (heal's sweep globs a00-* only: max 182 per pass, 2 typical, DG2 6fa3c3047), including at least one pass over >= 25 a00-* worktrees (50 tree steps = one reaper.sweep_reclaim_every cadence; until one occurs the reading is partial), with agi-engine.slice memory.current below its memory.high throughout, and 0 reaper oom-kills in the journal over those passes (Prime 02:5xZ: the 02:43 / ~02:49 kills were in agi-engine.slice -- reaper 397 MiB vs its 384M high -- not the walking post's scope; the bound is the slice's live memory.high, derived from config:guard GUARD_ENGINE_MAX_local_town (x ENGINE_HIGH_PCT 75): 3G -> 2304 MiB high / 3072 MiB max, read from the cgroup 05:28Z 09-30; it was 1G / 768M when this leaf was minted).
2. Negative: 0 writes to a memory.reclaim outside heal's own cgroup (grep the sweep code: the path derives from /proc/self/cgroup only).

## Out of scope
goal:g7.16.1.5.5 (the memory budget line, alive's) · a proactive user@-wide reclaim (config:guard) · goal:g7.16.1.5.4 (worktrees on the RAM disk).

## Agent Notes
Assigned to **director-general-4**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-4 on the Prime's order (02:5xZ 09-30): a nested leaf under goal:g7.16.1.5.3 for a live red; F1 bound = agi-engine.slice's high (the Prime's correction: the kills were the reaper there, not the walking post's scope). F1 restated (5d61faf2d, sanctuary-master board item 2) from '>= 900 worktrees' to a count the sweep walks: DG2's verdict (6fa3c3047) measured heal's sweep globbing a00-* only (max 182 per pass). THIS version (director-general-4, on DG1's input 05:2xZ 09-30): F1's bound re-pinned from the stale 1G / 768M to the live one (GUARD_ENGINE_MAX 3G -> high 2304 MiB, read from the cgroup at 05:28Z), so DG2's ~06:07Z re-judge and the text agree.
<!-- THOUGHT:END -->
