---
name: vision
derived_from: corpus-survey-2026-08-25 (n=17 as app_purpose); renamed app_purpose -> vision 2026-08-27; spawn block PRESCRIPTIVE from that date
fields:
  title: {type: str}
  parents: {type: list}      # moral ids — the constitution a vision is grounded in
  season: {type: int}        # which season this version of the vision belongs to
  season_parents: {type: list}   # overview ids from the previous season — NOT lineage, see [shape].md
  proposes_goals: {type: list}   # goal ids this vision proposes -- NOT lineage, see [shape].md
  moral_adherence: {type: dict}  # one entry per moral parent: aligned | violated | unknown
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
  allowed_parents: [moral]
  min_parents: 1
  max_parents: 4
  min_parents_by_type: {moral: 1}
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

## Spawn rule — PRESCRIPTIVE (L2 wave 1)

`allowed_parents: [moral]`, `min_parents: 1`, `max_parents: 4`,
`min_parents_by_type: {moral: 1}`.

A vision is now grounded in at least one moral (the constitution). The
previous season's overviews migrate to `season_parents:` (role: season,
non-traversable for chain depth). Cap of 3 visions from season 2 lives on
`.agi/nodes/.geometry/ladder.md`.

The 17 season-1 visions remain on `bigger_outcome` directly and are
grandfathered: they keep their structure, get retagged `season: 1` and
`status: closed` in wave 4, and still validate because the schema change is
creation-time only (G7).

## Seasons

`season: <int>` distinguishes versions of the vision. `season_parents:` holds
the previous season's overview ids — the `role: season` edge that bounds
chains across seasons without entering chain depth (see `[shape].md :: edge_fields`).

It is not a `@v2` node and not a `supersedes:` pair — those are forbidden here
as everywhere (G6.3); a new season is a **new node**, because it has different
parents (the morals of that season) and makes different proposals. Contrast
with the grid, which versions *the same* node as it is edited. Both dimensions
exist and they answer different questions: the grid says "how did this node
change", the season says "which iteration of the vision is this".

The scoring loop this enables — assemble a vision from overviews without
looking at the previous one, then measure how close it landed — is **designed
and not built**. What is built is the field and the acyclic shape that makes
it expressible. Recorded as the residual, not claimed as done.

## Moral adherence

`moral_adherence:` is a dict with one key per moral parent. Each value is one
of `aligned`, `violated` or `unknown`. Populated during the overview's
moral audit at season close; a vision inherits its overviews' audits.

| key | meaning |
|---|---|
| aligned | all overviews under this vision report the moral as satisfied |
| violated | any overview reports this moral violated |
| unknown | no overview has answered this moral's question yet |

## The `THOUGHT` block (goal:g2.11)

A node body may carry one authored region, marked exactly like the harness
markers it sits beside:

```
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
why this version differs from the last one
<!-- THOUGHT:END -->
```

**`body` is state; `thought` is delta.** The body says what this node asserts
now. The thought says why *this version* differs from the previous one — it is
rewritten from scratch on each change, not accumulated.

- **Absent means empty.** No node is required to carry one, which is why
  introducing the block churned 0 of 786 existing nodes. Fill it when there is
  something to say; never fabricate one after the fact.
- **It survives regeneration.** Writers that rebuild a body (`level3.py`,
  `snapshot-build-site.py`, `decompose-engine.py`) carry this region across
  verbatim via `write_frontmatter(..., preserve_body=...)`. Before 2026-08-27
  they did not, and 8,034 authored contract fields were destroyed unread
  (goal:g2.10).
- **Versioning is free.** The grid snapshots `node.md` once per version, so
  each grid commit already carries the thought current at that version.
- **Not in frontmatter, deliberately.** `write_frontmatter` flattens newlines,
  so multi-line prose in a frontmatter field is silently destroyed. The short
  scalar `thought_session:` is reserved there for goal:g2.7 / goal:g10.1 to
  point at the chat that produced a version; it is not populated yet.
- **Readers strip it.** Thought is provenance to zoom into, not weight every
  reader carries forever. `snapshot-goals.py --render` strips it explicitly via
  `strip_thought()`; `render-context.py` and `zoom.py` never see it because
  they read frontmatter only (`load_node_file(..., body=False)`) and so carry
  no body text at all. The rule binds any future reader that *does* read
  bodies.
