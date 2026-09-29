---
id: goal:g7.16.1.1.3
mint_id: e7a542af8ead448694610ce60abfc3bc
type: goal
parents:
  - goal:g7.16.1.1
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.1.3
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 83d17cc83e046e4a
season: 2
seeds: []
status: complete
tags:
  - formation
  - council-loop
  - bundle-1
  - local-maxxing
  - row-c
title: "G7.16.1.1.3: anonymize.py existing check refuses the box home path, one token list and a test pin it, and the 13 nodes carrying it are scrubbed in the same round (row C; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.1.3

## Why this exists
goal:g7.16.1.1 (bundle 1) row C. Measured 10:2xZ 09-29: `git grep -lF "$HOME" -- .agi/nodes | wc -l` = 13 (9 experiment · 2 goal (g7.33.11, g7.33.14) · 2 hypothesis nodes). extensions/agi/bin/anonymize.py `box_tokens` (+ `_secret_tokens`) builds the one token list its `scan` / `check` refuse, and no home-path token is in it. The HEAD's anonymize rule forbids a home or repo path value in any node.

## Target end-state
- anonymize.py's EXISTING `box_tokens` list carries the box user's home path, and `check` refuses staged text holding it. There is no second checker, and one committed test pins the refusal.
- The same round scrubs the 13 nodes through write.py (`sub <home> => <home>` style, text only). After that, no node holds the path.

## Invariants
- ONE token list, ONE checker (SM.122 seam).
- A scrub changes path text only. Node count and frontmatter stay the same.

## Falsifier
1. `python3 -m pytest extensions/agi/tests/ -q -k anonymize --basetemp /tmp/b1c` exits 0, with a row that feeds `check` the home path and expects a refusal.
2. Negative: `git grep -lF "$HOME" -- .agi/nodes | wc -l` prints 0.

## Out of scope
goal:g7.16.1.1.4 · paths outside .agi/nodes (the engine's own test fixtures)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by director-general-1 under the owner's 23:5xZ loop (build vs goal, then outcome): both falsifiers hold. F1 the anonymize suite carries the home-refusal row (all-is-one's run at the tip 00:2xZ); F2 `git grep -lF "$HOME" -- .agi/nodes` = 0 (director-general-1, 23:4xZ 09-29 at the tip). Evidence chain: outcome:council-bundle-1-g7-16-1-1.
<!-- THOUGHT:END -->
