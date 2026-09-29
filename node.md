---
id: goal:g7.16.1.3.1
mint_id: 19023171605c45dcae7400a85eb846da
type: goal
parents:
  - goal:g7.16.1.3
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.3.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 5ad4e4d16db52e6a
season: 2
seeds: []
status: active
tags:
  - formation
  - council-loop
  - bundle-3
  - local-maxxing
  - row-h3
title: "G7.16.1.3.1: one park form -- the 5 carriers of the 39 parked rows carry parked:g7.16.2, and the formation check FAILs on a row-park without its carrier tag (row H3; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.3.1

## Why this exists
goal:g7.16.1.3 (bundle 3) row H3. Bundle 2 row P made park a tag on goal and hypothesis nodes, but 39 parked ROWS live in the body tables of 5 carriers (goal:g7.33.19 · 11, hypothesis:pass10-0927-residue-batch · 11, pass11-0927 · 3, pass12-0928 · 8, passb1-0928 · 6; council measure 17:1xZ 09-29). A row has no `tags`, so switching to g7.16.2 wakes none of them.

## Target end-state
- Each of the 5 carriers carries the tag `parked:g7.16.2`, with no status change on a carrier that also holds keep rows.
- verification.py's formation check FAILs when a live node holds a `triage: parked: formation` row but no carrier tag. So a switch to g7.16.2 lists the carrier, and its body names the rows.

## Invariants
- Park stays tag-only (bundle 2 row P). No row text changes.

## Falsifier
1. The formation check FAILs on a fixture carrier with a parked row and no tag, and PASSes on the live graph.
2. Negative: `git grep -l 'triage: parked: formation' -- .agi/nodes ':!.agi/nodes/deprecated'`, minus the files tagged `parked:g7.16.2`, = 0.

## Out of scope
goal:g7.16.1.3.2 (the shared module the check moves into)

## Agent Notes
Assigned to **director-general-1**.
