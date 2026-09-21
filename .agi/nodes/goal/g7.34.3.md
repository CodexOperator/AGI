---
id: goal:g7.34.3
mint_id: 6598c5bf27f54089970d79bd04da234a
type: goal
parents:
  - goal:g7.34
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.34.3
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: d71478e1196418bf
season: 2
seeds: []
status: horizon
tags:
  - goal
  - subgoal
  - geometry
  - pass1
  - parked
thought_session: belam-geom-traj-spine-2026-09-21
title: "G7.34.3: B3 town → .geometry/towns/<slug>/.self (Pass 1 raw)"
town: core
---
<!-- BODY:BEGIN -->
# goal:g7.34.3

## Why
Towns lack Pass-1 raw .geometry/towns/<slug>/.self materialization; geometry home planned but not stood up.

## Target
Each live town has `.geometry/towns/<slug>/.self` Pass-1 raw (no formation recursion). town node references the path. No recursive formation expansion in this pass.

## Invariants
- Pass 1 = raw self only; no formation recursion.
- Slug matches town id leaf (core, local-maxxing).
- Does not rewrite goal parents.

## Falsifier
1. Missing `.geometry/towns/core/.self` or local-maxxing equivalent → not done.
2. Pass-1 performs formation recursion → invariant broken.

## Out of Scope
- Slim config cells (g7.34.4).
- Formation loader (g7.34.5).
- Trajectory mint (g7.34.2) except cross-links if needed.

## Agent Notes
Parked **town:core**. Parent **goal:g7.34**. B3 Pass-1 raw only.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Belam 2026-09-21: mint parked unassigned on town:core; geometry/trajectory spine; no director assign; no impl yet
<!-- THOUGHT:END -->
