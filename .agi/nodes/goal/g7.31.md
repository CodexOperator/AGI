---
id: goal:g7.31
mint_id: 95e3e8e928ff4c3db800f0af311d5346
type: goal
parents:
  - goal:g7
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.31
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 38b1b910616ff3c3
season: 2
seeds:
  - goal:g7.31.1
  - goal:g7.31.2
  - goal:g7.31.3
  - goal:g7.31.4
  - goal:g7.31.5
status: active
tags:
  - goal
  - subgoal
  - harness
  - grok-bot
  - adapter
  - magic-pane
  - spine
thought_session: magic-pane-2026-09-21
title: "G7.31: Grok-bot adapter holds a tmux/CLI pane that is the seat's spine into posts, pins, formation, auto-rotation, and the unified engine routes"
town: core
---
# goal:g7.31

## Why this exists

**Parent `goal:g7` (Sanctuary / seat lineage).** Owner ask 2026-09-21 ET: long-horizon **perfect grok-bot integration** — the adapter must hold a durable CLI/tmux pane that is the seat's **spine** into posts, pins, formation, auto-rotation, ~5 unified engine routes, SSH-or-not collaboration, native handbacks, and graph↔harness-doc sync. Prereqs already live as siblings under `goal:g7` (do not re-mint):

```
goal:g7
├─ g7.25 family   adapter REQUIRED surface
├─ g7.26          post briefs as custom instructions
├─ g7.27          templates sole harness arg builders
├─ g7.28          dispatch persistent mode
├─ g7.29          shrink rotate → orchestration
├─ g7.30          land grok adapter + post template
└─ g7.31 ★        THIS umbrella (spine into the rest)
   ├─ .1 measured CLI + durable pane hold
   ├─ .2 pane ↔ post/pin/formation/auto-rotation
   ├─ .3 five unified routes through the pane
   ├─ .4 native handbacks SSH-or-not
   └─ .5 graph ↔ harness-doc sync
```

Graph carries growth; directors split further and launch batches. Golden rule: **graph > words**.

## Target end-state

```
grok_bot_adapter
      │ build_command / restart
      ▼
 named tmux pane  ◄── seat keeps (durable hold)
      │
      ├── post / pin / formation / auto-rotation
      ├── five unified engine routes (see g7.31.3)
      ├── native harness messaging (SSH mesh or not)
      └── write route ↔ Grok Bot profile/settings sync
```

- One **pane** per grok-bot seat is the only spine; no second argv path; stub CLI retired for measured CLI (precursor to magic pane).
- Agent action prefers the five pane-facing routes over raw tools.
- Directors may further-split children and launch pi parent batches; merge-up to Belam.

## Invariants

- No duplicate claims already owned by `goal:g7.25`–`goal:g7.30` — link as Related, never re-author.
- Soft ≤2 concurrent parents preferred; children hang primarily under `goal:g7.31`.
- `dispatch.py` / `rotate.py` never gain a `grok` special-case (same falsifier lineage as g7.25 / g7.30).
- Graph is SoT; harness docs and profile surfaces may lag only transiently and must reconverge (g7.31.5).

## Falsifier

1. Six nodes exist on `origin/core/season2/main`: `goal:g7.31` + `.1`–`.5`, each with standing-format body (Why → … → Agent Notes).
2. Each child falsifier (below) is answerable by a CLI/grep measurement — none is vibes-done.
3. Grep of `dispatch.py`/`rotate.py` for harness-name special-case of `grok` outside comments: **zero** hits attributable to this family.

## Out of scope

- Landing the adapter itself (`goal:g7.30`) or measuring CLI flags alone (`goal:g7.25` family).
- Magic-pane productization beyond the durable named-pane precursor in g7.31.1.
- Pushing `core/main` (Belam/Prime only).

## Agent Notes

**Assignment (owner 2026-09-21 ET):**
- **director-belam (point):** `g7.31` + `g7.31.1` + `g7.31.3` (spine + routes) — may further split
- **director-helper:** `g7.31.2` + `g7.31.4` + `g7.31.5` AND keep `g7.26`–`g7.30` land batch — may further split
- **Both:** launch pi parent batches; diagram-max; batch-max; merge-up to Belam; blockers to owner only

**Related (prereqs, not parents):** `goal:g7.25` family, `goal:g7.26`, `goal:g7.27`, `goal:g7.28`, `goal:g7.29`, `goal:g7.30`.

Session: `magic-pane-2026-09-21`. Frame as TARGETS not tasks.
