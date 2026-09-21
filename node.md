---
id: hypothesis:l3-tests-pin-ladder-state
mint_id: d48d6d731c75403eaae73d5e4ec652bf
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: ubuntu
scaffold_hash: eaf2c8e620e8abf3
season: 2
testable_claim: No engine test asserts a live-graph value that a sanctioned operation (rollover, retag, goal edit) is expected to change; every such test pins the shape or reads the expected value from the node, and a red-first audit test fails on a hardcoded season, count or name
title: L3 tests pin ladder shape not state
---
# hypothesis:l3-tests-pin-ladder-state

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FOUND L3.09 (both kids): test_ladder_node_current_season asserted current_season == 1 against the live ladder and broke on the wave-2 rollover; the prime fixed that one test by hand (thought on the build node). FILES: extensions/agi/tests/*.py (audit every test that loads a live node and compares to a literal: seasons, node counts, goal counts, titles), a small audit test or lint. FIX: each such test pins shape or derives the expectation from the graph; anything that must be a literal moves to a fixture graph under tmp. VERIFY: red-first audit; suite green on season/s2 with current_season 2; re-run after a dry rollover to 3 on a temp copy stays green. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Do not commit, push, or run grid.py commit.
