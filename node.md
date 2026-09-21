---
id: goal:g2.3
mint_id: 5c2f2729778949ed98b3db262dbb1f4b
type: goal
parents:
  - goal:g2
confidence: 1.0
edited_by: season.py
goal_id: G2.3
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G2.3: `graph_builder` becomes data-source-agnostic and cold-builds fast"
---
`agi_algos/graph_builder.py` is the code-intelligence layer and the natural
substrate for zoom levels 4–5, but it is coupled to specific data sources and is
slow on a cold build. Absorbs **A1** (data-source-agnostic refactor) and **A3**
(cold-build optimisation).

Also carries a cleanup with a real trap in it: `graph_builder.parse_goals()`
parses a *different* `goals/` directory into `goal`-type nodes for a 35-node-type
code graph, and its only call site hardcodes a path that no longer exists, so it
returns 0. It is dead code, unrelated to `GOALS.md`, and **two different things
named "goal" in one codebase will mislead every future reader.** Repoint or
delete it.