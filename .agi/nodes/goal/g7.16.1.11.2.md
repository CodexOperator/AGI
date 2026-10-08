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
2. negative: a new workflow script under extensions/: `git log --since=2026-10-01T07:25:00Z --diff-filter=A --name-only --format= -- extensions | grep -c '/workflow[^/]*$'` prints 0 (the 3 existing workflow* files date from 09-07, 09-10, 09-18, before this round)
## Out of scope
the sibling leaves goal:g7.16.1.11.1 through goal:g7.16.1.11.10, each its own end-state
## OWNER, verbatim
"It's all just vectors literally pointing to things." (owner 03:48Z; full text verbatim on goal:g7.16.1.11)
## Agent Notes
Assigned to **council**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 10-07 (goal:g1.41 PASS B4; this goal was minted complete with no measurement recorded): falsifiers run at trunk 86d234fcd1. F1 `grep -c '^## [LMN] ' radically-simple-engine.md` prints 3 (sections L, M, N at lines 694, 756, 809). F2 as written ('zero new files named workflow*') had no cut and 3 such files exist; with the cut at this round's mint (10-01 07:25Z) it prints 0.
<!-- THOUGHT:END -->
