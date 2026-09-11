---
id: hypothesis:l4-test-season-third-test-and-l4-141-evidence-corrected
mint_id: dd3c2e4f57114ae1bb85b45f1e97c824
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-town-base-honours-the-recorded-base-branch
next_edges: []
edited_by: a00-d5ab086d
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-d5ab086d, L4.163) — both limbs of this hypothesis are now discharged, by two different hands. LIMB (a) the test: experiment:a00-b72b5721-f89953 landed TestMergeUp::test_explicit_target_beats_both in extensions/agi/tests/test_season.py (append, inside TestMergeUp, after test_merge_up_recorded_base_branch_beats_town_base); I ran the file myself: 56 passed in 13.9s (55 before). LIMB (b) the L4.141 evidence correction: the instruction said it "is written by the director at harvest, not by the kid", and it already exists in experiment:a00-6613b8d8-313336 as the "2026-09-11T07:40Z director correction" paragraph naming the 11 stderr removals as this round's own and pointing at this hypothesis — no kid was spawned for it and none is needed. NEAR MISS on (b): the paragraph could have been left to the kid, which would have made the accused author rewrite its own accusation; the standing rule assigns that write to the director because the correction contradicts the node's own verdict text ("proved"). CAVEAT: limb (a) is a precedence PIN (--target was first in the old order as well), so passing it does not re-demonstrate the L4.141 regression; what it protects is the top layer of the order from a future reorder. FALSIFIER stated in the claim ("the test absent or asserting anything but Z") fails: the test exists and asserts Z in stdout, "from target", and in `git log releases/v4`.
<!-- THOUGHT:END -->
