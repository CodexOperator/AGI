---
name: app_purpose
derived_from: corpus-survey-2026-08-25 (n=15 as app_purpose, +2 as app-purpose; both renamed 2026-08-26, n=17)
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
17 nodes: `bigger_outcome` 15, `outcome` 2. **Zero parentless.**

The 2026-08-25 survey read that as 14 + 2 + one parent typed `bigger-outcome`,
which was the spelling split showing up in an *edge* rather than just a
filename. The gate canonicalises `-` → `_` on both sides, so that edge
validated against `allowed_parents: [bigger_outcome, outcome]` while the split
was still there; had it matched literally, a correct edge would have been
rejected for punctuation.

## One spelling, as of 2026-08-26

`app_purpose` (17 nodes) is the only spelling in the corpus — the two
`app-purpose` nodes were renamed on 2026-08-26. See `[bigger_outcome].md` for
the identical story and the generator that produced it.
