---
id: goal:g7.29
mint_id: a2e875f4d95b4ff8b67fa89843d0d961
type: goal
parents:
  - goal:g7
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.29
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 33a6961718b2c8b8
season: 2
seeds: []
status: horizon
tags:
  - goal
  - subgoal
  - rotate
  - orchestration
thought_session: texas-two-step-belam-voice-2026-09-19
title: "G7.29: Shrink rotate.py to pure orchestration (no harness argv)"
town: core
---
# goal:g7.29

## Why this exists

**Parent `goal:g7` (Sanctuary / seat lineage).** `rotate.py` today both orchestrates (population, panes, succession) **and** builds harness argv (`_KNOWN_HARNESSES`, `_build_harness_command`, `_build_claude_command`, `_build_copilot_command`). That is why a landed `grok_bot_adapter` still cannot seat in the combined Teamux pane without special-casing. Owner ask 2026-09-19 (voice): shrink rotate to **pure orchestration**.

## Target end-state

- `rotate.py` decides the population, lays out the panes, and hands each **seat spec** to `dispatch` with the right **template**.
- Remove `_KNOWN_HARNESSES` and the inline `_build_harness_command` / `_build_copilot_command` / `_build_claude_command` argv builders.
- Rotate has **no harness knowledge** and **no argv construction**.

## Invariants

- Depends on `goal:g7.27` (templates) and `goal:g7.28` (persistent dispatch) — do not strip builders until dispatch can hold seats.
- Existing claude-code and copilot-cli seats still spawn after the shrink (measured dry-run / one live seat probe).
- Grep of `rotate.py` for harness flag construction (`--append-system-prompt`, `--allow-all`, `claude --remote-control`, etc.) is empty outside comments pointing at templates.

## Falsifier

1. `_KNOWN_HARNESSES` and `_build_*_command` are gone from `rotate.py`.
2. `rotate.py spawn` / seat window path calls persistent dispatch + template only.
3. Claude and copilot seats still come up; a third harness needs only template (+ thin hook), not a rotate edit.

## Out of scope

- Authoring the template format itself (`goal:g7.27`).
- Implementing persistent watch (`goal:g7.28`).
- Grok-specific land (`goal:g7.30`) — but this goal **unblocks** it.

## Agent Notes

Assigned to **director-helper**. Point director-belam stays on current batch — do not interrupt.
Consumes `goal:g7.27` + `goal:g7.28`.
