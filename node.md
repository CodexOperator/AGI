---
id: goal:g7.31.1.1.2
mint_id: ff11516fc67b45dbb4209cb967ec2280
type: goal
parents:
  - goal:g7.31.1.1
next_edges: []
confidence: 0.85
edited_by: director-belam
goal_id: G7.31.1.1.2
goal_kind: subgoal
heading_level: 6
origin: goals-doc
scaffold_hash: 8b6fc53cd4f6547e
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
  - harness
  - grok-bot
  - cli
  - measured
thought_session: belam-stop-line-nopi-20260928
title: "G7.31.1.1.2: Retire stub build_command flags to match recorded help"
town: core
---
# goal:g7.31.1.1.2

## Why this exists

**Parent `goal:g7.31.1.1`.** After measurement lands (`goal:g7.31.1.1.1`), `build_command` must emit argv that matches it and drop stub-only guessed flags (today: lone `-p` copilot spelling called out in adapter docstring).

## Target end-state

- `adapters.load("grok_bot").build_command(...)` argv matches the recorded measurement.
- Stub-only guessed flags absent from landed adapter path on `core/season2/main` (grep/diff proof).

## Invariants

- Measurement paste is prerequisite OOS on sibling `.1`.
- No second argv path; seam stays adapter `build_command`.

## Falsifier

1. Diff/grep on tip: emitted argv ⊆ measured flags; stub-only `-p` (or whatever measurement retires) gone if help forbids it.
2. Negative: docstring must not still claim "flag SHAPE is still a stub" once this leaf is complete.

## Out of scope

- `goal:g7.31.1.1.1` measurement record.
- Durable pane (`goal:g7.31.1.2`).

## Agent Notes

Assigned to **director-belam**. Director-direct under OWNER FULL STOP (NO pi).
