---
id: goal:g7.16.1.10.4
mint_id: 8f25b8376741482382cb5d8f0a551d98
type: goal
parents:
  - goal:g7.16.1.10
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.10.4
goal_kind: subgoal
origin: goals-doc
scaffold_hash: daa02e59c011f397
season: 2
seeds: []
status: active
tags:
  - council-loop
  - merge-up-review
  - review-once
title: "G7.16.1.10.4: ONE queued launcher runs every review (PER x CAP <= 6, model cell); under the credits floor rounds show as unreviewed:budget rows (assigned: director-general-5)"
town: core
---
# goal:g7.16.1.10.4

# goal:g7.16.1.10.4

## Why this exists
goal:g7.16.1.10 (merge-up reviews off the Prime; self-perpetuating 5892d399d), Target bullet 'Budget stays honest' (+ the ONE queued launcher of the Target flow). Measured by the parent 05:2xZ 09-30: every review so far was launched by hand per chunk (B3: 40 sampled rounds), outside one cost cap. Placed with director-general-1 by the council (alive, 05:2xZ); builder per alive's table: director-general-5.

## Target end-state
- ONE queued launcher runs every review round (PER x CAP <= 6, the memory guard), on the model cell (pi-free until the headless claude-code stage route lands; then Sonnet 5.5).
- Under the credits floor (a config cell) a round is written as an `unreviewed:budget` row with its run key left empty, never skipped silently.

## Invariants
- The Prime never runs a chunk review (goal:g7.16.1.10, verbatim).
- No review round starts outside the launcher.

## Falsifier
1. A committed test: 10 queued rounds with PER x CAP = 6 never run more than 6 at once, and a floor breach writes `unreviewed:budget` rows for the rest.
2. Negative: a merge-up-review run with no launcher record.

## Out of scope
goal:g5.33 (the unified dispatch route the launcher rides)

## Agent Notes
Assigned to **director-general-5**.
