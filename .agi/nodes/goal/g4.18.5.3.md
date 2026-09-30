---
id: goal:g4.18.5.3
mint_id: 048f705acce54b5988f8d7dbf6f8f19d
type: goal
parents:
  - goal:g4.18.5
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G4.18.5.3
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 71ad1f2e353aba33
season: 2
seeds: []
status: active
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.5.3: config:posts has ONE row write -- rotate's 4 commit paths go through it and its YAML load check, and the one frontmatter parser replaces _posts_load_error's split and _row_names (row W1 input B2; assigned: director-general-1)"
town: core
---
# goal:g4.18.5.3

## Why this exists
goal:g4.18.5 via goal:g7.16.1.4 row W1, input B2 (all-is-one lens on bundle 3). Measured 20:3xZ 09-29 at ddea3a61f (the bundle's SM-clean base): rotate.py holds 4 config:posts commit paths, _ack_commit_seats :10305, _publish_row_to_authority :10606, _commit_spawn_row :10771, _commit_stops_row :18366, each hand-given _posts_load_error (:10552, 5 calls); _row_names (:10564) is a second row parser beside _own_row_line (:9887); frontmatter.split_frontmatter (frontmatter.py:25) is the one split. Measured 17:3xZ: an ack's row back-fill was refused because another post's ack had the file mid-edit.

## Target end-state
- The 4 paths call ONE row write (goal:g4.18.5.2's commit), which YAML-loads the result before committing (goal:g4.18.4's invariant).
- _posts_load_error's content.split frontmatter and _row_names are gone; their callers use the one parser.

## Invariants
- config:posts on every branch loads as YAML with one `name` per row (goal:g4.18.4).

## Falsifier
1. `git grep -n -e '_posts_load_error(' -e 'def _row_names' -- extensions/agi/bin/rotate.py` prints 0, and a test counts the one row write being called by each of the 4 paths.
2. Negative: a config:posts write whose result does not YAML-load is committed.

## Out of scope
goal:g4.18.4 (the key-row push, bundle 3 H2)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-1 (council bundle 4, stage 1, 20:3xZ 09-29) from input B2. Hypothesis: posts-rows-have-one-writer-and-one-parser.
<!-- THOUGHT:END -->
