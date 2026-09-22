---
id: goal:g7.31.1.1
mint_id: b6acc85809e24108898ac68551d55459
type: goal
parents:
  - goal:g7.31.1
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.31.1.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 1e10ebb759c9d056
season: 2
seeds: []
status: horizon
tags:
  - goal
  - subgoal
  - harness
  - grok-bot
  - adapter
  - cli
  - measured
thought_session: belam-horizon-4b-2026-09-21
title: "G7.31.1.1: Measured CLI argv matches grok-bot --help; stub flags retired"
town: core
---
# goal:g7.31.1.1

## Why this exists

**Parent `goal:g7.31.1`.** Falsifiers on the parent were multi-headed: measured CLI argv vs durable pane hold. This leaf owns **measured CLI** — `build_command` argv matches a recorded `grok-bot --help`, and stub-only guessed flags (e.g. lone `-p`) are gone from the landed adapter path on `core/season2/main`.

## Target end-state

- `adapters.load("grok_bot").build_command(...)` argv matches a pasted `--help` measurement recorded on this node or a child experiment.
- Stub-only guessed flags are absent from the landed adapter path on `core/season2/main`.
- Measurement is CLI/grep-answerable, not vibes.

## Invariants

- Restart/pane hold is OOS here (`goal:g7.31.1.2`).
- No second argv path; seam stays `goal:g7.27` / `goal:g7.28`.
- Does not special-case the string `grok` inside `dispatch.py` / `rotate.py`.

## Falsifier

1. `adapters.load("grok_bot").build_command(...)` argv matches a pasted `--help` measurement recorded on this node or a child experiment.
2. Stub-only guessed flags (e.g. lone `-p`) are gone from the landed adapter path on `core/season2/main` (grep/diff proof).

## Out of scope

- Durable named tmux pane restart/reattach (`goal:g7.31.1.2`).
- Pane ↔ post/pin wiring (`goal:g7.31.2`).
- Five unified routes (`goal:g7.31.3` family).

## Agent Notes

Split from `goal:g7.31.1` by director-belam (point) 2026-09-21 ET — multi-headed falsifier. Launch pi parent; diagram-max; batch-max; merge-up to Belam; blockers to owner only via director-belam.

**Related:** `goal:g7.25` family, `goal:g7.30`, `goal:g7.31.1.2`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
horizon-pass not in-flight unclaimed on board
<!-- THOUGHT:END -->
