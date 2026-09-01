---
confidence: 1.0
goal_id: G2.2
goal_kind: subgoal
heading_level: 3
id: "goal:g2.2"
mint_id: e083c82ffed344569259f98cfc400f9f
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

## Interim: gitnexus, because agents grep code the graph should already answer

**The destination is this goal; the gap today is that nothing lets an agent
query the code as a graph at all.** Every kid so far has navigated the engine
by `grep` and `find` — and the cost is visible in their own reports: one burned
its first read guessing a filename from a node id, another fell back to `grep`
after reaching for `rg`. That is motion spent on operations, which is the one
thing the design ethic says to script away.

`gitnexus` is installed, works on ordinary code with no schema of ours, and
answers the structural questions the IO maps will eventually answer natively —
what calls this, what breaks if I change it, where does this flow. **It is a
stopgap and should be named as one**, for two reasons that are the same
reason: it indexes *files and symbols*, not nodes, so it knows nothing about
`payload_ref`, mint ids, or the contract entries `level3.py` derives; and its
index goes stale against a tree the loop is actively editing, so it reports
staleness rather than truth unless re-run.

**What to do with it, smallest first:** wire invocation into the `agi` skill so
a kid reaches for a query instead of a grep, and record which questions it
actually answered well. That last part is the useful output even after it is
retired — a measured list of what agents needed to ask about the code is
precisely the requirements document for the real IO maps, written by usage
instead of by guessing.

**Do not let the stopgap become the design.** If IO map work starts deferring
to "gitnexus already covers that", this goal has been replaced rather than
served — the maps are *inherited contract slices attached to nodes*, which is a
different object from an index of symbols, and only one of them survives a
`stitch.py --from-grid` of a historical version.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Added 2026-09-01 at the owner's direction, after they asked to "graph the code
asap" and correctly recalled that an IO map goal already existed rather than
letting a second one be seeded. Recorded here instead of as a new goal for
exactly that reason: a fresh goal would have split one intent across two ids,
and the failure mode this repo already knows is `goal:g4.3` — a goal whose
framing quietly steers every kid working under it.

The paragraph warning against the stopgap becoming the design is the load-
bearing one. Gitnexus answers structural questions well enough that deferring
to it is the path of least resistance, and the difference that matters is not
capability but *attachment*: an index is rebuilt from the current tree, while
an IO map is a slice inherited by a node and versioned with it. A graph that
cannot be materialised at version N is not this goal's object.

No status change. The judgement half and the S3 ordering are untouched.
<!-- THOUGHT:END -->
