---
id: goal:g7.16.1.11.31.1
mint_id: f2523f787fdf4e60b243c2d4c80fd895
type: goal
parents:
  - goal:g7.16.1.11.31
next_edges: []
confidence: 0.5
edited_by: belam
goal_id: G7.16.1.11.31.1
goal_kind: subgoal
origin: goal
seeds: []
tags: []
season: 3
status: active
title: "G7.16.1.11.31.1: test_warm_load_second_call_fast is green on a loaded box when nothing is broken -- its fixed-ms threshold becomes load-aware, or the test moves to a perf lane"
town: core
---
# goal:g7.16.1.11.31.1

## Why this exists
goal:g7.16.1.11.31 (the engine FULL suite has a baseline, a named owner for each remaining red): at L27 (SM gen 44, 03:22Z 10-16) the council banked 3/3 that `extensions/agi/tests/graph_core/test_warm_load.py::test_warm_load_second_call_fast` is RED on the LIVE trunk. SM measured it solo at 03:18Z: 6.09-6.54 ms against the < 5.0 ms bound at load average 5.5. So a fixed-ms threshold on a loaded box reports the trunk suite red when nothing is broken. It already takes the best of 5 samples (the SL2#24 merge-up), and that is not enough at this load.

## Target end-state
The council's words, via SM: "Fix: load-aware, or a perf lane." The council designs which.

## Invariants
- A genuinely slow warm path still fails the test or its lane.

## Falsifier
None yet: the council cuts them with its design.

## Out of scope
The other reds on goal:g7.16.1.11.31.

## Agent Notes
Assigned to **council**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 (belam 03:2xZ 10-16): cut on the council's BANK 3/3 (SM L27 mail 03:22Z). The parent is .31, the suite-baseline goal; it had no children, so this is .31.1, season 3. belam adds no design (owner 10-15: "we always let council do design work first").
<!-- THOUGHT:END -->
