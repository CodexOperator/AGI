---
id: goal:g2.2
mint_id: e083c82ffed344569259f98cfc400f9f
type: goal
parents:
  - goal:g2
confidence: 1.0
edited_by: season.py
goal_id: G2.2
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G2.2: IO maps as inherited contract slices"
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

## Two jobs added 2026-09-02: the IO map is the linkage, and the propagator

**The map stops being an annotation and becomes the table the read path
resolves through.** `goal:g13` records the owner's design for one read path and
one write path, and it rests on a node body being a **live link to a file**
rather than stored bytes. The declaration of *which file* is IO-map content:
standardized, configured, one shape for every node type. `payload_ref` is the
prototype — a build node already links rather than copies — and this widens it
from one type to all of them.

**Second job: the map is what says where a change propagates *to*.** With the
linkage declared, a rename or a reference update is mechanically decidable —
the map names every place that fact appears, and `goal:g13`'s write path is
what executes the edit as a kid or parent finishes its node. **The division is
exact and worth holding: this goal owns the links, G13 owns the traversal.**
Nothing is retyped by a model.

**The motivating measurement is this session's own.** Renaming `phasing-out` to
`retired` — a change with **zero semantic content** — costs a `status` regex, a
pass over 28 goal nodes, and hand-edits to `CLAUDE.md`, `SKILL.md` and the
schema file. A schema is declared once in `.agi/context/schemas/[name].md` and
then *restated in prose* in the two documents every agent reads: the lifecycle
states, the verdict taxonomy, the retirement convention, the type list. Three
copies of one fact, two hand-maintained, nothing comparing them. **The same
argument the design ethic makes about spawn briefs applies to renames: code
should spend the tokens, not a model.**

### The hard part is sub-file granularity, and the precedent is already here

Whole-file linking is the easy case and `payload_ref` already solves it. Schema
prose is the hard case: `CLAUDE.md` and `SKILL.md` are mostly hand-written and
only *contain* derived paragraphs, so the link is to a **region of a file**, not
a file. Two ways out, and only one of them is cheap:

- **Marked regions, which this repo has already paid for and proven.**
  `BUILD-CONTRACT:BEGIN/END` and `THOUGHT:BEGIN/END` are exactly "a span of one
  file owned by a different writer, surviving regeneration of everything around
  it." Generalizing that convention is the robust form of "symlink text inside
  another file" — the two halves already coexist in every build node, with the
  ownership rule enforced and understood.
- **Make the whole document derived**, the way `goal:g6.9` made `GOALS.md`
  derived with a byte-identical `--render --check`. Correct, proven, and far
  too heavy for a document that is 95% authored prose.

The acceptance test is G6.9's, narrowed to a span: the marked region re-renders
from the schema, and a `--check` fails when the two disagree.

This also sharpens the stopgap warning above rather than softening it. An index
of symbols cannot do either job: it is rebuilt from the current tree, so it
knows no node, no link, and nothing to propagate *to*.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version gives the IO map two jobs it did not have, both arriving from the
owner's read/write board on 2026-09-02, and both changing what kind of object
the map is. v2 described a map as an inherited contract *slice* — annotation
hanging off a node, read by humans and by `stitch.py --verify`. The linkage job
makes it structural: if a node body is a live link, the map is what the read
path dereferences, and an absent map means an unreadable node rather than a
thinner one.

The propagation job was recorded here rather than in a new goal for the same
reason the gitnexus section was: it is the IO map's object, and a second id
would split one intent. What made it statable now is a measurement rather than
an argument — the `retired` rename in flight this session is a change with no
semantic content that still costs a corpus pass plus three hand-edited
documents.

It was first drafted into `goal:g10.2` and moved here at the owner's
correction, which was right and is worth recording because the wrong placement
was plausible: G10.2 is about the *shape* of the hypergraph, while propagation
is a link (this goal) plus a traversal (`goal:g13`'s write path). The sub-file
question is the owner's too — whether text can be linked inside another file
robustly — and the answer turned out to be already in the repo rather than
needing invention: `BUILD-CONTRACT` and `THOUGHT` are marked regions with a
different owner from the prose around them, surviving regeneration, working
today.

Deliberately not restated: G13's three open questions. They are decisions that
constrain this map's shape and they belong to the goal that raised them; a copy
here would be exactly the drift `goal:s17` names.

No status change, and the S3 ordering for the judgement half is untouched.
<!-- THOUGHT:END -->