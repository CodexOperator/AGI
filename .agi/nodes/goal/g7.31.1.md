---
id: goal:g7.31.1
mint_id: ce4f8d0c8cf348faae0a35faf825c80f
type: goal
parents:
  - goal:g7.31
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.31.1
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 6999bdaf7388b52b
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
title: "G7.31.1: Measured CLI + durable named tmux pane hold (precursor to magic pane)"
town: core
---
# goal:g7.31.1

## Why this exists

**Parent `goal:g7.31`.** The practice stub argv (`<bin> [--model] -p <context>`) was never measured against real `grok-bot --help`. A seat that cannot **attach to a named tmux pane and hold it** has no spine for posts/pins/routes. Owner ask 2026-09-21 ET: measured CLI + durable pane hold — precursor to magic pane.

```
stub build_command ──X──▶ guessed flags
measured CLI       ──▶▶▶ named tmux pane (seat keeps)
restart            ──▶▶▶ re-attach same pane name
```

## Target end-state

- `grok_bot_adapter.build_command` argv matches measured `grok-bot --help` (not the practice stub alone).
- Adapter `restart` (or documented true impossibility) re-attaches to the **same named tmux pane** the seat keeps.
- Pane name is stable across adapter restarts; seat occupation is visible independently of process pid churn.
- This is the **precursor** to magic pane — durable hold first; magic UX later.

## Invariants

- One named pane per seat; no anonymous fire-and-forget for persistent grok seats.
- Restart goes through the same adapter/template seam as first spawn (`goal:g7.27` / `goal:g7.28`) — no second argv path.
- Does not special-case the string `grok` inside `dispatch.py` / `rotate.py`.

## Falsifier

1. `adapters.load("grok_bot").build_command(...)` argv matches a pasted `--help` measurement recorded on this node or a child experiment.
2. Kill the seat process; `restart` (or persistent-dispatch restart) reattaches to the **same** tmux pane name; `tmux list-panes` / capture shows the seat still there.
3. Stub-only guessed flags (e.g. lone `-p`) are gone from the landed adapter path on `core/season2/main`.

## Out of scope

- Magic-pane product chrome (later).
- Wiring pane ↔ post/pin/formation (that is `goal:g7.31.2`).
- The five unified routes catalog (`goal:g7.31.3`).

## Agent Notes

Assigned to **director-belam (point)** with umbrella + `.3`. May further split; launch pi parent batches; diagram-max; batch-max; merge-up to Belam; blockers to owner only.

**Related:** `goal:g7.25` family (REQUIRED surface), `goal:g7.30` (land adapter), `goal:g7.28` (persistent hold).
