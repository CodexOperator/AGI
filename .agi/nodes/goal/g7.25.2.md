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
status: active
tags:
  - goal
  - subgoal
  - grok-bot
  - config
thought_session: goal-glom-polish-2026-09-19
title: "G7.25.2: harnesses.grok-bot config row only (no dispatch.py edit)"
town: core
---
<!-- BODY:BEGIN -->
# goal:g7.25.2

## Agent Notes
Why: parent goal:g7.25 needs harnesses.grok-bot in .agi/config.json so adapters.resolve(cfg, grok-bot) works. This subgoal owns the config row only (adapter: grok_bot, models kid/parent, bin/provider as peers). Zero dispatch.py. Zero adapter file edits.
