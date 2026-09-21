---
id: goal:g12
mint_id: be648cffa7e2473f9962b087153c3fe6
type: goal
parents: []
confidence: 1.0
edited_by: season.py
goal_id: G12
goal_kind: long-term
heading_level: 2
origin: goals-doc
season: 1
seeds:
  - goal:g12.1
  - goal:g12.2
status: active
tags:
  - goal
  - root
thought_session: season
title: "G12: Only morals are parentless — moral spawns vision spawns goal"
---
**The rule, stated once: exactly one node type may have an empty `parents`
list — `moral`.** Every other type, without exception, resolves to at least
one moral by walking `parents` upward. Morals are the root; morals spawn
visions, which require a moral parent (but may take others too); visions
spawn goals, which require a vision parent (but may take others too). The
owner's framing: morals are "the original guardrails," a vision is "what must
be," a goal is the "concrete actionable steps" toward it. The payoff, in the
owner's own words: **"any node other than moral has a path of parenthood that
leads to one or a few morals."**

## The chain

```
moral   (parentless — the only type that is)
  -> vision   (requires >=1 moral parent; may also have verdict / bigger_outcome)
    -> goal   (requires >=1 vision parent; may also have idea / build / verdict / outcome)
```

## Why this is cheap: the enforcement mechanism already exists

`bin/spawn_gate.py` already enforces exactly this shape of rule for every type
in the corpus today: `parentless_types` is read from `[shape].md`,
`allowed_parents` / `min_parents` / `max_parents` / `min_parents_by_type` are
read per-type from each `[<type>].md`'s `spawn:` block, and both are checked
at write time by `check_spawn`. **Nothing about this goal asks for a new
enforcement engine.** What changes is three declared facts: `parentless_types`
collapses from three entries to one (`moral`), a new `[moral].md` schema is
minted with `allowed_parents: []`, and `[vision].md` / `[goal].md` get new
`spawn:` blocks matching the tables below. The owner's own reasoning for why
this is safe to lean on: **"using kids helps mitigate as they must spawn only
nodes that have parents only"** — a kid agent that can only produce
spawn-gate-approved nodes cannot itself create a new parentless node once
`moral` is the only legal shape, so the invariant holds going forward without
a human re-checking every write.

## The two allowed-parent tables, as specified

**Vision — parents arrive only through season-boundary edges** (no such edge
kind exists in the graph yet; see G12.1):

| parent type | required / optional |
|---|---|
| moral | required |
| verdict | required/optional |
| bigger_outcome | required/optional |

"Just needs any one of the required/optional parents to be valid" — see
Ambiguity 1 below.

**Goal — parents arrive only through intra-season standard edges** (the
ordinary `parents:` edges written today):

| parent type | required / optional |
|---|---|
| vision | required |
| idea | required/optional |
| build | required/optional |
| verdict | required/optional |
| outcome | required/optional |

## Ambiguity 1 — does "any one" override "moral(required)"?

The quote: *"vision node allowed parents ...: moral(required),
verdict(required/optional), bigger outcome(required/optional). Just needs any
one of the required/optional parents to be valid."* Two incompatible
readings:

- **(a) Moral is unconditionally mandatory.** `verdict` / `bigger_outcome` are
  each independently optional add-ons; the closing sentence only says you
  don't need both of them at once. This matches the rest of the spec
  verbatim — "vision nodes ... require moral parents" and the "leads to one
  or a few morals" payoff both only hold if moral is non-negotiable.
- **(b) The closing sentence overrides the per-type labels.** Any one of the
  three types satisfies the rule on its own — including a vision with only a
  `bigger_outcome` parent and no `moral` at all. This reading takes
  "required/optional" at face value and treats `moral(required)` as loosely
  worded rather than load-bearing.

**This node adopts reading (a)** — moral required unconditionally, i.e.
`min_parents_by_type: {moral: 1}` on `[vision].md`'s eventual `spawn:`
block — because reading (b) breaks this goal's own falsifier (below) and
contradicts the plain-prose statement of the design twice over. **This is an
adopted reading, not a confirmed decision — flagged here for the owner to
settle before `[vision].md` is actually edited.**

## What "cite the moral(s) it adheres to, and how" means for the schema

