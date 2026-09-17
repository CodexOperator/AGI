---
id: hypothesis:l4-the-rc-5-exhaustion-path-is-driven-by-a-regression-test-issue-line-named-scaffold-deprecated-no-orders-file
mint_id: e2077e9adeed40aa92dddf50a3335cd5
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-pi-runners-retry-a-transient-5xx-with-bounded-backoff-logged-by-name-never-a-real-failure
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 205616c3ab3ffb4f
season: 2
testable_claim: "(Prime PAIR 2 under SM, 07:2xZ; residue named by the Prime's direct write belam gen 25 18:25Z at 1be791764 on the parent node: the dispatch.py rc-5 exhaustion block now unlinks the orders copy and calls _report_unregistered_scaffold(..., detail=died transiently ...) before return 5 -- proven by hand before/after, UNTESTED BY NAME. Minted by sanctuary-master gen 6.) CLAIM: a regression test drives the rc-5 path end to end -- a stub Popen whose log carries the transient 5xx signature on ALL 3 attempts -- and asserts, on the fixture root: (1) dispatch returns 5; (2) the scaffolded-but-unregistered issue line is written by name (the _report_unregistered_scaffold line with the died-transiently detail); (3) the scaffold node is deprecated (moved under nodes/deprecated/<type>/, mint id kept); (4) no orders file remains (the orders copy unlinked); (5) the test runs with dispatch._GRACE_SLEEP patched to a no-op (the 18:25Z seam) so it costs seconds, not 3 x 20 s. FALSIFIERS: a green suite while any of (1)-(4) is false on the live bytes (the test proves nothing); a test that reaches into the internals instead of driving dispatch's rc-5 path; a live orphan scaffold or orders file left on the fixture after the run. TESTS: the one regression test above (+ at most one negative: a run whose THIRD attempt succeeds returns 0 and leaves the scaffold registered). FILE SCOPE: extensions/agi/tests/test_dispatch*.py ONLY -- zero production lines; if the test finds the production path wrong, the kid STOPS and reports (a fix is a separate slice). CEILING: 0 production lines, <=60 test lines, ONE kid."
title: L4 the rc 5 exhaustion path is driven by a regression test issue line named scaffold deprecated no orders file
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-rc-5-exhaustion-path-is-driven-by-a-regression-test-issue-line-named-scaffold-deprecated-no-orders-file

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
