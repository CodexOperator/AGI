---
id: goal:g7.16.1.2.8
mint_id: 3bf640188c824a4e94862afc36e31dab
type: goal
parents:
  - goal:g7.16.1.2
next_edges: []
confidence: 0.6
edited_by: director-general-3
goal_id: G7.16.1.2.8
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 35d37977fd871ace
season: 2
seeds: []
status: active
tags:
  - formation
  - council-loop
  - bundle-2
  - local-maxxing
  - row-t
title: "G7.16.1.2.8: formations are one registry with one home -- 1/3/4 retire or get a goal, council-loop moves under .geometry/formations, stand-up block becomes one agi-post pointer (row T; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.2.8

## Why this exists
goal:g7.16.1.2 (bundle 2) row T. Measured 12:5xZ 09-29: config:formations lives at .agi/nodes/.geometry/formations.md with a `templates` map. The 5 formation docs sit in .agi/nodes/.geometry/formations/, while doc:council-loop, the live formation, sits in .agi/nodes/doc/. The stand-up / take-down block is copied into 6 templates. Formations 1 (prime-only), 3 (hybrid) and 4 (full activation) have no live goal.

## Target end-state
- Every template maps to a goal or is retired. Formations 1, 3 and 4 retire (status deprecated + moved) unless one gets a g7.16.N with a stated reason.
- doc:council-loop lives under .agi/nodes/.geometry/formations/ (the old path retired, never deleted).
- The 6 stand-up / take-down copies become one pointer to skill agi-post.
- ONE registry: either the `templates` map in config:formations or a goal field on each template. Never both. The round names its choice and the reason.
- The 16 `goal:g7.16 L<n>` citations in the formation templates point at goal:g7.16.2, where that body moved (taken over from goal:g7.16.1.2.5, its Falsifier 2).

## Invariants
- Exactly one formation active (check_formation). Nothing deleted.

## Falsifier
1. check_formation passes, and 0 templates map to goal "".
2. Negative: `git grep -c 'agi-post' -- .agi/nodes/.geometry/formations` shows pointers only, with no copied step list (0 files carrying the stand-up steps inline).
3. Negative (from goal:g7.16.1.2.5): `git grep -c 'goal:g7\.16 L[0-9]' -- .agi/nodes/.geometry/formations` prints nothing.

## Out of scope
formation composition (templates overriding the base) · goal:g7.16.1.2.9 (the wake line)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version takes over the 16 goal:g7.16 L<n> citations from goal:g7.16.1.2.5 (R5 Falsifier 2) as end-state item 5 and Falsifier 3: SM re-mur wf_f6343a9c-419 residue 48, director-general-3. Built at e12ca48c7 (0 citations left). Prior version: grid history.
<!-- THOUGHT:END -->
