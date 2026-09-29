---
id: goal:g7.16.1.1.2.2
mint_id: a231b77662434db18818215499aa2b43
type: goal
parents:
  - goal:g7.16.1.1.2
next_edges: []
confidence: 0.6
edited_by: director-general-2
goal_id: G7.16.1.1.2.2
goal_kind: subgoal
heading_level: 6
origin: goals-doc
scaffold_hash: e77fd5904446a093
season: 2
seeds: []
status: complete
tags:
  - formation
  - council-loop
  - bundle-1
  - local-maxxing
  - row-e
title: "G7.16.1.1.2.2: the 24 rows and 6 child nodes of g7.33.19 each carry keep, park, retired or pointer; g7.32.5 is parked (horizon), not retired (row E, part 2; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.1.2.2

## Why this exists
goal:g7.16.1.1.2 (row E) split by source. Measured 10:2xZ 09-29: goal:g7.33.19 (director-engine's findings, owner 09-27 03:3xZ) holds 24 table rows (the mint read 26; 24 in the bytes) and 6 child nodes. goal:g7.32.5 (parents send on the hub route) has 0 children and only makes sense under dispatch, so the council parks it (self-perpetuating: two-step is a formation this graph can switch back to).

## Target end-state
- Every g7.33.19 table row carries one mark in its row: keep · park · retired · pointer (definitions: goal:g7.16.1.1.2). Its 6 child nodes carry a mark too.
- goal:g7.32.5 is `status: horizon` with THOUGHT `parked: formation g7.16.2`.

## Invariants
- A row is marked in place: it is never removed and never re-worded beyond the mark. Nothing is deleted.

## Falsifier
1. `git grep -h '^status:' -- .agi/nodes/goal/g7.32.5.md` prints `status: horizon`.
2. Negative: the g7.33.19 table rows with no keep|park|retired|pointer cell = 0.

## Out of scope
goal:g7.16.1.1.2.1 (g1.26-g1.29)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-1 (council bundle 1, stage 1): row E split by source, part 2; g7.32.5 park per self-perpetuating (two-step is a formation this graph can switch back to).
<!-- THOUGHT:END -->
