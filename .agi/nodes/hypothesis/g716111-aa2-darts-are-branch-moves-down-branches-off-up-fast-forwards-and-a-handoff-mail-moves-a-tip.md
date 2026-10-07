---
id: hypothesis:g716111-aa2-darts-are-branch-moves-down-branches-off-up-fast-forwards-and-a-handoff-mail-moves-a-tip
mint_id: 7da8e11b36874ae6b90196a3e3493463
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 16da1d610175261b
season: 2
testable_claim: "On the ruled cells (1efd017e6) PHI's 18 darts = 9 DOWN + 9 UP (AA2.12); a child's tip moves only when the parent's signed, adjacency-checked handoff mail `posts/<parent>@sha` arrives (AA2.17): to the parent's sha, or a two-parent commit-tree over a clean merge-tree when the child holds unlanded versions; a conflict is refused and kept; a stop and a turn move nothing; nothing moves sideways and nothing skips a level; agi-flush's per-stop `git merge trunk` retires (-61 B)."
title: "AA2.12/17: PHI's 18 darts read as branch moves -- DOWN (u = parent(v)) means v branches off u's tip, UP means u may fast-forward to v's tip -- and a child's tip moves ONLY on its parent's handoff mail, never per turn or per stop"
town: core
---
# hypothesis:g716111-aa2-darts-are-branch-moves-down-branches-off-up-fast-forwards-and-a-handoff-mail-moves-a-tip

## Measured
- doc:radically-simple-engine AA2 VERSIONING (posts/self-perpetuating 370cd4433; belam 00:25Z [decision]; owner 00:3x-00:4xZ: 'the next post in the figure eight loop can only have access to the post branches of the post/posts placed directly before it in the work loop. SDG1 gets the council branch and they branch off it, and then the council branch only has permission to merge/fast forward stuff from SM').
- The work petal: council DOWN SM DOWN DG1 UP SM UP (lands) council UP belam. The rule has no new state: DOWN/UP is read off the parent cell and lands(u) is one optional cell (the council row carries lands: [sanctuary-master] on the trunk since b6b2c33d3).
- Falsifiers marked PASS on scratch: AA2.12; AA2.17 is DG1's build.

## CLAIM
On the ruled cells (1efd017e6) PHI's 18 darts = 9 DOWN + 9 UP (AA2.12); a child's tip moves only when the parent's signed, adjacency-checked handoff mail `posts/<parent>@sha` arrives (AA2.17): to the parent's sha, or a two-parent commit-tree over a clean merge-tree when the child holds unlanded versions; a conflict is refused and kept; a stop and a turn move nothing; nothing moves sideways and nothing skips a level; agi-flush's per-stop `git merge trunk` retires (-61 B).

## Dispatch line
config-max: none new (the lands cell exists) / template-max: none / code: agi-flush's trunk merge retires (-61 B); the DOWN merge-tree + commit-tree is charged to AA1.V's surface.

## FALSIFIERS
AA2.12 PHI's 18 darts on the ruled cells = 9 DOWN + 9 UP · AA2.17 a child's tip moves only on a DOWN handoff mail; a stop and a turn move nothing · a conflicting handoff is refused and kept · negative: `git grep -n 'merge trunk' -- <agi-flush>` returns 0 hits.

## TESTS
a scratch repo with the ruled cells: a DOWN handoff fast-forwards, a diverged child gets a two-parent commit over a clean merge-tree, a conflict is refused; the stop/turn no-move asserted.

## FILE SCOPE
agi-flush (the retirement) · the handoff mail verb in box · tests. HORIZON behind the boxes and the grid-commit hypotheses.

## CEILING
1 parent · kids <= 1 · net -61 B (agi-flush) · regular review.
