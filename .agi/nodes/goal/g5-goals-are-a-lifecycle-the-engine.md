---
id: goal:g5
mint_id: 71c02192f832480f85cb075ad649a451
type: goal
confidence: 1.0
edited_by: season.py
goal_id: G5
goal_kind: long-term
heading_level: 2
origin: goals-doc
season: 1
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
thought_session: season
title: "G5: Goals are a lifecycle the engine reads, not a human convention"
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

## Landed 2026-09-02 — both halves, and the third clause the revision needed

`SCORING_GOAL_STATUSES` is now `{active, horizon, complete}` and
`RETIRED_GOAL_STATUSES` is `{retired, phasing-out}`. Measured on the live
corpus at the moment of the change: **`outcome_coverage` 0.232 -> 0.284**, from
27 `complete` goals whose chains had been excluded for no reason anyone had
decided. That is more than the 0.038 the 2026-09-01 sweep cost.

**The third clause is the one the revision above did not state, and without it
the fix would have armed a worse metric than it repaired.** The revision's
sub-case 2 and its own falsifier contradicted each other — the body said a
retired goal's unconverted hypotheses "should not appear in either side of the
ratio", the falsifier said "the ratio must be unchanged in both terms". The
owner resolved it on the narrow reading, and the resolution is a rule:

> **Retirement can only ever remove a *closed* chain, never bare denominator
> weight.** A hypothesis under a retired goal that never reached an mvp stays
> in the denominator.

Without it, retiring goals in bulk — which is exactly what a goal sweep does —
raises `outcome_coverage` for free, and nothing in the metric can tell that
apart from honest retirement. This project has already paid once for a gameable
primary metric (`goal:g3`); it did not need a second one wearing a lifecycle
field as a disguise. `retired_open_hypotheses` is emitted so the spared set is
visible rather than implicit.

Implementation note worth keeping: "on a closed chain" is computed by walking
**up** from every `mvp` through `parents`, stopping at goals. `parents` is the
edge direction stored on disk, so this needs no inverted index and no second
traversal order to keep in sync.

**The rename shipped with it**, as this goal said it should. `retired` is
canonical in the schema regex, `snapshot-goals.py`, `metrics.py`, `CLAUDE.md`,
`SKILL.md`, the goals preamble node, and the one live node carrying it
(`goal:g6.5`). **`phasing-out` stays accepted permanently, not for a migration
window** — projects predating the rename carry it, and a reader that stopped
recognising it would silently start scoring their retired chains.

`goals_retired` also stopped counting `complete`, which was the same collapse
`SCORING_GOAL_STATUSES` made, in the reporting layer. `goals_complete` is now
its own line.

**Five falsifier tests, all fixtures.** Every clause was unobservable on the
live corpus the day it shipped — 1 retired goal, 0 hypotheses beneath it — so
there was nothing to measure them against until a sweep creates the shape.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The active marker is a FOCUS BUDGET, not an in-flight census -- the owner clarified this on 2026-09-03, and metrics.py now says so where it used to say the opposite. The old warning read: a goal marked active claims to be in flight. Under that reading, 13 active goals against a cap of 9 was a lie to be corrected by relabelling four goals horizon. That correction would have been the field losing information a second way, because g3, g5 and g7 really are permanently active -- a long-term goal is always arguably active, and the marker earns its keep by selecting WHICH long-term goals chain-building aims at right now. So the cap bounds attention, not honesty: past it, kids spread across more goals than a run can move and no single chain gets enough hops to close. Cap raised 9 -> 15 deliberately rather than silenced by retagging. This settles the third banked decision from the 2026-09-02b session.
<!-- THOUGHT:END -->