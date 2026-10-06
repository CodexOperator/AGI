---
id: goal:g7.16.1.3.2.3.3
mint_id: 6933bc1e9a9c40d7a54b1f09a560fb6e
type: goal
parents:
  - goal:g7.16.1.3.2.3
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.3.2.3.3
goal_kind: subgoal
heading_level: 7
origin: goals-doc
scaffold_hash: 2ca2d070a2caa7eb
season: 2
seeds: []
status: complete
tags:
  - formation
  - council-loop
  - bundle-3
  - local-maxxing
  - row-h4
title: "G7.16.1.3.2.3.3: the seating announcement writes the transcript path home-relative through the one serializer (mur residue g; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.3.2.3.3

## Why this exists
goal:g7.16.1.3.2.3, residue (g) of council mur wf_4e0708df-4ef: rotate.py's seating announcement writes the ABSOLUTE transcript path into tracked comms, while bundle 2 row R1 made rotation records home-relative through one serializer. So every first seating re-adds a home path to a tracked file, which the generic home class now refuses.

## Target end-state
- The seating announcement writes the transcript path through anonymize.home_relative via bundle 2 row R1's serializer (the one goal:g7.16.1.3.2.1 moves into the shared module), never a new strip (council add 5, c0c8d3f82).

## Invariants
- A reader of the announcement resolves the path through the one resolver.

## Falsifier
1. A committed test: a first-seating announcement in a tmp home writes `~/`-relative, never the tmp home's absolute path.
2. Negative: no .agi/comms file written after the fix (482da3853) matches anonymize.HOME_PATH_RE. Older dms (newest 09-20) predate the fix and are history, not this row's.

## Out of scope
goal:g7.16.1.3.2.3.1 (the scrub of already-written files)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by director-general-1 (23:4xZ 09-29) under the owner's 23:5xZ loop (build vs goal, then outcome); bundle 3 SM mur CLEAN at 1f39ffb1c covers the test halves. F2 restated: 0 comms files since the fix match HOME_PATH_RE (older dms predate it); F1 test built with mvp:dg3-h4g-seating-transcript.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: complete goal not carried into s3; builds reparented to umbrella. -->
