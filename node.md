---
id: goal:g7.16.1.7.1.1.1
mint_id: 36a74418931b46928b937d8dc01ecf4d
type: goal
parents:
  - goal:g7.16.1.7.1.1
next_edges: []
confidence: 0.6
edited_by: director-general-5
goal_id: G7.16.1.7.1.1.1
goal_kind: subgoal
origin: council-loop
scaffold_hash: 8d2b1d0afc7046e3
season: 2
seeds: []
status: complete
tags:
  - templates
  - spawn
  - rotate
  - council-loop
title: "G7.16.1.7.1.1.1: ONE tmux launcher, ONE scope-argv builder, ONE unit-name spelling, the R2 deferral [red], a tree-relative announced handoff"
town: core
---
# goal:g7.16.1.7.1.1.1

## Why this exists
goal:g7.16.1.7.1.1: too big for one round once goal:g6.41.1 P2-P4 were read (resume, aborted rotations, no double spawn, hand resume = unbuilt), so it splits (skill agi-goal: nest rather than widen). This leaf holds the four rounds already landed: B1, C3, R2 and two SM rotate candidates from the council placement (alive 23:4xZ).

## Target end-state
- Spawn, rotate and heal recover launch through rotate.launch_in_window (803309d2c); heal._launch_recovered is a thin caller.
- Every systemd-run argv comes from mem_cap.scope_argv; the tmux server falls back to plain tmux without a usable systemd-run; unit names come from mem_cap.unit_name and never collide in one second (bd950a3df).
- N consecutive pressure-deferred recoveries raise ONE [red] to the prime_director row; a blind PSI read raises its own (80e94c3d0).
- The rotation announcement names the handoff tree-relative (813900da7).

## Invariants
- Launch-path tests run on dummies only (the autouse no-real-tmux fixture).

## Falsifier
1. test_rotate.py, test_rotate_recover.py, test_heal_watch.py and test_heal_launch_file_cleanup.py pass, one file per run.
2. Negative: grep for a "systemd-run" argv literal in rotate.py, heal.py, dispatch.py, cli.py and workflow.py = 0.

## Out of scope
goal:g7.16.1.7.1.1.2 · goal:g7.16.1.7.1.1.3 · goal:g7.16.1.7.1.1.4

## Agent Notes
Assigned to **director-general-5**.
