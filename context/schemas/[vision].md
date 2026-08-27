---
name: vision
derived_from: corpus-survey-2026-08-25 (n=17 as app_purpose); renamed app_purpose -> vision 2026-08-27; spawn block PRESCRIPTIVE from that date
fields:
  title: {type: str}
  parents: {type: list}      # overview ids
  season: {type: int}        # which season this version of the vision belongs to
  proposes_goals: {type: list}   # goal ids this vision proposes -- NOT lineage, see [shape].md
  next_edges: {type: list}
  tags: {type: list}
  status: {type: str}        # open | active | closed
  confidence: {type: float}
  subgraph: {type: bool}
validation:
  required: [id, type, mint_id, title, parents, tags]
  types:
    parents: list
    tags: list
spawn:
  allowed_parents: [overview]
  min_parents: 2
  max_parents: 4
  min_parents_by_type: {overview: 2}
---

# vision

**The convergence end of the graph, and its only cycle — closed across
seasons, never within one.** Renamed from `app_purpose` on 2026-08-27: the
old name described one kind of project (an app) and the node is not about
apps, it is about what the whole graph is for.

ID prefix: `vision:<short-slug>`.

## Why this is not the top of a chain any more

`app_purpose` was a terminus: outcomes aggregated into it and stopped. A
vision does one more thing — **it proposes the goals that start the next
season**, which is what makes the graph a loop rather than a funnel.

That loop is the dangerous part, and the shape below is chosen specifically
to keep it safe. Stated plainly, because getting it wrong breaks every
traversal in the engine:

    goal -> ... -> outcome -> bigger_outcome -> overview -> vision   (parents, lineage)
    vision --proposes_goals@season N+1--> goal                       (NOT parents)

**`proposes_goals` is not a `parents:` edge and must never become one.** If a
vision were a parent of a goal, the type graph would contain a directed cycle
(`goal -> ... -> vision -> goal`), and `parents` is what chain depth,
`outcome_coverage` and every renderer walk. This project has already been
broken once by cyclic structure — 9 chains x 2000 hops of shortcut cycles
whose pathological shape took out the render path — and a cycle at the *type*
level is worse than one instance of it, because every future node inherits it.
`[shape].md :: edge_fields` classifies `proposes_goals` as non-traversable for
exactly this reason.

The loop still closes. It closes **across seasons**, which is the only way it
can close and stay acyclic: `vision@season 1` proposes goals -> those goals
produce outcomes -> outcomes aggregate into `overview` nodes -> enough
overviews assemble `vision@season 2`. Instance-level, that is a DAG: no node
is ever its own ancestor, because the vision that proposes a goal is a
different, earlier version than the vision that goal eventually feeds.

## Spawn rule — PRESCRIPTIVE, like `[bigger_outcome].md`

`allowed_parents: [overview]`, `min_parents: 2`, `max_parents: 4`,
`min_parents_by_type: {overview: 2}`.

Measured over all 17 nodes before the rename: parents were `bigger_outcome`
15 and `outcome` 2, and **`overview` 0** — the type did not exist. So 17 of 17
violate the new rule and keep their place; the gate runs on the writer path
(G7). This is a floor for what gets written from here on.

Two overviews minimum is the convergence forcing. A vision assembled from a
single overview is a rename of that overview, not a synthesis, and the whole
point of this end of the graph is that it is **harder to earn than the middle**.

## Seasons

`season: <int>` distinguishes versions of the vision. It is not a `@v2` node
and not a `supersedes:` pair — those are forbidden here as everywhere (G6.3);
a new season is a **new node**, because it has different parents (the
overviews of that season) and makes different proposals. Contrast with the
grid, which versions *the same* node as it is edited. Both dimensions exist
and they answer different questions: the grid says "how did this node change",
the season says "which iteration of the vision is this".

The scoring loop this enables — assemble a vision from overviews without
looking at the previous one, then measure how close it landed — is **designed
and not built**. What is built is the field and the acyclic shape that makes
it expressible. Recorded as the residual, not claimed as done.
