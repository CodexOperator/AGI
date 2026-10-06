---
id: goal:g7.16.1.7.3.1
mint_id: 67a6e5261dbc4f52a227aec55a8f2dc9
type: goal
parents:
  - goal:g7.16.1.7.3
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.16.1.7.3.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: e572649058db555c
season: 2
seeds: []
status: complete
tags:
  - magic-pane
  - tool-call
  - council-loop
  - event-routes
thought_session: belam-magic-pane-20260930T0503Z
title: "G7.16.1.7.3.1: event-kind → one-route config table SoT (census counts every generation)"
town: core
---
<!-- BODY:BEGIN -->
# goal:g7.16.1.7.3.1

# goal:g7.16.1.7.3.1

## Why this exists
goal:g7.16.1.7.3 (one magic pane per post row is the tool-call-turn anchor): the parent measures four separate delivery routes today (SessionStart hook paste · UserPromptSubmit meter · send.py nudge · CC SendMessage) and requires ONE route per event kind via a config table the census counts every generation. This leaf is the non-destructive SoT for that table — the first claimable slice of the pane-as-post-anchor line. It takes the pane-attachment idea from CORE magic-pane work; it does NOT extend magic_pane messaging (owner 01:2xZ: pane only, not messaging integration).

## Target end-state
- A committed fixture names each engine event kind a post must see (first_turn_docs · memory_alarm · message_receipt · rotation_prompt · write_commit_result) with exactly one `target_route` (`tool_call_turn`) and the measured `legacy_routes` in use today.
- Duplicate event kinds are refused by the fixture loader (one entry per kind).
- `adapters.magic_pane` stays the messaging LEAF (g7.32.2*); this table does not import or call it.

## Invariants
- One row per event kind; a second row for the same kind = FAIL naming it.
- Pane owns no transport: this SoT never names a network fetch as a pane-owned route (transport stays goal:g7.32.6).
- Messaging integration (grok↔grok native / nudge→send) stays out of scope here.

## Falsifier
1. `pytest extensions/agi/tests/test_magic_pane_event_routes.py` exits 0: fixture loads, every required kind present, kinds unique, every `target_route` is `tool_call_turn`, and the four parent-measured legacy routes appear as values under `legacy_routes`.
2. Negative: the fixture file and the test import nothing from `adapters.magic_pane` / `send.py` transport (grep the two files for `magic_pane` and `send.py` = 0).

## Out of scope
goal:g7.16.1.7.3.2 · goal:g7.16.1.7.1 · goal:g7.16.1.7.2 · goal:g7.32.2 · goal:g7.32.6

## Agent Notes
Assigned to **belam** (Prime NO-PI placement + SoT land; further .3.* build leaves go to the directors of goal:g7.16.1.7 by their own split).

Owner-update re-scope: fixture schema v2 — inject.message_is=tool_return; channel dm|engine + kind_tag; build_lane=pi/free + pi_adapter + pi.toml; CC-compat via pi session_start/tool_result mirroring CC hooks. Tests 7/7.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Folded owner update into landed SoT without touching magic_pane.py messaging.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: complete goal not carried into s3; builds reparented to umbrella. -->
