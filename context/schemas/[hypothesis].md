---
name: hypothesis
derived_from: corpus-survey-2026-08-25 (n=105)
fields:
  title: {type: str}
  parents: {type: list}     # idea | goal | experiment | hypothesis ids
  next_edges: {type: list}
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
