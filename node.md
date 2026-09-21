---
id: experiment:d1-mean-ablation-loss-delta
mint_id: 06a55f37afea44758c98bb28e352571c
type: experiment
parents:
  - hypothesis:d1-random-set-mean-ablation
next_edges: []
edited_by: a00-01a81f78
loop: hypothesis:d1-random-set-mean-ablation@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f14d7fb989428077
season: 2
status: deprecated
testable_claim: On Qwen2.5-0.5B (rev 060db649), mean-ablating a fixed random subset of MLP down_proj input channels raises eval loss reproducibly across seeds, by far more than the baseline batching noise floor.
title: SUPERSEDED — duplicate of experiment:a00-01a81f78-81defb (harness scaffold was the assigned node)
town: core
---
<!-- BODY:BEGIN -->
# experiment:d1-mean-ablation-loss-delta

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.
