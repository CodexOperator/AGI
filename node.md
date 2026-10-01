---
id: goal:g7.16.1.11.2
mint_id: 5d598054c43746e79af48eac91a462a8
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.16.1.11.2
goal_kind: subgoal
origin: owner
scaffold_hash: 0aaffbf8a8883e12
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - redesign
  - bundle
title: "G7.16.1.11.2: round 4: everything is a vector -- launch vectors, schema / guard / location vectors, the pane as 2 files, 25 guards mapped (§L-§N)"
town: core
---
# goal:g7.16.1.11.2

## Why this exists
Parent goal:g7.16.1.11: Round 4 on goal:g7.16.1.11 (@bfc04e8588): the owner's 03:48Z vector line turned into §L-§N of doc:radically-simple-engine.
## Target end-state
round 4: everything is a vector -- launch vectors, schema / guard / location vectors, the pane as 2 files, 25 guards mapped (§L-§N).
## Invariants
posts, subagents and workflows are ONE launch vector run inside the wrapper; workflow.py retires.
## Falsifier
1. `grep -c '^## [LMN] ' .agi/nodes/doc/radically-simple-engine.md` prints 3
2. negative: a new workflow script under extensions/: zero new files named workflow*
## Out of scope
the sibling leaves goal:g7.16.1.11.1 through goal:g7.16.1.11.10, each its own end-state
## OWNER, verbatim
"It's all just vectors literally pointing to things." (owner 03:48Z; full text verbatim on goal:g7.16.1.11)
## Agent Notes
Assigned to **council**.
