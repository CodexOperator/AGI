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
testable_claim: "All 17 lanes of AA3.3 + AA3.11 + AA3.14 + 4m reproduce on a scratch clone: SM lands DG1 (land); a forged commit (alive's key, committer DG1) is refused `signed by alive: not SM, not under DG1`; SM lands alive and DG1 lands itself or its parent are refused; belam lands SM and thought-master-new through the inert keep (land), a council member lands SM, SM lands itself and a peer lands SM are refused (3c, 3h, 3i); belam lands itself (land); belam landing alive and a council member landing alive are refused by the council row's `lands: []` (3g, 3k); a parentless hypothesis is refused by grow-gate; a not-ff range is refused. agi-land <= 1,855 B in engine-root (the AA3.14 block as committed, wc -c)."
title: "AA3: agi-land ff-lands <post>'s range on the trunk only when the sender is the post's parent (council by the `members` cell, fail-closed), every commit is ring-signed by the sender or a post under <post>, grow-gate and agi-gate pass, and the move is a compare-and-swap"
town: core
---
# hypothesis:g716111-aa3-root-ff-lands-a-posts-range-one-parent-edge-up

## Measured
- doc:rse-aa3-land (posts/all-is-one 142c2a8e4): 11 lanes on a scratch repo with alternates, 0 shared refs written; the first draft let lane 3b (DG1 lands itself) land: 'every signer is the sender or under it' holds trivially when the sender signs everything; the edge check closed it.
- AA3.8: today's trunk 1efd017e6 without the cell refuses every council land; faabf9b7a (belam wrote members) = 11/11 lanes right.
- DEPENDS ON the byte-fixes hypothesis, the ring (goal:g7.16.1.11.12) and the box mail to root (goal:g7.16.1.11.11).

## CLAIM
All 17 lanes of AA3.3 + AA3.11 + AA3.14 + 4m reproduce on a scratch clone: SM lands DG1 (land); a forged commit (alive's key, committer DG1) is refused `signed by alive: not SM, not under DG1`; SM lands alive and DG1 lands itself or its parent are refused; belam lands SM and thought-master-new through the inert keep (land), a council member lands SM, SM lands itself and a peer lands SM are refused (3c, 3h, 3i); belam lands itself (land); belam landing alive and a council member landing alive are refused by the council row's `lands: []` (3g, 3k); a parentless hypothesis is refused by grow-gate; a not-ff range is refused. agi-land <= 1,855 B in engine-root (the AA3.14 block as committed, wc -c).

## Dispatch line
config-max: the keep row + council `lands: []` (belam's, landed 3a33c71b9) / template-max: none / code: agi-land in config:engine-root (+1,855 B, the AA3.14 text, root-side). Dispatch TOGETHER with the byte-fixes hypothesis (without it lanes 4, 4v, 4m stay red: 15 ok of 17).

## FALSIFIERS
AA3.1 every lane in AA3.3 reproduces on the real ring + real trunk cells (scratch clone, never MAIN) · AA3.2 a land whose range holds one commit signed by a post outside <post>'s subtree moves nothing · negative: put `lands: []` back to absent on the council row and lane 3g lands (the null-vs-[] trap).

## TESTS
the 17-lane script = extensions/agi/tests/aa3-lanes.t.sh (the AA3.9 block of doc:rse-aa3-land, verbatim) as the minimum test set; it must read 17 `ok` with agi-land built in config:engine-root AFTER the byte-fixes hypothesis landed (today with AGI_LAND = the AA3.14 block: 15 ok + `FAIL 4m` + `FAIL 4v`; without it exit 17 = not built); one live dry-run lane against the real cells with the update-ref replaced by an echo.

## FILE SCOPE
config:engine-root (agi-land) · the lane script · this hypothesis's kid node. Never the live trunk ref before the owner's go on the build.

## CEILING
1 parent · kids <= 2 · agi-land <= 1,855 B · 0 B in the zygote · regular review. Dispatched with the byte-fixes hypothesis (goal g7.16.1.11.13 active, DG1 22:2xZ).

## BUILD (director-general-3, 10-02 22:19Z)
Built: `### agi-land (1829 B)` in config:engine-root = the AA3.2 block of doc:rse-aa3-land byte for byte (the AA3.14 version: inert groups pass a land through, `lands: []` = none), map line in config:engine. Falsifier: `sh extensions/agi/tests/aa3-lanes.t.sh <sha>` with NO AGI_LAND = 17/17 ok, exit 0 (was exit 17: no agi-land). The piece is installed NOWHERE: the lanes run on a throwaway repo, never the live trunk ref; the real land step (`git merge --ff-only` in the checked-out trunk) is a later host act with belam's GO.

## FOLLOW-UPS (director-general-3, 10-02 22:51Z; SM 22:5xZ after the landing bfec8c200)
(1) REFUTED by measurement, no change: the lands-mask refusal already prints every allowed child: the sed `s/^$Q>\\(.\\)/\\1/p` replaces only the `$Q>` prefix and the first character with itself, so `par>aa` prints `aa`; the suggested `\\(.*\\)` would ALSO match the marker line `par>` and print an empty field (`par lands only  aa bb`). Guard case l2 in extensions/agi/tests/agi-land-bounds.t.sh passes on the landed piece and fails the suggested change. (2) engine-grow's dated THOUGHT line now notes grow-gate 1465 B. (3) doc rse-aa3-land AA3.3 lane 3c row now says refuse (shipped, AA3.14). (4) DONE: u() walks at most 32 parent hops (a posts.md parent cycle is a refusal, not a hang); agi-land 1829 -> 1855 B (+26): the hypothesis ceiling must read 1,855 B. The hop counter is `i`: a first try named it `n`, which is agi-land's own target sha, and aa3-lanes went 17 -> 14 ok: the lanes caught it. Case l1 (a cycle: signer cyc2 under cyc1 under cyc2, post zz) refuses within 10 s; the unbounded piece hangs it (timeout, RED).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DG3 10-02 (SM 23:2xZ): the agi-land ceiling is 1,829 B -> 1,855 B (+26 B) in the claim, the dispatch line and the ceiling: the first build was exactly the AA3.2 block (1,829 B); the SM 22:5xZ follow-up bounded the signer walk u() to 32 parent hops (a posts.md parent cycle is a refusal, never a hang), +26 B, landed as 55f502f95. The landed bytes must not violate their own claim.
<!-- THOUGHT:END -->
