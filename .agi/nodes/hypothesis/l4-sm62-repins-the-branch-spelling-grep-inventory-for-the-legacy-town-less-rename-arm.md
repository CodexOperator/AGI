---
id: hypothesis:l4-sm62-repins-the-branch-spelling-grep-inventory-for-the-legacy-town-less-rename-arm
mint_id: 4292b4e24135463d9b251c909098686d
type: hypothesis
parents:
  - hypothesis:l4-rename-boundary-preserves-the-real-branch-project-town-and-never-compares-it-to-the-home-town
next_edges: []
edited_by: sensei-director
scaffold_hash: 20b723d62caad261
season: 2
testable_claim: "Measured (sensei-director, SM.62 harvest, this session): post-merge, test_branch_spelling_grep.py::test_no_new_hand_spelled_branch_spelling and ::test_pinned_inventory_is_not_vacuous both fail -- _scan() finds one new hand-spelled literal in rotate.py, season2/p (from season2/posts/<name>), not present in the frozen PINNED[rotate.py] list. Root cause, confirmed: SM.62 kid a00-f6520184 documented a 3-line legacy arm in _rename_post_segment that preserves a town-less real ref (season2/posts/<name>, no town key) VERBATIM rather than re-spelling it town-first -- by definition this shape cannot route through branches.py (it has no town segment to derive from), so the hand-spelled literal is deliberate, not drift. CLAIM: append the single missing entry season2/p to PINNED[rotate.py] in test_branch_spelling_grep.py (test_branch_spelling_grep.py:102-123, after the run of seven season2/m entries, matching _scan() output order) so both tests pass; no other PINNED entry changes; no production file touched. FALSIFIERS: either test still fails after the edit; any entry other than the one addition differs; a production file is touched. TESTS: test_branch_spelling_grep.py itself (both named tests) is the verification -- both green after the edit, unchanged otherwise. FILE SCOPE: extensions/agi/tests/test_branch_spelling_grep.py ONLY -- a one-line data edit, not logic. CEILING: <=5 production-equivalent lines, 1 kid, no --cap."
title: L4 sm62 repins the branch spelling grep inventory for the legacy town less rename arm
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-sm62-repins-the-branch-spelling-grep-inventory-for-the-legacy-town-less-rename-arm

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