The owner: *"Each vision node must cite a moral guardrail(s) it adheres to,
and how, so that any agents spawning goals from them know whether it takes
the project in the right direction."* An edge (`parents: [moral:x]`) records
*that* a vision descends from a moral; it does not record *how* the vision
honors it. This needs a real field, not prose buried in the body — e.g.
`moral_adherence: {moral:x: "why this vision satisfies x", ...}` — so a
goal-spawning agent can read the justification mechanically rather than infer
it. **This is a real authoring burden**: every vision (eventually capped at 3,
see G12.1) needs a written justification per cited moral, not just an id.

## The falsifier

Mechanical and countable: walk `parents` from every node in the corpus; every
node resolves to at least one `moral` node, and the count of nodes with an
empty `parents` list equals the count of `moral` nodes.

Today: **113 of 799 nodes are parentless, and 0 are `moral`** — the type does
not exist, no node, no `context/schemas/[moral].md`. The target state is 5
parentless nodes total, all of type `moral`.

## What this collides with

**`[shape].md :: parentless_types` today lists three entries** —
`goal:long-term`, `goal:short-term`, `idea` — and this goal removes all
three, unconditionally. That is 10 long-term goals, the short-term (`S`)
goals, and 42 ideas that currently have zero parents and would all need a
vision-or-moral ancestor.

**The universal rule sweeps in types the owner's spec never mentions.** "Only
one type of node can be parentless" is stated as a total rule, not scoped to
goal/idea. Measured today: 15 `verdict` nodes and 15 `hypothesis` nodes are
also parentless, with no discussion in the spec of what a verdict's or a
hypothesis's path to a moral should look like. Migrating those 30 nodes is in
scope by the letter of the rule even though the owner's worked example
(moral -> vision -> goal) never names them.

**The existing `[vision].md` schema is not merely silent on this — it
actively conflicts.** It was authored 2026-08-27, two days before this spec,
and already declares a `spawn:` block: `allowed_parents: [overview]`,
`min_parents: 2`, `max_parents: 4`, `min_parents_by_type: {overview: 2}`,
sitting at the top of an already-designed chain
`outcome -> bigger_outcome -> overview -> vision`. Nothing in that chain is
`moral`, and `bigger_outcome` there is a *grandparent* of vision (via
`overview`), not the direct parent the owner's table names; `overview` does
not appear in the owner's table at all. Replacing `[vision].md`'s spawn rule
per this goal does not just add a new option — it discards a floor (2
overviews minimum) built deliberately as "harder to earn than the middle"
convergence forcing, with nothing here yet saying whether that floor is kept,
dropped, or reworked into the new table.

### That floor is currently satisfied by nothing, which changes the argument

Measured 2026-08-29, and it is the single most useful fact in this node:

| | |
|---|---|
| `overview` nodes in the corpus | **0** |
| vision nodes | 17 |
| their actual parent types | `bigger_outcome` ×17, `outcome` ×2 |
| visions meeting `min_parents_by_type: {overview: 2}` | **0 of 17** |

**The `overview -> vision` chain is a dead declaration.** `[overview].md`
itself requires 3 `bigger_outcome` parents, and not one overview node was ever
minted — so the floor `[vision].md` declares has never once been met, and
every vision in the graph is parented on `bigger_outcome` directly, exactly
one hop below where the schema says it should sit.

This reverses the collision into an argument *for* the change. The owner's
table is not overwriting a working rule; it is replacing one that **no node
has ever satisfied** with one that already describes what 17 of 17 visions
actually do — `bigger_outcome` as a direct vision parent is in the owner's
table, and `overview` is absent from it. What the change genuinely costs is
the convergence floor's *intent*, not its practice: whether "a vision must be
harder to earn than the middle of the graph" survives as a `min_parents_by_type`
on `moral`/`bigger_outcome`, or is dropped. That is a live question. The
`overview` type itself should be deprecated rather than deleted (CLAUDE.md's
retirement rule) if this lands, since a schema for a type with zero instances
is exactly the "prose with a directory name" failure `goal:g10.2` warns about.

## Total parentless count today, for reference

| type | total | parentless |
|---|---|---|
| idea | 72 | 42 |
| goal | 87 | 32 |
| verdict | 86 | 15 |
| hypothesis | 107 | 15 |
| build | 195 | 7 |
| experiment | 77 | 1 |
| doc | 1 | 1 |
| vision | 17 | 0 |
| **TOTAL** | | **113 of 799** |