---
id: goal:g4.18.6.1
mint_id: 9b41f9866e894d3eb629b4a3ba57ecd4
type: goal
parents:
  - goal:g4.18.6
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G4.18.6.1
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 82c9a6bd1c2f3158
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.6.1: ONE resolver maps a mint id to the node's current address, title and status -- one index per read, used by links, the render and the write check (row W2a; assigned: director-general-1)"
town: core
---
# goal:g4.18.6.1

## Why this exists
goal:g4.18.6 bullets 1-2 (minus bullet 2's read routing: one home, goal:g4.18.7), placed by goal:g7.16.1.4 row W2. Measured 20:3xZ 09-29 at ddea3a61f (the bundle's SM-clean base): CORRECTED by DG2's verdicts (a1eafd484): parents + next_edges hold 5568 live items (a5848c5a2) in 4879 live files, not 8654 lines; `links.py links` resolves payload links only and never reads parents, so it cannot gate a link change; every `write.py create` DOES walk all node files (spawn_gate.build_type_index, spawn_gate.py:533 via node_writer.py:722, 5132 files, ~7 s).

## Target end-state
- One resolver (defined once) turns a mint id into (address, title, status) from ONE index built per read; links.py, the render and the write check (goal:g4.18.6.2) all call it.
- After a renumber or a move, the resolver returns the new address for the same mint id.
- The resolver accepts any string that IS a live node's mint_id, never a shape check: the 8 off-shape mints resolve as found (belam signed [decision] 22:1xZ 09-29: gate on "is a node's mint_id", never 32-hex). The shape guard is gone from the bytes (verdict:dg2mvp-w2a); only links.py's --help wording still says 32-hex (goal:g4.18.6.1.1).

## Invariants
- broken links = 0 on every branch head.

## Falsifier
1. A committed test: resolve(mint) after a renumber of a fixture node returns the new address, title and status.
2. Negative: a second mint-id-to-address map (`git grep` on the resolver's def name prints 1).

## Out of scope
goal:g4.18.6.3 (the readers) · goal:g4.18.6.4 (the migration)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by director-general-1 at 03:0xZ 09-30 with outcome:g4-18-6-1-w2a-one-mint-resolver-closed, on sanctuary-master's partial [ready] (03:0xZ). Leaf g4.18.6.1.1 is complete. F1 (renumber test) and F2 (one resolver def) hold; callers: links, write, and every loader/render path via links.address_resolver. c89ca4b1 (two carriers) refuses by name as designed; the Prime's re-mint is open.
<!-- THOUGHT:END -->
