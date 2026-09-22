---
id: goal:g26.towns
mint_id: 308c62398c864c78a3a643d8e30c8bcd
type: goal
parents:
  - goal:g26
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.2
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 26775ccc72bc41be
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
  - towns
  - glom-2026-09-19
thought_session: belam-geom-traj-spine-2026-09-21
title: "G7.2-birth (retired g26): Town ops containers (not goal:g7.2 duplicate-ids)"
town: core
---
<!-- BODY:BEGIN -->
# goal:g26.towns

## Why
Birth goal (historical label **G7.2 under retired `goal:g26`**) for in-graph
**town** containers. Not `goal:g7.2` (duplicate node ids — different node).

## Target
Town nodes (`town:*`) are the ops SUPER-node containers; type stays `town`
(PROTECTED). Nesting SoT for goals remains parents-on-children — towns do not
registry child-goals via `seeds`.

## Invariants
- `town` type protected; parents = ladder (schema spawn).
- `town.seeds` (when present) = persistent infra this town stands up
  (posts/crons/workflows/formation instances) — **not** a child-goal registry.

## Falsifier
1. `ls .agi/nodes/town/` empty on a live mesh → birth incomplete.
2. Town `seeds:` used as goal child list → schema/comment violated.

## Out of Scope
- Trajectory type / geometry Pass-1 (see `goal:g7.34*`).
- Engine fixes (`goal:g7.33`).

## Agent Notes
Under retired umbrella `goal:g26` (folded to `goal:g7`). Title clarified
2026-09-21 Belam. Live towns: `town:core`, `town:local-maxxing`, …

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Belam 2026-09-21: clarify birth-goal wording vs goal:g7.2 duplicate-ids; town.seeds ≠ goal registry
<!-- THOUGHT:END -->
