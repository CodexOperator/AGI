---
id: goal:g10.3
mint_id: 71cb54ea76764946a6baade1b58e8c26
type: goal
parents:
  - goal:g10
confidence: 1.0
edited_by: season.py
goal_id: G10.3
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
title: "G10.3: The legendary map: a minimap that is itself the territory"
---
**The widest possible view — what exists, and what can be done to it.** The old
`.openclaw`/`.hermes` supermap, taken further and made legible: not just an
overview of the graph but **a legend of the actions available in it**, rendered
as part of the same surface an agent already reads.

The property that makes it worth building rather than writing as a help page:
**the legendary map is itself a map, with the same zoom and LOD axes as the
hypergraph.** It demonstrates the moves by being a thing you make the moves on.
An agent learning to navigate does so by navigating the legend — and it carries,
in itself, the statement that it is navigable the same ways. Self-describing in
the strict sense, not the decorative one.

This is what makes **G1.6**'s one-word commands discoverable without a manual.
The legend shows the command; the map you are looking at is where you practise
it; the graph you then move to responds identically.

Falsifier, and it is a behavioural one: give an agent the legendary map and no
other instruction on how to navigate, and see whether it moves. If it needs the
prose brief anyway, the legend has not replaced the manual — it has become a
second one, which is **G1.2**'s failure mode.

Depends on **G1.3** (the supermap convention it extends), **G10.2** (the actions
it lists should be read from the geometry, not hardcoded a second time).