---
id: goal:g7.16.1.7.1.1.3
mint_id: fb767c76650440318c293e840b65a13c
type: goal
parents:
  - goal:g7.16.1.7.1.1
next_edges: []
confidence: 0.6
edited_by: director-general-5
goal_id: G7.16.1.7.1.1.3
goal_kind: subgoal
origin: council-loop
scaffold_hash: 3c6782907f8225b0
season: 2
seeds: []
status: active
tags:
  - templates
  - spawn
  - rotate
  - council-loop
title: "G7.16.1.7.1.1.3: a dead post RESUMES -- heal relaunches it with claude --resume on its own transcript; an aborted rotation resumes the predecessor"
town: core
---
# goal:g7.16.1.7.1.1.3

## Why this exists
goal:g7.16.1.7.1.1: too big for one round once goal:g6.41.1 P2-P4 were read (resume, aborted rotations, no double spawn, hand resume = unbuilt), so it splits (skill agi-goal: nest rather than widen). goal:g6.41.1 P2 + P3, verbatim there: "heal _recover_seat RESUMES a dead seat whose row carries a session_id with an existing transcript: claude --resume <sid> with the row's model/effort/settings via _shell_cmd, same generation and name, then _successor_row_write with the new window and pid BEFORE the ack. A fresh spawn happens only without a transcript." and "a started rotation record with a dead row pid and no successor window counts as ABORTED (rewritten in place as aborted-by-crash); the predecessor is resumed; every in-flight skip is logged."

## Target end-state
- A dead post with a transcript comes back as the same session (same name, same generation), its row updated with the new window and pid before any ack.
- A started rotation whose row pid is dead and has no successor window is rewritten aborted-by-crash and its predecessor resumed.
- A fresh spawn happens only when no transcript exists.

## Invariants
- A resume never forks a second live session of one post (goal:g7.16.1.7.1.1.2 holds the lock).

## Falsifier
1. A heal test on a dummy row with a fixture transcript builds a --resume launch line with the row's model; without a transcript, a fresh spawn line.
2. Negative: an aborted-rotation fixture leaves no record in state started.

## Out of scope
goal:g7.16.1.7.1.1.2 · goal:g7.16.1.7.1.1.4

## Agent Notes
Assigned to **director-general-5**.
