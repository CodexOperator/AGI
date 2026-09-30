---
id: goal:g7.16.1.2.7
mint_id: 6fe0fce2bb894c08a763a6c1eca26f2a
type: goal
parents:
  - goal:g7.16.1.2
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.2.7
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 8f8965f30ed5b97b
season: 2
seeds: []
status: active
tags:
  - formation
  - council-loop
  - bundle-2
  - local-maxxing
  - row-m
title: "G7.16.1.2.7: node_writer owns the THOUGHT marker strings -- snapshot-goals.py and write.py import them, no literal left (row M; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.2.7

## Why this exists
goal:g7.16.1.2 (bundle 2) row M. Bundle 1 row B made node_writer the one THOUGHT definition for readers, but the marker STRINGS are still spelled elsewhere. Measured 12:5xZ 09-29: `git grep -nE 'THOUGHT:(BEGIN|END)' -- extensions/agi/bin/snapshot-goals.py extensions/agi/bin/write.py` = 4 lines (the council cited snapshot-goals.py:258 · write.py:2918).

## Target end-state
- node_writer owns the BEGIN/END marker strings as named constants. snapshot-goals.py and write.py import them.

## Invariants
- Rendered bytes are unchanged: `snapshot-goals.py --render --check` stays byte-identical.

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_thought_hygiene.py -q --basetemp /tmp/b2m` exits 0 and the render check exits 0.
2. Negative: `git grep -nE '"[^"]*THOUGHT:(BEGIN|END)' -- extensions/agi/bin/snapshot-goals.py extensions/agi/bin/write.py` prints 0 string literals.

## Out of scope
links.py's surface-file skip (bundle 1 row B, named out of scope)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-1 (council bundle 2, stage 1, 13:0xZ 09-29) from goal:g7.16.1.2 row M. Re-measured: 4 literal lines. Hypothesis: node-writer-owns-the-thought-marker-strings.
<!-- THOUGHT:END -->
