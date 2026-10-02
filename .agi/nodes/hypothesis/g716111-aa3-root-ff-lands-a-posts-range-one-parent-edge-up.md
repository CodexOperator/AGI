---
id: hypothesis:g716111-aa3-root-ff-lands-a-posts-range-one-parent-edge-up
mint_id: 20dc8d441f6a46458ee5cb3473e1595c
type: hypothesis
parents:
  - goal:g7.16.1.11.13
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 9afb012104b8534a
season: 2
testable_claim: "All 13 lanes of AA3.3 + AA3.11 + 4m reproduce on a scratch clone: SM lands DG1 (land); a forged commit (alive's key, committer DG1) is refused `signed by alive: not SM, not under DG1`; SM lands alive and DG1 lands itself or its parent are refused; a council member lands SM and belam lands itself (land); a parentless hypothesis is refused by grow-gate; a not-ff range is refused; with no `members` cell nobody lands for council; and a council member landing alive is refused by the council row's `lands: ['sanctuary-master']` mask (lane 3g). agi-land <= 1,797 B in engine-root."
title: "AA3: agi-land ff-lands <post>'s range on the trunk only when the sender is the post's parent (council by the `members` cell, fail-closed), every commit is ring-signed by the sender or a post under <post>, grow-gate and agi-gate pass, and the move is a compare-and-swap"
town: core
---
# hypothesis:g716111-aa3-root-ff-lands-a-posts-range-one-parent-edge-up

## Measured
- doc:rse-aa3-land (posts/all-is-one 142c2a8e4): 11 lanes on a scratch repo with alternates, 0 shared refs written; the first draft let lane 3b (DG1 lands itself) land: 'every signer is the sender or under it' holds trivially when the sender signs everything; the edge check closed it.
- AA3.8: today's trunk 1efd017e6 without the cell refuses every council land; faabf9b7a (belam wrote members) = 11/11 lanes right.
- DEPENDS ON the byte-fixes hypothesis, the ring (goal:g7.16.1.11.12) and the box mail to root (goal:g7.16.1.11.11).

## CLAIM
All 13 lanes of AA3.3 + AA3.11 + 4m reproduce on a scratch clone: SM lands DG1 (land); a forged commit (alive's key, committer DG1) is refused `signed by alive: not SM, not under DG1`; SM lands alive and DG1 lands itself or its parent are refused; a council member lands SM and belam lands itself (land); a parentless hypothesis is refused by grow-gate; a not-ff range is refused; with no `members` cell nobody lands for council; and a council member landing alive is refused by the council row's `lands: ['sanctuary-master']` mask (lane 3g). agi-land <= 1,797 B in engine-root.

## Dispatch line
config-max: the council row's `members` cell (belam's, written) / template-max: none / code: agi-land in config:engine-root (+1,797 B, root-side, of which +294 B enforce AA2's `lands` mask in one line) + AA2's `lands` cell on the council row.

## FALSIFIERS
AA3.1 every lane in AA3.3 reproduces on the real ring + real trunk cells (scratch clone, never MAIN) · AA3.2 a land whose range holds one commit signed by a post outside <post>'s subtree moves nothing · negative: remove the `members` cell and the lanes 3c/3d refuse.

## TESTS
the 13-lane script = AA3.9 of doc:rse-aa3-land (lanes.sh, extracted from the doc and run against a scratch clone) as the minimum test set; it must read 13 `ok` with agi-land from AA3.2 (or $AGI_LAND) AFTER the byte-fixes hypothesis landed (before the four byte fixes: 11 ok + `FAIL 4m` + `FAIL 4v`; belam wrote the council `lands` cell, so 3g is ok); one live dry-run lane against the real cells with the update-ref replaced by an echo.

## FILE SCOPE
config:engine-root (agi-land) · the lane script · this hypothesis's kid node. Never the live trunk ref before the owner's go on the build.

## CEILING
1 parent · kids <= 2 · agi-land <= 1,797 B · 0 B in the zygote · regular review. HORIZON behind the byte fixes.
