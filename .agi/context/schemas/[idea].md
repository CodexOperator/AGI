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
  status: {type: str}      # open | active | extended | abandoned | deprecated
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
    status: '^(open|active|extended|abandoned|deprecated)$'
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

**2026-09-03 (L1.09-cleanup): added `deprecated`.** Retirement writes
`status: deprecated` on the node itself — `CLAUDE.md`'s "Retire a node with
`status: deprecated`" convention — and the regex above rejected it, exactly
the same repair as this section already describes for `extended`/`abandoned`.
Caught on `idea:engine-todo`, then measured against the 8 `idea` nodes the
build-site cohort retirement (L1.09) deprecated: all 8 were schema-invalid
until this line included the one value retirement itself writes.

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
