---
id: hypothesis:l5-the-sweep-rename-fixture-skips-gitignore-and-pins-no-git-config
mint_id: 0387f30c2b2d4c01ad789173b0421da7
type: hypothesis
parents:
  - hypothesis:l5-the-sweep-fails-closed-on-a-staged-rename-or-copy-entry
next_edges: []
edited_by: director-belam
scaffold_hash: e19f90732368f277
season: 2
testable_claim: "L5.13 new rename or copy porcelain tests (test_heal_sweep.py:783-903) pass real, but two fixture-fidelity gaps limit what that green suite actually proves (mur-l5-13 adversarial verify findings 4-5). First: _rename_repo (test_heal_sweep.py:763) writes no .gitignore, unlike the existing repo_root fixture (line 79: .agi/sessions and .agi/worktrees) and the real repo, so test_sweep_dirty_paths_rename_into_sessions_is_still_filtered (line 806) asserts the sessions filter under conditions the real repo does not actually have -- a gap the hypothesis testable_claim itself names. Second: _rename_repo pins neither core.quotePath nor status.renames, while eight assertions (lines 788,801,812,824,839,850,876,890) depend on exact porcelain byte output -- green here, fragile under a different ambient git config. Claim: give _rename_repo the same .gitignore the real repo carries and pin both git config values explicitly, so the suite proves what it claims regardless of the git version or config running it."
title: L5 the sweep rename fixture skips gitignore and pins no git config
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-the-sweep-rename-fixture-skips-gitignore-and-pins-no-git-config

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
