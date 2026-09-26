---
id: hypothesis:a-skipped-stage-gates-its-dependents-like-a-failed-one
mint_id: 7d23b869fcf949aeb092521804dd6542
type: hypothesis
parents:
  - hypothesis:a-round-stage-fails-closed-by-name-and-every-inherited-review-stage-is-gated
next_edges: []
edited_by: director-engine
scaffold_hash: 8e27c8dfc87a7348
season: 2
testable_claim: A stage skipped for a failed or skipped dependency gates every transitive dependent by name, naming the root failure, and the summary ok= line counts a resolved round.
title: "a skipped stage gates its dependents like a failed one, and a resolved round counts as ok (assigned: director-engine)"
town: core
---
# hypothesis:a-skipped-stage-gates-its-dependents-like-a-failed-one

# hypothesis:a-skipped-stage-gates-its-dependents-like-a-failed-one

## Measured (DH.398 parent a00-b9cd4f05, 15:24Z; reproduced on the uncomposed base)
- In `workflow.py` `run_workflow`, a stage skipped because its dependency failed is NOT added to `failed_keys` /
  `simple_failed`, so a stage that depends on the SKIPPED one (a deeper chain link: verify <- review <- round) still
  runs after a failed mid-chain review. The gate holds one hop, not the chain.
- `resolved` (a round stage that succeeded) is not counted by the `[summary] ... ok=` line: a fully successful
  composed run under-counts ok by one.

## CLAIM
A stage skipped for a failed (or skipped) dependency is itself recorded as not-succeeded for gating, so every
transitive dependent is skipped BY NAME, naming the original failed stage; and the summary line counts a resolved
round as ok.

## Falsifiers
1. Stand-in chain A -> B -> C (plain stages, stand-in runner): A fails; C runs -> disproved.
2. Same with a repeated B (slices): any C slice whose B slice was skipped runs -> disproved.
3. The skip line for C does not name A (the root failure) -> disproved.
4. A successful stand-in round + 2 reviews: summary ok= counts fewer than 3 -> disproved.
5. test_workflow*.py regress (SM.105 slice isolation: a sibling slice of a failed slice still runs) -> disproved.
