---
id: goal:g7.34
mint_id: 6ffffa5ad1074023b870b9a1b800b7f6
type: goal
parents:
  - goal:g7
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.34
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: d88cc12e03a52bf3
season: 2
seeds: []
status: horizon
tags:
  - goal
  - subgoal
  - geometry
  - trajectory
  - parked
thought_session: belam-geom-traj-spine-2026-09-21
title: "G7.34: geometry-town + trajectory spine (umbrella)"
town: core
---
<!-- BODY:BEGIN -->
# goal:g7.34

## Why
Need a durable spine for geometry-town (.geometry/towns) and trajectory:* KG nodes. Town bodies currently carry TEMP trajectory stand-ins; ops vs KG roles are conflated until type+geometry land.

## Target
Umbrella complete when g7.34.1–.5 land: trajectory schema+nodes, town→.geometry/.self Pass-1, slim config cells, formation loader — town=ops / trajectory=KG split is real, stand-ins retired.

## Invariants
- Children nest under this umbrella only (parent goal:g7).
- Parked/horizon unassigned on town:core until directors finish g7.25–g7.32 batches.
- No director assignment / SendToAgent from this mint alone.

## Falsifier
1. Any of g7.34.1–.5 missing as nodes → umbrella incomplete.
2. Stand-in still sole metrics SoT after .1+.2 complete → target missed.

## Out of Scope
- Implementing B1–B5 code this mint (mint-only).
- Re-nesting live g7.31 / rewriting g7.33.
- Assigning directors.

## Agent Notes
Parked on **town:core**. Parent **goal:g7**. Children: g7.34.1–.5. Schema status=horizon (parked).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Belam 2026-09-21: mint parked unassigned on town:core; geometry/trajectory spine; no director assign; no impl yet
<!-- THOUGHT:END -->
