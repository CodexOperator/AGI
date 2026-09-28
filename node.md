---
id: goal:g4.18.1.5
mint_id: 8998631b0b1746a6b3fc9f5691fed211
type: goal
parents:
  - goal:g4.18.1
next_edges: []
confidence: 0.7
edited_by: director-engine
goal_id: G4.18.1.5
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 2390ab0bcd840c1f
season: 2
seeds: []
status: active
tags:
  - engine
  - write
title: "G4.18.1.5: a new version through the same route -- an answers file naming an existing id writes it in place, same validator"
town: core
---
# goal:g4.18.1.5

# goal:g4.18.1.5

## OWNER 2026-09-26 ~23:2xZ, verbatim (fragment; whole quote on goal:g4.18.1)
"Then also modifying an existing node with a new version could also use the same shared mint route as a brand new node with a fresh file." / "write is used for both or at least the node part and raw file is just written to disk."

## Why this exists
goal:g4.18.1 -- a new version is an in-place edit plus `grid.py commit` (G6.3), but it goes through write.py's verb script while a new node goes through `create`: two routes, two sets of checks.

## Target end-state
- An answers file or draft naming an EXISTING node id writes a new version of it in place through the same validator as a fresh mint; its raw file (if any) is rewritten at its location row.
- No second node file, no `@v2`, no `supersedes:` pair; the grid carries the history.

## Invariants
- A version write keeps the mint id and every existing edge.

## Falsifier
1. Re-minting an existing temp node from an edited answers file changes its bytes in place, keeps its mint_id, and creates no new file, exit 0.
2. Negative: the same answers file with a row its schema refuses writes nothing.

## Out of scope
goal:g4.18.1.1 · goal:g4.18.1.2 · goal:g4.18.1.3 · goal:g4.18.1.4

## Agent Notes
Assigned to **director-engine**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. Minted by director-engine as one of five nested leaves of goal:g4.18.1 (standing: nest an ASSIGNED goal into sketched leaves before any parent is spawned). The split follows the owner quote on goal:g4.18.1 and the refinements (a) (b) (c) read there; refinement (d) per-function skills is goal:g4.18.2 and is not repeated; (e) role-template text goes up through the master as template lines. confidence/origin/seeds/tags were set after the create because the agi-goal skill mint command omits them while [goal].md requires them.
<!-- THOUGHT:END -->
