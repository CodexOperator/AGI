---
id: hypothesis:g716111-aa2-the-engine-base-fits-8-kb-with-boxes-and-lap-as-expansion
mint_id: 271f6409f7154f64acc608119e73d762
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 1df6ac8d9262a682
season: 2
testable_claim: "`wc -c` of config:engine <= 8192 and `agi-gate HEAD` rc 0 on the built tree; the seed (section T.1) is 1,023 B unchanged; the box script, lap-project, the route check and lap mode live in engine-wrap / grow-project / grow-gate / agi-send (expansion), so the zygote does not grow."
title: "AA2: after the council row, the three matrix rows and the pi-path move, config:engine is <= 8,192 B with the 1,023 B seed unchanged and agi-gate HEAD green; boxes and the lap add 0 B to the zygote"
town: core
---
# hypothesis:g716111-aa2-the-engine-base-fits-8-kb-with-boxes-and-lap-as-expansion

## Measured
- today config:engine = 8,298 B (AA2) / 8,283 B (AA3's count), 91-106 over 8,192 before this bundle.
- OPEN for the owner (AA3.5): is the 8 KB base config:engine alone, or every engine*.md (34,885 B)? The owner's 23:2xZ line ('the graph can hold as much as you want, just the engine itself needs to be tiny') reads as the zygote. The round MEASURES both and states which it met.

## CLAIM
`wc -c` of config:engine <= 8192 and `agi-gate HEAD` rc 0 on the built tree; the seed (section T.1) is 1,023 B unchanged; the box script, lap-project, the route check and lap mode live in engine-wrap / grow-project / grow-gate / agi-send (expansion), so the zygote does not grow.

## Dispatch line
config-max: moves only (pi-path resolution -> engine-wrap -332 B; rows +110 B; one map line +70 B) / template-max: none / code: none new.

## FALSIFIERS
AA2.4 config:engine <= 8,192 B after the move and `agi-gate HEAD` rc 0 · the seed byte count unchanged · negative: `git diff --stat` shows no new piece file.

## TESTS
agi-gate on the built tree; a size assertion test over config:engine (belongs with the engine's own size guard if one exists, else one new row).

## FILE SCOPE
config:engine · config:engine-wrap (the moved block) · this hypothesis's kid node. The Prime lands cells it owns.

## CEILING
1 parent · kids <= 1 · net bytes in config:engine <= 0 · regular review.
