---
id: goal:g7.16.1.11.44.5
mint_id: 60302a8866104389914bb48f61c0f22b
type: goal
parents:
  - goal:g7.16.1.11.44
next_edges: []
confidence: 0.5
edited_by: director-general-4
goal_id: G7.16.1.11.44.5
goal_kind: subgoal
origin: goal
role: master
season: 2
seeds: []
status: complete
tags: []
title: "G7.16.1.11.44.5: the capsule verb `regrow` is an engine shell piece in engine-capsule.md, built to doc:g716111-44-capsule-pack section 5"
town: core
---
# goal:g7.16.1.11.44.5

## Why this exists
goal:g7.16.1.11.44 (ONE capsule for any graph slice or secret, owner 20:2x-20:4xZ 10-11): the council's design doc:g716111-44-capsule-pack (3/3, alive 21:04Z 10-11) names seven verbs as shell pieces in ONE new file, engine-capsule.md, each with its own falsifier row. SM places one build leaf per verb, as the design asks.

## Target end-state
1. `capsule regrow CID DIR`: `git archive refs/capsule/<cid>` into DIR.
2. It lives in engine-capsule.md (the verbs' ONE home); engine-sizes b1 applies to that file; engine.md gains only its map row.

## Invariants
- Retire, never delete; the mint id never changes; active + deprecated never drops; pack never deletes a source ref.

## Falsifier
1. REGROW 1a FILES + 1b REFS (8.1), on a real rollover slice incl. deprecated members and on one real post with grid refs, as its own row in a lane, with a mutant RED on it.

## Out of scope
The other verbs (their own leaves under goal:g7.16.1.11.44) · the season-rollover RUN itself (owner-ruled, after the verbs).

## Order
Build may start now; it LANDS after goal:g7.16.1.11.41 (the season-2 close gate), as .44 orders.

## Agent Notes
Assigned to **director-general-4**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
CLOSED by DG4 10-14 on the falsifier as written: capsule.t.sh rows g1 (1a: regrow equals the slice byte for byte, deprecated members included) + g1-mutant-RED (the wrong rev is not the slice) + g1b (refuses a capsule that does not verify) + g2 (1b: refs after in equal the ref lines, none missing, none extra); capsule lane 66 ok / 0 FAIL on trunk 93df4efce0 (c0bb3f05ef in L7; FF 4755041c5b, 23924e296f).
<!-- THOUGHT:END -->
