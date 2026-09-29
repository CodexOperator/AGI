---
id: goal:g7.16.1.7.2.2
mint_id: 22ff79cf630d4286a4396a69bc460b3b
type: goal
parents:
  - goal:g7.16.1.7.2
next_edges: []
confidence: 0.6
edited_by: director-general-5
goal_id: G7.16.1.7.2.2
goal_kind: subgoal
origin: council-loop
scaffold_hash: a90000a0b3c4b0d3
season: 2
seeds: []
status: horizon
tags:
  - templates
  - spawn
  - rotate
  - council-loop
title: "G7.16.1.7.2.2: a config switch-over is atomic -- the new resolved config is written beside the old and ONE symlink rename swaps it"
town: core
---
# goal:g7.16.1.7.2.2

## Why this exists
goal:g7.16.1.7: the owner, verbatim there: "Add a way to smoothly switch the symlink over to the new config settings." and point 3 "Yup that works." (write beside the old file, swap the symlink by one rename).

## Target end-state
- Each post's resolved config lives at a stable symlink path; a switch renders the new resolution beside the old file, then renames a temp symlink over the stable one (one rename(2)).
- A reader at any instant sees the old or the new config, never neither and never a partial file.
- The previous target stays on disk until the next switch, so a switch can be undone by one rename.

## Invariants
- A live post is never left without a readable config.

## Falsifier
1. The swap's test file passes: a concurrent reader loop over N switches never reads a missing or truncated file.
2. Negative: no writer truncates the stable path in place (grep for open(... 'w') on it = 0).

## Out of scope
goal:g7.16.1.7.2.1 · goal:g7.16.1.7.2.4

## Agent Notes
Assigned to **director-general-5**.
