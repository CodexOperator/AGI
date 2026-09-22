---
id: goal:g7.31.3.1
mint_id: 6e198db23b7e4f14b869c6ef13100e9a
type: goal
parents:
  - goal:g7.31.3
next_edges: []
confidence: 0.9
edited_by: owner-go
goal_id: G7.31.3.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 15398bdb0a820ecd
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
  - harness
  - grok-bot
  - routes
  - brief
thought_session: magic-pane-2026-09-21
title: "G7.31.3.1: Cold seat brief lists five pane-facing routes"
town: core
---
# goal:g7.31.3.1

## Why this exists

**Parent `goal:g7.31.3`.** Falsifiers on the parent were multi-headed. This leaf owns the **cold seat brief / custom-instruction surface** listing the five pane-facing routes by contract names (write / read / send / dispatch|workflow / rotate|spawn).

## Target end-state

- A cold seat brief or custom-instruction surface lists the five routes by the names in `goal:g7.31.3` table (or records a deliberate rename with old→new).
- Names are the contract; engine renames update the parent table + this falsifier in one edit.

## Invariants

- ONE workflow router (`goal:g1.14`).
- Routes are harness-agnostic at the engine boundary.
- Sample agent-action proof is OOS here (`goal:g7.31.3.2`).
- No sixth "special grok route" in `dispatch.py` / `rotate.py`.

## Falsifier

1. A cold seat brief / custom-instruction surface lists the five routes by the names in the `goal:g7.31.3` table (or records a deliberate rename with old→new). Grep/read proof on the brief artifact.

## Out of scope

- Running sample write+send+dispatch through CLIs (`goal:g7.31.3.2`).
- Durable pane hold (`goal:g7.31.1` family).
- SSH handbacks / profile sync (`.4` / `.5`).

## Agent Notes

Split from `goal:g7.31.3` by director-belam (point) 2026-09-21 ET — multi-headed falsifier. Via `goal:g7.26` / `goal:g7.27` surfaces, not a second path. Launch pi parent; diagram-max; batch-max; merge-up to Belam; blockers to owner only via director-belam.

**Related:** `doc:standing-llm-ops` §4, `goal:g7.26`, `goal:g7.27`, `goal:g7.31.3.2`.
