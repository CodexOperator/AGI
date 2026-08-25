---
name: level3
derived_from: corpus-survey-2026-08-25 (n=185)
fields:
  title: {type: str}
  payload_ref: {type: str}    # path of the file this node IS, relative to engine root
  origin: {type: str}         # level3-scan | build-version
  parents: {type: list}       # idea | goal ids
  confidence: {type: float}
  tags: {type: list}
  supersedes: {type: str}
  version: {type: int}
validation:
  required: [id, type, mint_id, title, payload_ref, origin, confidence, tags]
  types:
    payload_ref: str
    confidence: float
    tags: list
spawn:
  allowed_parents: [idea, goal]
  min_parents: 1
  max_parents: 2
---

# level3

One file of the engine, as a node. `payload_ref` names where the bytes belong
in the engine tree; since G6.3 the bytes themselves live in the node's grid
ref (`refs/grid/node/<mint-id>:payload`), which is what makes the graph the
source and the engine tree the thing that falls out.

ID prefix: `level3:<payload_ref>` — e.g. `level3:.gitignore`.

## Spawn rule

`allowed_parents: [idea, goal]`, `max_parents: 2`. Observed over 185 nodes:
`idea` 178, `goal` 6. 183 of 185 carry exactly one parent; 2 are parentless
and are a **report, not a purge**.

`min_parents: 1` — a level-3 node is a census entry under a decomposition
idea. Floating free, it belongs to no decomposition.

## The name is a migration artefact, and the schema says so

G10.2 is explicit: **a node must not be titled `level3`.** Zoom is a property
of the view, never of the node; naming the grain on the node tells an agent to
identify with a grain instead of working at one. This schema describes the 185
nodes that exist today under that name — it is **not** an endorsement of
minting more. Ids are permanent, so nothing is renamed; the intended
destination is that the grain becomes a facet the renderer reads.

## The harness-owned contract block

Each node body carries a `LEVEL3-CONTRACT:BEGIN/END` block derived by
`bin/level3.py` from the payload. It is **harness-owned**: a model may fill
`why`/`perf`/`security` and must never add, remove or reorder fields. Not
expressible in the field DSL (it lives in the body, not the frontmatter), so
it is stated here and enforced by `level3.py`.
