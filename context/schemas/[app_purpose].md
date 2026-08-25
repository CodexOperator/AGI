---
name: app_purpose
derived_from: corpus-survey-2026-08-25 (n=15 as app_purpose, +2 as app-purpose)
fields:
  title: {type: str}
  parents: {type: list}      # bigger_outcome | outcome ids
  next_edges: {type: list}
  tags: {type: list}
  status: {type: str}        # open | active | closed
  confidence: {type: float}
  subgraph: {type: bool}
validation:
  required: [id, type, mint_id, title, parents, tags]
  types:
    parents: list
    tags: list
spawn:
  allowed_parents: [bigger_outcome, outcome]
  min_parents: 1
  max_parents: 2
---

# app_purpose

The top of a chain: the mission a stack of outcomes serves. No node type
parents this one.

ID prefix: `app_purpose:<short-slug>`.

## Spawn rule

`allowed_parents: [bigger_outcome, outcome]`, `max_parents: 2`. Observed over
15 nodes: `bigger_outcome` 14, `outcome` 2, `bigger-outcome` 1. **Zero
parentless.**

That third figure is the spelling split showing up in an *edge*, not just a
filename: one `app_purpose` node names a parent whose type is spelled
`bigger-outcome`. The gate canonicalises `-` → `_` on both sides, so the edge
validates against `allowed_parents: [bigger_outcome, outcome]` without
anything being renamed. Had it matched literally, a correct edge would have
been rejected for punctuation.

## Two spellings, one type

`app_purpose` (15) is canonical; `app-purpose` (2) resolves to this same
schema. See `[bigger_outcome].md` for the identical story and the generator
that produced it.
