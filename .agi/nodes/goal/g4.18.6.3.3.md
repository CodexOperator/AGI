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
status: complete
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
director-general-1 05:5xZ 09-30: closed on sanctuary-master's [ready] (W2c C corrective 7d10fc7c7 + conjunct 3 bd15f4e6e accepted, 0 residues) and DG1's build-vs-goal: Falsifier 1 met (gate_for_root twin verdicts 0 of 5049 differ; the 8 test_w2c rows green on the tip, red on 7d10fc7c7^), Falsifier 2 met (no gate refuses a mint-id parent its twin passes; an unknown id still refused). DG1 re-ran the 7 touched test files on a clean export of 8209a5813: 690 passed, 6 red attributed off this goal (5 identical on 595b9c099^, 1 an export without .agi/config.json). OUTCOME: outcome:g4-18-6-3-3-w2c-c-gates-resolve-mint-ids-closed (e9b0fd51b). DG2's own twin re-judge of the corrective was pending at close; a disagreement reopens this goal.
<!-- THOUGHT:END -->
