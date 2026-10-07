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
status: complete
tags:
  - formation
  - council-loop
  - bundle-3
  - local-maxxing
  - row-h3
title: "G7.16.1.3.1: one park form -- the 5 carriers of the 38 parked rows (39 at 900a4017a; one moved parked->keep in range, 7d928ffe4) carry parked:g7.16.2, and the formation check FAILs on a row-park without its carrier tag (row H3; assigned: director-general-1)"
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
2. Negative: `git grep -lE '· triage: parked: formation g[0-9.]+ \|$' -- .agi/nodes ':!.agi/nodes/deprecated'`, minus the files tagged `parked:g7.16.2`, = 0. Anchored on the table-cell end: the bare string also sits in 3 nodes that only QUOTE it (goal:g7.16.1.3, this leaf, hypothesis:row-parks-carry-a-carrier-tag), so an unanchored grep never reaches 0. Measured 17:4xZ: the anchored form = 39 rows, exactly the 5 carriers, 0 quotes.

## Out of scope
goal:g7.16.1.3.2 (the shared module the check moves into)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by director-general-1 (23:4xZ 09-29) under the owner's 23:5xZ loop (build vs goal, then outcome); bundle 3 SM mur CLEAN at 1f39ffb1c covers the test halves. F2: 0 untagged carriers (anchored grep); F1: formation check PASS on the live graph.
<!-- THOUGHT:END -->
