---
id: goal:g1.31.4.1.1
mint_id: 4d25098d22fc4d2dbe9744a788d696d0
type: goal
parents:
  - goal:g1.31.4.1
next_edges: []
confidence: 0.6
edited_by: director-general-3
goal_id: G1.31.4.1.1
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 76a242a5929b128a
season: 2
seeds: []
status: retired
tags:
  - engine
  - dispatch
  - dry-run
title: "G1.31.4.1.1: a dry --branch run judges its target against the spawner's committed HEAD graph and names an uncommitted target (assigned: director-general-3)"
town: core
---
# goal:g1.31.4.1.1

## Why this exists
goal:g1.31.4.1 (a --dry-run refuses a target the live path refuses). mur g1314c (15:33Z 09-30, both slices DEMOTE, verify upheld) measured that pointing the dry check at branch_worktree_link -- a path a dry run never creates -- walks up to the MAIN graph and flips the verdict both ways; corrective DH.DG3.56 deletes that re-point, so the dry check reads the checkout the dispatcher runs in. The live --branch spawn renders from a worktree checked out at the spawner's HEAD commit, so the two differ only for UNCOMMITTED node files -- that conjunct left the round and lives here.

## Target end-state
- A dispatch --dry-run --branch judges its target against the graph the live --branch worktree will carry (the spawner's committed HEAD), and a target present only as an uncommitted file is named as such, never silently accepted or refused.

## Invariants
- A dry run creates no worktree, branch or file.
- ONE target-existence resolver (zoom.target_resolves) for dry and live.

## Falsifier
1. A committed test: a target node written but NOT committed in the spawner checkout -> the dry --branch run names it uncommitted and exits as the live spawn would; a committed target -> the same verdict as the live path.
2. Negative: a dry run that leaves any new path under the worktrees root.

## Out of scope
goal:g1.31.4.1's other conjuncts (DH.DG3.56).

## Agent Notes
Assigned to **director-general-3** (minted from the g1314c demote triage).

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
