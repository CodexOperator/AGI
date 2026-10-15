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
testable_claim: "REDIRECTED by sanctuary-master (SM.62 review, 5aaa654fc, corrects the original director brief): the original diagnosis was wrong about WHERE the hand-spelled literal lives. Measured (SM, grep rotate.py): the ONLY season2/posts-shaped literal in the merged rotate.py is a DOCSTRING mention at rotate.py:3484, not a string built/returned by the legacy-arm code itself. CLAIM: do NOT add an entry to PINNED in test_branch_spelling_grep.py -- the inventory exists to name hand-spelled literals that need triage, and a docstring mention is exactly the kind of hit that should be REMOVED by rewording, not grandfathered in. Fix: reword the docstring line at rotate.py:3484 so it no longer spells the literal path shape (e.g. describe it as a legacy town-less post ref instead of spelling season2/posts/<name>). FALSIFIERS: PINNED gains a new entry; any file other than rotate.py is touched; the docstring still spells the literal after the edit; either test_branch_spelling_grep.py test still fails. TESTS: test_branch_spelling_grep.py (both named tests) green afterward, byte-identical otherwise; no new test needed. FILE SCOPE: extensions/agi/bin/rotate.py, line 3484 ONLY -- the docstring, not the logic. test file untouched. CEILING: <=2 production lines, 1 kid, no --cap."
title: L4 sm62 repins the branch spelling grep inventory for the legacy town less rename arm
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-sm62-repins-the-branch-spelling-grep-inventory-for-the-legacy-town-less-rename-arm

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
