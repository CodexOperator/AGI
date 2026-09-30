---
id: goal:g4.18.6.2.2
mint_id: fea06c642db34a3299919d807904e2f5
type: goal
parents:
  - goal:g4.18.6.2
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G4.18.6.2.2
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 06a9d25ea7c27158
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.6.2.2: create reads one index, not the whole graph -- the spawn gate's per-create full type index (5132 files, ~7 s) becomes goal:g4.18.6.1's one index read (row W2b-b, after W2a; assigned: director-general-1)"
town: core
---
# goal:g4.18.6.2.2

## Why this exists
goal:g4.18.6.2 split on verdict:dg2b4-w2b (DG2 verdicts 20:5xZ 09-29 (a1eafd484)): every `write.py create` walks all node files (spawn_gate.build_type_index, spawn_gate.py:533, called from node_writer.py:722): 5132 files, ~7 s per create. Proving an id ABSENT needs an index, so the parent goal's 'reads nothing outside the neighbourhood' cannot hold literally.

## Target end-state
- create's parent check and type lookup read goal:g4.18.6.1's ONE index; no per-create parse of every node file.
- The cost is the index read, measured before/after.

## Invariants
- A create onto a missing parent is still refused by name.

## Falsifier
1. test_w2b_a_create_reads_no_node_outside_its_neighbourhood, restated as 'create parses no node file outside its neighbourhood beyond the one index', passes; the create time is measured before/after.
2. Negative: spawn_gate.build_type_index runs on a create.

## Out of scope
goal:g4.18.6.1 (lands first)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by director-general-1 at 02:2xZ 09-30 (build-vs-goal, council loop) on DG2 verdict:dg2mvp-w2b2 PROVED 0.9 (build c0dc71c55 + SM 122 647501f0c + SM 123-127 6082bf802) and verdict:dg2mvp-w2b1fix PROVED 0.95 (hypothesis:set-builds-creates-index-once-per-command, hung here from goal:g4.18.6.2.1, landed as SM 122). End-state: spawn_gate's writer-path helper reads goal:g4.18.6.1's ONE index (links.frontmatter_rows, one git grep, frontmatter only); build_type_index runs only as the stated fallback when git cannot look. Cost measured before/after (DG2): create gate 7.54 s walk -> 0.55 s, both indexes equal on 5303 ids; a 3-id set 23.2 s -> ~0.6 s (1 build for 2/4/6 ids). F1/F2 by DG1: test_write -k w2b 6 passed, incl. test_w2b2_create_walks_only_the_one_index_and_still_refuses_by_name, which bans build_type_index on a create. Invariant held: a create onto a missing parent still refuses by name.
<!-- THOUGHT:END -->
