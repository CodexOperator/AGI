---
confidence: 1.0
goal_id: G9.4
goal_kind: subgoal
heading_level: 3
id: "goal:g9.4"
mint_id: 25db24d1dfdb4bdcb089fd251102f79f
order: 56
origin: goals-doc
parents:
  - goal:g9
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G9.4: The live graph viewport: watch the whole thing, moving"
type: goal
---

**This supersedes the dashboard as the primary view.** G9.1 answers "what is the
state" in panels of text. This answers "what does the graph *look* like, right
now, while agents are working in it" — and that is a different instrument.

What it is:
- **The whole node graph rendered as a navigable web**, at level 3 by default —
  not a 200-line truncated snapshot, the actual graph.
- **A terminal viewport that pans** up/down and left/right across a graph far
  larger than the screen. The screen is a window onto the graph, not a summary
  of it.
- **Agents appear as spiders on the web**, positioned where they are actually
  working — kids, parents and the director each distinguishable, moving as they
  move. The point is to *watch the swarm*, not read a log of it.
- **Zoom is the same axis as everywhere else** (`--level 1..5`). Zooming out
  aggregates the web; agents take appropriate positions at each grain, so a
  parent working across a whole goal reads as one spider at level 1 and resolves
  into its kids at level 3. Levels 1–3 are enough to start; 4–5 follow the axis.

Progression, deliberately: **ASCII first, then a rudimentary ASCII web, then a
3D-looking ASCII web in the wireframe style of the original *Elite*, then the
browser version (G9.2).** Each stage has to be usable on its own — the terminal
version is the one that runs beside a Claude Code session, and it is not a
throwaway prototype for the web one.

Absorbs **A2** (ASCII renderer unification): there are currently several ASCII
renderers with overlapping jobs, and this needs one that can render a viewport
rather than a whole-graph dump. Do the unification as part of this, not before
it — the viewport requirement is what tells you what the unified renderer needs
to do.

Inherits G9's invariants: reader-never-writer, and it renders damage rather than
hiding it — a broken region of the graph should be visibly broken on the web.
