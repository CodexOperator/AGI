---
id: goal:g7.16.1.3.3
mint_id: 3a06fba52f0842b4be03953ab5c42853
type: goal
parents:
  - goal:g7.16.1.3
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.3.3
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 9408750426d7ca46
season: 2
seeds: []
status: complete
tags:
  - formation
  - council-loop
  - bundle-3
  - local-maxxing
  - row-s1
title: "G7.16.1.3.3: messaging is ONE route, or a verdict -- measure first, then fold the core dm family as a replacement that retires the inbox, or record why not (row S1; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.3.3

## Why this exists
goal:g7.16.1.3 (bundle 3) row S1. Core added messaging BESIDE the inbox, not instead of it. Measured 17:2xZ 09-29 at origin/core/season2/main fca147fe1: dm_address 115 · dm_engine 128 · dm_no_inbox 74 · dm_nudge_gate 75 · dm_read_version 64 · dm_send_version 80 · dm_sync_cron 92 lines + send_transport 39, with 8 tests. send.py `inbox` refs: trunk 152, core 149. The trunk has 0 dm_* modules. Porting as-is gives 2 routes. Split: goal:g7.16.1.3.3.1 MEASURES first, and goal:g7.16.1.3.3.2 lands a replacement or a verdict.

## Target end-state
- Messaging on this trunk is ONE route: either the folded dm module replaces the inbox route (routes 2 -> 1), or a verdict node records why not and nothing is ported. CC SendMessage is the interim.
- adapters/magic_pane follows S1's outcome.

## Invariants
- Nothing is written on core. The dm file format stays byte-compatible.

## Falsifier
1. `git grep -h '^status:' -- .agi/nodes/goal/g7.16.1.3.3.*.md | sort -u` prints only `status: complete`.
2. Negative: if S1 landed, `git ls-files extensions/agi/bin | grep -c '^extensions/agi/bin/dm_'` <= 1; if S1 is a verdict, 0.

## Out of scope
goal:g7.32.6 itself (S1 measures its targets only) · bundle 4 (core edits to existing files)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by director-general-1 (23:4xZ 09-29) under the owner's 23:5xZ loop (build vs goal, then outcome); bundle 3 SM mur CLEAN at 1f39ffb1c covers the test halves. every .3.* leaf complete; S1 is a verdict, 0 dm_ files.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: complete goal not carried into s3; builds reparented to umbrella. -->
