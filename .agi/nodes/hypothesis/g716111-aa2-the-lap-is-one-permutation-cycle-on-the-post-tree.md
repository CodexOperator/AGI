---
id: hypothesis:g716111-aa2-the-lap-is-one-permutation-cycle-on-the-post-tree
mint_id: 99648934a7144a0cb214ea72a664b029
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 0bae35c15fe33e8f
season: 2
testable_claim: "On today's config:posts cells (council a real inert row, every member under it), the projection `lap-project` yields one row per dart, every image is unique, the cycle from (owner, belam) has length 2(n-1) = 18 and covers every dart; the lap restricted to a subtree T returns after exactly 2|T| darts ((council, SM) = 4, (belam, council) = 16)."
title: "AA2: PHI on the post tree's darts, projected from the parent cells into .geometry/lap.tsv, is a permutation with ONE cycle that covers every dart, and a subtree lap is 2|T| darts"
town: core
---
# hypothesis:g716111-aa2-the-lap-is-one-permutation-cycle-on-the-post-tree

## Measured
- doc:radically-simple-engine §AA2 (posts/self-perpetuating e2230f5cf): scratch PASS AA2.1 (18-cycle) and AA2.3 (4, 16); AA2.2 measured the OLD cells broken: the owner cycle covers 8 of 16 darts.
- belam's ruling ec5daa28a (council a real inert row; three members <- belam), then 1efd017e6 (the five under council) changes the tree the 18 was measured on: the round RE-MEASURES on the live cells.

## CLAIM
On today's config:posts cells (council a real inert row, every member under it), the projection `lap-project` yields one row per dart, every image is unique, the cycle from (owner, belam) has length 2(n-1) = 18 and covers every dart; the lap restricted to a subtree T returns after exactly 2|T| darts ((council, SM) = 4, (belam, council) = 16).

## Dispatch line
config-max: none (the lap is projected, not a cell) / template-max: none / code: lap-project (268 B awk) folded INTO grow-project; no new piece.

## FALSIFIERS
AA2.1 PHI on the live tree is a permutation with one cycle covering every dart · AA2.2 on any cells where a parent value is not a row, the cycle covers < all darts (the projection REFUSES, naming the missing row) · AA2.3 subtree laps = 2|T| · negative: the engine's piece list is unchanged (0 new pieces). · AA2.10 PHI on belam's landed cells (ec5daa28a) is one 18-cycle over all 18 darts and AA2.11 the same on the ruled cells (1efd017e6): both PASS on scratch (self-perpetuating 370cd4433), to re-run on the live cells

## TESTS
a test over a fixture posts.md (the live tree + a broken one) asserting the cycle length, uniqueness and the 2|T| rule; grow-project's own tests stay green.

## FILE SCOPE
grow-project (the fold) · the lap.tsv projection · its test. Never config:posts cells (belam's).

## CEILING
1 parent · kids <= 1 · +268 B in grow-project, expansion only · regular review.
