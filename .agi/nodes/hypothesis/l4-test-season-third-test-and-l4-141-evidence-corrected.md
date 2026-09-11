---
id: hypothesis:l4-test-season-third-test-and-l4-141-evidence-corrected
mint_id: dd3c2e4f57114ae1bb85b45f1e97c824
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-town-base-honours-the-recorded-base-branch
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 8710d2c1e552160a
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-27: L4.141 stated three tests and landed two — the third ('explicit --target beats both the recorded base and the current branch') is missing from extensions/agi/tests/test_season.py; and L4.141's evidence paragraph calls its own stderr regression 'pre-existing' (the 11 stderr removals were its own, restored by L4.145). CLAIM: test_season.py gains `test_explicit_target_beats_both` (recorded base X, current branch Y, `--target Z` -> Z wins, asserted on the resolved base); the L4.141 experiment's evidence paragraph carries a director correction note (written by the director at harvest, not by the kid). TESTS: the one test. FALSIFIER: the test absent or asserting anything but Z. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/test_season.py ONLY (append; a live round on that file -> a new file test_season_target.py, state which). EXCLUDED: season.py."
thought_session: sanctuary-director-gen12
title: test_season.py gains the stated third test (explicit --target beats both) and L4.141's evidence paragraph is corrected
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-test-season-third-test-and-l4-141-evidence-corrected

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-27: L4.141 stated three tests and landed two — the third ('explicit --target beats both the recorded base and the current branch') is missing from extensions/agi/tests/test_season.py; and L4.141's evidence paragraph calls its own stderr regression 'pre-existing' (the 11 stderr removals were its own, restored by L4.145). CLAIM: test_season.py gains `test_explicit_target_beats_both` (recorded base X, current branch Y, `--target Z` -> Z wins, asserted on the resolved base); the L4.141 experiment's evidence paragraph carries a director correction note (written by the director at harvest, not by the kid). TESTS: the one test. FALSIFIER: the test absent or asserting anything but Z. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/test_season.py ONLY (append; a live round on that file -> a new file test_season_target.py, state which). EXCLUDED: season.py.
