---
id: goal:g4.18.6.2.1
mint_id: 7771407b87dd46808aa098804f15348c
type: goal
parents:
  - goal:g4.18.6.2
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G4.18.6.2.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: d1621eb825268003
season: 2
seeds: []
status: active
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.6.2.1: set refuses a missing link id -- `set parents` / `set next_edges` naming a missing id is refused by name and nothing is written, as create already does (row W2b-a; assigned: director-general-1)"
town: core
---
# goal:g4.18.6.2.1

## Why this exists
goal:g4.18.6.2 split on verdict:dg2b4-w2b (DG2 verdicts 20:5xZ 09-29 (a1eafd484)): create refuses a missing parent by name (node_writer.py:787-798), but `set parents` / `set next_edges` naming a missing id exits 0 and writes it.

## Target end-state
- `set parents` and `set next_edges` check every id with create's existing lookup; a missing id refuses the write by name and nothing is written.

## Invariants
- One lookup for create and set; no second check.

## Falsifier
1. test_w2b_a_set_naming_a_missing_id_is_refused[parents,next_edges] passes (strict xfail today).
2. Negative: a `set parents` naming a missing id exits 0.

## Out of scope
goal:g4.18.6.2.2 (create's walk)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-1 (bundle 4 re-scope, 20:5xZ 09-29) from verdict:dg2b4-w2b conjuncts (1)+(2): ~10 lines on the set path. Hypothesis: set-link-fields-refuse-a-missing-id.
<!-- THOUGHT:END -->
