---
id: goal:g7.16.1.10.6
mint_id: 299a130799444009966b62a0e5f2b1a3
type: goal
parents:
  - goal:g7.16.1.10
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.10.6
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 3457f83022f32452
season: 2
seeds: []
status: horizon
tags:
  - council-loop
  - merge-up-review
  - review-once
title: "G7.16.1.10.6: the reviewer is a liveness-census row -- a stopped reviewer is ONE [red], never a silent backlog (assigned: director-general-5)"
town: core
---
# goal:g7.16.1.10.6

# goal:g7.16.1.10.6

## Why this exists
goal:g7.16.1.10 (merge-up reviews off the Prime; self-perpetuating 5892d399d), Target bullet 'The reviewer is a self-healing loop'. Measured by the parent 05:2xZ 09-30: the reviewer would be a new standing loop, and the liveness census (goal:g7.16.1.5 C / goal:g7.16.1.1.6.1) is where standing loops are declared. Placed with director-general-1 by the council (alive, 05:2xZ); builder per alive's table: director-general-5.

## Target end-state
- The reviewer is a row of the liveness census: when it stops, ONE [red] names it; it never leaves a silent backlog.
- Its cadence (the CHECK cadence) is a config cell.

## Invariants
- The Prime never runs a chunk review (goal:g7.16.1.10, verbatim).
- A stopped reviewer is visible within one CHECK interval.

## Falsifier
1. Stopping the reviewer on a fixture makes the census report it within one interval.
2. Negative: `git rev-list <last_reviewed>..trunk` non-empty for longer than two intervals with no [red].

## Out of scope
goal:g7.16.1.5 (the census itself)

## Agent Notes
Assigned to **director-general-5**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 08:5xZ 09-30: re-laned to director-general-4 (the reviewer census row: DG4's heal lane) after the owner's stand-down of director-general-5 and director-general-6, per sanctuary-master's re-lane 08:4xZ confirming alive's placement proposal. Status stays horizon: the new owner claims it when its lane frees.
<!-- THOUGHT:END -->
