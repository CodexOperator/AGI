---
id: hypothesis:g716111-aa3-the-trunk-has-one-writer-root
mint_id: 86bd1f3d631348089d4b455c165bfa44
type: hypothesis
parents:
  - goal:g7.16.1.11.13
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: f91a21f4aac7fa5a
season: 2
testable_claim: "On the built system, every movement of the trunk ref (and of the town trunk -> season2/main) is a root-run agi-land / ff move: `git reflog <trunk>` lists no other committer; a post-side `git update-ref` or push on the trunk is refused by permission, not by convention; the hub pre-receive is no longer the ONLY gate."
title: "AA3: after the switch the trunk reflog shows root as its only writer, and belam's own config:posts commits reach the trunk through a land too"
town: core
---
# hypothesis:g716111-aa3-the-trunk-has-one-writer-root

## Measured
- doc:rse-aa3-land AA3.5-AA3.6: retires the master's hand-gated merge-up (skill agi-master-gate's landing path); agi-merge-pass's PASS becomes ONE land one edge up (the trunk = the receiving row's engine.trunk cell, the sender = its parent).
- Production difference: MAIN has the trunk CHECKED OUT, so root's last step is `git -C <MAIN> merge --ff-only`; merge refuses a non-ancestor, which IS the compare-and-swap.

## CLAIM
On the built system, every movement of the trunk ref (and of the town trunk -> season2/main) is a root-run agi-land / ff move: `git reflog <trunk>` lists no other committer; a post-side `git update-ref` or push on the trunk is refused by permission, not by convention; the hub pre-receive is no longer the ONLY gate.

## Dispatch line
config-max: each row's engine.trunk cell (exists) / template-max: none / code: the root-side switch (permissions + agi-land as the only trunk writer).

## FALSIFIERS
AA3.3 the trunk reflog shows ONLY root as the trunk writer after the switch · negative: `git update-ref <trunk>` as a post uid fails with a permission error.

## TESTS
a reflog assertion on a scratch clone; the live check is one `git reflog` read after the first real land.

## FILE SCOPE
root-side permissions + the land path. HORIZON: needs the build and the owner's go.

## CEILING
1 parent · kids <= 1 · regular review.
