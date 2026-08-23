---
confidence: 1.0
goal_id: G1.3
goal_kind: subgoal
id: "goal:g1.3"
origin: goals-doc
parents:
  - goal:g1
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G1.3: The injected map teaches its own use"
type: goal
---

**The map shows what is in the graph and says nothing about how to move through
it.** An agent arrives holding 200 lines of ASCII render and no addressing
scheme, so the only move it knows is the one it brought from outside: open a
file. G1.1 asks for navigation to *exist*; this asks for the injected context to
*teach* it, in the same block, at the top, before the agent has spent a token.

**Adopt the supermap convention rather than inventing one.** The `.openclaw` and
`.hermes` harnesses already address a workspace coordinate-first — short stable
handles, a compact legend, full injection on the first turn and deltas after,
with an explicit refresh command instead of a per-turn re-render. Two properties
are worth copying exactly:

- **Coordinates, not identifiers.** A node is reachable by a short handle an
  agent can hold in working memory and name in one token, not by a 40-character
  id it has to copy. Ids stay canonical on disk; coordinates are the interface.
- **Full once, deltas after.** The first injection carries the whole map and the
  legend. Subsequent refreshes carry what changed. Re-rendering the entire graph
  every turn is precisely the motion this loop exists to remove.

The legend is the part that does not exist today and is the cheapest half: a
short header listing the moves available — step to a neighbour, widen, pull an
adjacent region, refresh — so navigation is discoverable from the context rather
than from a skill file the kid was never given.

**Familiarity is the point, and it is a real constraint, not a preference.** The
operator already thinks in this vocabulary across two other harnesses. A third
dialect for the same idea is the G1.2 failure mode — four overlapping
vocabularies for one concept — arriving through the front door.

Falsifier, and it must be checked both ways: if kids given coordinates still
quote full node ids and still request whole-graph renders to answer a follow-up,
the layer added tokens instead of saving them. If the injected block grows
faster than tool calls fall, the legend is too long.

Shares its substrate with **G1.1** and **G9.4** — the coordinate a kid names,
the region it requests and the viewport a human pans are one query at three
resolutions. Build one mechanism with three front-ends.
