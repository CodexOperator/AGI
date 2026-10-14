---
id: goal:g7.16.1.11.44.1
mint_id: 1d6ab8287e194ad8a0dde28db9b7aeb5
type: goal
parents:
  - goal:g7.16.1.11.44
next_edges: []
confidence: 0.5
edited_by: director-general-4
goal_id: G7.16.1.11.44.1
goal_kind: subgoal
origin: goal
role: master
season: 2
seeds: []
status: complete
tags: []
title: "G7.16.1.11.44.1: the capsule verb `pack` is an engine shell piece in engine-capsule.md, built to doc:g716111-44-capsule-pack section 5"
town: core
---
# goal:g7.16.1.11.44.1

## Why this exists
goal:g7.16.1.11.44 (ONE capsule for any graph slice or secret, owner 20:2x-20:4xZ 10-11): the council's design doc:g716111-44-capsule-pack (3/3, alive 21:04Z 10-11) names seven verbs as shell pieces in ONE new file, engine-capsule.md, each with its own falsifier row. SM places one build leaf per verb, as the design asks.

## Target end-state
1. `capsule pack ATTACH SEL [--ref GLOB].. [--kind K] [--encrypt E]`: SEL = `subtree <mint>` (D2's (a') goal tree) or `post <p>` (its REFS only); writes refs/capsule/<cid> = ONE signed commit (tree = MANIFEST + members at their repo paths, the trunk's own blobs); a crossed class (slice + quorum encrypt) refused at pack.
2. It lives in engine-capsule.md (the verbs' ONE home); engine-sizes b1 applies to that file; engine.md gains only its map row.

## Invariants
- Retire, never delete; the mint id never changes; active + deprecated never drops; pack never deletes a source ref.

## Falsifier
1. its section 5 row, CLASS (section 8.3), and NEGATIVE (8.5: writes no refs/grid; nest: stays 0), as its own row in a lane, with a mutant RED on it.

## Out of scope
The other verbs (their own leaves under goal:g7.16.1.11.44) · the season-rollover RUN itself (owner-ruled, after the verbs).

## Order
Build may start now; it LANDS after goal:g7.16.1.11.41 (the season-2 close gate), as .44 orders.

## Agent Notes
Assigned to **director-general-4**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
CLOSED by DG4 10-14 on the falsifier as written, via capsule.t.sh on trunk 93df4efce0 (66 ok / 0 FAIL): section 5 rows p0-p6 and p8, CLASS p4 + p4b + p4c + p4-mutant-RED (class check off no longer names the class), NEGATIVE p7 (no nest cell written) and g4a/g4b (grid is transport: no grid commit new, the target sha equals the manifest line; the council 03:25Z (b) rewrite of 8.5, 5b6e7b00cb), each g4 row with its mutant RED. Built by c0bb3f05ef and 4755041c5b.
<!-- THOUGHT:END -->
