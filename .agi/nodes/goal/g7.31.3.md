---
id: goal:g7.31.3
mint_id: c9aad9d7d8804a478a0325d0990e6c4f
type: goal
parents:
  - goal:g7.31
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.31.3
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: f3e486a8b7f08b2f
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
  - rotate
thought_session: magic-pane-2026-09-21
title: "G7.31.3: Five unified engine routes through the pane (write/read/send/dispatch|workflow/rotate|spawn)"
town: core
---
# goal:g7.31.3

## Why this exists

**Parent `goal:g7.31`.** Owner ask 2026-09-21 ET: ~five unified engine routes through the pane; all agent action prefers these over raw tools. Confirmed against live engine (2026-09-21) + `doc:standing-llm-ops` §4 + L4 ONE-workflow router (`goal:g1.14`) + message/nudge path (`send.py`):

| # | Route (pane-facing) | Engine seam | Notes |
|---|---------------------|-------------|-------|
| 1 | **write** | `write.py` | mutate graph; also `commands.md` `write` under workflow `see` |
| 2 | **read** | `commands.py` list/show/run + viewport `see`/`read` workflows | inspect; not a separate `read.py` |
| 3 | **send** | `send.py` | dm / audience / nudge; L4 message path (wake token ≠ body) |
| 4 | **dispatch \| workflow** | `dispatch.py` + `workflow.py` | ONE workflow router (`goal:g1.14`); stages as kids |
| 5 | **rotate \| spawn** | `rotate.py` | spawn / rotate-self / auto-rotation orchestration |

```
pane
 ├─ write     → write.py
 ├─ read      → commands.py / viewport
 ├─ send      → send.py
 ├─ dispatch  → dispatch.py ─┬─ workflow.py (ONE router)
 └─ rotate    → rotate.py    └─ spawn / rotate-self
```

Historical L4 owner language named **three** (viewing / writing / dispatching). Standing-llm-ops §4 expands operator surface to write / read / send + chain-growth. **This goal names the five pane-facing seams above** — adjust only if a measured engine rename lands; document the five you found (these).

## Target end-state

- Grok-bot seat (and eventually every seat) prefers these five routes for agent action; raw tool sprawl is the exception, named when used.
- Pane exposes or documents how each route is invoked from the held CLI session (custom instructions / post brief / template — via `goal:g7.26` / `goal:g7.27`, not a second path).
- Names above are the contract; if engine vocabulary shifts, update this node's table and falsifiers in one edit.

## Invariants

- ONE workflow router — no parallel ad-hoc workflow invokers (`goal:g1.14`).
- Message bodies are files/stdin, never backtick-laden argv (L4 message ruling).
- Routes are harness-agnostic at the engine boundary; grok-bot is one adapter behind them.

## Falsifier

1. A cold seat brief / custom-instruction surface lists the five routes by the names in the table (or records a deliberate rename with old→new).
2. Sample agent action for write + send + one dispatch/workflow run goes through the named CLIs, not a parallel script.
3. No sixth "special grok route" appears in `dispatch.py` / `rotate.py`.

## Out of scope

- Implementing durable pane hold (`goal:g7.31.1`) or pin wiring (`goal:g7.31.2`).
- SSH-or-not handback transport (`goal:g7.31.4`).
- Profile/doc sync (`goal:g7.31.5`).

## Agent Notes

Assigned to **director-belam (point)** with umbrella + `.1`. May further split; launch pi parent batches; diagram-max; batch-max; merge-up to Belam; blockers to owner only.

**Related:** `doc:standing-llm-ops` §4, `goal:g1.14`, `command:commands`, `goal:g7.26`, `goal:g7.27`.
