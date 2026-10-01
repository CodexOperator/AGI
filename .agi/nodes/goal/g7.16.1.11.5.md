---
id: goal:g7.16.1.11.5
mint_id: 4b93433413834949b09316c9083ca166
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.11.5
goal_kind: subgoal
origin: owner
scaffold_hash: e977890a2a0c9afa
season: 2
seeds: []
status: active
tags:
  - council-loop
  - redesign
  - bundle
title: "G7.16.1.11.5: ROUND 5: the BOOTSTRAP config:engine <= 8,192 B (§Q zygote + the §R folds + agi-infer); expansions engine-post / engine-wrap may be larger; total <= 20,480 B"
town: core
---
# goal:g7.16.1.11.5

## Why this exists
Parent goal:g7.16.1.11: Round 5 on goal:g7.16.1.11 (c620220b4, b60af0b63): zygote 7,342 B, total 18,830 B; owner GO 06:1xZ.
## Target end-state
ROUND 5: the BOOTSTRAP config:engine <= 8,192 B (§Q zygote + the §R folds + agi-infer); expansions engine-post / engine-wrap may be larger; total <= 20,480 B.
## Invariants
every moved piece byte-exact vs v4c; parity rows unchanged.
## Falsifier
1. `[ $(wc -c < .agi/nodes/.geometry/engine.md) -le 8192 ]` exits 0 and engine-post + engine-wrap exist
2. negative: a v4c piece lost in the split: zero rows GONE in the Q.2 map
## Out of scope
the sibling leaves goal:g7.16.1.11.1 through goal:g7.16.1.11.10, each its own end-state
## OWNER, verbatim
"I just mean the 'bootstrap' package is under 8kb you get it?" (owner 05:38Z) · "Q is go" (06:1xZ; verbatim on goal:g7.16.1.11)
## Agent Notes
Assigned to **director-general-3**.
