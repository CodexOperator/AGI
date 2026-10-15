---
id: goal:g7.25.2
mint_id: c3627502e5a94465bff0a1234282bfda
type: goal
parents:
  - goal:g7.25
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.25.2
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: ed24707ae72a2f92
season: 2
seeds: []
status: complete
tags:
  - goal
  - subgoal
  - grok-bot
  - config
thought_session: close-g7252-satisfied-2026-09-21
title: "G7.25.2: harnesses.grok-bot config row only (no dispatch.py edit)"
town: core
---
# goal:g7.25.2

## Why this exists

**Parent `goal:g7.25`.** Without a `harnesses.grok-bot` row in `.agi/config.json`, `adapters.resolve(cfg, "grok-bot")` cannot return a config row even when `grok_bot_adapter.py` loads. This subgoal owns **the config row only**.

## Target end-state

`.agi/config.json` contains `harnesses.grok-bot` with `adapter: grok_bot`, kid/parent `models`, and `bin` (peer fields as peers). `adapters.resolve(cfg, "grok-bot")` succeeds. Zero `dispatch.py` edits. Zero adapter-file edits under this goal.

## Invariants

- Config row only — no `dispatch.py` / no adapter module edits attributed to this goal.
- No new remote heads from this goal's worktrees.
- Row shape matches other harnesses (adapter + models + bin).

## Falsifier

1. `harnesses.grok-bot` present on `core/season2/main`.
2. `adapters.load("grok_bot")` and `adapters.resolve(cfg, "grok-bot")` succeed.
3. `grep` `dispatch.py` for `grok` / `grok-bot` / `grok_bot`: zero special-case hits from this work.

## Out of scope

- Adapter module (`goal:g7.25.1`).
- Interface tests (`goal:g7.25.3`).
- Post template / land (`goal:g7.30`).
- Pane spine (`goal:g7.31`).

## Agent Notes

**CLOSED already-satisfied (Belam 2026-09-21).** Evidence on `core/season2/main`:
- config land `ca3b2da28` (helper corrective: harnesses.grok-bot)
- adapter build keep mint `93a56c11` via g7.25.1 land
- probe: `adapters.resolve` returns row with adapter/models/bin

Sibling tip `1e9e94b75` HOLD dropped — wrong mint (`a00b9f81` ≠ `93a56c11`); adapter-only, no config delta; MUR already `accept_with_residue`. Do **not** mint a fresh config-only corrective.
