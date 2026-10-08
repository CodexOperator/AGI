---
id: goal:g7.31.1.2
mint_id: fb589b44ed9f46eaa6c0b4c4323bba0f
type: goal
parents:
  - goal:g7.31.1
next_edges: []
confidence: 0.9
edited_by: director-belam
goal_id: G7.31.1.2
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 67eb4b9e47d1ff69
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
  - harness
  - grok-bot
  - adapter
  - tmux
  - pane
thought_session: magic-pane-2026-09-21
title: "G7.31.1.2: Durable named tmux pane restart/reattach hold"
town: core
---
# goal:g7.31.1.2

## Why this exists

**Parent `goal:g7.31.1`.** Falsifiers on the parent were multi-headed. This leaf owns **durable named tmux pane hold** — kill the seat process; `restart` (or persistent-dispatch restart) reattaches to the **same** tmux pane name the seat keeps.

## Target end-state

- Adapter `restart` (or documented true impossibility) re-attaches to the same named tmux pane.
- Pane name is stable across adapter restarts; seat occupation is visible independently of process pid churn.
- Precursor to magic pane — durable hold first; magic UX later.

## Invariants

- One named pane per seat; no anonymous fire-and-forget for persistent grok seats.
- Restart goes through the same adapter/template seam as first spawn (`goal:g7.27` / `goal:g7.28`).
- Measured CLI argv shape is OOS here (`goal:g7.31.1.1`).
- Does not special-case `grok` inside `dispatch.py` / `rotate.py`.

## Falsifier

1. Kill the seat process; `restart` (or persistent-dispatch restart) reattaches to the **same** tmux pane name; `tmux list-panes` / capture shows the seat still there.

## Out of scope

- Measuring CLI flags / retiring stub argv (`goal:g7.31.1.1`).
- Magic-pane product chrome.
- Pane ↔ post/pin (`goal:g7.31.2`).

## Agent Notes

Split from `goal:g7.31.1` by director-belam (point) 2026-09-21 ET — multi-headed falsifier. Launch pi parent; diagram-max; batch-max; merge-up to Belam; blockers to owner only via director-belam.

**Related:** `goal:g7.28`, `goal:g7.31.1.1`.
