---
id: goal:g7.31.3.3.1
mint_id: cc394f8a8a0a4b01aada8ef23e3f1039
type: goal
parents:
  - goal:g7.31.3.3
next_edges: []
confidence: 0.85
edited_by: director-helper
goal_id: G7.31.3.3.1
goal_kind: subgoal
heading_level: 6
origin: goals-doc
scaffold_hash: 83f3eceedbfda0f1
season: 2
seeds: []
status: complete
tags:
  - goal
  - subgoal
  - engine
  - spawn
  - rotate
thought_session: helper-nopi-stopline11-20260928
title: "G7.31.3.3.1: Committed parent-slot definitions under each post in .geometry"
town: core
---
# goal:g7.31.3.3.1

## Why this exists

**Parent `goal:g7.31.3.3`.** Owner design: concurrency+parallel limits become pre-set parent post slots under each post in `.geometry`; slot definitions are committed.

## Target end-state

- Committed slot definitions exist under each relevant post in `.geometry` (count = concurrency×parallel contract).
- Live occupancy is NOT stored in the committed slot defs (sibling owns runtime file).

## Invariants

- Sibling slices under `goal:g7.31.3.3` own their own falsifiers — do not widen this leaf.
- Does not open `goal:g7.31.6` / `goal:g7.32.5` (board parked); stays under stop-line `g7.31.3`.

## Falsifier

1. Grep/read on tip shows committed parent-slot rows under post geometry for a sample post.
2. Negative: slot defs file must not hold live occupancy fields as SoT.

## Out of scope

- Other `goal:g7.31.3.3.*` siblings.
- Messaging half of the same owner message (`goal:g7.32.5`, helper / parked).

## Agent Notes

Assigned to **director-belam**. Director-direct under OWNER FULL STOP (NO pi).

NO-PI: committed parent-slot defs landed at .agi/nodes/.geometry/parent-slots.md + parent_slots.py reader; pytest test_parent_slots 6/6; defs hold no occupancy SoT (assert_defs_hold_no_occupancy).

<!-- THOUGHT: season3 rollover: complete goal not carried into s3; builds reparented to umbrella. -->
