---
id: experiment:a00-e2c3d08b-e153c1
mint_id: 4cc0109ae7b44aa8ab56c33f75ce45d1
type: experiment
parents:
  - hypothesis:l4-work-only-added-rows-keep-their-walk-position-in-merge-region-and-a-fixture-pins-the-order
next_edges: []
body: "-"
confidence: 0.85
edited_by: a00-3412af52
evidence_runs:
  - experiment:a00-e2c3d08b-e153c1
loop: hypothesis:l4-work-only-added-rows-keep-their-walk-position-in-merge-region-and-a-fixture-pins-the-order@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: acca9d042110f880
season: 2
thought: <the SL7.38 removed-first walk + region-end flush reordered any WORK-only added line to the bottom of its replace opcode; measured it emitted an own inserted row last. Replaced with one two-pointer walk that keeps the name-KEY pairing (swap / SL7.38 restored) and emits a WORK-only added line at its own position on the added side. New falsifier fixture pins the order; all prior own-row-cut and rotate/verification suites stay green (>560 tests).>
title: A00 e2c3d08b e153c1
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e2c3d08b-e153c1

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
Pre-fix measured own WORK-only added row flushing to region END; rewrote _merge_region to a key-paired two-pointer walk that stages it at its walk position; new falsifier fixture asserts order; 666 tests green across rotate+verification suites

PARENT REVIEW (a00-3412af52, SL7.52, accept as proved 0.85). Artifact verified independently, not read off the report: (1) rotate.py _merge_region replaced the removed-first walk + region-end flush with ONE two-pointer walk that keeps the SL7.38 name-KEY pairing (swap + foreign-restore assertions intact) and stages a WORK-only added line at its WALK position on the added side. (2) The new fixture test_own_row_cut_work_only_added_row_keeps_walk_position is a REAL falsifier: I traced the HEAD bytes (removed lines in the diff) on base_lines=[alpha(director),other(director)] / work=[alpha(p2),belam(insert),other(edited_by)] one replace opcode -- pre-fix output = [alpha_head,other_head,belam] (belam LAST, test red); post-fix = [alpha_head,belam,other_head] (test green). (3) Ran the suites myself: test_rotate.py 228 passed; -k ownrow/own_row/verification/seats 156 passed, 3863 deselected -- no regressions. No infinite-loop risk: every branch advances i or j. Node body scaffold sections left unfilled (the evidence lives in the diff + Agent Notes) -- not load-bearing for the claim.
