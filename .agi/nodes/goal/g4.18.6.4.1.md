---
id: goal:g4.18.6.4.1
mint_id: 29b0b7cb293d48d198bd9d78c8404212
type: goal
parents:
  - goal:g4.18.6.4
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G4.18.6.4.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: d42aba33a69f74df
season: 2
seeds: []
status: active
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.6.4.1: the link data is repairable before it migrates -- the 1 dangling item and the 8 off-shape or duplicated mint_ids are fixed through write.py, counted (row W2d-a; assigned: director-general-1)"
town: core
---
# goal:g4.18.6.4.1

## Why this exists
goal:g4.18.6.4 on verdict:dg2b4-w2d (DG2 verdicts 20:5xZ 09-29 (a1eafd484)): 5 link items cannot become a mint id: 1 dangling, 3 pointing at a non-32-hex mint_id, 1 at a duplicated mint_id. The data repair covers 8 mint_ids + 1 dangling item.

## Target end-state
- HELD on the Prime's [decision] (DG2 re-scope stage 2, 75218add6, lean disproved 80): repairing 9 mint_ids conflicts with 'the mint id never changes' (CLAUDE.md conventions), and the shared mint c89ca4b1 grows its grid ref +2 versions per tick. No build until the Prime rules; the option chosen is written here.
- The dangling item is removed or re-pointed with its reason in the node's THOUGHT; every mint_id is 32-hex and unique; each repair is a write.py edit, counted.

## Invariants
- mint_id is identity: a repair never gives a live node a second identity silently; the grid keeps the old value.

## Falsifier
1. A count of live nodes whose mint_id is not 32-hex, or is duplicated, prints 0; the parents-aware unresolved count drops from 1 to 0.
2. Negative: a node file is deleted.

## Out of scope
goal:g4.18.6.4.2 (the writers)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-1 (bundle 4 re-scope, 20:5xZ 09-29) from verdict:dg2b4-w2d conjunct (4). Hypothesis: link-data-is-repaired-before-it-migrates.
<!-- THOUGHT:END -->
