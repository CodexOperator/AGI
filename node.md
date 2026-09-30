---
id: goal:g1.31.3.1
mint_id: 20ae71ad3f7e4a05beb071dbc3d109e7
type: goal
parents:
  - goal:g1.31.3
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.3.1
goal_kind: subgoal
origin: goals-doc
scaffold_hash: d2094292d56c8439
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - residue
  - node-answer
title: "G1.31.3.1: PASS B3 verdict/evidence residues -- 9 nodes whose verdict or evidence pointer the bytes contradict agree with the bytes"
town: core
---
# goal:g1.31.3.1

## Why this exists
goal:g1.31.3: PASS B3 upheld 9 verdict/evidence contradictions on nodes in 8 rounds (#31 moved to goal:g1.31.4.2.1) (a00-4d063889-c4e95d · lm-bonsai2-27b-abc-coding-test-on-the-8gb-box · l3w4-branch-shared-state · thought-verb-edits-only-the-top-level-thought-block · l4-test-zoom-unresolvable-tier-id-errors-only-inside-the-ful · a00-ec5ee032-7eefb8 · l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-cla · l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gate · harness-bin-paths-resolve-per-box). 10 > 6, so split by theme: a verdict that the bytes contradict (5) vs an evidence pointer that is dead, stale, unrecorded or unreproducible (5). At HEAD ff09c6101: 9 open, 1 already fixed (#11).

## Target end-state
- goal:g1.31.3.1.1 — every named verdict field agrees with the bytes and with its own node's record (#1 #6 #13 #46).
- goal:g1.31.3.1.2 — every named evidence pointer resolves to committed, current bytes or is marked UNREPRODUCIBLE/superseded on the node (#5 #11 #29 #30 #39).

## Invariants
- A residue is closed by a reviewed round, never by a note.
- A verdict only moves toward what the bytes show; a demotion is written to the frontmatter, not only to a THOUGHT.

## Falsifier
1. Every child goal:g1.31.3.1.1 and goal:g1.31.3.1.2 is complete (each child's falsifier 1 exits 0).
2. Negative: `git grep -n 'bonsai/abc/humaneval' -- .agi/nodes` returns zero hits.

## Out of scope
goal:g1.31.3.2 (scrub damage + leaked literals) · every other goal:g1.31.* leaf · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6**.
