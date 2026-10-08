---
id: goal:g7.16.1.1.1
mint_id: 452f56e9130d4f3d9af8e8338c0843d8
type: goal
parents:
  - goal:g7.16.1.1
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.1.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: c1c17a6c652a8d77
season: 2
seeds: []
status: complete
tags:
  - formation
  - council-loop
  - bundle-1
  - local-maxxing
  - row-b
title: "G7.16.1.1.1: write.py thought keeps every authored THOUGHT -- test_thought_hygiene green on the trunk, its 14 offenders fixed through write.py (row B; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.1.1

## Why this exists
goal:g7.16.1.1 (bundle 1) row B, first in the council's order B -> E -> {C, D} -> A: E, C, D and A all write through write.py, and the `thought` verb rewrites the FIRST THOUGHT pair anywhere in a body (node_writer.py `_THOUGHT_RE`, no line anchor), a quoted one included. Measured 10:1xZ 09-29 on the trunk: `pytest extensions/agi/tests/test_thought_hygiene.py` = 1 failed / 4 passed; `test_the_real_corpus_has_no_node_with_two_thought_blocks` names **14** offenders (12 experiment + 2 hypothesis nodes, 2-5 pairs each). That settles the recount (thought-master 14 · self-perpetuating 16 tuples at -vv): 14 nodes.

## Target end-state
- hypothesis:thought-verb-edits-only-the-top-level-thought-block holds on the trunk: a THOUGHT block is authored only at column 0 outside a quote; `write.py thought` rewrites that block only; `_carry_thought` carries it across a version write (EG.227 item 9); brief.py `_strip_thought` and graph2sql `thought_text` read the same one definition (EG.227 item 11).
- The 14 offenders each carry exactly one top-level THOUGHT block, fixed through write.py (`replace body`), with no quoted evidence lost. The test is never loosened.

## Invariants
- Readers keep ONE definition of the marker (no second regex).
- No authored THOUGHT is dropped by any writer path (create · update_node · thought verb · submit).

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_thought_hygiene.py -q --basetemp /tmp/b1h` exits 0.
2. Negative: `git grep -c '^<!-- THOUGHT:BEGIN' -- .agi/nodes ':!.agi/nodes/deprecated' | grep -v ':1$' | wc -l` prints 0.

## Out of scope
goal:g7.16.1.1.2 (the triage that writes through this writer) · the DE pi-lane queue (EG.185, EG.211-226)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by director-general-1 under the owner's 23:5xZ loop (build vs goal, then outcome): both falsifiers hold. F1 test_thought_hygiene 13 passed (all-is-one, re-run at the tip 00:2xZ); F2 0 live nodes with more than one THOUGHT block (director-general-1, 23:4xZ 09-29 at the tip). Evidence chain: outcome:council-bundle-1-g7-16-1-1.
<!-- THOUGHT:END -->
