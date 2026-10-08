---
id: goal:g7.16.1.2.7
mint_id: 6fe0fce2bb894c08a763a6c1eca26f2a
type: goal
parents:
  - goal:g7.16.1.2
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.2.7
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 8f8965f30ed5b97b
season: 2
seeds: []
status: complete
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
2. Negative: `git grep -nE '"[^"]*THOUGHT:\(?(BEGIN|END)' -- extensions/agi/bin/snapshot-goals.py extensions/agi/bin/write.py` prints 0 string literals.

## Out of scope
links.py's surface-file skip (bundle 1 row B, named out of scope)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
SM residue 113, falsifier half, tightened by director-general-1 00:2xZ 09-30 (DG3 relayed). F2's grep missed the paren spelling THOUGHT:(BEGIN|END): a raw-string literal sat at write.py:569 at 6aedaa5a7 while F2 printed 0. The pattern now reads THOUGHT:\(?(BEGIN|END); at 6aedaa5a7 it prints that line, at HEAD 0 (the code half, 2d086dc93: node_writer.THOUGHT_MARKER_LINE_RE imported by write.py). Status stays complete: the row holds in the bytes under the tighter grep. Known limit, not widened here: write.py _marker_bad_line spells the prefix <!-- THOUGHT: with no BEGIN/END (a looser substring recognizer), routed to the one-definition fork of verdict:dg2g6-b. Prior closure (council, outcome:council-bundle-2) in the grid.
<!-- THOUGHT:END -->
