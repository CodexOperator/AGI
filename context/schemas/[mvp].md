---
name: mvp
derived_from: corpus-survey-2026-08-25 (n=26)
fields:
  title: {type: str}
  parents: {type: list}        # verdict | goal | experiment | hypothesis ids
  next_edges: {type: list}
  source_files: {type: list}   # paths to actual code -- optional, see below
  tests_pass: {type: bool}
  commit_hash: {type: str}
  confidence: {type: float}
  status: {type: str}          # open | implemented | complete
  subgraph: {type: bool}
  tags: {type: list}
validation:
  required: [id, type, mint_id, title, parents]
  types:
    tests_pass: bool
    parents: list
spawn:
  allowed_parents: [verdict, goal, experiment, hypothesis]
  min_parents: 1
  max_parents: 2
---

# mvp

Minimum viable production code. Children are `outcome` nodes (i/o-doc fusion).

ID prefix: `mvp:<short-slug>`.

## Spawn rule

`allowed_parents: [verdict, goal, experiment, hypothesis]`, `max_parents: 2`.
Observed over 26 nodes: `verdict` 20, `goal` 5, `experiment` 2, `hypothesis`
1. **Zero parentless**, and `parents` is present on 26/26 — the only content
type besides `task` with perfect parent coverage, so `parents` is `required:`
here on measured grounds rather than aspiration.

## Repair: `source_files` was required and is carried by no node

Pre-2026-08-25 `required: [title, source_files]`. Measured: `title` 25/26,
`source_files` **0/26**, `tests_pass` 0/26, `commit_hash` 0/26. All three of
the fields that would make an MVP node *verifiable* have never been written
once, which is worth stating plainly rather than fixing by fiat.

`source_files` is demoted to optional and kept declared, unlike
`[experiment].md`'s `run_id` which was dropped: an MVP genuinely should point
at code, and the gap is a real finding about the corpus rather than a field
that never meant anything. Making it required today would fail every existing
MVP and block every new one until someone invented a path — the failure mode
the old schema already had, just louder.
