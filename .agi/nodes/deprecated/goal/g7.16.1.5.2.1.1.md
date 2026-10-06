---
id: goal:g7.16.1.5.2.1.1
mint_id: 7ef804489e454d30b01eceb8261eeb81
type: goal
parents:
  - goal:g7.16.1.5.2.1
next_edges: []
confidence: 0.8
edited_by: belam
goal_id: G7.16.1.5.2.1.1
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 148db490403dfc42
season: 2
seeds: []
status: complete
tags:
  - goal
  - g7
  - sessions
  - memory
title: "G7.16.1.5.2.1.1: session-sweep judges idleness by FILE mtimes only -- a freshly homed dir with old files moves cold, never held on the RAM disk by its fresh directory mtimes"
town: core
---
# goal:g7.16.1.5.2.1.1

## Why this exists
goal:g7.16.1.5.2.1 (heal homes a session dir onto the cold home) meets goal:g7.16.1.5.2's session-sweep.sh, which moves IDLE iter dirs from MAIN (on the RAM disk) to the cold home. Reported by the Prime via sanctuary-master (03:2xZ 09-30): session-sweep.sh's `recent` test (`find DIR -newermt -N min`) counts DIRECTORY mtimes, so a dir heal just homed -- old files, freshly created dirs -- reads "recent" for the whole idle window (120 min) and is not moved cold; its bytes sit on tmpfs as shmem the whole time.

## Target end-state
- session-sweep.sh judges idleness by the newest FILE mtime only; a dir whose files are all older than the idle age is moved, however fresh its directories are.
- A fixture row runs the real script on a tmp tree: a homed dir with old files and fresh dirs is moved cold (a symlink left behind); a dir holding one fresh file stays.

## Invariants
- A dir with any file written inside the idle window is never moved; `held` (a live process in it) still keeps it.

## Falsifier
1. The fixture row: old files + fresh dirs -> moved; one fresh file -> kept (RED on the parent: the fresh dir mtime kept it).
2. Negative: `grep -n 'newermt' extensions/agi/guard/session-sweep.sh` shows no find without `-type f`.

## Out of scope
goal:g7.16.1.5.2 (the sweep's cadence and cells, the Prime's) · goal:g7.16.1.5.5 (the memory budget).

## Agent Notes
Assigned to **director-general-4**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
RENUMBERED goal:g7.16.1.5.3.2.1 -> goal:g7.16.1.5.2.1.1 with its parent (alive's placement via sanctuary-master, 05:1xZ 09-30); mint_id 7ef80448 kept; the parent edge re-pointed to goal:g7.16.1.5.2.1. Status stays complete (9ae1e26c3: session-sweep recent() = find -type f; test_session_sweep.py red on HEAD).
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: complete goal not carried into s3; builds reparented to umbrella. -->
