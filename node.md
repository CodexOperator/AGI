---
id: goal:s27
mint_id: 9689d2979de44066aa583ed9bbfac080
type: goal
parents:
  - goal:g15
confidence: 0.9
edited_by: season.py
goal_id: S27
goal_kind: short-term
heading_level: 2
origin: goals-doc
season: 1
seeds: []
status: complete
tags:
  - goal
  - root
  - short-term
thought_session: season
title: "S27: Dispatch scaffolds an authored node for every tier, including the one that must not author"
---
**Found by the parent itself, in its `struggles:` line, on the first
parent-tier run this project ever completed (2026-09-02).** Quoted verbatim,
because a defect report from the agent that hit it is worth more than a
paraphrase:

> dispatch scaffolds a hypothesis node for the parent tier, but the parent's
> role is review, not hypothesis authorship — the scaffold is dead weight the
> parent must fill with something to pass `cli.py done`

`dispatch.py::_scaffold_node_for_agent` runs for every agent, and
`_node_type_for` picks the type from the *target's* type, never from the
**tier**. So a parent aimed at a goal is handed a `hypothesis` skeleton and
must author it. `hypothesis:a00-a54f694b-b20b78` is that node: a review report
carrying `type: hypothesis`.

## Three consequences, and the third was not chosen by anyone

1. **The parent does work it was briefed not to do.** `brief.py`'s parent brief
   says "You run a loop. You do not write the node yourself" — and then the
   harness requires it to. A brief contradicted by the scaffold is worse than
   no brief: it teaches the agent that the brief is approximate.
2. **`cli.py done` needs a `--node-id`**, so there is no way to signal
   completion without one. The completion contract assumes one agent, one
   authored node.
3. 🔴 **It moves the primary metric.** A parent's review report counts in
   `scoring_hypothesis_count` as a hypothesis that never reached an mvp — so
   every parent-tier run permanently lowers `outcome_coverage` by adding
   denominator that was never a hypothesis. Same class as `goal:s26`: a
   bookkeeping artefact with a numeric consequence, in a metric that
   `goal:g3` exists to keep honest.

## The decision this needs first, and it is not obvious

**What IS a parent's session artifact?** Three candidates, none free:

- **No node at all.** Cleanest conceptually — the parent's output is the
  reviewed kid nodes. Requires `cli.py done` to accept a completion with no
  `--node-id`, and `completion.is_complete` currently keys on a scaffold
  acquiring content, so a nodeless agent would need a second completion shape
  — which is exactly the harness-specific branching `goal:g4.6` forbids.
- **A node of a non-scoring type.** `doc` exists. Cheap, honest, and leaves
  the parent's reasoning in the graph where `goal:g2.7` wants it.
- **A first-class `review` type.** Most expressive, most expensive: a new
  schema, a new spawn rule, and a new thing every reader must know about.

**Recommendation is the second**, on the grounds that it costs one line in
`_node_type_for` and decides nothing that cannot be revisited. But the choice
belongs to the owner, and this goal exists to put it in front of them rather
than to have it made silently by whoever next runs a parent.

## Decided and built 2026-09-02 — and the owner's framing beat all three options

**None of the three candidates was right, because all three asked the wrong
question.** They asked what object a parent authors. The owner's answer:

> Parents aren't nodeless, they are directly responsible for their kids' nodes
> just like real parents.

**A parent's artefact IS its kids' nodes.** That dissolves the problem instead
of trading it: no new type, no second completion shape, no lost provenance, and
the metric artefact disappears because nothing is authored to land in the
denominator.

**Completion follows from it and stays a graph event.** A kid fills its
scaffold and runs `cli.py done`; the parent propagates once every kid is
finished. `completion.owns_all_complete(root, ids)` is `is_complete` applied to
each id — no pid, no `agent.json`, no harness name in the decision. Tier is
first-class in this engine and a harness name is not, so branching on the
former is not what `goal:g4.6` forbids. **Owning nothing is not complete**: a
parent that spawned nothing failed to start its loop, and returning True there
would make the commonest parent failure indistinguishable from success — the
exact shape that hid the dropped-verdict bug for the whole life of the pi
runtime.

