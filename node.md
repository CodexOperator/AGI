---
id: goal:s26
mint_id: 46d3da15cddd4baaae02af095551cd78
type: goal
parents:
  - goal:g15
confidence: 0.9
edited_by: season.py
goal_id: S26
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
title: "S26: An overarching goal is not `complete` while its subgoals are live"
---
**The owner's rule, stated during the 2026-09-02 sweep, and it caught a real
misclassification in the act.** The sweep's recommendation was to mark
`goal:g5` `complete` — every falsifier it names is met and iteration 1 built
the last of it. The owner refused it: G5 is *overarching*, and `goal:g5.1` is
`horizon`. A long-term goal's purpose is not achieved just because its own
text is satisfied; it is achieved when the work it organises is.

**Invariant:** a goal with `goal_kind: long-term` may not be `complete` while
any goal listing it in `parents:` is `active` or `horizon`.

## Why this is worth mechanising rather than remembering

`status` is supposed to be a field the engine acts on (`goal:g5`) — a rule
enforced by whoever happens to be running the sweep is the human convention
that goal exists to replace. Three specific consequences, and the third is the
one that bites:

1. **A wrongly-`complete` root disappears from the tracker** exactly when the
   project has decided to use active goals as the tracker instead of
   `HANDOFF.md`.
2. **It reads as a claim about its children.** A reader seeing `G5: complete`
   reasonably concludes G5.1 is done too.
3. **It is now load-bearing on the metric.** Since iteration 1 of 2026-09-02,
   `complete` **scores** while retired does not. So a premature `complete` on a
   root silently moves `outcome_coverage` — a bookkeeping mistake with a
   numeric consequence, which is the class of defect `goal:g5`'s revision was
   written to stop.

## Where it goes, and the check it must not become

The natural home is `snapshot-goals.py`, beside `KNOWN_STATUSES`, as a
**warning on render** rather than a hard failure — the same shape as
`METRIC_WARNING goal_rotation=`. A hard failure would make a legitimate
intermediate state (retiring a tree bottom-up, one commit per goal)
unrepresentable, and `goal:g5`'s own invariant says a project must stay
legitimate at every depth.

**It must not become a walk that any metric consults.** `parents:` on a goal is
lineage and this check reads it, but a *count* derived from it is a fresh
gaming surface — `goal:g3` and `goal:g4.5` both name that hazard, and G4.5
names it about this exact edge field.

## Falsifier

Mark a long-term goal `complete` while one of its subgoals is `active`:
`snapshot-goals.py --render` warns, names both goals, and exits 0. Retire or
complete every subgoal, re-render: the warning is gone. Then mark a
**short-term** goal `complete` with no subgoals at all — no warning, because
the rule is about roots with live children and nothing else.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted at the owner's direction after they overruled the sweep's own
recommendation. Worth recording that the rule arrived as a correction rather
than as a design: the sweep proposed `goal:g5` -> `complete`, the owner asked
whether an overarching goal can be complete while its subgoals are live, and
the answer was obviously no once asked.

Filed as short-term rather than under `goal:g5` because g5 owns "status is a
field the engine acts on" and this is one specific check to add to that
statement, with its own falsifier. Folding it into g5 would grow the goal a
third revision layer, and g5 has already been revised twice.

The third consequence is the reason this is not cosmetic and it did not exist
before today. Iteration 1 made `complete` score. That turned goal
classification into an input to the primary metric, so a premature `complete`
is now a number moving for a bookkeeping reason -- which is precisely the
defect `goal:g5`'s revision was written to remove, re-entering through a
different door.

Left `horizon` rather than `active`: it is scheduled, not being worked, and
`horizon` is what that means.
<!-- THOUGHT:END -->