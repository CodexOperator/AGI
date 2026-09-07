---
id: goal:g9.8
mint_id: ac9c67717e254ace897eea4c8952c151
type: goal
parents:
  - goal:g9
  - build:COMPLETE.md
next_edges: []
confidence: 1.0
edited_by: season.py
goal_id: G9.8
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: aca900e6d41c2e21
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G9.8: One live hook layer, two skins, and a player avatar that browses the graph"
---
# goal:g9.8

## Agent Notes
**Owner spec, 2026-09-04.** The live view shipped as a list. This goal is the
half that has to exist before either skin is worth drawing: **one hook layer,
one frame stream, two renderings.** `viewport.py --emit both` already proves the
principle for human/LLM text; this extends the same discipline to two *visual*
skins that share every hook and differ only in paint.

What the layer owes:

- **Every node, not just goals.** The web is the whole graph — 1,275 nodes and
  1,196 edges today — laid out in 2D top-down, not a filtered list of the
  interesting ones.
- **Live agent positions as events, not polls.** A frame carries where each
  agent is, which edge it is traversing, and what it is doing to the node it
  sits on (reading, writing, reviewing, cleaning up after a kid). Bits streaming
  into the graph, rendered as they land.
- **A player avatar.** The viewer is *in* the graph: free movement across it,
  `f` to dock to a node, and once docked, browse that node's grid versions and
  the chat sessions attached to it (`goal:g2.7`, `goal:g10.1` — this is the
  first consumer that makes chat-to-node linking visibly worth it).
- **LOD as approach, not a flag.** A node grows less opaque as the avatar nears
  it, revealing its subnodes; it never goes fully clear. `z` / `x` zoom in and
  out from anywhere on the graph. This is `goal:g2.8`'s second axis, made
  physical.
- **Recursive by construction, in both directions.** More zoom layers above and
  below, and more agent hierarchy layers than director/parent/kid, must be
  additions to a table — never a new branch in the renderer.

**Skins are downstream of this and must not fork it:** `goal:g9.9` (spider web)
and `goal:g9.10` (space) are two paint jobs over these hooks. If a skin needs a
hook the other cannot use, the hook is wrong.