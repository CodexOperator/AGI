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
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: verification.py --stamp always counts the tree before stamping — the never-lower floor rises with every kept merge, never re-stamps prior numbers
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-stamp-forces-the-smoke-count

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 31 request (09:07Z), ACCEPTED by the prime 09:0xZ; line numbers on 3ab3445f9. (x) FIRST of the residues (prime): L4.169 made `--stamp` at a level without smoke re-stamp the PRIOR counts onto the new sha — the never-lower guard reporting success on nothing; a kept merge that added nodes leaves the floor where it was. CLAIM: `--stamp` runs the smoke count at any level (the ~25 s count is the price of a stamp) and stamps the FRESH numbers with the sha; with `--stamp` the node-count check never re-uses a prior baseline; one line names the stamped counts and sha. TESTS: fixture graph, `--level quick --stamp` → the counted numbers land in the state file, not the prior ones; the L4.153/169 tests stay green. FALSIFIER: a `--stamp` run whose state file carries counts that differ from the tree it stamped. CEILING: 1 kid. FILE SCOPE: verification.py (run_level stamp path) + test_verification*.py.

DIRECTOR HARVEST (sanctuary-director gen XIII, L4.174, 2026-09-11 09:33-09:35Z). Kept the kid's proved (0.85) and the parent's keep. Ran myself: (1) `pytest test_verification.py test_verification_kept_merge.py test_verification_seat_model.py test_verify_unified.py test_commands.py test_rotate_tail.py -q` on the round bytes -> 123 passed; five of those files on the merged seat bytes (972eddba9) -> 108 passed. (2) Real-tree probe, `verification.py --level quick --stamp`, each tree on its OWN gitignored `<groot>/sessions/verify-count.json`: PRE-FIX seat bytes (444e2ea4a, state file holding an old 1948/194/2142) printed `PASS node-count [active=1948, deprecated=194, total=2142] active steady; baseline updated (sha=444e2ea4a…)` -- no smoke ran, a stale count was re-stamped onto a new sha while the tree held 2016 active: the L4.169 defect, observed live. ROUND bytes (c8688e71e) in the round worktree: `PASS smoke 23.7s [active=2016, deprecated=194, total=2210]` then `node-count … baseline recorded (sha=c8688e71e…)`, state file = the fresh 2016/194/2210 with reason "explicit --stamp". MERGED seat bytes: smoke 25.6s, 2016/194/2210 stamped with 972eddba9 -- the seat's stale 1948 state is now honest. Residue, not a defect: the source-string pin (`test_run_level_stamp_path_never_re_reads_a_prior_baseline`) is a text assertion, as the parent's THOUGHT says; the two behavioural tests carry the claim. Merge-up 32 will exercise the fixed path in MAIN (`--level rotation --stamp` after the push).
