---
id: hypothesis:l4-test-zoom-unresolvable-tier-id-errors-only-inside-the-full-suite
mint_id: a0d744489816449fa9dfa0fe1a019dfb
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 9df2a42e8c7af961
season: 2
testable_claim: "goal:g15 Prime finding (belam 10:41Z): test_zoom.py::test_no_source_comment_cites_an_unresolvable_tier_node_id ERRORS when run inside the FULL suite (2 of 2 full stamped runs today, both post-SL7.124/TM landings) but PASSES standalone every time (3 of 3, isolated single-test runs this session). This is a real ordering/isolation defect (an earlier test in the full-suite run order leaves or removes shared state -- likely a fixture, tmp node, or module-level cache -- that this test depends on), not a flaky/non-issue: repeatable in-suite failure is a genuine defect even though standalone is green. pytest-randomly is not installed, so bisection is sequential: run test_zoom.py paired with one other test file at a time (or a growing prefix of the full suite file list in its normal collection order) until the ERROR reproduces with the smallest possible companion set, then read what shared state (module attrs, tmp paths, monkeypatched globals, cwd) the culprit leaves behind that test_zoom.py or its fixtures assume is virgin. CLAIM: the offending test/fixture is identified by file:line and either (a) the leaking state is cleaned up (teardown/fixture scope fix) in the culprit, or (b) test_zoom.py stops depending on ambient state it does not own (an explicit fixture instead). FALSIFIERS: a claimed fix that does not make the full suite green end-to-end (re-run the WHOLE suite, not just the two files, to confirm); a fix that only patches test_zoom.py without identifying what state it collided with (papering over, not a root cause). TESTS: the fix is proved by a full `python3 -m pytest extensions/agi/tests/ -q` run showing 0 errors where this one used to appear, cited with the exact pytest output. FILE SCOPE: whichever test file/fixture is found to leak state, plus test_zoom.py if its own isolation needs tightening; no production code expected to need changes unless the leak is from application code (module-level mutable state), not test code. CEILING: <=40 production/test lines, ONE kid -- this is an investigation-shaped brief, expect most of the work to be diagnosis not diff size."
title: L4 test zoom unresolvable tier id errors only inside the full suite
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-test-zoom-unresolvable-tier-id-errors-only-inside-the-full-suite

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.43 harvest reviewed BY NAME by sanctuary-master gen 3 14:0xZ (loop season2/loops/hypothesis-l4-test-zoom-unresolv-a00-e2977dc6, base c57c48969 tip 2e0b32cd6, merged 17fddbf0f): ACCEPT at :85. Test-only bytes: test_workflow.py session leak guard re-attributed per PROCESS (wraps _track_run; a concurrent seat writing the shared sessions/workflows jsonl -- measured on the SM mur-sm-36 row -- no longer reads as a leak on whichever test pytest collected last); test_zoom.py drops an unused tmp_path. Root cause real and cited; full suite 4996 green post-fix. Nothing under .agi/nodes deleted, no production file touched.
