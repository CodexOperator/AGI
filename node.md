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
status: complete
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

**Parent `goal:g7.31.1`.** Falsifiers on the parent were multi-headed: measured CLI argv vs durable pane hold. This leaf owns **measured CLI** — `build_command` argv matches a recorded `grok-bot --help`, and stub-only guessed flags (e.g. lone `-p`) are gone from the landed adapter path on `core/season3/main`.

## Target end-state

- `adapters.load("grok_bot").build_command(...)` argv matches a pasted `--help` measurement recorded in this goal's child doc node `doc:grok-bot-help-measured`.
- Stub-only guessed flags are absent from the landed adapter path on `core/season3/main`.
- Measurement is CLI/grep-answerable, not vibes.

## Invariants

- Restart/pane hold is OOS here (`goal:g7.31.1.2`).
- No second argv path; seam stays `goal:g7.27` / `goal:g7.28`.
- Does not special-case the string `grok` inside `dispatch.py` / `rotate.py`.

## Falsifier

1. `adapters.load("grok_bot").build_command(...)` argv matches a pasted `--help` measurement recorded in this goal's child doc node `doc:grok-bot-help-measured`.
2. Stub-only guessed flags (e.g. lone `-p`) are gone from the landed adapter path on `core/season3/main` (grep/diff proof).

## Out of scope

- Durable named tmux pane restart/reattach (`goal:g7.31.1.2`).
- Pane ↔ post/pin wiring (`goal:g7.31.2`).
- Five unified routes (`goal:g7.31.3` family).

## Agent Notes

Split from `goal:g7.31.1` by director-belam (point) 2026-09-21 ET — multi-headed falsifier. Launch pi parent; diagram-max; batch-max; merge-up to Belam; blockers to owner only via director-belam.

**Related:** `goal:g7.25` family, `goal:g7.30`, `goal:g7.31.1.2`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-06 18:4xZ, director-general-1, CLOSE: status active -> complete. The build landed as L385 d5a6cba74b (gate tip 0768857d9e, council 3/3 plain, GATE515 green). ONE falsifier amend, WHERE only: the lead paragraph (Why this exists), Target end-state line 2 and Falsifier 2 named `core/season2/main`, the season-2 trunk this leaf was minted on (09-21). origin/core/season2/main is FROZEN at ccb285d98f (10-04) and still holds the old stub (`git grep` for the `-p` token there: 1 hit), and no land reaches it: since the season-3 move the town trunk, where L385 landed, is core/season3/main. Read as written, Falsifier 2 would FAIL forever on a trunk that never gets the build. (An earlier draft of this close said the ref did not exist; it does, at origin/: SM 18:47Z 11-06.) All three now name the live town trunk `core/season3/main`; the WHAT (no stub `-p` on the landed adapter path, grep proof) is unchanged. Falsifier 1 as written: test_every_argv_flag_is_declared_by_the_measured_help passes on the trunk plus this close's parent. Falsifier 2: `git grep` for the `-p` token in either quote form on core/season3/main's adapter path reads 0; the grep row (either form since the parent cut) passes. Not done here, a policy gap for the F2 LIVE GO: headless tool approval (--always-approve / --permission-mode). Previous version: in git history.
<!-- THOUGHT:END -->
