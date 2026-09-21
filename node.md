---
id: goal:g2.1
mint_id: d1a6a806b6af413a82f6cc1b2a7471f9
type: goal
parents:
  - goal:g2
confidence: 1.0
edited_by: season.py
goal_id: G2.1
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds:
  - hyp:level3-node-anatomy
  - idea:engine-agi-algos
  - idea:engine-level3
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G2.1: Level 3 first: code nodes that stitch back into a running tree"
---
**Build level 3 before any other level.** It is the one that makes the graph an
executable artifact rather than a description of one, and it is the level with
an existing index to stand on: GitNexus already holds this repo's symbols, call
graph and execution flows. A level-3 node is not a new parse of the code — it is
a code surface **plus the thought attached to it**: why it exists, what it
promises, what it requires.

What has to be true:
- A level-3 node round-trips: graph → directory of files → running software →
  back to graph, with no hand-editing in either direction.
- Its contract half (IO map, invariant citations, file paths, frontmatter) is
  **attached mechanically by the harness**, never authored by a summarising
  model. G2's measured falsifier is why: 0.000 frontmatter recall, 0.111 file
  paths.
- The index is a *seed*, not the source of truth. Known gap: GitNexus has zero
  symbol coverage of all twelve `bin/*.py`, which is the half of the engine
  where every 2026-08 change landed.