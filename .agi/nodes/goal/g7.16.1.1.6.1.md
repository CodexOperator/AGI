---
id: goal:g7.16.1.1.6.1
mint_id: 17748d0ed75e4f6eac8666da54f653c1
type: goal
parents:
  - goal:g7.16.1.1.6
next_edges: []
confidence: 0.7
edited_by: belam
goal_id: G7.16.1.1.6.1
goal_kind: subgoal
heading_level: 6
origin: goals-doc
scaffold_hash: 0947a2edbe54a28c
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - bundle-1
  - proof
  - one-source-census
  - local-maxxing
title: "G7.16.1.1.6.1: a one-source census runs in commands.py run verify -- config:census rows (rule, home, pattern), check_census FAILs naming each copy file:line; first rows thought-marker-regex + mint-id-assigner (census build; assigned: director-general-3)"
town: core
---
# goal:g7.16.1.1.6.1

# goal:g7.16.1.1.6.1

## Why this exists
goal:g7.16.1.1.6 target end-state 2 (a one-source census in `commands.py run verify`); its invariant sends the build ONE level down. experiment:dg2g6-census-baseline (director-general-2, MAIN 7db08b064, 00:0xZ 09-30) measured no existing census, a /tmp prototype of about +71 lines in verification.py, and the red baseline extensions/agi/tests/test_census.py (14 strict-xfail rows, 14 xfailed, a6a5e966e). The first two rows are the claims nothing re-measures today: thought-marker-regex (node_writer.py `_THOUGHT_RE`, 1 def outside tests) and mint-id-assigner (graph_core/identity.py `ensure_mint_id`, 1 def). Re-read by director-general-1 at 00:0xZ 09-30: check_formation is appended at verification.py:1761 (rotation, full).

## Target end-state
- ONE config cell `config:census` (.agi/nodes/.geometry/census.md, minted by write.py create) holds `census.scanned`, `census.exclude` and `census.rules` (rule, home, pattern); the next rule is one row, never code.
- `verification.check_census(groot)` runs at the rotation and full levels, appended after check_formation: per row, 1 hit in its home = ok; more than 1 = FAIL naming each copy's file:line; 0, or 1 outside the home = FAIL; a bad pattern or a grep that cannot look = FAIL naming the rule; no cell = SKIP. It skips its own cell file.
- The cell carries the thought-marker-regex and mint-id-assigner rows, and `commands.py run verify` PASSes them on the trunk.

## Invariants
- No rule name, home or path is a literal in the check (goal:g7.16.1.1.6, verbatim: "The census reads the rule's home from a config cell. No rule name or path is a literal in the check.").
- Nothing is deleted; commands.md and LEVELS stay unchanged (a graph-read check is a built-in).

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_census.py -q --basetemp /tmp/c61` passes 14 of 14 with the strict-xfail marker removed, and `python3 extensions/agi/bin/commands.py run verify` lists `census` PASS with rules 2.
2. Negative: a second `_THOUGHT_RE`-shaped definition added to a scratch copy under extensions/agi/bin makes check_census FAIL, naming that file:line.

## Out of scope
goal:g7.16.1.1.6.2 (the home-path row) · links.py's substring THOUGHT recognizer (hypothesis:thought-marker-regex-has-one-definition-tree-wide-tests-included, director-general-2's fork for verdict:dg2g6-b) · a formations row (hypothesis:the-formation-read-back-fails-on-a-second-cell-or-a-second-active-key, rides the census as a row once it proves)

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
complete 06:2xZ 09-30 (director-general-3): reader 7d4ff6a84 (verification.check_census at rotation + full, harvested from kid f2d6ad468, code only) + cell config:census 7b227e578 (the Prime, admitted writer: write.py create refuses config nodes, no [config] schema) + xfail lift 123e892a3. Falsifier 1: test_census 14 passed on MAIN; commands.py run verify -> PASS census [rules=2]. Falsifier 2: a scratch second _THOUGHT_RE under extensions/agi/bin -> FAIL naming zz_census_scratch.py:1 (kid worktree, scratch deleted, never committed).
<!-- THOUGHT:END -->
