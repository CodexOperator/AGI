---
id: goal:g7.34.4
mint_id: 336a082250194b808fb2a6f7f58a41d9
type: goal
parents:
  - goal:g7.34
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.34.4
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 072060429f5ebcdc
season: 2
seeds: []
status: horizon
tags:
  - goal
  - subgoal
  - geometry
  - config-max
  - parked
thought_session: belam-geom-traj-spine-2026-09-21
title: "G7.34.4: B4 slim config/template pointer cells on town.self (L6)"
town: core
---
<!-- BODY:BEGIN -->
# goal:g7.34.4

## Why
town.self needs L6 config-max: slim config / template pointer cells, not fat inlined blobs.

## Target
town.self carries slim pointer cells to config/templates (L6 config-max). Fat bodies refused by convention; pointers resolve.

## Invariants
- Pointers over copies.
- Compatible with Pass-1 .self from g7.34.3.
- No second SoT for posts/crons beyond existing config nodes.

## Falsifier
1. town.self inlines full template bodies → not done.
2. Pointers dangling (missing targets) → not done.

## Out of Scope
- Formation nested template loader (g7.34.5).
- Trajectory schema (g7.34.1).

## Agent Notes
Parked **town:core**. Parent **goal:g7.34**. B4 L6 config-max.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Belam 2026-09-21: mint parked unassigned on town:core; geometry/trajectory spine; no director assign; no impl yet
<!-- THOUGHT:END -->
