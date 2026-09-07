---
id: goal:g1.7
mint_id: d188e9268fde4b87877dc8c8d59aaace
type: goal
parents:
  - goal:g1
confidence: 1.0
edited_by: season.py
goal_id: G1.7
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
title: "G1.7: The demotion path is a command, not a careful hand"
---
Demoting a verdict is a **four-field** edit -- `verdict`, `status`,
`demoted_from`, `demote_reason` -- and `bin/evidence_gate.py` only owns the
first. The other three are left to whoever is holding the keyboard.

**This is not hypothetical: it was reproduced on 2026-08-27, by the repair
crew, inside the pass that was fixing S16.** One verdict was demoted through
`apply_gate` correctly, `verdict:` was rewritten to
`inconclusive_lean_proved:50`, and the legacy `status: proved` was left
sitting underneath it -- **S16's exact defect, re-created by the fix for
S16**. It was caught only because `metrics.py` emits
`shadow_decisive_verdicts`, which went 0 -> 1 on the next run. Without that
counter it would have shipped.

That is the whole argument. A control that depends on remembering three
follow-up edits is a prose control wearing a code control's clothes, which is
the thing **G1** exists to abolish and **S17** named for spawn rules.

What this asks for:

- **One entry point that demotes a node completely.** `evidence_gate.stamp`
  already writes `demoted_from`/`demote_reason`; it does not reconcile the
  `status:` shadow. Fold that in, so the four fields move together or not at
  all.
- **Make the shadow non-authoritative or make it derived.** `status:` is
  declared a legacy shadow of `verdict:` in `[verdict].md` and 61 nodes still
  carry both. Either drop it or compute it -- two hand-maintained copies of
  one fact is **S17**'s defect again.
- **Fail loudly on divergence.** `shadow_decisive_verdicts` caught this after
  the fact. The writer path should refuse before it.

Pairs with **S16** (which closed the code path but not the data), **G3.1**,
and **G7.6** (one persistence model). Falsifier: demote a verdict with one
command and have `shadow_decisive_verdicts` stay 0 without anyone checking.