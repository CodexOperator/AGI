---
confidence: 1.0
goal_id: G5
goal_kind: long-term
heading_level: 2
id: "goal:g5"
mint_id: 71c02192f832480f85cb075ad649a451
origin: goals-doc
seeds:
  - exp:g5-lifecycle-enforcement
  - goal:g5.1
  - idea:engine-schema-registry
  - idea:engine-snapshot-build-site
  - idea:engine-snapshot-goals
  - mvp:strict-goal-refs
status: active
tags:
  - goal
  - root
title: "G5: Goals are a lifecycle the engine reads, not a human convention"
type: goal
---

`status:` should be a field the engine acts on: stop accruing score to
`phasing-out` and `complete` goals while keeping their chains attributable, and
fail loudly when a seed node points at a goal id that does not exist.

**Invariant:** a project is legitimate at three depths — goals only (ideation),
goals + seed ideas (chains starting), goals + build site (execution). A
goals-only project is a valid state, not a broken one.

Banked: **L15** — goals are first-class nodes, derived from this file, linked by
parent-pointing, with referential integrity live and an H0-safe origin-guarded
prune. A missing `GOALS.md` prunes nothing.

Owns: **L5** (rotation the engine enforces), **L18** (the ideation stage; a
missing build site must degrade like a missing `GOALS.md` does, not abort the
driver).

**Landed 2026-08-23** (`exp:g5-lifecycle-enforcement`, `mvp:strict-goal-refs`):
retired goals stop scoring while staying attributable; **L5** rotation warns
every iteration (`METRIC_WARNING goal_rotation=`, currently reading 37/3);
**L18** a goals-only project runs instead of aborting; and `--strict-goals`
makes a dangling goal reference fail the run, wired into `driver.sh` while the
count is still 0 — which is when to start enforcing, not after the first one.

## Revision 2026-09-01: `complete` must keep scoring; only `retired` stops

**This goal's own sentence above is the defect.** "Stop accruing score to
`phasing-out` *and* `complete` goals" collapses two states the lifecycle
already distinguishes, and `metrics.py` implements the collapse:
`SCORING_GOAL_STATUSES = frozenset({"active", "horizon"})`.

The consequence is measured, not theoretical. The 2026-09-01 sweep marked nine
goals `complete`/`phasing-out` on falsifiers and `outcome_coverage` fell
**0.27 -> 0.232** — purely from bookkeeping, with no work undone and no node
removed. **The metric penalises finishing**, which is a live disincentive
against the sweep this project has wanted for three sessions.

**The two states mean different things and must score differently:**

- **`complete` — the goal was achieved.** Its chains are real, valid, and
  still extendable; a later hypothesis may hang off them. The evidence stays
  in the corpus and **stays in the metric**. Completing a goal is the success
  case and must never look like regression.
- **`phasing-out` / retired — the goal stopped making sense.** Folded into
  another goal, accomplished incidentally while working on something else, or
  simply no longer worth pursuing. Its results are not useful to the corpus as
  a whole, so they leave the score.

Two sub-cases the retired side needs, and they are why this is not a one-line
constant change:

1. **A chain that concluded "retire this goal" is excluded.** Such a chain did
   produce evidence — the evidence *for stopping* — but that is a decision
   about the graph, not a contribution to the corpus's outcome coverage.
   Counting it would reward abandoning goals.
2. **A goal retired before any chain closed is ignored wholly.** No completed
   chain means nothing to include or exclude; it should not appear in either
   side of the ratio rather than counting as an unconverted hypothesis.

**Falsifier.** Mark a goal with a closed hypothesis->mvp chain `complete`:
`outcome_coverage` must not move. Mark a goal whose chain concluded "retire
this" as retired: its mvps and hypotheses must leave both numerator and
denominator. Retire a goal with no closed chain: the ratio must be unchanged
in both terms.

**Naming is the only real gap.** The lifecycle already has four states and
`phasing-out` already means "retired"; `CLAUDE.md` documents retirement as
marking `phasing-out`. Renaming it to `retired` would read better and costs a
`status` regex plus a corpus pass — worth doing with the change, not before it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version reverses a decision the previous one made, on evidence the
previous one could not have had.

v1 said retired AND complete goals should stop scoring, and that shipped as
`SCORING_GOAL_STATUSES = {active, horizon}`. It reads sensibly — score work in
flight — and it was wrong about half of its scope. The 2026-09-01 goal sweep is
what showed it: nine goals reclassified on falsifiers, no work undone, no node
removed, and `outcome_coverage` fell 0.27 -> 0.232. A metric that drops when you
finish things teaches you not to finish them, and this project has left 49 goals
`active` against a cap of 3 for three sessions.

The distinction is the owner's and it is sharper than "retired vs not": a
COMPLETE goal still parents chains that exist and can be extended, so its
evidence is permanent corpus; a RETIRED goal's chains led to the conclusion
that the goal was not worth pursuing, so their output is a decision about the
graph rather than a contribution to it. Hence the two sub-cases — a
concluded-in-retirement chain is excluded rather than merely unattributed, and
a goal retired before any chain closed leaves both terms of the ratio alone
instead of counting as an unconverted hypothesis.

Recorded here rather than as a new S-goal deliberately: the active count is
40 against a cap of 3 and adding a goal to fix the goal-scoring rule would be
the wrong shape. G5 already owns "status is a field the engine acts on", and
this is that sentence being wrong.
<!-- THOUGHT:END -->
