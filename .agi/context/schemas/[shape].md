---
name: shape
structural: true
derived_from: corpus-survey-2026-08-25
fields:
  ref_namespaces: {type: dict}      # grid ref layout, keyed by dimension
  node_tree_entries: {type: list}   # entry names inside a node's D2 commit
  parentless_types: {type: list}    # the ONLY types allowed an empty parents list
  max_parents_ceiling: {type: int}  # global upper bound on any type's max_parents
  spawn_rule_source: {type: str}    # where the per-type table actually lives
  canonical_type_spelling: {type: str}
validation:
  required: [ref_namespaces, parentless_types, max_parents_ceiling]
  types:
    max_parents_ceiling: int
    parentless_types: list
    node_tree_entries: list

# ===========================================================================
# The geometry itself. Read by bin/spawn_gate.py.
# ===========================================================================

# D2/D3 of the git grid (bin/grid.py REF_NS = "refs/grid").
ref_namespaces:
  node: "refs/grid/node/<mint-id>"
  session: "refs/grid/session/<iter>/<agent>/<id>"

# A node's D2 commit is a tree, not a blob. Two entries since goal:g6.3;
# `node.md` alone before that. bin/grid.py NODE_ENTRY / PAYLOAD_ENTRY.
node_tree_entries:
  - node.md      # always
  - payload      # only when the node has a payload_ref; real mode (644/755/120000)

# The parentless whitelist. Since goal:g12 exactly one entry: `moral`,
# creation-time only. The 113 pre-existing parentless nodes (long-term
# goals, short-term goals, ideas) are season 1, grandfathered, never
# re-gated.
parentless_types:
  - moral

# No type may declare max_parents above this without also raising the ceiling.
# Two deliberate edits, which is the point, and this is the second one:
# raised 2 -> 4 on 2026-08-27 so `bigger_outcome` can carry the 2 verdict +
# 2 outcome floor its `min_parents_by_type` now declares. Nothing else in the
# corpus uses more than 2; raising the ceiling licenses a budget, it does not
# hand one out.
max_parents_ceiling: 4

# Which frontmatter fields are EDGES, and which of those a traversal may
# follow. `parents` is lineage: it is what chain depth, outcome_coverage and
# every renderer walk. `depends_on` is scheduling -- build order, not
# descent -- and must never enter a chain walk. A scheduling edge that gets
# counted is a fresh metric-gaming surface, which this project has already
# paid for once (9 chains x 2000 hops of shortcut cycles, which then broke
# the render path outright). Declaring the classification is what lets the
# guard be mechanical instead of remembered.
#
# `proposes_goals` is the graph's only backward edge -- vision -> goal, which
# closes the loop the whole design is built around. It is NOT lineage and must
# never be moved into `parents`: at the type level `goal -> ... -> vision ->
# goal` is a directed cycle, and `parents` is what every chain walk follows.
# The loop stays acyclic at the instance level because the vision that
# proposes a goal is an earlier season than the vision that goal later feeds.
edge_fields:
  parents:         {role: lineage,    traversable: true}
  next_edges:      {role: lineage,    traversable: true}
  depends_on:      {role: scheduling, traversable: false}
  seeds:           {role: provenance, traversable: false}
  proposes_goals:  {role: proposal,   traversable: false}
  season_parents:  {role: season,     traversable: false}
  grounded_in:     {role: provenance, traversable: false}
  authors:         {role: provenance, traversable: false}

# The per-type table lives in each [<type>].md `spawn:` block and NOWHERE
# else. Copying it here would recreate the exact defect S17 names -- one fact
# with three definitions. This file declares the grammar; the type files hold
# the values.
spawn_rule_source: "context/schemas/[<type>].md :: spawn"

canonical_type_spelling: underscore
---

# shape

**Structural node type — the graph's own geometry (G10.2, `.geometry`).**
Declares what shape the ref system takes, which types may be parentless, and
the ceiling on parent count. Not content: no `shape` node exists in the
corpus, and this file is a schema, not a node.

## What reads this

`bin/spawn_gate.py` — `parentless_types` and `max_parents_ceiling` are both
enforced. G10.2's constraint is that a geometry declaration a code path does
not consult is "prose with a directory name"; these two fields are consulted.

