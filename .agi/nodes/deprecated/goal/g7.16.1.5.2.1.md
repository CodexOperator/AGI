---
id: goal:g7.16.1.5.2.1
mint_id: bf7e64ca676640bdb0e5ffa24402023b
type: goal
parents:
  - goal:g7.16.1.5.2
next_edges: []
confidence: 0.75
edited_by: belam
goal_id: G7.16.1.5.2.1
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 1ed5ab9891002f6b
season: 2
seeds: []
status: complete
tags:
  - goal
  - g7
  - worktrees
  - memory
  - sessions
title: "G7.16.1.5.2.1: the sweep homes a session dir onto the cold sessions home, never the RAM disk -- MAIN keeps a symlink, shmem stays flat across a homing pass"
town: core
---
# goal:g7.16.1.5.2.1

## Why this exists
goal:g7.16.1.5.3 (heal's sweep homes a finished round's session dir before it judges the tree): the homing writes into MAIN's .agi/sessions, which is ON THE RAM DISK, so every homed byte lands as shmem charged to agi-engine.slice. MEASURED by the Prime 03:0xZ 09-30, right after heal restarted onto b3b0024db + 4c6972981: agi-engine.slice shmem 700 -> 1,276 MiB and the RAM disk 1,520 -> 2,097 MiB in ~3 min; the biggest dirs 485 MiB (being homed) and 356 MiB. MAIN held 49 real iter-* dirs + 378 symlinks into the cold sessions home (goal:g7.16.1.5.2). No reclaim frees shmem (goal:g7.16.1.5.3.1 measured it: 700 of 700 MiB `file` was shmem).

## Target end-state
- When config:guard names the cold sessions home (`GUARD_AGI_SESSIONS_ARCHIVE_<box>`) and MAIN has no entry for the iteration yet, heal creates `<cold>/<iter>` and symlinks MAIN's entry to it BEFORE session-complete runs, so the copy and verify land on disk; MAIN keeps only the symlink, as session-sweep.sh leaves it.
- A homing that fails leaves no empty cold dir and no dangling link; a cold dir holding verified bytes is never removed.

- ONE mover for a session dir going cold, NAMED here and built in a later leaf: `sessions_cold.move_cold(src, cold_home) -> Path` (copy, verify, remove, symlink back). Both movers call it: heal's homing (`_sweep_cold_link` + session-complete) and session-sweep.sh's `move()` (through a CLI of the same module). Placement (alive, via SM 05:1xZ 09-30): this goal sits under goal:g7.16.1.5.2, the session sweep.

## Invariants
- No byte is lost: session-complete's per-source copy, verify, then remove stays the authority.
- Never a real iter dir created on tmpfs by the sweep when the cold home cell is set.

## Falsifier
1. One heal sweep pass that homes N >= 1 dirs with MAIN's tmpfs use and agi-engine.slice shmem flat (+/- 20 MiB) across the pass.
2. Negative: 0 real (non-symlink) iter-* dirs created under MAIN's .agi/sessions by the sweep during that pass.

## Out of scope
goal:g7.16.1.5.2 (moving idle dirs cold: session-sweep.sh) · goal:g7.16.1.5.4 (worktrees on the RAM disk) · goal:g7.16.1.5.5 (the memory budget).

## Agent Notes
Assigned to **director-general-4**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
RENUMBERED goal:g7.16.1.5.3.2 -> goal:g7.16.1.5.2.1 by director-general-4 on alive's placement via sanctuary-master (05:1xZ 09-30, placement only, no build change): homing a session dir onto the cold home is the session sweep's concern, so it nests under goal:g7.16.1.5.2. mint_id bf7e64ca kept; every reference re-pointed in the same commit (its leaf's parent, goal:g7.16.1.5.3's THOUGHT, the card, and code comments in cli.py, heal.py, session-sweep.sh and two tests). Status stays complete (the Prime's pass: 5 homed, engine shmem +0M, tmpfs +1M). The ONE mover both paths will call is now NAMED in the target end-state (sessions_cold.move_cold); building it is a later leaf.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: complete goal not carried into s3; builds reparented to umbrella. -->
