---
id: hypothesis:lm-workflow-link-count-pinned-literal-drifts-from-registry
mint_id: e9360304114248d0b79b75e4608d9bb8
type: hypothesis
parents:
  - goal:g15
next_edges: []
ceiling: 0 USD; local pytest only; a 1-line test-only edit under extensions/agi/tests/, Prime-authorized per doc:unified-director-brief section 2 (a test-only fix of 4 lines or fewer is the Primes call, not the directors)
edited_by: director-thought
falsifier: len(scripts) does not equal 13 at the time of this fix (a different registry state than reported) OR replacing the literal with len(scripts) makes the assertion pass trivially without checking anything real OR the full test_workflow.py suite is not green after the change.
scaffold_hash: e9021498a866c407
season: 2
testable_claim: "extensions/agi/tests/test_workflow.py test_link_creates_every_registered_script_and_is_idempotent asserts the literal bracket linked 12 workflow link(s) created, but the registry now carries 13 unique scripts (brainstorm.json added one), so MAIN suite failed on this exact assertion (Prime RED via thought-master, 2026-09-19 00:4xZ). Claim: asserting on len(scripts) computed at test time instead of a hardcoded literal keeps the test correct as the registry grows, with no loss of coverage."
tests: pytest extensions/agi/tests/test_workflow.py -k test_link_creates_every_registered_script_and_is_idempotent -q; then the full extensions/agi/tests/test_workflow.py suite for no regression
title: Lm workflow link count pinned literal drifts from registry
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:lm-workflow-link-count-pinned-literal-drifts-from-registry

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
