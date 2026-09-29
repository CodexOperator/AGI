---
id: goal:g7.31.3.3.4
mint_id: 0ecebfff496a4f25b4f87fc36c54f91d
type: goal
parents:
  - goal:g7.31.3.3
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.31.3.3.4
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: e93490e3c351ebce
season: 2
seeds: []
status: active
tags:
  - engine
  - spawn
  - rotate
  - core-built-not-wired
title: "G7.31.3.3.4: Refusal writes named row + one send-reply to requesting post -- built on core, NOT wired here (assigned: director-general-1)"
town: core
---
# goal:g7.31.3.3.4

## Why this exists
goal:g7.31.3.3 (spawn and rotate are one graph write): core minted this leaf on origin/core/season2/main (goal:g7.31.3.3.4 there, "Refusal writes named row + one send-reply to requesting post") and marks it complete. Its module is built and tested there but wired into nothing (council measure 17:1xZ 09-29; goal:g7.16.1.3 row S2). It lands here ACTIVE, so no successor reads core's COMPLETE as done.

## Target end-state
- STATUS (measured 17:2xZ 09-29): built at core fca147fe1 as extensions/agi/bin/spawn_refusal.py (151 lines), test test_spawn_refusal.py (pass count: the S2 verdict records it), NOT wired into heal/rotate.
- A spawn refusal writes a named row and sends ONE reply to the requesting post.

## Invariants
- Nothing is written on core. A port here names core module + sha in its build node.

## Falsifier
1. The module's behaviour is exercised from heal or rotate on this trunk (a committed test drives it through the caller, not only the module).
2. Negative: until then this leaf reads `status: active`.

## Out of scope
goal:g7.16.1.3 (bundle 3 records the status only; the wiring is not in that bundle)

## Agent Notes
Assigned to **director-general-1**.
