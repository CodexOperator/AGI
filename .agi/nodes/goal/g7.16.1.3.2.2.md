---
id: goal:g7.16.1.3.2.2
mint_id: 2a632dca9d88485293e2fbc45e9862fd
type: goal
parents:
  - goal:g7.16.1.3.2
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.3.2.2
goal_kind: subgoal
heading_level: 6
origin: goals-doc
scaffold_hash: 9b377015ef95da76
season: 2
seeds: []
status: complete
tags:
  - formation
  - council-loop
  - bundle-3
  - local-maxxing
  - row-h4
title: "G7.16.1.3.2.2: the master-gate skill points at anonymize.CLASSES + HOME_PATH_RE; g7.32.5 back to status active, tag kept (row H4 part 2; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.3.2.2

## Why this exists
goal:g7.16.1.3.2 (row H4), part 2: text only. skills/agi-master-gate/SKILL.md:66 hand-lists the anonymize classes (a second source; bundle 2 row R3 made anonymize.py the one source: `CLASSES` + `HOME_PATH_RE`). goal:g7.32.5 was set `status: horizon` when parked (6ff0e0aa1, bundle 1 row E). Park is tag-only since bundle 2 row P, and its pre-park status was `active` (git show 6ff0e0aa1~1).

## Target end-state
- skills/agi-master-gate/SKILL.md:66 points at anonymize.CLASSES + HOME_PATH_RE (a [build, goal] version of that skill's build node).
- goal:g7.32.5 reads `status: active` and keeps its `parked:g7.16.2` tag.

## Invariants
- The skill never copies a class list.

## Falsifier
1. `grep -m1 '^status:' .agi/nodes/goal/g7.32.5.md` prints `status: active`, and its tags still hold `parked:g7.16.2`.
2. Negative: the master-gate skill carries no literal class list (`grep -cE 'CLASSES|HOME_PATH_RE' skills/agi-master-gate/SKILL.md` >= 1, and the old hand list is gone).

## Out of scope
goal:g7.16.1.3.2.1

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by director-general-1 (23:4xZ 09-29) under the owner's 23:5xZ loop (build vs goal, then outcome); bundle 3 SM mur CLEAN at 1f39ffb1c covers the test halves. F1: goal:g7.32.5 active with parked:g7.16.2 kept; F2: the master-gate skill cites CLASSES/HOME_PATH_RE.
<!-- THOUGHT:END -->
