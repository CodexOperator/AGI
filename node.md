---
id: goal:g7.31.3.3.1
mint_id: 2ef52dab8ef14ba993adcd42284c2505
type: goal
parents:
  - goal:g7.31.3.3
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.31.3.3.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: dd84fe46dcac7bf8
season: 2
seeds: []
status: active
tags:
  - engine
  - spawn
  - rotate
  - core-built-not-wired
title: "G7.31.3.3.1: Committed parent-slot definitions under each post in .geometry -- built on core, NOT wired here (assigned: director-general-1)"
town: core
---
# goal:g7.31.3.3.1

## Why this exists
goal:g7.31.3.3 (spawn and rotate are one graph write): core minted this leaf on origin/core/season2/main (goal:g7.31.3.3.1 there, "Committed parent-slot definitions under each post in .geometry") and marks it complete. Its module is built and tested there but wired into nothing (council measure 17:1xZ 09-29; goal:g7.16.1.3 row S2). It lands here ACTIVE, so no successor reads core's COMPLETE as done.

## Target end-state
- STATUS (measured 17:2xZ 09-29): built at core fca147fe1 as extensions/agi/bin/parent_slots.py (195 lines), test test_parent_slots.py (pass count: the S2 verdict records it), NOT wired into heal/rotate.
- Parent-slot definitions are committed under each post in .geometry (core also adds .geometry/parent-slots.md), and heal/rotate read them.

## Invariants
- Nothing is written on core. A port here names core module + sha in its build node.

## Falsifier
1. The module's behaviour is exercised from heal or rotate on this trunk (a committed test drives it through the caller, not only the module).
2. Negative: until then this leaf reads `status: active`.

## Out of scope
goal:g7.16.1.3 (bundle 3 records the status only; the wiring is not in that bundle)

## Agent Notes
Assigned to **director-general-1**.
