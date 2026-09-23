---
id: goal:g2.22
mint_id: aa97fbfc71ef44f28bebbb6bab1a6824
type: goal
parents:
  - goal:g2
next_edges: []
confidence: 1.0
edited_by: belam
goal_id: G2.22
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: fdc13718afdbce29
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: g1-g7-rewrite-2026-09-19
title: "G2.22: The space skin — systems, bodies, and a fleet that mirrors the tier split"
---
# goal:g2.22

## Agent Notes
**The space skin.** Same hooks as `goal:g2.21`, same 2D top-down frame stream,
different universe.

- **Nodes are bodies:** systems, planets, moons, asteroids — the mapping from
  node type and degree to body class is a table, not a branch.
- **Agents are ships that mine them.** Ship size mirrors the tier split: a large
  ship spawns smaller ones which spawn smaller ones again — director, parent,
  kid, and whatever tiers come after.
- **Modular tiers:** space station, terraformer, colony ship and friends are rows
  in the same table, so a new agent hierarchy layer is a row rather than a
  rewrite.
- **The player ship** flies the graph, docks with `f`, and browses a node's
  versions and attached chat sessions from the dock. Opacity resolves on
  approach; `z` / `x` zoom anywhere.

If this skin and the spider skin ever need different frame data, the hook layer
in `goal:g2.20` is under-specified — fix it there.
