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
  status: {type: str}          # pending | in_progress | done
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
    status: '^(pending|in_progress|done)$'
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

## Uniform values worth knowing

`tier: -1` on 91/91 (the build-site tiering was never assigned), `status:
pending` on 91/91 (no task has been marked done through this field),
`effort`: M 58, S 29, L 4.
