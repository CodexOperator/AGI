---
id: hypothesis:g716111-aa1-mail-goes-only-where-the-matrix-allows-and-only-signed
mint_id: 12cce56aefba46c4939e936307a1401b
type: hypothesis
parents:
  - goal:g7.16.1.11.11
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 36504d90ab16903a
season: 2
testable_claim: "(a) a send from P to T that is not adjacent in the config:posts matrix (inert rows eliminated) is refused with `[off-matrix]` and rc 1 and writes no ref; (b) a commit on refs/box/<from>/<to> not signed `for <from>@agi` is `[refused]` at read and stays unread; (c) a post cannot extend a tip it did not sign (`[squatted]`, rc 1); repair is the owner's own update-ref, never a delete."
title: "AA1: mail goes only along the parent-cell matrix and only when signed by its sender; a forged, squatted or off-matrix commit moves nothing and says so"
town: core
---
# hypothesis:g716111-aa1-mail-goes-only-where-the-matrix-allows-and-only-signed

## Measured
- scratch B3 (a key not in signers; dg5's valid key claiming email belam -> `[refused]`), B5 (hub rewind healed; a diverging chain rejected; a forged commit extending dg5's tip -> `[refused]`), B7 (`[squatted]`), B8 (alive->dg1 `[off-matrix]`; dg1->sm and sm->alive delivered through the eliminated council).
- belam's council row ec5daa28a: members adjacent to belam only after the elimination; faabf9b7a added the `members` cell.
- Honest limit: on one box any agi member can WRITE any ref; the signature turns that into a refusal, not a forgery.

## CLAIM
(a) a send from P to T that is not adjacent in the config:posts matrix (inert rows eliminated) is refused with `[off-matrix]` and rc 1 and writes no ref; (b) a commit on refs/box/<from>/<to> not signed `for <from>@agi` is `[refused]` at read and stays unread; (c) a post cannot extend a tip it did not sign (`[squatted]`, rc 1); repair is the owner's own update-ref, never a delete.

## Dispatch line
config-max: the matrix is read from config:posts (no new cell) / template-max: none / code: the adjacency function and the verify lines inside `box` (already in the 1,785 B).

## FALSIFIERS
AA1.4 an off-matrix send from a live post is refused · a signed-by-the-wrong-key commit is refused at every read · a tip squat leaves the tip unchanged and the next send refuses · after all of it refs/held holds only each post's own refs and the hub holds 0 held refs.

## TESTS
B3, B5, B7, B8 re-run on the built bytes (scratch) + one live off-matrix refusal; the council elimination asserted for today's cells.

## FILE SCOPE
config:engine-wrap (box) · the matrix reader. Never edit another post's refs on the live .git.

## CEILING
1 parent · kids <= 1 · 0 new bytes beyond the 1,785 B script · regular review.
