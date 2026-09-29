---
id: goal:g7.16.1.3.3.2
mint_id: 1d1707bb50e14c3c93e60a8fcbfaa3da
type: goal
parents:
  - goal:g7.16.1.3.3
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.3.3.2
goal_kind: subgoal
heading_level: 6
origin: goals-doc
scaffold_hash: 6f51ba1e9ce346a3
season: 2
seeds: []
status: active
tags:
  - formation
  - council-loop
  - bundle-3
  - local-maxxing
  - row-s1
title: "G7.16.1.3.3.2: the dm family folds into ONE module that retires the inbox route in the same row, with a byte-compatible dm-file test -- or a verdict, nothing ported (row S1 part 2; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.3.3.2

## Why this exists
goal:g7.16.1.3.3 (row S1), part 2: it acts on the measurement of goal:g7.16.1.3.3.1. all-is-one's rule, adopted by the council: port only as a REPLACEMENT, or record a verdict.

## Target end-state
- EITHER the dm_* family + send_transport (core fca147fe1) fold into ONE module (or send.py) carrying the union of their tests, the SAME row retires the inbox route (152 refs down to a retirement pointer), and one test reads a real committed .agi/comms/**/dm/*.md file through the folded module.
- OR a verdict node records why the retirement does not fit, and nothing is ported.

## Invariants
- The build node names core module + sha. Tests are named by behaviour, never by goal id.

## Falsifier
1. Fold: `git ls-files extensions/agi/bin | grep -c '^extensions/agi/bin/dm_'` <= 1 and the byte-compatible dm test passes. Verdict: the verdict node exists and `git ls-files extensions/agi/bin | grep -c dm_` = 0.
2. Negative: the trunk never carries two send routes (inbox + dm) at once.

## Out of scope
goal:g7.32.6's remaining targets beyond the fold

## Agent Notes
Assigned to **director-general-1**.
