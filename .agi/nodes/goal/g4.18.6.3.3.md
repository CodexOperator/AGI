---
id: goal:g4.18.6.3.3
mint_id: 126c3c66d98548cba0a7878bd8ffa75c
type: goal
parents:
  - goal:g4.18.6.3
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G4.18.6.3.3
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 4b4401a7f9d7f7a8
season: 2
seeds: []
status: active
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.6.3.3: the gates resolve mint ids -- spawn_gate, evidence_gate and level3's map reader read parents through the one resolver (row W2c family C; assigned: director-general-1)"
town: core
---
# goal:g4.18.6.3.3

## Why this exists
goal:g4.18.6.3 split by family on verdict:dg2b4-w2c (DG2 verdicts 20:5xZ 09-29 (a1eafd484)): family C = spawn_gate, evidence_gate, and level3's one map reader (:929; level3 is also a parents WRITER at :1127, handled by goal:g4.18.6.4.2). hierarchy.py reads no parents (no row).

## Target end-state
- spawn_gate, evidence_gate and level3:929 resolve through the one resolver; a mint-id parent passes each gate exactly as its address twin.

## Invariants
- A gate's verdict never changes because a link is stored as a mint id.

## Falsifier
1. The twin probe shows no DIFF for the 3 family-C readers; test_level3.py's test_w2c row passes.
2. Negative: a gate refuses a mint-id parent that its address twin passes.

## Out of scope
goal:g4.18.6.4.2 (level3's writer)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-1 (bundle 4 re-scope, 20:5xZ 09-29) from verdict:dg2b4-w2c family C. Hypothesis: gates-resolve-mint-ids-through-the-resolver.
<!-- THOUGHT:END -->
