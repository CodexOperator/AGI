---
id: hypothesis:g716111-skills-load-matrix-excludes-by-sparse-checkout-not-by-deletion
mint_id: 1dc3f7624d5d476bab9671d5a5c9ccb7
type: hypothesis
parents:
  - goal:g7.16.1.11.14
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 3d00fc114b23a66a
season: 2
testable_claim: "With a per-worktree sparse-checkout that marks agi-node-write skip-worktree, `git status` in the v4 worktree shows 0 deleted paths and agi-turn's `add -A` stages 0 D, and the loaded skill listing for that post lacks agi-node-write; a deleted committed symlink would have landed the deletion for every post."
title: "Skills: a v4 post's load matrix excludes agi-node-write (and carries the agi-rotate / agi-post / agi-goal deltas) through a per-worktree sparse-checkout, so agi-turn's `add -A` never stages a skill deletion"
town: core
---
# hypothesis:g716111-skills-load-matrix-excludes-by-sparse-checkout-not-by-deletion

## Measured
- doc:radically-simple-engine §AA2 / doc:rse-aa1-boxes AA1.S: 'The exclusion cannot be a deleted symlink: agi-turn's `add -A` commits the deletion and the next land removes the skill for EVERY post (all-is-one, measured).' agi-rotate's delta is AA2's (alive 23:5xZ correction).
- The rotate / post / goal deltas: rotation = an out-line + a fresh generation key; a post = a child ROW; a goal = a plain node file committed by agi-turn.

## CLAIM
With a per-worktree sparse-checkout that marks agi-node-write skip-worktree, `git status` in the v4 worktree shows 0 deleted paths and agi-turn's `add -A` stages 0 D, and the loaded skill listing for that post lacks agi-node-write; a deleted committed symlink would have landed the deletion for every post.

## Dispatch line
config-max: the load matrix cell (which skills a row loads) / template-max: none / code: the sparse-checkout setup at post stand-up.

## FALSIFIERS
`git sparse-checkout list` in a v4 worktree names the exclusion; `git status --porcelain | grep -c '^ D'` = 0 after `git add -A`; negative: the committed .claude/skills link for agi-node-write still exists on the trunk. · AA2.9 the `skills` matrix row's sparse line removes agi-node-write from the post's tree on BOTH harness paths, git status clean, MAIN untouched: PASS on scratch (self-perpetuating 370cd4433)

## TESTS
a scratch repo test: sparse-checkout + add -A stages 0 deletions; the old-setup posts still load all skills.

## FILE SCOPE
the post stand-up (agi-post) + the load matrix cell. HORIZON.

## CEILING
1 parent · kids <= 1 · regular review.
