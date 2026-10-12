---
id: goal:g7.16.1.11.44.7
mint_id: 093556ec6c4b474482fcd756d6aa754c
type: goal
parents:
  - goal:g7.16.1.11.44
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.44.7
goal_kind: subgoal
origin: goal
seeds: []
tags: []
role: master
season: 2
status: active
title: "G7.16.1.11.44.7: the capsule verb `move` is an engine shell piece in engine-capsule.md, built to doc:g716111-44-capsule-pack section 5"
town: core
---
# goal:g7.16.1.11.44.7

## Why this exists
goal:g7.16.1.11.44 (ONE capsule for any graph slice or secret, owner 20:2x-20:4xZ 10-11): the council's design doc:g716111-44-capsule-pack (3/3, alive 21:04Z 10-11) names seven verbs as shell pieces in ONE new file, engine-capsule.md, each with its own falsifier row. SM places one build leaf per verb, as the design asks.

## Target end-state
1. `capsule move POST BOX` = section 6: DRY pack in a job-owned clone + TARGET verify + a scratch `in` on MAIN's filesystem with a refs-dir write probe, all BEFORE the stop; then the real pack / carry ONE file / `in --atomic`; RECOVERY = [move-in-failed], the row reverted, the post started on FROM, FROM's refs unchanged. Replaces box-move.sh :32-:45, keeps :31 unit-paths and the row edit.
2. It lives in engine-capsule.md (the verbs' ONE home); engine-sizes b1 applies to that file; engine.md gains only its map row.

## Invariants
- Retire, never delete; the mint id never changes; active + deprecated never drops; pack never deletes a source ref.

## Falsifier
1. MOVE (8.4: the next box move runs section 6 and the .39 counts per namespace match) + the section 6 rows (a dry run leaves MAIN's refs/capsule/* count unchanged; RECOVERY), as its own row in a lane, with a mutant RED on it.

## Out of scope
The other verbs (their own leaves under goal:g7.16.1.11.44) · the season-rollover RUN itself (owner-ruled, after the verbs).

## Order
Build may start now; it LANDS after goal:g7.16.1.11.41 (the season-2 close gate), as .44 orders. Builds on .44.1-.44.4 (pack, out, verify, in) and on DG2's .39.2-.39.4.

## Agent Notes
Assigned to **director-general-2**.
