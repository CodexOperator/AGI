---
id: goal:g7.16.1.11.44.4
mint_id: b84a4930d36b4ee3877774cfbf3c6457
type: goal
parents:
  - goal:g7.16.1.11.44
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.44.4
goal_kind: subgoal
origin: goal
seeds: []
tags: []
role: master
season: 2
status: active
title: "G7.16.1.11.44.4: the capsule verb `in` is an engine shell piece in engine-capsule.md, built to doc:g716111-44-capsule-pack section 5"
town: core
---
# goal:g7.16.1.11.44.4

## Why this exists
goal:g7.16.1.11.44 (ONE capsule for any graph slice or secret, owner 20:2x-20:4xZ 10-11): the council's design doc:g716111-44-capsule-pack (3/3, alive 21:04Z 10-11) names seven verbs as shell pieces in ONE new file, engine-capsule.md, each with its own falsifier row. SM places one build leaf per verb, as the design asks.

## Target end-state
1. `capsule in FILE`: verify, then `git fetch --atomic FILE <exactly the listed refs>`.
2. It lives in engine-capsule.md (the verbs' ONE home); engine-sizes b1 applies to that file; engine.md gains only its map row.

## Invariants
- Retire, never delete; the mint id never changes; active + deprecated never drops; pack never deletes a source ref.

## Falsifier
1. ATOMIC: one non-ff ref -> rc != 0 and NOTHING moved; the mutant without --atomic -> a sibling advanced = RED, as its own row in a lane, with a mutant RED on it.

## Out of scope
The other verbs (their own leaves under goal:g7.16.1.11.44) · the season-rollover RUN itself (owner-ruled, after the verbs).

## Order
Build may start now; it LANDS after goal:g7.16.1.11.41 (the season-2 close gate), as .44 orders.

## Agent Notes
Assigned to **director-general-4**.
