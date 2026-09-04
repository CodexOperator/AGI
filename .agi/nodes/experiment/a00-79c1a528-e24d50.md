---
id: experiment:a00-79c1a528-e24d50
mint_id: 5da667b3634049d28958a4ad0b76e2e2
type: experiment
parents:
  - hypothesis:loop-scoped-iteration-ids-cannot-clobber
next_edges: []
confidence: 0.6
scaffold_hash: febd4b8f889a2a4b
title: A00 79c1a528 e24d50
verdict: inconclusive_lean_proved:60
---
# experiment:a00-79c1a528-e24d50

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.


## Agent Notes
Code audit: locations.py has full claim_iteration/next_free_iteration allocator that works (refuses occupied iter-001, produces L1.01). But driver.sh still uses seq 1 MAX_ITERS — allocator exists, unwired. post_wire.py still overwrites graph.json without merge. 1454 tests pass.
