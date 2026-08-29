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
  allowed_parents: [outcome, verdict]
  min_parents: 4
  max_parents: 4
  min_parents_by_type: {verdict: 2, outcome: 2}
---

# bigger_outcome

A module-level purpose composed from several `outcome` nodes. Aggregates
upward into `vision`, via `overview`.

ID prefix: `bigger_outcome:<short-slug>`.

## Spawn rule — PRESCRIPTIVE, not derived

Most schemas here are derived: they describe what the corpus does, and where
corpus and rule disagreed the rule was widened to the corpus. **This one is
deliberately the other way round**, as of 2026-08-27 — as are `[overview].md`
and `[vision].md`, the other two tiers of the convergence end. It states what
an aggregate is *supposed* to rest on, and the corpus does not satisfy it
yet. That inversion is the point, so it is written at the top rather than
buried: a reader who assumes "derived" here will misread every number below.

`allowed_parents: [outcome, verdict]`, `min_parents: 4`, `max_parents: 4`,
`min_parents_by_type: {verdict: 2, outcome: 2}`.

Measured over all 19 nodes before the change: `outcome` 19/19, `mvp` 2,
**`verdict` 0**. 17 of 19 carry exactly one parent. So **19 of 19 violate the
new rule**, and that is expected — this is a floor for what gets written from
here on, not a claim about what is already there. Report, not purge (G7):
the gate runs on the writer path, so all 19 keep their place.

Why a per-kind floor instead of a bigger `min_parents`: two outcomes and
"one verdict plus one outcome" are the same arity and different shapes. Only
the second is convergence. Arity alone cannot express that, which is what
`min_parents_by_type` was added to `spawn_gate.py` for.

**`mvp` was dropped from `allowed_parents`, and this costs something.** The
floors sum to 4 and `max_parents` is 4, so the budget is fully spoken for —
an `mvp` parent could never fit alongside them, and leaving it listed would
advertise a shape no node could ever write. The 2 historical `mvp`-parented
nodes are grandfathered, not rewritten.

`max_parents: 4` is why `[shape].md`'s ceiling went 2 → 4 on the same day.
That is the second deliberate edit to the ceiling, which is the whole design
of having one: raising a budget takes two files.

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
