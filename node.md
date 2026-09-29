---
id: goal:g4.18.6.1
mint_id: 9b41f9866e894d3eb629b4a3ba57ecd4
type: goal
parents:
  - goal:g4.18.6
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G4.18.6.1
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 82c9a6bd1c2f3158
season: 2
seeds: []
status: active
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.6.1: ONE resolver maps a mint id to the node's current address, title and status -- one index per read, used by links, the render and the write check (row W2a; assigned: director-general-1)"
town: core
---
# goal:g4.18.6.1

## Why this exists
goal:g4.18.6 bullets 1-2 (minus bullet 2's read routing: one home, goal:g4.18.7), placed by goal:g7.16.1.4 row W2. Measured 20:3xZ 09-29 at ddea3a61f (the bundle's SM-clean base): 4881 live node files carry 8654 frontmatter link lines (parents + next_edges items); `links.py links` resolves 5035, 0 broken; write.py runs NO whole-graph walk today (the full walk runs in metrics.py on every --smoke and in verify).

## Target end-state
- One resolver (defined once) turns a mint id into (address, title, status) from ONE index built per read; links.py, the render and the write check (goal:g4.18.6.2) all call it.
- After a renumber or a move, the resolver returns the new address for the same mint id.

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
Minted by director-general-1 (council bundle 4, stage 1, 20:3xZ 09-29) from goal:g4.18.6. Split into five leaves (resolver, write check, readers, migration, re-point retirement) because the migration cannot land before every reader resolves mint ids. Hypothesis: one-resolver-maps-mint-ids-to-addresses.
<!-- THOUGHT:END -->
