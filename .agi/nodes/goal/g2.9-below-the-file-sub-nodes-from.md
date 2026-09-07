---
id: goal:g2.9
mint_id: ec10d3fa10824c9e8e679e129c16272a
type: goal
parents:
  - goal:g2
confidence: 1.0
edited_by: season.py
goal_id: G2.9
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
title: "G2.9: Below the file: sub-nodes from in-file markers, then language primitives"
---
**Below base level you are inside one node, never traversing the graph.** That
is the structural invariant: supernode groupings above base level span many
nodes, but everything below it — versions, chats, and the decomposition here —
is scoped to a single node. Zoom out to relate things; zoom in to resolve one
thing.

Turning LOD up past the raw file decomposes it further, in two steps:

1. **Sub-nodes from in-file markers.** Regions of a file are marked by comments
   carrying short alphanumeric ids — single or double digit. Those ids extend
   the address scheme downward: a 7-character node address plus a sub-node id
   addresses a region of a file as unambiguously as the node itself, still by
   truncation (**G2.5**). Author-placed rather than inferred, so the
   decomposition is a claim the author made, not a guess a parser produced.
2. **The primitive graph.** Past that, resolve what the code *actually does* in
   base-level logic: arithmetic, filesystem operations, memory reads and writes
   including variable creation and mutation. Imported functions resolve through
   to the primitives they bottom out in, so a call stops being an opaque name
   and becomes the operations it performs.

**Chats decompose too, one step: turn by turn.** A chat at high LOD is its
individual turns. Nothing finer is specified yet, and inventing a deeper
decomposition before there is a use for it would be speculative — say so rather
than leaving a blank that reads as an oversight.

Depends on **G2.8** for the dial and **G2.5** for addresses that extend below a
node. The primitive graph is the ambitious half and should not block the marker
half, which is cheap and immediately useful.