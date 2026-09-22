---
id: goal:g7.32.3
mint_id: 637c7ca04f464d38a6d241b8fe10c428
type: goal
parents:
  - goal:g7.32
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.32.3
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 986ff4e54a717896
season: 2
seeds: []
status: horizon
tags:
  - goal
  - subgoal
  - adapter
  - pane-methods
thought_session: owner-ask-2026-09-21
title: "G7.32.3: One adapter/harness with optional pane methods"
town: core
---
# goal:g7.32.3

## Why this exists

**Parent `goal:g7.32`.** Owner vision: **one adapter/harness** with **optional pane methods** — pane ops are methods on the same adapter object that already exposes `build_command` (g7.25), not a second parallel API.

## Target end-state

```
grok_bot_adapter
  required: build_command, …          (g7.25 family — done surface)
  optional: pane_attach / pane_send / pane_read / …
                 │
                 └── only if seat holds a named pane (g7.31.1)
```

- Callers feature-detect optional methods; absence ⇒ non-pane harness path.
- No second `grok_pane_adapter.py`.

## Invariants

- Required surface stays g7.25 — this goal adds **optional** methods only.
- Durable hold semantics stay g7.31.1 — methods wrap, do not re-own hold.
- Zero `grok` special-case in dispatch/rotate.

## Falsifier

1. Adapter module exposes optional pane methods behind a single interface; harnesses without panes omit them.
2. Unit test: calling optional method without a held pane fails closed with a named error (not hang).
3. `ls` / import graph: still one adapter module for grok-bot.

## Out of scope

- Messaging product semantics (g7.32.2).
- Session ingest (g7.32.1).
- Rewriting g7.25 REQUIRED stubs.

## Agent Notes

**Extends:** `goal:g7.25`, `goal:g7.31.1`. Session: `owner-ask-2026-09-21`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
standing body whole-replace owner-ask-2026-09-21
<!-- THOUGHT:END -->
