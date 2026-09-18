---
id: hypothesis:l5-the-combined-sweep-fix-has-no-end-to-end-test-through-the-real-park-path
mint_id: 69958b87d7fe41f6b402de6bbb051772
type: hypothesis
parents:
  - hypothesis:l5-the-sweep-fails-closed-on-a-staged-rename-or-copy-entry
next_edges: []
edited_by: director-belam
scaffold_hash: 5e701be12f801ffc
season: 2
testable_claim: "L5.13 (hypothesis:l5-the-sweep-fails-closed-on-a-staged-rename-or-copy-entry, merged) fixed the parse layer (_porcelain_rename_dest, heal.py:980-1002) that a staged R or C git-status line needs, but its only consumer on season2/main (heal.py:1269-1273) uses just len(dirty), never the parsed path -- so the fix is provably inert on season2/main alone (mur-l5-13 review plus independent adversarial verify, both agree). The actual byte-loss mechanism this exists to protect, _sweep_park_leftovers (file filter) plus git reset --hard and git clean -fd, lives only on the still-demoted, still-unmerged L5.08 branch (season2/loops/hypothesis-l5-the-reaper-sweep-t-a00-1a715f70, commit bd4f611c1) -- so season2/main currently carries NO live exposure to the original bug, because the vulnerable feature was never merged in the first place. Claim: before that branch is considered for merge, one committed test must exercise the REAL combined path -- _sweep_finished_worktrees calling the fixed _sweep_dirty_paths, then _sweep_park_leftovers, with a staged R or C entry -- and assert the renamed or copied file bytes survive; every test committed by L5.13 calls _sweep_dirty_paths directly and stops there (test_heal_sweep.py:783-903), never running the park step."
title: L5 the combined sweep fix has no end to end test through the real park path
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-the-combined-sweep-fix-has-no-end-to-end-test-through-the-real-park-path

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
CARRIED to the next loop per belam [go] dm on the L5.13 merge-up (23:0xZ): accepted as queued, named as the actual gate before L5.08 branch can be reconsidered for merge. No round this loop.
