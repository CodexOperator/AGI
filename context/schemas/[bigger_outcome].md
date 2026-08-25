---
name: bigger_outcome
derived_from: corpus-survey-2026-08-25 (n=17 as bigger_outcome, +2 as bigger-outcome)
fields:
  title: {type: str}
  parents: {type: list}      # outcome | mvp ids
  next_edges: {type: list}
  tags: {type: list}
  status: {type: str}        # open | closed
  confidence: {type: float}
  subgraph: {type: bool}
validation:
  required: [id, type, mint_id, title, parents, next_edges]
  types:
    parents: list
    next_edges: list
spawn:
  allowed_parents: [outcome, mvp]
  min_parents: 1
  max_parents: 2
---

# bigger_outcome

A module-level purpose composed from several `outcome` nodes. Aggregates
upward into `app_purpose`.

ID prefix: `bigger_outcome:<short-slug>`.

## Spawn rule

`allowed_parents: [outcome, mvp]`, `max_parents: 2`. Observed over 17 nodes:
`outcome` 17, `mvp` 2. **Zero parentless** — this type has never violated the
rule it is now held to.

## Two spellings, one type

`bigger_outcome` (17 nodes) and `bigger-outcome` (2) are the same type. The
underscore form is canonical (`[shape].md :: canonical_type_spelling`), and
`spawn_gate.py` canonicalises `-` → `_` before matching, so a
`bigger-outcome` node resolves to *this* schema. **No file is renamed** —
19 renames buy nothing and cost every id that references them. The generator
that minted the hyphens is `bin/cli.py` `NODE_TYPES` (now writes underscores,
still accepts hyphens as input aliases) and `bin/dispatch.py` `NODE_TYPES`,
which still mints hyphens and is outside this change.
