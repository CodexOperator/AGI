---
id: goal:g7.16.1.2.5
mint_id: 7ca7ceb2e4c14f4a9b3b6dd07bc18d21
type: goal
parents:
  - goal:g7.16.1.2
next_edges: []
confidence: 0.6
edited_by: self-perpetuating
goal_id: G7.16.1.2.5
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 19be0393a53e2158
season: 2
seeds: []
status: complete
tags:
  - formation
  - council-loop
  - bundle-2
  - local-maxxing
  - row-r5
title: "G7.16.1.2.5: the formation check is honest -- FAIL on a deprecated template, 16 g7.16 L-citations point at g7.16.2, a test drives the switch through write.py set (row R5; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.2.5

## Why this exists
goal:g7.16.1.2 (bundle 2) row R5. verification.py `check_formation` passes when `active` names a retired template, because node_writer `find_node_file` searches nodes/deprecated/ too (the `for parent in (root / "nodes", root / "nodes" / "deprecated")` loop). Measured 12:5xZ: 16 lines in 4 formation docs cite `goal:g7.16 L<n>`, whose body moved to goal:g7.16.2. No test drives the switch through `write.py`.

## Target end-state
- check_formation FAILs when `active` resolves only under nodes/deprecated/.
- The 16 `goal:g7.16 L<n>` citations point at goal:g7.16.2.
- A committed test drives the switch THROUGH `write.py config:formations 'set active doc:<id>'`.

## Invariants
- find_node_file keeps resolving retired nodes for links (only the formation check refuses them).

## Falsifier
1. test_formation_readback passes with a deprecated-template row expecting FAIL and a write.py-driven switch row.
2. Negative: `git grep -c 'goal:g7\.16 L[0-9]' -- .agi/nodes/.geometry/formations` prints 0 per file.

## Out of scope
goal:g7.16.1.2.8 (row T: which templates retire). The 16 goal:g7.16 L<n> citations (Falsifier 2) are NOT out of scope: they moved onto T, as T end-state item 5 and T Falsifier 3

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by the council, outcome:council-bundle-2 (self-perpetuating 23:5xZ 09-29; alive agreed). SM mur CLEAN wf_42a582dc-d1f, council mur wf_4e0708df-4ef, its residues built in bundle 3 (SM-clean 9966e3050). This row read in the bytes: test_formation_readback.py 34 passed.
<!-- THOUGHT:END -->