Five changes: `dispatch.py` skips the scaffold at `tier == "parent"`;
`cli.py done` takes `--owns <node-id> ...` instead of `--node-id`;
`completion.owns_all_complete`; `post_wire` admits a parent by its kids and
wires nothing for it; `brief.py` tells the parent all of this.

## 🔴 The caveat this must not lose: review prose is parked, not homed

**Where a parent's review goes today: the kid node's `THOUGHT` block.** That is
honest rather than a workaround — a parent's edit to a kid's node *is* a new
version of it, and a thought is by definition the reasoning behind a version.
The parent may fill or refine body and thought on the nodes it owns.

**It is a stopgap and the brief says so in the brief itself**, so the
compression is never mistaken for the design. The owner's requirement, recorded
verbatim in intent:

> once we have webhooks and custom session recording ... the review prose can
> go somewhere. It would go in the higher-LOD view for a given node ... with
> the webhooks and session ID'd API calls it would be trivial to attach
> appropriate kid and parent sessions and even turns to appropriate nodes.
> Least adaptation.

So the destination is **`goal:g2.7`** (the finest zoom is the chat that
produced the version) and **`goal:g10.1`** (chats are thoughts, so chats are
nodes), surfaced through **`goal:g10.2`**'s LOD axis. `thought_session:` is
already reserved in frontmatter for exactly this and nothing writes it yet.

**Two sub-thought fields — one kid, one parent — were considered and
rejected by the owner** as "wasted context details". The reasoning holds
independently: session linking attaches *turns* to versions, at which point a
hand-split field is a coarser copy of something the graph already knows
precisely. Splitting now would build the thing session linking makes redundant.

**Until then, settle for the parent's report plus the node thought blocks.**
That is the whole interim contract, stated so the next reader knows it is a
floor and not a ceiling.

## Falsifier

Spawn a parent. It completes without authoring anything typed `hypothesis`,
`experiment`, `verdict` or `mvp`; `scoring_hypothesis_count` is unchanged by
the run; and the parent's review is still recoverable from the graph
afterwards. All three, or the fix has traded a metric artefact for lost
provenance.

**Status: first two clauses satisfied in code and under test** (no scaffold at
`tier == "parent"`, nothing authored, so nothing reaches the denominator).
**The third is satisfied only by convention** — the brief instructs the parent
to write into its kids' `THOUGHT` blocks, and nothing enforces that it did. A
parent that reviews silently loses its reasoning, and no test can currently
tell that from a parent that had nothing to say. That gap closes with session
linking, not before, and it is the honest reason this goal ships `complete`
with a named residual rather than pretending the third clause is mechanical.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2 is the decision, and the decision was not on the menu v1 offered.

v1 laid out three candidate artefacts and recommended the cheapest. All three
shared an assumption I had not noticed I was making: that a parent must author
*something*, and the only question was what type. The owner rejected the frame
rather than the options -- a parent is responsible for its children's nodes,
the way a real parent is responsible for its children. Once said, it is
obviously right, and it dissolves every cost the three options were being
traded against: no new schema, no second completion shape, no lost provenance,
and the metric artefact simply does not arise because nothing is authored.

It also answered the objection I had raised against "no node at all" -- that
`cli.py done` needs a node id and `is_complete` keys on a scaffold acquiring
content, so a nodeless agent would need a second completion shape. The owner's
answer was that the kids already produce exactly that signal and the parent
propagates it. `owns_all_complete` is four lines and reuses `is_complete`
unchanged.

The residual is stated rather than smoothed over. Clauses 1 and 2 of the
falsifier are mechanical and tested; clause 3 -- that the parent's review is
still recoverable -- holds only by convention, because nothing checks that a
parent actually wrote into its kids' thoughts. I would rather ship `complete`
with that named than write a test that asserts the convention was followed and
call the gap closed.

The webhook/session-linking caveat is recorded at length deliberately. It is
the difference between "the thought block is where reviews live" and "the
thought block is where reviews live *for now*", and the second is what was
decided. A future reader finding review prose squeezed into thought blocks
should find the reason next to it.
<!-- THOUGHT:END -->