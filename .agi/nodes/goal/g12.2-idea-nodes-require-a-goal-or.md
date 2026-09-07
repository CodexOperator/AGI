---
id: goal:g12.2
mint_id: fda3dccbd4d74ec28dfc99d544b9f69a
type: goal
parents:
  - goal:g12
confidence: 1.0
edited_by: season.py
goal_id: G12.2
goal_kind: long-term
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
thought_session: season
title: "G12.2: Idea nodes require a goal or vision parent, and what they may spawn depends on which"
---
**G12 establishes the parentage spine — `moral → vision → goal`, `moral` the
only parentless type. This is that spine's sub-goal for `idea`.**

## The parent requirement

An idea node requires **at least one `goal` OR at least one `vision`** —
either is sufficient, neither is mandatory over the other. Today's schema
(`context/schemas/[idea].md`) declares `allowed_parents: [goal]`,
`min_parents: 0`, and lists `idea` in `[shape].md :: parentless_types` as one
of exactly three shapes ever licensed to float free. Both change under this
goal: `vision` joins `allowed_parents`, and `min_parents` moves from 0 to 1,
which also means removing `idea` from `parentless_types`.

**That removal is one of three, not the last one.** `parentless_types` ends up
holding exactly one entry, `moral` — `goal:long-term` and `goal:short-term`
come out too, under `goal:g12`, because a goal requires a vision parent and a
vision requires a moral parent. This sub-goal removes `idea`; G12 removes the
other two. Stating it the other way round — that goal and vision remain
parentless alongside moral — would contradict the spine G12 exists to
establish, whose whole payoff is that **every** node but a moral has a path of
parenthood leading to one.

## The conditional spawn rule — the genuinely new mechanism

What an idea may spawn depends on **what its own parents are**, not on
anything intrinsic to the idea node itself:

- **Parents are only goal(s)/vision(s).** The idea must invoke the full
  scientific-method lifecycle: hypothesis → experiment → verdict → mvp →
  outcome. No shortcut.
- **Parents include a required goal/vision AND an existing `build` node.**
  The idea may spawn an MVP, or a new version of that build node, directly —
  skipping the chain.

So the same idea type has two different downstream contracts, selected by
parent composition. That is a distinction the current spawn model has no way
to hold.

## Why this is a new shape for the spawn gate

`bin/spawn_gate.py` validates a node against its **own type's** rules —
`min_parents`, `max_parents`, `allowed_parents` from the schema, plus
`parentless_types` from `[shape].md`, all read at the moment the node itself
is written. Every check in `check_spawn()` looks upward, at what a node's
parents are permitted to be. This rule looks the other way: it constrains a
node's **children** based on its **parents** — a downstream node (a build
version, say) has to be checked not just against its own type's
`allowed_parents`, but against what its *idea* parent's own parent set was.
Nothing in the gate expresses that today, and nothing in `[shape].md`'s two
cross-cutting facts (`parentless_types`, `max_parents_ceiling`) reaches it
either. Say this plainly because it is the main implementation cost of this
goal: it is not a new rule slotted into the existing per-type table, it is a
second axis (parent composition of the grandparent idea) that the gate's
one-hop, own-type check was never built to see. Whoever picks this up should
budget for that shape, not for a `spawn:` block edit.

## Idea as the graph analogue of the thought block, with extra metadata

The owner's own framing, and it draws a sharp line against `goal:g2.11`'s
`THOUGHT` block rather than restating it. `body` is state, `thought` is
delta — but a `THOUGHT` block is bound to **one node's version**: it lives
inside that node's body, is rewritten from scratch each version, and has no
edges of its own. An idea is a **free-floating first-class node** with its
own id, its own `parents`, and its own `next_edges` — it can be pointed at,
spawned from, and outlive the version of whatever prompted it. That is what
lets it re-orient work mid-season in a way a `THOUGHT` block cannot: a
thought is provenance for the node that carries it; an idea is a node in its
own right that other nodes can descend from.

## The two uses the owner named

- **Gently re-orienting mid-season**, as an idea spawned from an existing
  `goal` or `vision` reveals a gap the current chain does not cover, without
  requiring a whole new goal to be declared first.
- **Spawning the experiment chains that justify changing a vision node**,
  at the next season boundary — an idea parented on the vision it means to
  revise, running the full lifecycle above, whose outcome is the evidence a
  season roll-over cites when minting the vision's next version.

## Measured facts (2026-08-29, do not re-measure without cause)

- **72 idea nodes exist; 42 are parentless.** This rule breaks all 42 on day
  one — each needs a `goal` or `vision` parent assigned, or needs
  deprecating in place per CLAUDE.md's retirement convention (never deleted).
- 799 nodes total, 113 parentless across all types.
- 17 vision nodes, 87 goal nodes, 195 build nodes, 27 mvp nodes.

## Falsifier

```
every idea node has >=1 parent of type goal or vision
every idea node whose parents include no build node has no mvp child
```

Both are mechanical: the first is a frontmatter+type-index scan identical in
shape to what `spawn_gate.build_type_index` already does; the second is a
child-edge walk gated on the same parent-type resolution. Neither requires
judgement to check.

## Out of scope

**Migrating the 42 parentless idea nodes is not this goal.** This goal
records the rule and its cost; assigning parents (or deprecating) to 42
existing nodes is a separate, mechanical follow-up once the schema change
itself is made — bundling the two would let the rule's definition drift
while the migration is still being decided node by node.