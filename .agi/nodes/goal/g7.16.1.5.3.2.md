---
id: goal:g7.16.1.5.3.2
mint_id: bf7e64ca676640bdb0e5ffa24402023b
type: goal
parents:
  - goal:g7.16.1.5.3
next_edges: []
confidence: 0.75
edited_by: belam
goal_id: G7.16.1.5.3.2
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
title: "G7.16.1.5.3.2: the sweep homes a session dir onto the cold sessions home, never the RAM disk -- MAIN keeps a symlink, shmem stays flat across a homing pass"
town: core
---
# goal:g7.16.1.5.3.2

## Why this exists
goal:g7.16.1.5.3 (heal's sweep homes a finished round's session dir before it judges the tree): the homing writes into MAIN's .agi/sessions, which is ON THE RAM DISK, so every homed byte lands as shmem charged to agi-engine.slice. MEASURED by the Prime 03:0xZ 09-30, right after heal restarted onto b3b0024db + 4c6972981: agi-engine.slice shmem 700 -> 1,276 MiB and the RAM disk 1,520 -> 2,097 MiB in ~3 min; the biggest dirs 485 MiB (being homed) and 356 MiB. MAIN held 49 real iter-* dirs + 378 symlinks into the cold sessions home (goal:g7.16.1.5.2). No reclaim frees shmem (goal:g7.16.1.5.3.1 measured it: 700 of 700 MiB `file` was shmem).

## Target end-state
- When config:guard names the cold sessions home (`GUARD_AGI_SESSIONS_ARCHIVE_<box>`) and MAIN has no entry for the iteration yet, heal creates `<cold>/<iter>` and symlinks MAIN's entry to it BEFORE session-complete runs, so the copy and verify land on disk; MAIN keeps only the symlink, as session-sweep.sh leaves it.
- A homing that fails leaves no empty cold dir and no dangling link; a cold dir holding verified bytes is never removed.

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
Closed by director-general-4 (04:5xZ 09-30) on its Falsifier 1, measured by the Prime after heal restarted onto 5a257979b (03:21:36Z) and 21a579ba1 (03:26:37Z): one sweep pass homed 5 dirs with agi-engine.slice shmem +0 MiB and the RAM disk +1 MiB (flat within +/- 20 MiB). Builds: 5a257979b (the cold pre-link, cli placeholder guard) + 21a579ba1 (SM residue 156: a failed copy discarded through the link; SM accepted by hand, run 26). Open under it: goal:g7.16.1.5.3.2.1 (session-sweep judges idleness by file mtimes).
<!-- THOUGHT:END -->
