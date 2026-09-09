---
name: doc
fields:
  title: {type: str}
  link_ref: {type: str}           # path of the design doc this node IS, relative to `location`; absent = body-is-data (goals-preamble)
  location: {type: str}           # NAME of the base link_ref resolves against; default source_root
  origin: {type: str}             # doc-scan | doc-version
  parents: {type: list}
  confidence: {type: float}
  tags: {type: list}
  status: {type: str}             # absent = live; `deprecated` = retired in place
validation:
  required: [id, type, mint_id, title, tags]
  types:
    tags: list
    confidence: float
  regex: {}
spawn:
  allowed_parents: [goal]
  min_parents: 1
  max_parents: 1
---

# doc

A schema-less `.agi/context/*.md` design doc given a node. `link_ref` names the
bytes the node stands for, in the same tree build nodes have always used; the
pre-existing 0-parent shape (`doc:goals-preamble`) is grandfathered, exactly as
build's 19 parentless nodes are.

## `link_ref` — the file this node IS

`link_ref` is this type's name for build's `payload_ref` (its legacy alias).
`link_ref` absent means the body itself is the data, which is how
`doc:goals-preamble` already behaves today.

## Spawn rule

`allowed_parents: [goal]`, `min_parents: 1`, `max_parents: 1`. A new doc node
is minted by a goal that names the design doc, not out of nothing — build's
`[build, goal]`-for-a-version shape does not apply because a doc node does not
change its file's *kind*, only claims it.
