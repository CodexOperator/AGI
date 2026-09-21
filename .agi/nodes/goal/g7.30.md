---
id: goal:g7.30
mint_id: 7717757b610e458f8a68902b18f74db2
type: goal
parents:
  - goal:g7
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.30
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 1d93355cd41ddb58
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
  - harness
  - grok-bot
  - adapter
thought_session: texas-two-step-belam-voice-2026-09-19
title: "G7.30: Land grok-bot adapter + post template on core/season2/main"
town: core
---
# goal:g7.30

## Why this exists

**Parent `goal:g7` (Sanctuary / seat lineage).** Practice adapter + config + tests live on loop tip `76d141786` (`goal:g7.25` family) but **not** on `core/season2/main`. Stub argv (`<bin> [--model] -p <context>`) was never measured against real `grok-bot --help`. Even after land, `rotate.py`'s allowlist would refuse a grok seat. Owner ask 2026-09-19 (voice): land the adapter on main, write its **post template**, and make a Grok Bot seat drop in with **no special-casing** once templates + shrink-rotate land.

## Target end-state

- `grok_bot_adapter.py` + `harnesses.grok-bot` + interface tests are on `core/season2/main`.
- **Prerequisite:** measure the real CLI — read `<bin> --help`, replace guessed `-p` flags; implement `restart` (or document true impossibility).
- A **post template** for grok-bot exists (via `goal:g7.27` format) so seating uses the same path as Claude/copilot.
- A grok-bot seat drops in automatically once this + `goal:g7.27`/`goal:g7.29` land — **no** rotate/dispatch special-case for the string `grok-bot`.

## Invariants

- No edit to `dispatch.py` that names `grok` (same falsifier as `goal:g7.25`).
- No new `_KNOWN_HARNESSES` entry — rotate must already be harness-blind (`goal:g7.29`) or this goal waits on it.
- Chain growth for directors still uses pi parents via dispatch (operating note from `goal:g7.25`); this goal is **seat** land, not replacing OpenRouter parents.

## Falsifier

1. On `core/season2/main`: `adapters.load("grok_bot")` succeeds; `adapters.resolve(cfg, "grok-bot")` returns the config row.
2. `build_command` argv matches measured `--help` (not the practice stub alone); `restart` is callable without "unmeasured" refusal **or** a node documents why NotImplementedError remains.
3. `rotate.py` / `dispatch.py` grep for `grok` / `grok-bot` / `grok_bot` outside comments: **zero** special-case hits.
4. One dry-run (or live probe) seats grok-bot through the unified template + persistent dispatch path.

## Out of scope

- Same-harness workflow / SendToAgent handback (still deferred from `goal:g7.25`).
- Full sanctuary migration of every town onto Grok Bot.

## Agent Notes

Assigned to **director-helper**. Point director-belam stays on current batch — do not interrupt.
Prerequisite: measure real CLI. Soft-depends on `goal:g7.27` (template) and `goal:g7.29` (harness-blind rotate) for the "no special-case seat" claim; adapter+config land can proceed earlier.
