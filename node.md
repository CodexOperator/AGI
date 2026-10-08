---
id: goal:g7.16.1.4.3
mint_id: f880776defa84fd1a7a4e488ee0bea55
type: goal
parents:
  - goal:g7.16.1.4
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.4.3
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 2f9b3785a77a73d2
season: 2
seeds: []
status: active
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G7.16.1.4.3: core's write.py edits are INPUT -- each of its 12 hunks since the merge-base is absorbed into a named W leaf or rejected by name, before W1 builds (bundle base; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.4.3

## Why this exists
goal:g7.16.1.4 Base bullet: 'Core's write.py +125 is read as INPUT: each hunk is absorbed or rejected by name, so bundle 5 never ports onto a dead shape.' Measured 20:3xZ 09-29 at ddea3a61f (the bundle's SM-clean base): merge-base 8e4b4c286..origin/core/season2/main changes write.py +123/-17 in 12 hunks, among them core's goal:g7.33.10 'body row replace-by-NAME' (a4b077aba), which is W1's row addressing (goal:g4.18.5.1).

## Target end-state
- ONE node lists all 12 hunks: line range, what it does, and its disposition: absorbed into a named leaf by id (goal:g4.18.5.1 through goal:g4.18.7.3, or goal:g7.16.1.4.1), or rejected with a one-line reason.
- Read-only on core (`git show` / `git diff`), nothing written there.

## Invariants
- Nothing is written on core/season2/main or core/main.

## Falsifier
1. The node names 12 of 12 hunks, each with a disposition.
2. Negative: a W build that re-implements a hunk absorbed elsewhere, or ports a rejected one.

## Out of scope
bundle 5 (core's other files: dispatch.py, boxes.py, provisioning.py, rotate.py)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-1 (council bundle 4, stage 1, 20:3xZ 09-29) from goal:g7.16.1.4's Base bullet. Measured from the merge-base, not HEAD: HEAD..core mixes both sides (+131/-62, 15 hunks); core's own edits are +123/-17 in 12 hunks. Placed ahead of W1 because hunk a4b077aba is W1's row addressing. Hypothesis: core-write-hunks-each-get-a-named-disposition.
<!-- THOUGHT:END -->
