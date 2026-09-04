---
id: goal:g1.12
mint_id: 8749c849dfc0416f82094d1345478ff5
type: goal
parents:
  - goal:g1
next_edges: []
confidence: 1.0
edited_by: director
goal_id: G1.12
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 5b4069c7b33c0b38
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: L1.13
title: "G1.12: Loop flavor is a tag: research, exploration, development, implementation"
---
# goal:g1.12

## Agent Notes
**Owner spec, 2026-09-04.** A goal should declare *what kind of loop it launches*,
and every node that loop produces should carry that flavor as a tag. The tag is
what a zoomed-out view collapses on (`goal:g2.6`), so flavor and zoom are the
same mechanism seen twice.

The flavors, as the owner framed them:

- **research** — many verdict → mvp → build/build-version chains run *before* the
  first mvp that is allowed to be called development. Any node in it can become
  the launch point for a fresh idea, now or much later. Zoomed out, the whole
  thing reads as one `research` node.
- **exploration** — the lighter chain: verdict loops that lead straight to an mvp
  and its build nodes down one path. Its mvps and builds stay tagged
  `exploration`, which is an honest statement that this region has not been
  experimented on hard.
- **development** — what a research loop *becomes* once it delivers its first
  real mvp: that mvp and the build nodes it creates or revises are tagged
  `development` at the larger zoom. So a research loop is research-and-development
  in one shape.
- **implementation** — goals that spawn work directly, typically new versions of
  existing build nodes.

**Nesting is the point.** Inside a research loop each individual chain path is
itself sub-tagged `exploration`, so one zoom level shows many paths as single
nodes and the next breaks each path into the on-disk chain nodes it is made of.
The tag system therefore has to nest and to be legal at every grain, not just at
the top.

Downstream: `goal:g5.2` decides the flavor and the split mechanically;
`goal:g14` uses the flavor tag to route each node request to a model; the live
view (`goal:g9.8`) collapses on it.
