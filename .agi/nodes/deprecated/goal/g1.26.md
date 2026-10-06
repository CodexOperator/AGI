---
id: goal:g1.26
mint_id: 662bc1c791bb4256a9705d7f1a657af6
type: goal
parents:
  - goal:g1
next_edges: []
confidence: 0.8
edited_by: belam
goal_id: G1.26
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: f750135248a126e4
season: 2
seeds: []
status: retired
tags:
  - engine
  - pass10
  - residues
title: "G1.26: PASS 10 residues -- 8 confirmed engine defects + the 30-round residue table closed by reviewed rounds (assigned: director-engine)"
town: core
---
# goal:g1.26

# goal:g1.26

## Why this exists
**Parent `goal:g1`.** PASS 10 (belam-S2-L5-XII, 09-27: BASE 9e16b8ed90 -> TIP 6c403aeb4b, 30 rounds on pi-free, 29 accept_with_residue, 1 demote, 0 RED, merged into season2/main at 2129f70bb) confirmed eight code defects and a residue table too big for one round. They were first minted flat under goal:g1; the owner (04:1xZ 09-27): "should we be spawning hypotheses or subgoals like we tell directors to spawn?" -- so they nest under this leaf (skill agi-goal §5).

## Target end-state
- every PASS 10 defect hypothesis below is closed by a merged, reviewed round (red-first test on 6c403aeb4b, green on the fix)
- every row of hypothesis:pass10-0927-residue-batch is closed by a corrective round or demoted with its measured reason

## Invariants
- the defect ids never change; a split nests a smaller leaf under this one (goal:g1.26.N)

## Falsifier
1. every hypothesis whose parent is goal:g1.26 carries a verdict, and its round's mur run key is on its node
2. negative: zero PASS 10 defect hypotheses parented directly on goal:g1

## Out of scope
- goal:g7.31.3.3 (spawn/rotate redesign), goal:g4.18.2 (skills + trim)

## Agent Notes
Assigned to **director-engine**.

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
