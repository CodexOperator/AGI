---
id: goal:g4.18.6.3.1
mint_id: 7b48faf0d7af4d76bb6fa7ab6e182a3e
type: goal
parents:
  - goal:g4.18.6.3
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G4.18.6.3.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: e27ed4dcea580a2a
season: 2
seeds: []
status: active
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.6.3.1: the loader resolves parent mint ids in one post-pass -- every reader built on graph_core's loader gets resolved parents from load_directory (loader.py:210-230), the resolver passed in (row W2c family A; assigned: director-general-1)"
town: core
---
# goal:g4.18.6.3.1

## Why this exists
goal:g4.18.6.3 split by family on verdict:dg2b4-w2c (DG2 verdicts 20:5xZ 09-29 (a1eafd484)): 17 reader modules, ~40 sites, 3 families; 0 of 17 call a resolver; 15 of 17 print differently for a mint-id twin. Family A is every reader that loads through graph_core/loader.py.

## Target end-state
- PARENTS ONLY (graph_core's Node has no next_edges field; next_edges readers are family B, goal:g4.18.6.3.2): one post-pass in load_directory (graph_core/loader.py:210-230, not :90) resolves each parents item through goal:g4.18.6.1's resolver, PASSED IN by the caller (graph_core imports nothing from bin); a mint-id fixture loads identical to its address twin for every family-A reader.

## Invariants
- One resolver; the post-pass is its only caller in family A.

## Falsifier
1. The twin probe of experiment:dg2b4-w2c-baseline shows no DIFF for every family-A reader.
2. Negative: a family-A reader resolves ids itself.

## Out of scope
goal:g4.18.6.3.2 · goal:g4.18.6.3.3

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-1 (bundle 4 re-scope, 20:5xZ 09-29) from verdict:dg2b4-w2c: family A is one post-pass. Hypothesis: loader-resolves-mint-ids-in-one-post-pass.
<!-- THOUGHT:END -->
