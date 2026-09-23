---
id: goal:g7.31.3.2
mint_id: 5d8e1944a727494ba10f7aa37cd62cf8
type: goal
parents:
  - goal:g7.31.3
next_edges: []
confidence: 0.9
edited_by: director-belam
goal_id: G7.31.3.2
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: f4e3664c7088b5f6
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
  - harness
  - grok-bot
  - routes
  - write
  - send
  - dispatch
thought_session: magic-pane-2026-09-21
title: "G7.31.3.2: Sample write+send+dispatch through named CLIs"
town: core
---
# goal:g7.31.3.2

## Why this exists

**Parent `goal:g7.31.3`.** Falsifiers on the parent were multi-headed. This leaf owns **sample agent action** for write + send + one dispatch/workflow run going through the named CLIs (`write.py` / `send.py` / `dispatch.py`+`workflow.py`), not a parallel script.

## Target end-state

- Sample agent action for write + send + one dispatch/workflow run goes through the named CLIs.
- Evidence is a recorded transcript / experiment with command lines cited — not a vibes claim.

## Invariants

- ONE workflow router (`goal:g1.14`).
- Message bodies are files/stdin, never backtick-laden argv (L4 message ruling).
- Brief listing of the five names is OOS here (`goal:g7.31.3.1`).
- No sixth "special grok route" in `dispatch.py` / `rotate.py`.

## Falsifier

1. Sample agent action for write + send + one dispatch/workflow run goes through the named CLIs, not a parallel script (transcript/experiment proof).

## Out of scope

- Authoring the cold brief list (`goal:g7.31.3.1`).
- Durable pane hold / pin wiring / handbacks / doc sync.

## Agent Notes

Split from `goal:g7.31.3` by director-belam (point) 2026-09-21 ET — multi-headed falsifier. Launch pi parent; diagram-max; batch-max; merge-up to Belam; blockers to owner only via director-belam.

**Related:** `goal:g1.14`, `command:commands`, `goal:g7.31.3.1`.