`edge_fields` is **parsed but not yet enforced** (2026-08-27). `spawn_gate.py`
reads it into `Geometry.edge_fields` and exposes `is_traversable(field)` /
`scheduling_edges()`; no walker consults those yet, because nothing in the
engine traverses `depends_on` today — `blocked_by`, its predecessor, is
written by `snapshot-build-site.py` and read by nothing. So the declaration
is currently a **guard against a regression rather than a fix for a live
bug**, and saying otherwise would overclaim. The consumer — a traversal
deny-list in `metrics.py` and the chain walkers — is G4.5's.

`ref_namespaces` and `node_tree_entries` are **declared but not yet read** —
`grid.py` still holds them as `REF_NS` / `NODE_ENTRY` / `PAYLOAD_ENTRY`
constants. Recorded here as the residual, not claimed as done.

## The spawn grammar

A `spawn:` block in a `[<type>].md` schema takes one of two forms.

**Flat** — the type has one shape:

```yaml
spawn:
  allowed_parents: [experiment, verdict, hypothesis]
  min_parents: 1
  max_parents: 2
```

**Discriminated** — the type has several shapes under one `type:` value:

```yaml
spawn:
  discriminator: goal_kind
  variants:
    long-term: {allowed_parents: [], min_parents: 0, max_parents: 0}
    subgoal:   {allowed_parents: [goal], min_parents: 1, max_parents: 1}
```

**Per-kind floors** — either form may add `min_parents_by_type`, a mapping of
parent type to the minimum number of parents of that kind:

```yaml
spawn:
  allowed_parents: [outcome, verdict]
  min_parents: 4
  max_parents: 4
  min_parents_by_type: {verdict: 2, outcome: 2}
```

`min_parents` counts parents; this counts parents *of a kind*. Two outcomes
and "one verdict plus one outcome" are the same arity and different shapes,
and only the second is convergence — arity alone cannot say so. Used today by
`[bigger_outcome].md` and nothing else.

Four ways it is unsatisfiable, and all four are **schema errors** that leave
the type unverified rather than runtime rejections — a rule no node could
ever pass would reject its whole type forever, which is louder than the
missing rule it replaced:

- a key `allowed_parents` does not permit,
- floors summing above `max_parents`,
- a count below 1 (write no key rather than `0`, which reads as a rule and
  enforces nothing — the prose-control trap this file exists to close),
- a non-mapping value.

Rules:

- `allowed_parents: []` **plus** `min_parents: 0` is what makes a type
  parentless-legal, and it is only accepted for entries in
  `parentless_types` above.
- `max_parents` must be `<= max_parents_ceiling`.
- Every other type must set `min_parents: >= 1`.
- A type with no `spawn:` block is **unverified**, not approved — the same
  fail-open the schema DSL uses for a missing `validation:` block
  (`schema_registry/dsl.py`, R4.1), and it is announced as such.

## Type spelling

`underscore` is canonical: `bigger_outcome` not `bigger-outcome`,
`app_purpose` not `app-purpose`. The gate canonicalises `-` to `_` before
matching a rule, so both spellings resolve to the same schema.

**Both generators are fixed.** `bin/cli.py` `NODE_TYPES` accepts both and
writes the underscore form; `bin/dispatch.py`'s un-gated duplicate — which
this file previously recorded as "still mints hyphens" — was **deleted** on
2026-08-26 (commit `dccaec865`). Every writer now calls `bin/node_writer.py`,
which holds the type table once.

**The corpus is only half-migrated, measured 2026-08-27.** `type:` is
underscore on all 781 nodes, but the split survives in two places the type
field does not cover:

| | still hyphenated |
|---|---|
| directories | `nodes/app-purpose/` (8), `nodes/bigger-outcome/` (11) |
| `id:` prefixes | `app-purpose:` (10), `bigger-outcome:` (12) |

and the hyphenated ids leak into **edges** — 2 `app_purpose` nodes name a
`bigger-outcome:` parent. Those edges validate only because
`canonical_type` folds both sides. So `canonical_type` is not vestigial
tidiness; it is currently load-bearing. Retiring it requires finishing the
id and directory migration first (S17, and the Phase 1 data repair).

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
