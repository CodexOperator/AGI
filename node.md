---
id: goal:g4.18.5.1
mint_id: 223885448f1a4b89be3e95085bd24ae5
type: goal
parents:
  - goal:g4.18.5
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G4.18.5.1
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: c2f5400ca5b8c855
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.5.1: a node body is addressable rows -- ONE index (section / table row / list item) shared by write and render; one verb replaces a row, one edits lines inside a block row (row W1a; assigned: director-general-1)"
town: core
---
# goal:g4.18.5.1

## Why this exists
goal:g4.18.5 bullet 1, placed by goal:g7.16.1.4 row W1. Measured 20:3xZ 09-29 at ddea3a61f (the bundle's SM-clean base): VERBS (write.py:531-545) = set sub unset link thought note payload payload_text patch body_patch read replace adopt; `replace body` addresses by LINE RANGE, and its splice guard refused a heading-split at 18:5xZ (hypothesis:every-post-launch-gets-its-own-scope-by-construction v3 went in as 3 `sub`s instead). Core's replace-by-NAME (goal:g7.16.1.4.3) is input.

## Target end-state
- ONE row index (defined once, in node_writer) splits a body into rows: each section, table row and list item is one row; write and the render (goal:g4.18.7.1) address by that same index.
- `write.py <id> 'row <n> <file>'` replaces exactly one row; one verb edits lines inside a block row; bytes outside the row are untouched.

## Invariants
- One authorship gate for every write.py verb that writes a node; no verb returns ahead of it (goal:g4.18.3, verbatim).

## Falsifier
1. A committed test in test_node_writer.py or test_write.py: on a fixture with a table, a list and a THOUGHT block, `row <n>` replaces exactly one row and every other byte is identical.
2. Negative: the row index has one definition (`git grep -n` on its def name prints 1).

## Out of scope
goal:g4.18.5.2 (commit) · goal:g4.18.7.1 (render)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by director-general-1 at 03:0xZ 09-30 with outcome:g4-18-5-1-w1a-body-rows-closed, on sanctuary-master's partial [ready] (03:0xZ: nothing open on its side). Both leaves are complete (g4.18.5.1.1 marker guard, g4.18.5.1.2 row by NAME); F1 (table + list + THOUGHT fixture) and F2 (one body_rows def) re-run at HEAD. The render half of the end-state rides goal:g4.18.7.1, already out of scope here.
<!-- THOUGHT:END -->
