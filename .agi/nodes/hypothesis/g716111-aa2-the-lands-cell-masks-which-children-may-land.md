---
id: hypothesis:g716111-aa2-the-lands-cell-masks-which-children-may-land
mint_id: 23802cd0c2cf469789f45879e0b44ca3
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: fa034f2a9ca24798
season: 2
testable_claim: "With the cell `lands` on the council row naming sanctuary-master, a council member landing alive is refused `council lands only sanctuary-master` (lane 3g of AA3.9), while every other lane is unchanged; with no cell a row's children all may land; the rule is ff(P) = the UP-darts into P times the `lands` cell on P's row (a projection of the parent cells, not new engine code)."
title: "AA2.11: a `lands` cell on a row masks which of its children may land (no cell = all children); the council row carries `lands: ['sanctuary-master']`, so only SM lands for council, enforced in ONE line of agi-land"
town: core
---
# hypothesis:g716111-aa2-the-lands-cell-masks-which-children-may-land

## Measured
- doc:rse-aa3-land AA3.11 (AA2 defines, AA3 enforces; self-perpetuating 00:4xZ): agi-land enforces it in ONE line after the edge check (+294 B, 1,503 -> 1,797); measured lane 3g on a scratch trunk carrying the cell = refused; it read FAIL on the real trunk until belam wrote the council `lands` cell (b6b2c33d3, 01:0xZ), after which 3g is ok.
- Owner line carried by AA2: 'council only from SM'.
- The cell is a row cell: the Prime (belam) writes it; this leaf names it, it does not edit config:posts.

## CLAIM
With the cell `lands` on the council row naming sanctuary-master, a council member landing alive is refused `council lands only sanctuary-master` (lane 3g of AA3.9), while every other lane is unchanged; with no cell a row's children all may land; the rule is ff(P) = the UP-darts into P times the `lands` cell on P's row (a projection of the parent cells, not new engine code).

## Dispatch line
config-max: the `lands` cell on the council row of config:posts (belam's) / template-max: none / code: the one-line mask check in agi-land (AA3's hypothesis, counted in its 1,797 B).

## FALSIFIERS
AA3.9 lane 3g reads `ok` (the cell exists on the trunk since b6b2c33d3; it was FAIL before) · negative: delete the cell and 3g flips to FAIL while the other 12 lanes stay ok. · AA2.16 AA3's land refuses an UP outside lands(P) and a non-ff: PASS on scratch via all-is-one's lane 3g; the council row carries `lands: [sanctuary-master]` on the trunk since b6b2c33d3, so 3g is ok live

## TESTS
lanes.sh (AA3.9) with and without the cell on a scratch trunk.

## FILE SCOPE
config:posts council row (cell, the Prime's) · agi-land (counted in the land hypothesis). No code of its own.

## CEILING
1 parent · kids <= 1 · 0 B in the zygote · regular review.
