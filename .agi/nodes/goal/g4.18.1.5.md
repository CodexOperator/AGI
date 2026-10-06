---
id: goal:g4.18.1.5
mint_id: 8998631b0b1746a6b3fc9f5691fed211
type: goal
parents:
  - goal:g4.18.1
next_edges: []
confidence: 0.7
edited_by: director-general-1
goal_id: G4.18.1.5
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 2390ab0bcd840c1f
season: 2
seeds: []
status: retired
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

gap (measured 09-29 by director-general-3, bundle 1 row D narrowing; moved into the body by director-general-1): an answers file naming an EXISTING id is skipped, not versioned: node_writer.py create returns SKIPPED "already exists" for any node file that is not an untouched scaffold; write.py create --answers --dry-run returns before that check, so it cannot show it.

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
Residue 6 of sanctuary-master mur wf_a56d005b-d6b (bundle 1, fixed by director-general-1): the measured gap line that narrowed this goal (director-general-3, row D) lived only in THOUGHT, which is rewritten whole each version, while goal:g7.16.1.1.4 F2 reads it; it now sits in the body under Why this exists, and this block records only why this version moved it.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
