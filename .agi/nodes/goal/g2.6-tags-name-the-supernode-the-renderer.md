---
id: goal:g2.6
mint_id: 8dc9d0b7100b4d59b89901756c4fbdf5
type: goal
parents:
  - goal:g2
confidence: 1.0
edited_by: season.py
goal_id: G2.6
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
title: "G2.6: Tags name the supernode; the renderer groups on them live"
---
**Tags are the human-readable half of G2.5's addressing.** An id is short,
unambiguous and machine-facing; a tag is long, descriptive and person-facing.
Each node carries the tag of the supernode it belongs to, and the renderer
applies that grouping at render time rather than baking it into the graph.

Why they are separate from ids, and why both are wanted:
- **A tag is as long as it needs to be — and may be as short as 5 characters.**
  Nothing about it is padded, truncated or budgeted, so it stays readable to a
  human *and* to a model reading an injected map — which is the readability G9 depends on and the
  reason opaque identifiers were rejected for the visible layer.
- **Retagging is how a node moves.** Change the tag, the renderer places the
  node in a different supernode, and its id re-derives to the new prefix. No
  re-parenting, no edge rewriting.
- **Ids may be derived from tags.** Padding, truncating or selecting characters
  from a tag to fit the 7-character format keeps the two layers legibly related
  instead of arbitrarily paired. Overlapping names are a feature here, not a
  collision.

**What this goal owes G2.5:** the tag taxonomy is what decides supernode
membership, so it is what must satisfy the ≤36 (or ≤62) members-per-prefix
budget. A flat tag applied to hundreds of nodes — `level3` currently spans 181 —
cannot be a supernode. The taxonomy has to be hierarchical enough that no single
group exceeds one character's worth of slots, and **measuring that against a
real proposed tag set is G2.5's re-registered falsifier.**

Unbuilt on purpose: recorded now so the id work can be designed against it, to
be implemented after G2.5's addressing lands.