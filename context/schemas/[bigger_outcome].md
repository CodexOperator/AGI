---
name: bigger_outcome
derived_from: corpus-survey-2026-08-25 (n=17 as bigger_outcome, +2 as bigger-outcome; both renamed 2026-08-26, n=19)
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

## One spelling, as of 2026-08-26

`bigger_outcome` (19 nodes) is the only spelling in the corpus. The two
`bigger-outcome` nodes were renamed on 2026-08-26 — file, `id:` and `type:` —
and the five ids that referenced them were rewritten in the same pass.

The generator that minted the hyphens was `bin/dispatch.py`, which carried its
own un-gated copy of the scaffold routine with its own hyphenated type tuple.
That copy is deleted: every writer now calls `bin/node_writer.py`, which holds
the type table once and writes the canonical spelling.

`spawn_gate.canonical_type` still folds `-` → `_` before matching, and stays.
It costs nothing, it is what let the historical nodes validate against this
schema without being renamed, and it is the reason renaming them was a tidy-up
rather than a repair.
