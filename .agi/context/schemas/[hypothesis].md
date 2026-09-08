---
name: hypothesis
derived_from: corpus-survey-2026-08-25 (n=105)
fields:
  title: {type: str}
  parents: {type: list}     # idea | goal | experiment | hypothesis ids
  next_edges: {type: list}
  push_further: {type: str}  # hypothesis:l3w4-push-further-loops — what a continuation run at this id should push further
  subgraph: {type: bool}    # body is a CoT subgraph?
  testable_claim: {type: str}
  confidence: {type: float}
  origin: {type: str}       # build-site (61/105) -- generated, do not hand-edit
  tags: {type: list}
validation:
  required: [id, type, mint_id, title, testable_claim]
  types:
    title: str
    testable_claim: str
    subgraph: bool
spawn:
  allowed_parents: [idea, goal, experiment, hypothesis]
  min_parents: 1
  max_parents: 2
---

# hypothesis

Testable claim derived from one or more ideas. Each hypothesis spawns
experiments.

When `subgraph: true`, the body itself is parsed as a CoT graph
(premise → inference → claim → testable).

ID prefix: `hyp:<short-slug>`.

## Spawn rule

`allowed_parents: [idea, goal, experiment, hypothesis]`, `max_parents: 2`.
Observed over 105 nodes: `idea` 77, `goal` 3, `hypothesis` 1, `experiment` 1.
A hypothesis parented by an experiment is the "that run raised a new
question" shape and is legal precisely because the corpus does it.

`min_parents: 1`. **24 of 105 are parentless today — the largest violation
group in the graph.** Report, not purge: G7's first invariant is that node
count never drops, and G7.1 settled that inferring the missing edge is
inventing one. The gate runs on the writer path, so these 24 keep their place
and no new one joins them.

## Note on `origin: build-site`

61 of 105 are generated from `context/kits/` + `context/plans/build-site.md`.
**`snapshot-build-site.py` deletes every `origin: build-site` node it does not
re-derive on that run** — hand-edits to their `parents` are silently
overwritten, and emptying the generator inputs prunes them wholesale (H0i).
Retire such a node by deprecating it, never by deleting the input.

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
