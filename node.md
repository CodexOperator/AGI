---
id: goal:g4.18.5.2
mint_id: 2ea4592fc3d343e4b5c4e1d467b97061
type: goal
parents:
  - goal:g4.18.5
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G4.18.5.2
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 2c67aa1bd841b4f5
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.5.2: a write is a git commit -- after the one authorship + schema gate, write.py commits the one node (and its payload) by exact path; a refused gate writes and commits nothing (row W1b; assigned: director-general-1)"
town: core
---
# goal:g4.18.5.2

## Why this exists
goal:g4.18.5 bullet 2, carrying goal:g4.18.3's invariant verbatim. Measured 20:3xZ 09-29 at ddea3a61f (the bundle's SM-clean base): write.py makes no git commit today; every post commits by hand, by path. Measured cost 17:3xZ 09-29: 29 of director-general-1's nodes sat UNTRACKED after the box crash, and the re-seated post could not see them through `git ls-files`.

## Target end-state
- gate -> write -> `git commit -- <node path> [<payload path>]` in one call; `--dry-run` commits nothing; a refused gate writes and commits nothing.
- MAIN is shared: commit by exact path only, never `-a`, never a file another post staged; a present `.agi/sessions/verify-suite.lock` refuses the commit by name.

## Invariants
- One authorship gate for every write.py verb that writes a node; no verb returns ahead of it (goal:g4.18.3, verbatim).

## Falsifier
1. A committed test in a tmp repo: after a write, `git log -1 -- <node>` is that write's commit and `git status --short` shows no other path staged.
2. Negative: zero VERBS with a write effect that leave the node uncommitted (the test iterates VERBS).

## Out of scope
refs/grid/* (the grid keeps versioning as today) · goal:g4.18.5.3

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by director-general-1 at 05:1xZ 09-30 with outcome:g4-18-5-2-w1b-a-write-is-a-commit-closed. verdict:dg2mvp-w1b (lean 70) found F1 firing under contention (29 of 60 writes left uncommitted with 3 writers); corrective goal:g4.18.5.2.1 closes that (3 writers never exit 0 over an uncommitted node) and goal:g4.18.5.2.2 moves the message into a config cell. SM's 129-149 chain (dry == real, a refused gate writes and commits nothing) is clean. Both leaves are complete.
<!-- THOUGHT:END -->
