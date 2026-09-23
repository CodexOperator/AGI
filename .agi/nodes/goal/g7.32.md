---
id: goal:g7.32
mint_id: d58cac000537400591ac74935db9da55
type: goal
parents:
  - goal:g7
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.32
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 93fa8e801200a683
season: 2
seeds:
  - goal:g7.32.1
  - goal:g7.32.2
  - goal:g7.32.3
  - goal:g7.32.4
status: active
tags:
  - goal
  - subgoal
  - messaging
  - session-ingest
  - magic-pane
  - send-router
thought_session: belam-status-hygiene-sot-2026-09-22
title: "G7.32: Session ingest + magic-pane messaging + adapter pane methods + send.py thin router"
town: core
---
# goal:g7.32

## Why this exists

**Sibling of `goal:g7.31`, parent `goal:g7`.** Owner ask 2026-09-21 ET + director-belam tie-break: `g7.31` already has **live nesting** (`.1`–`.5`, `.1.1`/`.1.2`, `.3.1`/`.3.2`) and WIP tips — **do not re-nest or rewrite the g7.31 umbrella**. New surface intent lands here at the **same level**:

```
goal:g7
├─ g7.25–g7.30   adapter land + harness prereqs (Related)
├─ g7.31 ★       pane = seat spine (UNTOUCHED this ask)
│  └─ .1–.5 …
└─ g7.32 ★       THIS — messaging / session-ingest / pane methods / send router
   ├─ .1 session ingest
   ├─ .2 magic-pane messaging
   ├─ .3 optional pane methods on one adapter
   └─ .4 send.py thin router
```

Owner vision covered (no duplicate of g7.31.1–.5 meanings):
- grok **session ingest**
- **magic-pane messaging** (grok↔grok native; grok→claude/pi nudge→send)
- **one adapter/harness** with optional pane methods
- **send.py** thin router

## Target end-state

```
 sessions/ ──ingest──▶ graph nodes          (g7.32.1)
 grok pane ◄──native──▶ grok pane           (g7.32.2)
 grok pane ──nudge──▶ send.py ──▶ claude/pi (g7.32.2 + .4)
 grok_bot_adapter.{build_command, pane?}    (g7.32.3)
 send.py = thin transport router only       (g7.32.4)
```

- g7.31 owns durable pane hold + five engine routes + handbacks + doc sync.
- g7.32 owns what travels **on** that spine once the pane exists: ingest, messaging, method surface, routing.

## Invariants

- Never reparent or rewrite `goal:g7.31` tree for these intents.
- No duplicate of g7.31.1 (CLI+hold), .2 (occupation), .3 (five routes), .4 (handbacks), .5 (doc sync) — **link Related**.
- `dispatch.py` / `rotate.py` still gain **zero** harness-name special-case for `grok`.
- send.py stays thin: choose transport, never policy/formation.

## Falsifier

1. Five nodes on `origin/core/season2/main`: `goal:g7.32` + `.1`–`.4`, standing bodies (Why→…→Agent Notes).
2. `goal:g7.31` file SHA / body unchanged by this ask except optional town Agent Notes elsewhere.
3. Grep: no new `grok` special-case in `dispatch.py`/`rotate.py` from this family.

## Out of scope

- Re-nesting under g7.31; rewriting g7.31 umbrella.
- Landing adapter itself (g7.25/g7.30) or durable pane hold (g7.31.1).
- Pushing `core/main` (Belam/Prime only — this ask's merge is Belam-led).

## Agent Notes

| id | intent | extends (not duplicates) |
|---|---|---|
| g7.32.1 | session ingest | — |
| g7.32.2 | magic-pane messaging | g7.31.1 precursor pane |
| g7.32.3 | optional pane methods | g7.25 adapter surface + g7.31.1 |
| g7.32.4 | send.py thin router | g7.31.3 send route |

**Related:** `goal:g7.25`–`goal:g7.31` family. **Town:** `town:core` (encryption-town host; no separate encryption town node).

Session: `owner-ask-2026-09-21`. Frame as TARGETS not tasks.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
horizon-pass not in-flight unclaimed on board
<!-- THOUGHT:END -->
