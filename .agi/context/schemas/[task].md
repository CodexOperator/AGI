---
name: task
derived_from: corpus-survey-2026-08-25 (n=91) -- the only pre-existing schema that needed no repair
fields:
  title: {type: str}
  cavekit_req: {type: str}     # "graph-core/R1"
  acceptance_criteria: {type: list}
  blocked_by: {type: list}     # task ids
  effort: {type: str}          # S | M | L
  tier: {type: int}
  status: {type: str}          # pending | in_progress | done | deprecated
  origin: {type: str}          # build-site -- generated, do not hand-edit
  parents: {type: list}        # hypothesis ids
  tags: {type: list}
validation:
  required: [id, type, mint_id, title, cavekit_req, status, parents, acceptance_criteria, blocked_by, effort, tier, origin, tags]
  types:
    tier: int
    acceptance_criteria: list
    blocked_by: list
  regex:
    effort: '^[SML]$'
    status: '^(pending|in_progress|done|deprecated)$'
spawn:
  allowed_parents: [hypothesis]
  min_parents: 1
  max_parents: 1
---

# task

Build-site task from `context/plans/build-site.md`. One per T-NNN id. Maps to
a cavekit requirement and a set of acceptance criteria.

ID prefix: `task:<short-slug>` (e.g. `task:t-001-node-primitive`).

## Spawn rule — the tightest in the graph

`allowed_parents: [hypothesis]`, `max_parents: 1`, `min_parents: 1`. Over 91
nodes there is exactly one observed parent type and never more than one
parent: `hypothesis` 91/91, **zero parentless, zero exceptions**. The budget
is 1 because 1 is all the corpus has ever used — see `[shape].md`; raising it
is a deliberate act, not a default.

## The one schema that was already honest

Every field this schema declared required is present on 91/91 nodes. It is
the control case for the repairs applied to `[experiment].md`, `[mvp].md` and
`[outcome].md`, and the reason is visible in the corpus: all 91 tasks are
`origin: build-site`, written by one generator, so the declared shape and the
written shape were produced together. The three schemas that drifted describe
types written by **agents**, freehand.

`required:` is widened here from `[title, cavekit_req, status]` to the full
91/91 set — not new rules, just the measurement written down.

## 2026-09-03 (L1.09-cleanup): `status` regex widened to admit `deprecated`

"Already honest" stopped being true the moment the corpus changed under it:
the entire 91/91 build-site task cohort was retired in L1.09, each one
rewritten with `status: deprecated` per `CLAUDE.md`'s retirement convention —
and the pre-existing regex, `^(pending|in_progress|done)$`, had never had to
admit a fourth value because no task had ever left `pending` through this
field. Same repair `[idea].md` already carries for the same reason
(precedent: `idea:engine-todo`), applied here because retirement is a
cross-type convention, not an idea-only one.

## Uniform values worth knowing

`tier: -1` on 91/91 (the build-site tiering was never assigned), `status:
pending` on 91/91 (no task has been marked done through this field),
`effort`: M 58, S 29, L 4.

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
