---
confidence: 1.0
goal_id: G2.2
goal_kind: subgoal
heading_level: 3
id: "goal:g2.2"
mint_id: e083c82ffed344569259f98cfc400f9f
order: 10
origin: goals-doc
parents:
  - goal:g2
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G2.2: IO maps as inherited contract slices"
type: goal
---

Every node declares required inputs and promised outputs, each with a how/why,
a performance note and a security note; the maps re-derive when neighbours
change.

**Half of this shipped 2026-08-22 and the half that shipped is the mechanical
half** — `level3.py` emits 1,110 contract entries whose `how` is derived from
`ast` with a line number, and `stitch.py --verify` re-derives and diffs them, so
a contract that drifts from its code is detected rather than rotting invisibly.
That is the freshness problem the anatomy node had recorded as unsolved.

**What remains is the judgement half.** `why`, `perf` and `security` are emitted
as explicit `TODO(model)` placeholders — deliberately blank, because a
fabricated security note is worse than an absent one. Filling them is a model
pass over the placeholders, and it is the first real test of the split this goal
rests on: the harness owns the shape, the model only ever fills free text. Its
falsifier is already pre-registered in `hyp:level3-node-anatomy` — harness
fields must hit 1.000 recall by construction, and prose must hold ≥ 0.792.

Do the model pass only after **S3** — a truncated `how` can currently contain a
fence-lookalike that trips a naive reader, and the model pass is exactly the
next consumer that would hit it.
