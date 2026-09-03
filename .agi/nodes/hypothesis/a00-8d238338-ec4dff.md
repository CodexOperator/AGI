---
id: hypothesis:a00-8d238338-ec4dff
mint_id: 1bc9bd353ec44374b69b3b30fa9666e0
type: hypothesis
parents:
  - goal:g4.8
next_edges:
  - experiment:a00-f0fd9669-ce583f
confidence: 0.0
scaffold_hash: 3ae0dcace5c11e52
testable_claim: With bound `B`, `N` parents each spawning `M` kids, the max concurrent process count across all N×M kids never exceeds `B`, regardless of timing skew between parent spawns.
title: A00 8d238338 ec4dff
verdict: pending
---
# hypothesis:a00-8d238338-ec4dff

## Hypothesis

A parent delegator enforcing `spawn.parallel` as a global concurrency bound across all spawned kid harnesses can keep total live processes ≤ bound, even when N parents run concurrently spawning M kids each.

### Testable claim

With bound `B`, `N` parents each spawning `M` kids, the max concurrent process count across all N×M kids never exceeds `B`, regardless of timing skew between parent spawns.

### What would prove it

An experiment running 3 parents (`N=3`), each spawning 4 kids (`M=12` total), with `spawn.parallel=2` (`B=2`):
- Max concurrent `ps` count across all kid processes ≤ 2 at every 100ms sample
- All 12 kids complete (none lost to starvation)
- Wall time > sequential because of bound, verifying bound is real not theoretical

### What would disprove it

- Any sample shows live process count > `B` (bound is broken)
- Kids fail or deadlock because bound causes starvation
- Parent completes before its kids finish (parent does not wait on bound release)

### Relation to g4.8

Directly tests falsifier clause 3 (process bound) and clause 4 (kid collisions — kids on same working tree with bounded concurrency must not collide). A passed experiment means the concurrency primitive exists; a failed one isolates whether the failure is in the bound mechanism or in working-tree collision.

<!-- Director's note, 2026-09-02: the sentence above ended `... the working tree
collisionism or the working tree collision."` — a duplicated clause, a coined
word, and a stray quote. The parent flagged two of the three as non-blocking and
did not fix them; the director repaired the text and changed no claim. Recorded
because "the parent reviewed it" and "the parent fixed it" are different
statements, and only the first is true here. -->




## Agent Notes
Proposed concurrency-bound hypothesis: spawn.parallel as global bound across N-parents × M-kids ≤ B. Tests falsifier clause 3 of g4.8.