---
id: goal:g9.4
mint_id: 25db24d1dfdb4bdcb089fd251102f79f
type: goal
parents:
  - goal:g9
confidence: 1.0
edited_by: director
goal_id: G9.4
goal_kind: subgoal
heading_level: 3
origin: goals-doc
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: L1.13
title: "G9.4: The live graph viewport: watch the whole thing, moving"
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

## Agent Notes
## Owner review, 2026-09-04 — what shipped is not this, and the goal returns to `horizon`

`viewport.py --live` renders **a list**, not a web: goals and a few neighbours,
no full node graph, no edges you can read as connections, and "spiders" that are
markers in text rather than creatures on a web. Judged against the intent above
this is a **completion failure**, and it is the clearest example the project has
of a goal delivered against its words while missing what was asked for.

The diagnosis is not that the kids underperformed. **The goal was too saturated
to aim at** — renderer unification, viewport panning, live agent positions, the
zoom axis and an ASCII-to-3D-to-browser progression, all in one node with one
mvp. Nothing in the engine detects that, so it fell to a director who did not.
That is `goal:g5.1`'s thesis observed live, and `goal:g5.2` is the mechanical
fix.

**Split, and each half chases its own mvp:**

- `goal:g9.8` — one hook layer and frame stream, the player avatar, docking, and
  LOD-on-approach. Everything both skins share.
- `goal:g9.9` — the spider web skin: every node on a web, animated ASCII spiders
  that crawl edges and mess with the nodes they are working on, motion that reads
  as alive rather than linear.
- `goal:g9.10` — the space skin: systems, planets, moons, asteroids; ships whose
  size mirrors the tier split, plus modular tiers (station, terraformer, colony);
  a player ship that flies, docks, and browses versions and chats.

Both skins are 2D top-down, share every hook, and are designed for recursion in
both directions — more zoom layers, and more agent hierarchy layers, are rows in
a table, never new branches.

**This node stays as the umbrella** and goes back to `horizon`: it is not being
worked, and it is not `complete`. It closes when the three subgoals do.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Owner review 2026-09-04: the shipped --live view is a list, not a web, so the goal returns to horizon and splits into goal:g9.8 (hook layer, player avatar, LOD), goal:g9.9 (spider skin) and goal:g9.10 (space skin). Recorded here as the worked example of a goal too saturated to aim at -- the case goal:g5.2 exists to catch mechanically.
<!-- THOUGHT:END -->
