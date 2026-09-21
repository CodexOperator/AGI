---
id: goal:g7.34.2
mint_id: af0ef6a1881e4318a1c3d4ef55b5e5b0
type: goal
parents:
  - goal:g7.34
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.34.2
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: aada0edf944db2d0
season: 2
seeds: []
status: horizon
tags:
  - goal
  - subgoal
  - trajectory
  - mint
  - parked
thought_session: belam-graph-only-coord-2026-09-21
title: "G7.34.2: mint trajectory:core + local-maxxing; town→traj; traj→chain"
town: core
---
<!-- BODY:BEGIN -->
# goal:g7.34.2

## Why
Stand-ins in town:core / town:local-maxxing bodies must become real trajectory:* nodes with town→traj and traj→chain links.

## Target
trajectory:core + trajectory:local-maxxing minted from stand-ins; town bodies point to them; traj nodes link into chain/metric movers; doc:lm-town-trajectory deprecated pointer only.

## Invariants
- Migration moves content (never silent delete).
- Town keeps ops bundle; traj owns metrics/progress/links.
- mint_id preserved on any rename/migrate path.

## Falsifier
1. `ls .agi/nodes/trajectory/` missing core or local-maxxing → not done.
2. town body still sole metrics SoT with no traj link → not done.
3. links.py reports broken traj→chain edges → not done.

## Out of Scope
- Authoring [trajectory] schema (g7.34.1).
- .geometry/towns Pass-1 (g7.34.3).
- Research round execution.

## Agent Notes
Parked **town:core**. Parent **goal:g7.34**. G7.34.2 only. Depends on goal:g7.34.1.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Belam 2026-09-21: mint parked unassigned on town:core; geometry/trajectory spine; no director assign; no impl yet
<!-- THOUGHT:END -->
