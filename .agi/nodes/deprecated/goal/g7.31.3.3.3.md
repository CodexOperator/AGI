---
id: goal:g7.31.3.3.3
mint_id: 0d858dc22a26462bbf73f7887d5e2701
type: goal
parents:
  - goal:g7.31.3.3
next_edges: []
confidence: 0.85
edited_by: director-helper
goal_id: G7.31.3.3.3
goal_kind: subgoal
heading_level: 6
origin: goals-doc
scaffold_hash: e49946d754d35aba
season: 2
seeds: []
status: complete
tags:
  - goal
  - subgoal
  - engine
  - spawn
  - rotate
thought_session: helper-nopi-stopline12-20260928
title: "G7.31.3.3.3: AGI_BOX host-only loop acts and clears needs-rotate"
town: core
---
# goal:g7.31.3.3.3

## Why this exists

**Parent `goal:g7.31.3.3`.** Owner design: only the box hosting the post acts (checked via AGI_BOX); the loop clears `needs-rotate: true` after acting.

## Target end-state

- Loop/reaper acts on a row only when `AGI_BOX` matches the row's host.
- After a successful rotate/spawn action, `needs-rotate` is cleared by the same loop.

## Invariants

- Sibling slices under `goal:g7.31.3.3` own their own falsifiers — do not widen this leaf.
- Does not open `goal:g7.31.6` / `goal:g7.32.5` (board parked); stays under stop-line `g7.31.3`.

## Falsifier

1. Cross-box probe: non-matching AGI_BOX does not mutate the row; matching box clears `needs-rotate` after act.
2. Negative: no silent clear of `needs-rotate` without an action record.

## Out of scope

- Other `goal:g7.31.3.3.*` siblings.
- Messaging half of the same owner message (`goal:g7.32.5`, helper / parked).

## Agent Notes

Assigned to **director-belam**. Director-direct under OWNER FULL STOP (NO pi).

NO-PI stopline12: needs_rotate.py AGI_BOX host-only act+clear; test_needs_rotate 5/5; cross-box no-mutate; silent-clear refused

<!-- THOUGHT: season3 rollover: complete goal not carried into s3; builds reparented to umbrella. -->
