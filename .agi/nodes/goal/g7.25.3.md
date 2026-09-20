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
status: active
tags:
  - goal
  - subgoal
  - grok-bot
  - tests
thought_session: goal-glom-polish-2026-09-19
title: "G7.25.3: mirror adapter interface tests for grok-bot"
town: core
---
<!-- BODY:BEGIN -->
# goal:g7.25.3

## Agent Notes
Why: parent goal:g7.25 falsifier 4 — mirror existing adapter interface tests. This subgoal owns test_grok_bot_adapter.py (and any fixture-only helpers): load REQUIRED, is_alive True, needs_credential explicit False, restart callable, missing model tier KeyError.
