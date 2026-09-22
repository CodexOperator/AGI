---
id: goal:g7.31.4
mint_id: 911a41deef2d487ba4188c10c183aeec
type: goal
parents:
  - goal:g7.31
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.31.4
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: a8d684b726c362da
season: 2
seeds: []
status: horizon
tags:
  - goal
  - subgoal
  - harness
  - grok-bot
  - send
  - handback
  - mesh
thought_session: belam-horizon-4b-2026-09-21
title: "G7.31.4: Native handbacks SSH-or-not — same function surface; engine fills mesh gaps"
town: core
---
# goal:g7.31.4

## Why this exists

**Parent `goal:g7.31`.** Messaging initiated in the grok pane must use **native harness messaging**; other posts get a small nudge in their panes; some seats are on the SSH mesh and some are not — the engine fills gaps. Owner ask 2026-09-21 ET: **same function surface either way** (SSH-or-not).

```
initiator (grok pane)
   │ native harness message
   ▼
peer post(s)
   │ small nudge in THEIR pane
   ▼
engine gap-fill
   ├─ same-host / SSH-mesh seats
   └─ non-mesh seats
        same send/read/nudge function surface
```

## Target end-state

- Pane-initiated messaging uses the harness-native channel when available (Grok Bot SendToAgent / owner chat path converging on `send.py` as the one seam — see standing-llm-ops §4 send).
- Recipients always get a **small nudge** in their own pane (wake token), not a pasted body dump.
- Mixed topology (some seats SSH-mesh, some not) still exposes one function surface; engine fills transport gaps without a second API.
- No daemon required for messages (standing L4 ruling: repo + nudge, not a router process).

## Invariants

- Wake token ≠ message body (send.py nudge contract).
- Authority / identity verified against the graph (`config:seats`), never against the pane string alone.
- Same caller-facing functions whether peer is mesh-reachable or local.

## Falsifier

1. From a grok pane: one outbound message lands in recipient inbox **and** a nudge appears in the recipient pane (capture or send.py proof).
2. Repeat with one peer on SSH-mesh and one not (or a documented dry-run of both transports): **same** function names/args succeed; no caller branch on "is_ssh".
3. No new message daemon process appears in the heal/cron surface for this goal.

## Out of scope

- Building the durable pane itself (`goal:g7.31.1`).
- Five-route catalog (`goal:g7.31.3`).
- Graph↔profile doc sync (`goal:g7.31.5`).
- Full sanctuary migration of every town onto Grok Bot.

## Agent Notes

Assigned to **director-helper** with `.2` + `.5` AND keep `g7.26`–`g7.30` land batch. May further split; launch pi parent batches; diagram-max; batch-max; merge-up to Belam; blockers to owner only.

**Related:** `goal:g7.25` (deferred same-harness handback), `send.py`, mesh commands in `command:commands`, `doc:standing-llm-ops` §4 send.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
horizon-pass not in-flight unclaimed on board
<!-- THOUGHT:END -->
