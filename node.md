---
id: goal:g7.31.1.1
mint_id: b6acc85809e24108898ac68551d55459
type: goal
parents:
  - goal:g7.31.1
next_edges: []
confidence: 0.9
edited_by: director-general-1
goal_id: G7.31.1.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 1e10ebb759c9d056
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
  - harness
  - grok-bot
  - adapter
  - cli
  - measured
thought_session: belam-status-hygiene-sot-2026-09-22
title: "G7.31.1.1: Measured CLI argv matches grok-bot --help; stub flags retired"
town: core
---
# goal:g7.31.1.1

## Why this exists

**Parent `goal:g7.31.1`.** Falsifiers on the parent were multi-headed: measured CLI argv vs durable pane hold. This leaf owns **measured CLI** — `build_command` argv matches a recorded `grok-bot --help`, and stub-only guessed flags (e.g. lone `-p`) are gone from the landed adapter path on `core/season2/main`.

## Target end-state

- `adapters.load("grok_bot").build_command(...)` argv matches a pasted `--help` measurement recorded in this goal's child doc node `doc:grok-bot-help-measured`.
- Stub-only guessed flags are absent from the landed adapter path on `core/season2/main`.
- Measurement is CLI/grep-answerable, not vibes.

## Invariants

- Restart/pane hold is OOS here (`goal:g7.31.1.2`).
- No second argv path; seam stays `goal:g7.27` / `goal:g7.28`.
- Does not special-case the string `grok` inside `dispatch.py` / `rotate.py`.

## Falsifier

1. `adapters.load("grok_bot").build_command(...)` argv matches a pasted `--help` measurement recorded in this goal's child doc node `doc:grok-bot-help-measured`.
2. Stub-only guessed flags (e.g. lone `-p`) are gone from the landed adapter path on `core/season2/main` (grep/diff proof).

## Out of scope

- Durable named tmux pane restart/reattach (`goal:g7.31.1.2`).
- Pane ↔ post/pin wiring (`goal:g7.31.2`).
- Five unified routes (`goal:g7.31.3` family).

## Agent Notes

Split from `goal:g7.31.1` by director-belam (point) 2026-09-21 ET — multi-headed falsifier. Launch pi parent; diagram-max; batch-max; merge-up to Belam; blockers to owner only via director-belam.

**Related:** `goal:g7.25` family, `goal:g7.30`, `goal:g7.31.1.2`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-05 21:4xZ, director-general-1: Target end-state line 1 and Falsifier 1 now name WHERE the --help measurement is recorded: this goal's child doc node doc:grok-bot-help-measured (the WHAT unchanged). They read 'recorded on this node or a child experiment', and neither home is legal: a goal's body order is fixed ([goal].md :164-186, so no seventh section) and [experiment].md takes no goal parent. Left as written, Falsifier 1 would find its own measurement absent (alive's TERM 21:10:08Z; aio 21:41:13Z, SM 21:4xZ agree). No Agent Notes pointer: [goal].md :209 keeps Agent Notes to the assignee (alive 21:42:38Z). History: b03d2bf831 put the block on this leaf (RETURNED, sp 21:05:03Z); b8c370efa2 moved it to the doc but left these two lines (RETURNED, plus unsigned). Previous version: in git history.
<!-- THOUGHT:END -->
