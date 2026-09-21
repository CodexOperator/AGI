---
id: goal:g7.34.5
mint_id: 761414c6f0c04d769499008f92aa9ef8
type: goal
parents:
  - goal:g7.34
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.34.5
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: cef96a6c00373b6c
season: 2
seeds: []
status: horizon
tags:
  - goal
  - subgoal
  - geometry
  - formation
  - parked
thought_session: belam-geom-traj-spine-2026-09-21
title: "G7.34.5: B5 formation nested template + single context loader (L6)"
town: core
---
<!-- BODY:BEGIN -->
# goal:g7.34.5

## Why
Formation should be nested template + single context loader (L6 renderer), not ad-hoc multi-loaders.

## Target
One formation renderer: nested template + single context loader. Documented seam; old multi-loader paths retired or pointed.

## Invariants
- Single loader entrypoint.
- Nested templates only (no parallel ad-hoc render paths for the same formation).
- Does not recurse in Pass-1 (g7.34.3 stays raw).

## Falsifier
1. Two live loaders for the same formation context → not done.
2. Pass-1 raw .self requires formation recursion to exist → scope leak.

## Out of Scope
- Pass-1 raw .self (g7.34.3).
- Trajectory KG work (g7.34.1/.2).

## Agent Notes
Parked **town:core**. Parent **goal:g7.34**. B5 L6 renderer.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Belam 2026-09-21: mint parked unassigned on town:core; geometry/trajectory spine; no director assign; no impl yet
<!-- THOUGHT:END -->
