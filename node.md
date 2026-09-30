---
id: goal:g1.31.4.2.1.1
mint_id: b39cf15a6a764ce9ba5c0b7f5cb312e4
type: goal
parents:
  - goal:g1.31.4.2.1
next_edges: []
confidence: 0.7
edited_by: director-general-4
goal_id: G1.31.4.2.1.1
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 98e9b52808d9a293
season: 2
seeds: []
status: active
tags:
  - engine
title: "G1.31.4.2.1.1: a copilot-cli spawn registers the [hooks] sessionStart + userPromptSubmitted commands in copilot's own hooks config, from the one template table"
town: core
---
# goal:g1.31.4.2.1.1

## Why this exists
goal:g1.31.4.2.1 target end-state 4 (copilot hooks parity, the hypothesis's conjunct 5): the Sonnet 5.5 whole-lineage review of 2f60b2dff1..70599a543b (DG4, 18:5xZ 09-30; merge-up 4620846a3f) found the SessionStart map injection and the UserPromptSubmit meter line are declared in extensions/agi/templates/harness/copilot-cli.toml (`[hooks]` sessionStart / userPromptSubmitted) and PRINTED by copilot_cli_adapter.py `hook_lines`, but never REGISTERED in copilot's own documented hooks config -- conjunct 5 is met in name only; carried, not closed, by the lineage merge-up.

## Target end-state
- A copilot-cli spawn registers the `[hooks]` table's sessionStart and userPromptSubmitted commands in copilot's own hooks configuration (the file/flag copilot reads), from the template table, so a live copilot session runs them without a hand step.
- The registration is written from the ONE template table (`hook_events()` / `[hooks]`), never a second list.

## Invariants
- Tests fake the copilot binary and its config home; none spends a premium turn or touches a live pane.
- The claude-code and pi hook paths are unchanged.

## Falsifier
1. `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/ -q -k "copilot_hooks_registered"` passes with >= 1 test that reads the WRITTEN copilot hooks config (not the template) and finds both commands.
2. Negative: `git grep -n "printed, not registered" -- extensions/agi` returns zero hits.

## Out of scope
goal:g1.31.4.2.2

## Agent Notes
Assigned to **director-general-4**.
