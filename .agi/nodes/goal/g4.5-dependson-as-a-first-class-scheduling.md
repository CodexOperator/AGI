---
id: goal:g4.5
mint_id: 3caaf35b1cb24fc8811eaf51364e1df2
type: goal
parents:
  - goal:g4
confidence: 1.0
edited_by: season.py
goal_id: G4.5
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
title: "G4.5: `depends_on` as a first-class scheduling edge"
---
The edge already exists, under another name and confined to one type.
`blocked_by` is carried by 94 `task` nodes, 89 of them populated, with exactly
**one** dangling reference (`task:t-012` -> `task:t-020`, which names no node)
and **zero cycles** at a maximum depth of 15. That is the best referential
integrity of any edge in this graph, and it is invisible to every other type.

Three moves, in order:

1. **Generalize.** Rename `blocked_by` -> `depends_on` and allow it on every
   type. Reader accepts both spellings first, then the data migrates, then the
   writer drops the old name -- the S11 sequence, for the S11 reason: a
   half-applied rename that a generator no longer recognises prunes real
   nodes.
2. **Keep it out of every walk.** `parents` is lineage; `depends_on` is build
   order. `[shape].md :: edge_fields` now classifies both and `spawn_gate.py`
   parses it, but **no walker consults that classification yet** -- this goal
   owns adding the deny-list to `metrics.py` and the chain walkers. Until it
   lands the guard is a declaration, not a control.
3. **Dispatch reads it.** Build order should follow the dependency graph, not
   attractiveness score alone.

**Why the walk guard is not optional.** A scheduling edge that a depth metric
counts is a new gaming surface, and this project has already paid for that
exact mistake once: 9 chains x 2000 hops of shortcut cycles carrying no
signal, whose pathological structure then broke the render path outright.
`depends_on` is denser and more legitimate-looking than a shortcut cycle,
which makes it a worse offender, not a better one. Pairs with **G3**.