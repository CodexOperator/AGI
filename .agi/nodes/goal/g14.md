---
id: goal:g14
mint_id: c721e86dd1c545f0abfcbcac486919c3
type: goal
parents: []
next_edges: []
confidence: 1.0
edited_by: director
goal_id: G14
goal_kind: long-term
heading_level: 2
origin: goals-doc
scaffold_hash: 7bceacd8528266d8
seeds: []
status: horizon
tags:
  - goal
  - root
thought_session: L1.13
title: "G14: Local-maxxing: the smallest model that can do the job, everywhere"
---
# goal:g14

## Agent Notes
**Owner goal, 2026-09-04: local-maxxing.** Use the smallest, fastest, most open
model that can do each job, everywhere it can be done — and make the graph itself
the thing that decides which model that is.

The shape:

- **Mechanistic tagging at creation.** Classifiers, encoders, or small tuned
  models assign a node its tags the moment it is minted, rather than a large
  model being asked to introspect (`goal:g5.2`, `goal:g1.12`).
- **Tags route the model.** Which model writes the next node is a function of the
  requested node's type, flavor tag and grain, given the node it follows in the
  chain. That is config, declared in the graph (`goal:g1`), never improvised per
  spawn.
- **Specialists get sharper over time.** Every routed call is training data for
  the model that serves that slot, so models become hyper-specialised per
  granularity, per loop flavor, per harness piece — narrow capability, tiny
  prompt, tiny output.
- **A lattice, not a ladder.** Many hyper-tuned models each doing one subtask,
  with classifiers and encoders breaking a goal into optimal sub-goals and the
  results stitched back together live at every zoom level — the way DNA is
  stitched during replication, or proteins working inside a cell. No single large
  model in the middle of the loop.

**Why it is a goal rather than an optimisation:** the director's context is the
scarce resource (measured across loop L1) and provider spend is the other. Both
fall out of the same fix — put the smallest competent model at every node and let
the graph, not a human, decide what competent means here.

Related: `goal:g4` (right model at the right grain), `goal:g4.2` (a
reasoning-effort dial), `goal:g4.4` (a web of specialists, each owning a region),
`goal:g2.4` and `goal:s32` (the embeddings pipeline this needs).

### Addendum, 2026-09-04 — the cheapest thing on this lattice is a gap-spotter

The completion review that produced `COMPLETE.md` (`goal:g1.13`) was done by a
large model reading a handoff. **It did not need to be.** The gaps it surfaced —
a goal marked `complete` two days before its code existed, sixteen hazards
carried instead of closed, three goals minted hours before the budget ended, a
decision banked that silently gated half the run's throughput — are all
**pattern-matchable against a parent's own report**. A classifier, or a very
small model, reading a parent report plus the node diff should flag every one of
them. That is the first slot on the lattice worth filling, because it is the one
whose ground truth already exists in the corpus.

**The framing this goal is really about.** There are two ways to get an agent to
behave, and both are bad on their own:

- A **fully deterministic program** — a decision tree at its core. Predictable,
  and unable to handle anything its author did not enumerate.
- **Prompt-maxxing** — write the instruction into `SKILL.md` and hope. Most of
  what is in a skill document today *could* be harness code; instead it is text
  handed to a model, which turns a should-be-invariant into a Markov chain where
  maybe it completes and maybe it does not.

**The lattice is the thing in between.** Many tiny, hyper-tuned models, each with
a narrow capability and a tiny prompt-and-output, wired by classifiers and
encoders — statistical where judgement is genuinely needed, mechanical
everywhere else, and never a single large model asked to hold the whole
instruction set in its head. Each slot is small enough to be trained, scored and
replaced independently.

**The migration path is explicit, and we are on step one:** write the rule into
`skills/agi/SKILL.md` (prompt), observe it hold or fail across loops, then
replace it with a scored model or a plain check. A rule that has survived a few
loops as prose is a rule with a labelled dataset behind it. `COMPLETE.md`'s fixed
failure-category set exists to make those labels.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Owner addendum 2026-09-04: named the first lattice slot (a classifier that spots completion gaps in a parent report -- ground truth already in the corpus), and framed the lattice as the middle ground between a deterministic decision tree and prompt-maxxing, where an instruction that should be harness code is handed to a model as text and becomes a Markov chain. Migration path recorded: SKILL.md prose first, scored model second.
<!-- THOUGHT:END -->
