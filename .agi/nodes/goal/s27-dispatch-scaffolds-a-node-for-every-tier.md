---
confidence: 0.9
goal_id: S27
goal_kind: short-term
heading_level: 2
id: "goal:s27"
mint_id: 9689d2979de44066aa583ed9bbfac080
origin: goals-doc
seeds: []
status: horizon
tags:
  - goal
  - root
  - short-term
title: "S27: Dispatch scaffolds an authored node for every tier, including the one that must not author"
type: goal
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

## Falsifier

Spawn a parent. It completes without authoring anything typed `hypothesis`,
`experiment`, `verdict` or `mvp`; `scoring_hypothesis_count` is unchanged by
the run; and the parent's review is still recoverable from the graph
afterwards. All three, or the fix has traded a metric artefact for lost
provenance.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted straight from a `struggles:` line, which is the second time in this
session that field found something the review around it missed. `SKILL.md`
already argues those two lines are the cheapest signal in the system; this is
the run that turned the argument into evidence.

The third consequence is the one that made this worth a goal rather than a
note. The first two are ergonomic -- annoying, survivable. The metric effect
is not: it means running the parent tier at all degrades the number the loop is
scored on, so the system would quietly penalise using its own new capability.
That is the same shape as `goal:g5`'s finished-goals defect and `goal:s26`'s
premature-complete, and three instances in one session is a pattern worth
naming: **lifecycle and scaffolding bookkeeping keeps leaking into the primary
metric.**

Left `horizon` and deliberately undecided. The three candidate artefacts are
laid out with costs because the recommendation is weak -- `doc` is cheap and
reversible, not obviously right -- and a goal that pre-decides a schema
question is how `goal:g4.3` steered kids for weeks.
<!-- THOUGHT:END -->
