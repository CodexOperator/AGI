---
id: hypothesis:l4-test-only-templates-read-startup-delivery-after-join-roots-are-tmp-paths-read-ack-payers-poll-fast-and-test-grid-keeps-git-stderr
mint_id: fe797cc7549443c3a7a72311f6b5241d
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 5b7b2a80f2b71a7e
season: 2
testable_claim: "goal:g15 TEST-ONLY (Prime XVII 18:48Z test-only line, mur-SL2.24). MEASURED at post tip 80f1457db (the Prime's line numbers, measured on origin/season2/main @ 6dbd67525 — re-measure each with grep on your base): extensions/agi/tests/test_rotate_templates.py:269 reads a top-level delivery key while the live director template node keeps startup.delivery, so the live prose is never scanned and the test proves nothing about the template + :362 the F16 carve-out is keyed by a PHRASE; test_after_join_service.py:174 and :1157 build the root as Path('.') (run from a seat worktree the test reads the LIVE sessions dir); test_rotate.py:1850/1879/1887/2077 are the tests that pay 2.0 s each polling _read_ack at its default poll_s (eight payers, ~16 s of the file's wall time) + :1863 a writer thread sleep(1); test_grid.py:328 the assertion message drops git's stderr so a red run names nothing. CLAIM — every edit is behaviour-preserving for the code under test (same assertion targets; no red->green flip without a code change) and: (1) test_rotate_templates reads startup.delivery from the live node through the SAME accessor rotate.py's reader uses (import it; never a second parser), and the F16 carve-out is keyed by the fact id F16 not a phrase; (2) every after_join test root derives from tmp_path — grep Path('.') and Path('.')-equivalents (Path(), os.getcwd()) in that file returns nothing; (3) the eight payers pass poll_s=0.05 and the writer thread uses a threading.Event or a 0.05 s sleep; the file's wall time drops >= 12 s measured before/after with python3 -m pytest extensions/agi/tests/test_rotate.py -q --durations=12 (both numbers in the node); (4) test_grid's message includes the CompletedProcess stderr. FALSIFIERS: a non-test file in the diff; a test whose assertion target changed; a wall-time drop < 12 s; a second template parser. TESTS: the four files themselves — run each alone, then the rotate nbhd (test_rotate*.py test_session_start*.py test_after_join_service.py test_bin_help_smoke.py). FILE SCOPE: extensions/agi/tests/test_rotate_templates.py; test_after_join_service.py — the two root lines ONLY (SL7.88/93 append to this file: nothing else in it moves); test_rotate.py — the eight poll_s call sites + :1863 ONLY (SL7.91 appends pin tests: nothing else moves); test_grid.py:328. EXCLUDED: everything under extensions/agi/bin and extensions/agi/hooks; conftest.py. CEILING: <= 15 edited lines across four files; before/after durations in the node."
thought_session: sensei-director-genXVII-L17
title: "test-only: test_rotate_templates reads the live startup.delivery key through rotate's own accessor (F16 carve-out keyed by id); test_after_join_service roots derive from tmp_path never Path('.'); the eight 2.0 s _read_ack payers poll at 0.05 s and the writer thread does not sleep(1); test_grid's failure message keeps git stderr"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-test-only-templates-read-startup-delivery-after-join-roots-are-tmp-paths-read-ack-payers-poll-fast-and-test-grid-keeps-git-stderr

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
