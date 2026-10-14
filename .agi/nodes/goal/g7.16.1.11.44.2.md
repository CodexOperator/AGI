---
id: goal:g7.16.1.11.44.2
mint_id: c014e07f6d074f729a3a23e31ec5395f
type: goal
parents:
  - goal:g7.16.1.11.44
next_edges: []
confidence: 0.5
edited_by: director-general-4
goal_id: G7.16.1.11.44.2
goal_kind: subgoal
origin: goal
role: master
season: 2
seeds: []
status: complete
tags: []
title: "G7.16.1.11.44.2: the capsule verb `out` is an engine shell piece in engine-capsule.md, built to doc:g716111-44-capsule-pack section 5"
town: core
---
# goal:g7.16.1.11.44.2

## Why this exists
goal:g7.16.1.11.44 (ONE capsule for any graph slice or secret, owner 20:2x-20:4xZ 10-11): the council's design doc:g716111-44-capsule-pack (3/3, alive 21:04Z 10-11) names seven verbs as shell pieces in ONE new file, engine-capsule.md, each with its own falsifier row. SM places one build leaf per verb, as the design asks.

## Target end-state
1. `capsule out CID > FILE`: the thin git bundle (+ the outer seal when flagged).
2. It lives in engine-capsule.md (the verbs' ONE home); engine-sizes b1 applies to that file; engine.md gains only its map row.

## Invariants
- Retire, never delete; the mint id never changes; active + deprecated never drops; pack never deletes a source ref.

## Falsifier
1. O1: `git bundle verify` passes on a repo holding `base`, fails on one that does not, as its own row in a lane, with a mutant RED on it.

## Out of scope
The other verbs (their own leaves under goal:g7.16.1.11.44) · the season-rollover RUN itself (owner-ruled, after the verbs).

## Order
Build may start now; it LANDS after goal:g7.16.1.11.41 (the season-2 close gate), as .44 orders.

## Agent Notes
Assigned to **director-general-4**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
CLOSED by DG4 10-14 on the falsifier as written: capsule.t.sh o1 (git bundle verify passes where base is held) and o1b (fails where base is not held) on trunk 93df4efce0, 66 ok / 0 FAIL; the thin-bundle size row rides 4755041c5b, engine-sizes 0 FAIL. Built by c0bb3f05ef and 4755041c5b. Mutant: o1b is the RED side (a bundle that verifies without its base would pass o1b wrongly).
<!-- THOUGHT:END -->
