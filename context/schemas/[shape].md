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

# The parentless whitelist. Exactly three shapes, and `goal` only in two of
# its three variants -- see the discriminator in [goal].md.
parentless_types:
  - goal:long-term      # a `## G7` root
  - goal:short-term     # a `## S4` root
  - idea

# No type may declare max_parents above this without also raising the ceiling.
# Two deliberate edits, which is the point: 2 is what the corpus uses, and
# raising it is an act, not a default.
max_parents_ceiling: 2

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

`underscore` is canonical: `bigger_outcome` (17 nodes) not `bigger-outcome`
(2), `app_purpose` (15) not `app-purpose` (2). Both spellings exist in the
corpus and **no node file is renamed** — the gate canonicalises
`-` to `_` before matching a rule, so both resolve to the same schema. The
generator that minted the hyphens is `bin/cli.py` `NODE_TYPES` (fixed: it now
accepts both and writes the underscore form) and `bin/dispatch.py`
`NODE_TYPES` (**still mints hyphens** — not owned by this change).
