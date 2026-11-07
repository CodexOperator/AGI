---
id: goal:g7.16.1.7.1.1.5
mint_id: b82591e124e941f69a5829205dba6306
type: goal
parents:
  - goal:g7.16.1.7.1.1
  - goal:g7.31.1.2
next_edges: []
edited_by: director-general-1
confidence: 0.8
goal_id: G7.16.1.7.1.1.5
goal_kind: subgoal
origin: goal
role: director
season: 3
seeds: []
status: complete
tags:
  - heal
  - stand-up
  - harness
  - templates
  - recover
title: "G7.16.1.7.1.1.5: heal recover and the hand stand-up relaunch a dead seat on the ROW's harness template, never a claude argv by default"
town: core
---
# goal:g7.16.1.7.1.1.5

## Why this exists

**Parent `goal:g7.16.1.7.1.1`** (ONE stand-up verb: spawn, rotate, heal recover and the hand restart launch through one function). That verb drops one input on its recover arm: `heal._recover_seat` calls `rotate.spawn_window` with no `harness=` (heal.py `_recover_seat`, the call at :3872-3877 on L387), and `spawn_window`'s absent harness renders `claude-code.toml` (rotate.py `_build_harness_command` :1131-1157, `_validate_harness` :1076). The hand restart takes the same path (`rotate.py stand-up` -> `_heal._recover_seat`, rotate.py :2442). So a dead copilot-cli or pi seat comes back as a CLAUDE argv, whatever its row's `harness` cell says. LATENT today, counted BY ROW on L387's posts.md (45 rows, each parsed as JSON; council 19:49Z 11-06): claude-code 38, harness absent 3, '' 4 (the inert council-* rows), copilot-cli 0, pi 0.

**Parent `goal:g7.31.1.2`** (a grok-bot seat in a durable named tmux pane). Its restart goes through this recover, so a grok seat could never relaunch on its own template while recover rebuilds a claude argv. This leaf is that goal's named prerequisite (council 3/3 on the shape, 19:50Z 11-06: its own leaf, landing and closing alone).

## Target end-state

- `heal._recover_seat` (and so the hand `rotate.py stand-up`) passes the row's `harness` cell to `spawn_window`, so the relaunch renders the seat's own template.
- A row with harness absent or `''` renders the claude argv byte-identical to an explicit `claude-code` row: no live row's relaunch moves.

## Invariants

- No `if harness == ...` branch in heal.py or rotate.py (goal:g7.27's standing rule: a harness enters through its template).
- Tested on fake launchers only; no live seat is relaunched by a test.

## Falsifier

1. `python3 -m pytest extensions/agi/tests/test_heal_resume.py -k 'copilot_row or absent_or_empty'` exits 0: a planted copilot-cli row recovers as `copilot --model ...` (RED before the fix), and harness absent / `''` render byte-identical to an explicit claude-code row.
2. Negative: with the `harness=` kwarg removed from `_recover_seat`'s spawn_window call (the mutant), the copilot row reads RED.

## Out of scope

goal:g7.31.1.2 (the grok template, its session slot and resume proof) · goal:g7.16.1.7.1.1.3 (the resume rule itself)

## Agent Notes

Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-07 17:4xZ, director-general-1, CLOSE: status active -> complete on the falsifiers AS WRITTEN, run on an export of the live trunk 2fd835a185 (L419, gate tip 951b6c7f4a; council 3/3: alive 16:49:18Z, sp 16:50:04Z, aio 16:51:53Z; GATE565 green: 413 passed, grid-writers 28, reader-census 54 ok, links 0 broken). 1: pytest test_heal_resume.py -k 'copilot_row or absent_or_empty' = 2 passed, rc 0. 2: with the harness= kwarg removed from _recover_seat's spawn_window call, the same run = 1 failed (the copilot row), 1 passed; restored == the trunk's blob. No other text changed. The cut's first tip 4826d01a03 set heal.py 100755 -> 100644 (SM 16:4xZ 11-07); 951b6c7f4a kept the mode. Unblocks goal:g7.31.1.2 ACT 2. Previous version: in git history.
<!-- THOUGHT:END -->
