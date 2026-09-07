---
id: goal:g9.9
mint_id: 6b292e4fdd41404e98de2844500ff829
type: goal
parents:
  - goal:g9
  - build:COMPLETE.md
next_edges: []
confidence: 1.0
edited_by: season.py
goal_id: G9.9
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 672c16a6614fe72a
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G9.9: The spider web skin — a living web, animated spiders, every node on it"
---
# goal:g9.9

## Agent Notes
**The spider skin.** The graph is a web, drawn in ASCII, and it is alive.

- Nodes are anchor points, edges are silk. The web is the real graph, every node
  on it.
- **Agents are little animated ASCII spiders that crawl** — a parent sits on the
  goal or node it was pointed at; when it needs to clean up after a kid it
  *walks the edge* to that node and visibly messes with it. Kids jump between the
  nodes they are editing. You watch the swarm work rather than read a log of it.
- Motion must read as **living, not linear**: a jump is a wind-up, a leap and a
  settle, minimal in glyphs but never a constant-rate slide between two cells.
- The player avatar is a jumping spider that can traverse the web in any
  direction, same animation grammar.
- Damage stays visible (`goal:g9`'s invariant): a broken region of the graph
  looks like a torn web.

Everything under it comes from `goal:g9.8`'s hook layer. This node owns the
paint, the animation grammar, and nothing else.