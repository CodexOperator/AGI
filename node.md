---
id: goal:g7.25
mint_id: 3a7b92ce2fbe4623aecf159b072750b4
type: goal
parents:
  - goal:g7
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.25
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 0fda225eb2dba49a
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
  - harness
  - grok-bot
  - adapter
thought_session: g1-g7-rewrite-2026-09-19
title: "G7.25: Grok Bot is a third-party harness adapter with the same hooks as pi and Claude Code"
---
<!-- BODY:BEGIN -->
# goal:g7.25

## Why this exists

**Parent `goal:g17` (the seat system).** Seats declare harness per role. Without a `grok-bot` adapter file, a seat row that names `harness: grok-bot` cannot be loaded through `adapters.load` / `adapters.resolve`, so seating on Grok Bot is config theater. This sub-goal is the missing adapter — **parity with what `pi_adapter`, `claude_code_adapter`, and `copilot_cli_adapter` already do today**, nothing more.

**Practice-run scope (owner 2026-09-19).** Tiny on purpose so Belam and a director can walk a level-1 graph modification loop (hypothesis → experiment → verdict) and feel the graph. Same-harness workflow/message handback, cross-machine messaging, and finishing `goal:g1.14` / `goal:g1.15` are **later** — not falsifiers here.

## Target end-state

`grok-bot` is a named harness behind one adapter module that answers the **exact same five questions** every shipped adapter answers (`adapters.REQUIRED` + the g4.7 restart contract):

1. `build_command(...)` → argv that starts one agent
2. `child_env(...)` → environment that argv runs in
3. `is_alive(pid)` → whether the process is still running
4. `restart(...)` → re-spawn; return new pid (or raise `NotImplementedError` only if the harness truly cannot — pi and Claude Code both restart)
5. `needs_credential(harness)` → whether dispatch should mint an OpenRouter-style per-spawn key

Plus the ordinary helpers the others carry where they apply: `NAME`, `resolve_bin`, `model_args` (tier missing from a declared `models` block errors by name, never silent fallback).

Adding it is **one** `harnesses.grok-bot` config entry + **one** `bin/adapters/grok_bot_adapter.py`. `dispatch.py` is not edited. The third-harness falsifier of `goal:g4.6` / the copilot claim holds again for a fourth name.

**What directors do with it (operating note, not a build clause):** seats on grok-bot still grow chains by `dispatch.py` spawning **pi parents** (OpenRouter). The adapter lets a grok-bot *seat* exist; it does not replace pi as the chain-growth harness. Directors use unified dispatch + unified workflow for round review — that is why they are directors.

## Invariants

- A harness is an adapter named in config; never a town; never a fork of read/write/dispatch/workflow/send.
- `adapters.load("grok_bot")` succeeds and the module defines every name in `adapters.REQUIRED`.
- No edit to `dispatch.py` to teach it about grok-bot.
- No new remote git heads.
- Chain growth stays on pi parents via dispatch; grok-bot adapter parity does not move token-heavy parent/kid work off OpenRouter.

## Falsifier

1. Drop in `grok_bot_adapter.py` + a `harnesses.grok-bot` row. `python -c 'import adapters; adapters.load("grok_bot")'` succeeds; missing any `REQUIRED` name fails at load with the existing `AdapterError` shape.
2. `adapters.resolve(cfg, "grok-bot")` returns the config row with `adapter` defaulting as the other harnesses do. Spawn argv for kid and parent tiers comes only from `build_command` — no shared-path branch on the string `grok-bot`.
3. `grep` `dispatch.py` for `grok` / `grok-bot` / `grok_bot` after the change: **zero** hits outside comments that already discuss harnesses in the abstract (ideally zero absolute). If a hit appears, the seam is in the wrong place.
4. Mirror the existing adapter tests: `is_alive` on the current pid is True; `needs_credential` is explicit True/False (not an AttributeError); `restart` is callable.

## Out of scope (explicit — next steps, not this goal)

- Same-harness workflow handback (Claude Code already has a seam; generalize later).
- Same-harness message handback / native `SendToAgent` re-route.
- Updates to pi / Claude Code / copilot adapters.
- Full sanctuary seating of every town on Grok Bot.
- Cross-machine mesh messaging.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Tightened 2026-09-19 by interim Belam after owner chose practice-run scope: match today's adapter surface only. Handback vision deferred. Directors still dispatch pi parents for chain growth.
<!-- THOUGHT:END -->
