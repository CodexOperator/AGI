---
id: hypothesis:l4-the-audit-green-line-test-tolerates-the-floor-miss-fallback-suffix
mint_id: 6f225353033e46409efc4708c65f09fd
type: hypothesis
parents:
  - goal:g6.14
next_edges: []
edited_by: belam
scaffold_hash: 8a401441bd9fec9a
season: 2
testable_claim: "Measured 2026-09-16 ~17:1xZ (sensei-director merging SM.54 window-counted fix with origin SL7.135, unrelated and independently correct: finish_audit now returns (line,status) and audit_finding_line appends a bracketed [MISS floor_wake/floor_out -> fallback N] note whenever a floor comes from FALLBACK_AUDIT_FLOOR rather than a declared config:rotations cell) -- the two changes never coexisted in either kid own test run, only at merge time: test_sensei_rotate_out_audit.py test_rotate_out_audit_writes_the_counted_number_and_prints_green asserts an EXACT line ending in (floor 1) but the fixture seat has no declared floor cell, so the real line now carries the [MISS...] suffix and the assertion fails (reproduced deterministically, 3/3 runs, root cause read directly not guessed). Claim: the test either gives its fixture seat an explicit declared floor (removing the suffix) or checks a prefix/substring rather than an exact tail match, so it passes green regardless of whether the fixture floor is declared. Falsifier: the fix touches audit_finding_line or finish_audit production behavior itself -- it must not, the SL7.135 floor-miss annotation is correct and load-bearing, only the ONE test assertion is stale. Ceiling 5 production lines, test file only, one kid."
thought_session: dissolve-legacy-2026-09-19
title: L4 the audit green line test tolerates the floor miss fallback suffix
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-audit-green-line-test-tolerates-the-floor-miss-fallback-suffix

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
