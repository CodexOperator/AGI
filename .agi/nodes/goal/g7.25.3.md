---
id: goal:g7.25.3
mint_id: 3314a71de2c349f28c1edffc5b7dc588
type: goal
parents:
  - goal:g7.25
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.25.3
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: f997b95365fae6da
season: 2
seeds: []
status: complete
tags:
  - goal
  - subgoal
  - grok-bot
  - tests
thought_session: close-g7253-satisfied-2026-09-21
title: "G7.25.3: mirror adapter interface tests for grok-bot"
town: core
---
# goal:g7.25.3

## Why this exists

**Parent `goal:g7.25` falsifier 4.** Adapter land without mirrored interface tests leaves regressions invisible. This subgoal owns `extensions/agi/tests/test_grok_bot_adapter.py` (and fixture-only helpers).

## Target end-state

A grok-bot adapter test module mirrors the existing adapter interface suite: `adapters.load` REQUIRED surface, `is_alive` True on current pid, `needs_credential` explicit False, `restart` callable, missing model tier raises KeyError (no silent fallback). Tests green on `core/season2/main`.

## Invariants

- Tests only — no `dispatch.py` special-case for `grok`.
- Mirror peer adapter test shapes; do not invent a second contract.
- No new remote heads from this goal's worktrees.

## Falsifier

1. `python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py` → all green on `core/season2/main`.
2. Coverage includes: load REQUIRED · `is_alive` · `needs_credential` explicit · `restart` callable · missing tier KeyError.
3. `grep` `dispatch.py` for `grok` / `grok-bot` / `grok_bot`: zero special-case hits from this work.

## Out of scope

- Adapter module (`goal:g7.25.1`) · config row (`goal:g7.25.2`).
- Post template / land (`goal:g7.30`) · pane spine (`goal:g7.31`).

## Agent Notes

**CLOSED already-satisfied (Belam 2026-09-21).** Evidence:
- tip `d99b0bb02` ⊆ `core/season2/main` (`c9287715f` at close)
- `pytest test_grok_bot_adapter.py` → **15/15 passed**
- config peer `ca3b2da28` (g7.25.2) · adapter peer via g7.25.1 land

No parent dispatch. Format repaired at close.
