---
id: goal:g7.32.1
mint_id: e2c0919696d749889a42216f10888d49
type: goal
parents:
  - goal:g7.32
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.32.1
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 5e06ad0f4163378e
season: 2
seeds: []
status: horizon
tags:
  - goal
  - subgoal
  - session-ingest
  - grok-bot
thought_session: owner-ask-2026-09-21
title: "G7.32.1: Grok session ingest — sessions land as graph nodes"
town: core
---
# goal:g7.32.1

## Why this exists

**Parent `goal:g7.32`.** Owner vision: **grok session ingest** — a completed (or checkpointed) Grok Bot session must land as graph-addressable residue, not a stranded transcript under `sessions/`.

g7.31 owns the pane spine; this child owns the **ingest pipe** from session artifacts → nodes.

## Target end-state

```
grok session artifact
        │ ingest
        ▼
 hypothesis / experiment / note  (minted, linked, town:core)
        │
        └── seed/parent edges back to the seat's live goal
```

- One ingest path; idempotent on re-run (same session → same mint or explicit supersession).
- Directors can point a batch at "ingest last N grok sessions" without hand-copy.

## Invariants

- Does not replace g7.31.5 (graph↔harness-doc sync) — ingest is session→graph, not profile sync.
- No silent drop: every ingest writes a measurable node id or a refused reason.
- Actor/provenance preserved (`edited_by`, `thought_session`).

## Falsifier

1. CLI/script: given a fixture grok session, produces ≥1 new graph node id on stdout and a file under `.agi/nodes/`.
2. Re-ingest of the same fixture does not fork duplicate mint_ids (or records an explicit supersession edge).

## Out of scope

- Magic-pane messaging (g7.32.2); send routing (g7.32.4).
- Durable pane hold (g7.31.1).

## Agent Notes

**Related:** `goal:g7.32`, `goal:g7.31.5` (sync, not ingest). Session: `owner-ask-2026-09-21`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
standing body whole-replace owner-ask-2026-09-21
<!-- THOUGHT:END -->
