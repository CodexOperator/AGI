---
name: idea
derived_from: corpus-survey-2026-08-25 (n=71)
fields:
  title: {type: str}
  scale: {type: str}       # "big" | "small"
  authors: {type: list}    # list of agent ids; for co-authored memo ideas every listed author is required (goal:g12.2, section 2 Ideas as memos)
  parents: {type: list}    # goal or vision ids, or empty -- idea was once parentless-legal
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
  allowed_parents: [goal, vision]
  # No longer parentless-legal (parentless_types is now [moral]; the 42
  # pre-existing parentless ideas are season 1, grandfathered).
  # A co-authored memo idea names every author and lists every goal/vision
  # parent the memo emerges from; authorship rules in section 2 (goal:g12.2).
  min_parents: 1
  max_parents: 2
---

# idea

Big or small concept seed. Spawns hypotheses and level-3 census nodes. May
fork mid-chain.

- **big** = top-level new chain, broad (26/71)
- **small** = granular extension of an existing chain (40/71)

ID prefix: `idea:<short-slug>` (e.g. `idea:capillary-dag-memory`).

## Spawn rule — goal or vision parent, no longer parentless-legal

`min_parents: 1`. Since `goal:g12`, `moral` is the **only** parentless-legal
shape (`[shape].md :: parentless_types`); `idea` lost that status at
creation time. The 42 pre-existing parentless ideas are season 1,
grandfathered, never re-gated. Every new idea names a `goal` or `vision`,
because a parentless idea is attributable to no goal and therefore cannot
move `outcome_coverage`.

`max_parents: 2` — widened from 1 on 2026-09-06 to allow a co-authored
memo idea (section 2, goal:g12.2) that emerges from two goals/visions. An
idea with two vision parents is a synthesis of two convergence outcomes; an
idea with two goal parents is a cross-chain memo.

## The `authors` field (goal:g12.2, section 2)

`authors: [list of agent ids]`. For a co-authored memo idea, every listed
author is required to exist as an agent node. A solo-authored idea may omit
the field. The field is provenance, not lineage, and is tracked as such in
`[shape].md :: edge_fields`.

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
