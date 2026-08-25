---
name: idea
derived_from: corpus-survey-2026-08-25 (n=71)
fields:
  title: {type: str}
  scale: {type: str}       # "big" | "small"
  parents: {type: list}    # goal ids, or empty -- idea is parentless-legal
  next_edges: {type: list}
  tags: {type: list}
  confidence: {type: float}
  status: {type: str}      # open | active | extended | abandoned
  origin: {type: str}      # engine-decomp (55) | build-site (7)
  unit_kind: {type: str}   # engine-decomp: what kind of unit this idea covers
  unit_path: {type: str}   # engine-decomp: the path it covers
validation:
  required: [id, type, mint_id, title, scale]
  types:
    title: str
    scale: str
  regex:
    scale: '^(big|small)$'
    status: '^(open|active|extended|abandoned)$'
spawn:
  allowed_parents: [goal]
  min_parents: 0
  max_parents: 1
---

# idea

Big or small concept seed. Spawns hypotheses and level-3 census nodes. May
fork mid-chain.

- **big** = top-level new chain, broad (26/71)
- **small** = granular extension of an existing chain (40/71)

ID prefix: `idea:<short-slug>` (e.g. `idea:capillary-dag-memory`).

## Spawn rule — one of exactly three parentless-legal shapes

`min_parents: 0`. `idea`, `goal:long-term` and `goal:short-term` are **the
only** shapes in the graph permitted an empty `parents` list
(`[shape].md :: parentless_types`). 42 of 71 ideas are parentless and every
one of them is legal; the other 29 name a `goal`, which is the shape to
prefer, because a parentless idea is attributable to no goal and therefore
cannot move `outcome_coverage`.

`max_parents: 1` — never more than one goal observed. Raising it is a
deliberate act: bump this **and** `max_parents_ceiling` in `[shape].md`.

## Repair: the declared `status` enum did not match the corpus

The pre-2026-08-25 regex was `^(open|extended|abandoned)$`. Measured: `open`
66, `active` 1, `extended` 0, `abandoned` 0. So the one value actually in use
besides `open` was the one value the regex rejected, and two declared values
have never been written. Widened to the union rather than narrowed to
observation — `extended`/`abandoned` describe a real lifecycle and removing
them would silently make a documented transition illegal.
