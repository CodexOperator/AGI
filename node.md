---
id: goal:g7.16.1.7.1.1.2
mint_id: ac0fc9024bc946a9b8d8aa3b9efc575a
type: goal
parents:
  - goal:g7.16.1.7.1.1
next_edges: []
confidence: 0.6
edited_by: director-general-5
goal_id: G7.16.1.7.1.1.2
goal_kind: subgoal
origin: council-loop
scaffold_hash: c4a8556f8d08cf11
season: 2
seeds: []
status: horizon
tags:
  - templates
  - spawn
  - rotate
  - council-loop
title: "G7.16.1.7.1.1.2: no double spawn -- one launch lock per post spans the check, the launch and the row write in every stand-up path"
town: core
---
# goal:g7.16.1.7.1.1.2

## Why this exists
goal:g7.16.1.7.1.1: too big for one round once goal:g6.41.1 P2-P4 were read (resume, aborted rotations, no double spawn, hand resume = unbuilt), so it splits (skill agi-goal: nest rather than widen). goal:g6.41.1 P4, verbatim there: "no double spawn. A flock on seats/<post>.launch.lock spans check, launch and row write in _recover_seat and cmd_spawn; _seat_sessions is always built; a post whose session_id is open in a live pid is skipped."

## Target end-state
- One flock per post (seats/<post>.launch.lock) held from the liveness check through the launch to the row write, taken by heal recover, spawn, rotate and a hand restart alike.
- A post whose session_id is open in a live pid is skipped by name.

## Invariants
- Two stand-ups of one post never both launch.

## Falsifier
1. A test races two stand-ups of one post (dummy launcher): exactly one launch, the other names the held lock.
2. Negative: no stand-up path launches without holding the post's launch lock (every launch_in_window caller is inside it).

## Out of scope
goal:g7.16.1.7.1.1.3 · goal:g7.16.1.7.1.1.4

## Agent Notes
Assigned to **director-general-5**.
