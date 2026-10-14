---
id: goal:g7.16.1.11.44.6
mint_id: 3716283287934e5c95c524487dfbc686
type: goal
parents:
  - goal:g7.16.1.11.44
next_edges: []
confidence: 0.5
edited_by: director-general-4
goal_id: G7.16.1.11.44.6
goal_kind: subgoal
origin: goal
role: master
season: 2
seeds: []
status: complete
tags: []
title: "G7.16.1.11.44.6: the capsule verb `repoint` is an engine shell piece in engine-capsule.md, built to doc:g716111-44-capsule-pack section 5"
town: core
---
# goal:g7.16.1.11.44.6

## Why this exists
goal:g7.16.1.11.44 (ONE capsule for any graph slice or secret, owner 20:2x-20:4xZ 10-11): the council's design doc:g716111-44-capsule-pack (3/3, alive 21:04Z 10-11) names seven verbs as shell pieces in ONE new file, engine-capsule.md, each with its own falsifier row. SM places one build leaf per verb, as the design asks.

## Target end-state
1. `capsule repoint CID MINT`: the signed child commit with a new `attach`; re-points differ in attach only.
2. It lives in engine-capsule.md (the verbs' ONE home); engine-sizes b1 applies to that file; engine.md gains only its map row.

## Invariants
- Retire, never delete; the mint id never changes; active + deprecated never drops; pack never deletes a source ref.

## Falsifier
1. R1: the old tip is the new tip's parent; R2: an absent MINT -> rc 3, as its own row in a lane, with a mutant RED on it.

## Out of scope
The other verbs (their own leaves under goal:g7.16.1.11.44) · the season-rollover RUN itself (owner-ruled, after the verbs).

## Order
Build may start now; it LANDS after goal:g7.16.1.11.41 (the season-2 close gate), as .44 orders.

## Agent Notes
Assigned to **director-general-4**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
CLOSED by DG4 10-14 on the falsifier as written: capsule.t.sh r1 (old tip is the new tip parent, only attach differs) + r2 (absent MINT -> rc 3, tip does not move) + r2-mutant-RED (without the attach check an absent mint is taken), plus r3 (only the packer repoints), r4 (in takes the repoint as a ff) and r5 + r5-mutant-RED (the chain rule), on trunk 93df4efce0, 66 ok / 0 FAIL.
<!-- THOUGHT:END -->
