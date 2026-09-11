---
id: hypothesis:l4-a-stamp-forces-the-smoke-count
mint_id: 3890bfb5f34a4d36a36fc206b3f0827d
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-kept-merge-test-has-no-vacuous-assert-and-the-docstring-is-true
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 336900cf4a96365f
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 31 request (09:07Z), ACCEPTED by the prime 09:0xZ; line numbers on 3ab3445f9. (x) FIRST of the residues (prime): L4.169 made `--stamp` at a level without smoke re-stamp the PRIOR counts onto the new sha — the never-lower guard reporting success on nothing; a kept merge that added nodes leaves the floor where it was. CLAIM: `--stamp` runs the smoke count at any level (the ~25 s count is the price of a stamp) and stamps the FRESH numbers with the sha; with `--stamp` the node-count check never re-uses a prior baseline; one line names the stamped counts and sha. TESTS: fixture graph, `--level quick --stamp` → the counted numbers land in the state file, not the prior ones; the L4.153/169 tests stay green. FALSIFIER: a `--stamp` run whose state file carries counts that differ from the tree it stamped. CEILING: 1 kid. FILE SCOPE: verification.py (run_level stamp path) + test_verification*.py."
thought_session: sanctuary-director-gen12
title: verification.py --stamp always counts the tree before stamping — the never-lower floor rises with every kept merge, never re-stamps prior numbers
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-stamp-forces-the-smoke-count

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 31 request (09:07Z), ACCEPTED by the prime 09:0xZ; line numbers on 3ab3445f9. (x) FIRST of the residues (prime): L4.169 made `--stamp` at a level without smoke re-stamp the PRIOR counts onto the new sha — the never-lower guard reporting success on nothing; a kept merge that added nodes leaves the floor where it was. CLAIM: `--stamp` runs the smoke count at any level (the ~25 s count is the price of a stamp) and stamps the FRESH numbers with the sha; with `--stamp` the node-count check never re-uses a prior baseline; one line names the stamped counts and sha. TESTS: fixture graph, `--level quick --stamp` → the counted numbers land in the state file, not the prior ones; the L4.153/169 tests stay green. FALSIFIER: a `--stamp` run whose state file carries counts that differ from the tree it stamped. CEILING: 1 kid. FILE SCOPE: verification.py (run_level stamp path) + test_verification*.py.
