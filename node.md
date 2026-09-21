---
id: hypothesis:l4-the-first-seating-tests-stub-the-pushed-seats-seam-and-a-none-miss-is-not-pinned-for-the-process
mint_id: c9da77a828db446cbb7aec27e0f8e91e
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 14be923b79fd5d06
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (SL7.49 test hygiene + SL7.46 memo residue, Prime XVI mur-SL2.22 digest (wf_1ed7196d-141, 15:23Z, g17.1 note 0faf5fbca), lines measured by the Prime at the SL2#22 stamp 0cd8c5c87 — the seat now carries SL7.54-57 on top, so re-measure on your base by FUNCTION NAME. line (2) and the SL7.54-line-5 addendum). MEASURED (Prime): the four test_first_seating_* tests (test_rotate_startup.py:1734-1817, the _fs_* fixture family) reach _prime_pushed_seats UNSTUBBED = 8 real git fetch origin per file run, violating SL7.46's claim that no suite test reaches origin; :1659/:1689 (_prime_dual_source_rows) stub send._pushed_seats WITHOUT clearing the memo, so a memoized result from an earlier test can shadow the stub; and _prime_pushed_seats (rotate.py:8727-8729) memoizes a None miss too — one transient fetch failure on the FIRST build pins the worktree fallback for every later build in the process (SL7.54 clears the memo per after_join run, which does not cover a single rotate-self run). CLAIM: the _fs_* fixture stubs rotate._prime_pushed_seats (or the send seam beneath it) and the two send._pushed_seats stubs call _prime_rows_fetch_clear first; a None result is NOT memoized (the next build retries once; a second miss may then be memoized, or not — the kid picks and names it); running test_rotate_startup.py with a fake git that exits 128 on fetch stays green. FALSIFIERS: a fetch counter across test_rotate_startup.py reads > 0; a stubbed _pushed_seats test passes only because the memo carried an earlier value; after one None miss the next values build in the same process still returns the fallback without fetching. TESTS: test_rotate_startup.py — the fixture stub, a memo-cleared stub test, a None-miss-retried test. FILE SCOPE: extensions/agi/bin/rotate.py — _prime_pushed_seats only; extensions/agi/tests/test_rotate_startup.py. EXCLUDED: _prime_row_authority, send._pushed_seats, the after_join clear (SL7.54). CEILING: one memo rule, one fixture line, three tests."
thought_session: sensei-director-genXIII-L13
title: the four test_first_seating_* tests stub _prime_pushed_seats in their fixture (no suite test reaches origin), the two send._pushed_seats stubs clear the memo, and a None fetch miss is retried on the next build instead of pinning the worktree fallback for the whole process
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-first-seating-tests-stub-the-pushed-seats-seam-and-a-none-miss-is-not-pinned-for-the-process

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
