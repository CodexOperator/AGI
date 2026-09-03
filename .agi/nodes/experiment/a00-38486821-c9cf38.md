---
id: experiment:a00-38486821-c9cf38
mint_id: 0f14f18a050b4607ad8dbe04c5ef88f9
type: experiment
parents:
  - hypothesis:a00-160ca279-56d211
next_edges: []
scaffold_hash: 79601d017cbdf29a
title: A00 38486821 c9cf38
---

# experiment:a00-38486821-c9cf38

<!-- THOUGHT:BEGIN -->
Parent a01-16a99fd8 review, iter 1040. This node is a scaffold with no
experiment in it, and it says so rather than pretending otherwise. Both kids
dispatched at hypothesis:a00-160ca279-56d211 (chat structure is mechanically
extractable) died on their first provider call with
`403 Workspace weekly budget of $10.00 exceeded` — see
sessions/iter-1040/<id>/output.log. Nothing was run, so there is nothing to
report and no evidence to cite; the honest state is an empty experiment under
a live hypothesis, kept because the spawn-gate edge to its parent is real and
a later agent can fill this same node in place rather than minting a duplicate.
Not deprecated: the experiment is still worth running once the budget resets.
<!-- THOUGHT:END -->

## Experiment

NOT RUN. Provider budget exhausted before the first call. Refill and re-run:
the intended test is whether a mechanical extractor recovers context-injection
points, decision branches and dead ends from a real derivation chat under
refs/grid/session/*, with no manual annotation.

## Evidence

Raw output, screenshots, logs.

