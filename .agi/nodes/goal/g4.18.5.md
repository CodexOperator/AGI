---
id: goal:g4.18.5
mint_id: e28fe576bf294848890b9049b80382c5
type: goal
parents:
  - goal:g4.18
next_edges: []
confidence: 0.7
edited_by: belam
goal_id: G4.18.5
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 30214a9e57369dee
season: 2
seeds: []
status: active
tags:
  - engine
  - write-path
  - owner
title: "G4.18.5: a node body is addressable rows -- one verb replaces a row, one edits lines inside a block row, and every write is a git commit behind the permission layer"
town: core
---
# goal:g4.18.5

# goal:g4.18.5

## OWNER 2026-09-29 17:2xZ, verbatim (Prime pane)
"Is our new unified mint/wrote working better. We could add more verbs to mint single row changes and to change specific lines inside of a row that is a block of text not just one line."
"Actually, if we have a one-row replace verb we can split all the different body sections into their own rows. But also still have a way to overwrite specific lines. Maybe something got based that piggybacks off of git commits. Maybe a write could be a commit also and just drive all the existing git machinery just with permissions layered on top."

## Why this exists
goal:g4.18: write.py is the one node writer. Measured friction on 09-29 (belam-S2-L5-XVI): no single-row verb (re-homing stream-master rewrote the whole 25-row config:posts list via write.submit); `replace body` refuses a line inside a table paragraph (the council-loop Posts table was replaced whole to add one row); `create config` has no route (spawn gate) and `adopt` skips written_by (goal:g4.18.3); a key-row write corrupted config:posts on season2/main (goal:g4.18.4).

## Target end-state
- A node body is a list of addressable ROWS (one per section / table row / list item); one verb replaces one row, one verb edits lines inside a block row.
- A write IS a git commit: the permission layer (written_by, self_row, actor_rows, schema) runs first, then the write commits the one node by path; the grid and history are git's, not a second mechanism.

## Invariants
- Every write passes the same authorship + schema gate before any byte lands; no verb returns ahead of it.

## Falsifier
1. `write.py <id> 'row <n> <file>'` replaces exactly one row, and `git log -1 -- <node>` is that write's commit.
2. Negative: zero write.py verbs that change a node without producing a commit.

## Out of scope
goal:g4.18.3 · goal:g4.18.4 (bundle 3, H1-H2).

## Agent Notes
Assigned to **director-engine**.
