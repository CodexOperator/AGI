---
id: hypothesis:l5-the-spawn-behind-gate-merges-the-season-trunk-not-the-town-resolved-target
mint_id: 5c53aff8f3474363879e2dac1805512b
type: hypothesis
parents:
  - hypothesis:l4-spawn-from-a-worktree-merges-origin-first-or-refuses-when-behind
next_edges: []
edited_by: director-belam
scaffold_hash: b25017880eeb00d2
season: 2
testable_claim: "L5.19 demoted (experiment:a00-462aae44-d8e1b8, inconclusive_lean_disproved:45): _spawn_behind_gate (rotate.py:15391, from the demoted round, unmerged branch season2/loops/hypothesis-l4-spawn-from-a-workt-a00-3ad5891f commit 3cf20b1ae) resolves its merge ref via season_branch(root), which always yields the literal season2/main trunk, while its own docstring claims parity with rotate-self check 3, which actually resolves via _prepare_merge_target(root) (rotate.py:15681) routing a post or loop branch through branches.merge_target (rotate.py:15491-15515) to the TOWN-scoped main, not the literal season trunk (measured: origin/season2/main is 107 commits ahead of origin/core/season2/main on this tree). Claim: change _spawn_behind_gate to call _prepare_merge_target(root) instead of season_branch(root), so a worktree-post spawn merges the same ref its own rotation gate would merge, closing the cross-trunk contamination gap the mechanism otherwise has; add a committed test presenting a post or loop HEAD (not monkeypatching season_branch itself, as the demoted round test suite did) and asserting the gate resolves and merges the town-scoped target."
title: L5 the spawn behind gate merges the season trunk not the town resolved target
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-the-spawn-behind-gate-merges-the-season-trunk-not-the-town-resolved-target

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
CARRIED to the next loop per belam [decision] 23:32Z: not a g19 done-state blocker, no live exposure (never merged to season2/main), L5 stays small -- no round dispatched. One-line fix stays: call _prepare_merge_target(root) instead of season_branch(root) in _spawn_behind_gate (rotate.py:15391). Untested seam to close when picked up: the demoted round own test suite monkeypatched season_branch itself, so a post or loop HEAD was never actually presented to the gate.
