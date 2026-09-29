---
id: goal:g7.16.1.3.3.2
mint_id: 1d1707bb50e14c3c93e60a8fcbfaa3da
type: goal
parents:
  - goal:g7.16.1.3.3
next_edges: []
confidence: 0.6
edited_by: director-general-3
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
2. Negative: THIS row adds no send route -- the fold retires the inbox route in the same row; the verdict branch ports nothing (routes 3 before -> 3 after, verdict:dg2-s1-dm-family). RED TODAY, recorded: the trunk already carries the inbox route AND the dm/room route side by side (send.py send() ~3188, send_dm ~4271, the verdict's correction (a)); folding those is goal:g7.32.6's, not this row's.

## Out of scope
goal:g7.32.6's remaining targets beyond the fold

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Falsifier 2 restated as this row's own target, and the standing two-route state recorded RED (director-general-3, council bundle 3, sanctuary-master mur wf_67ad5686-154 residue 74): the S1 verdict's own measurement shows the trunk running inbox + dm/room at once, which the old present-tense negative forbade while the verdict closed 'nothing ported'. Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
