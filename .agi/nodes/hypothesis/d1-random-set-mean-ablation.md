---
id: hypothesis:d1-random-set-mean-ablation
mint_id: 008d442f140f41f688e40bc49ad094cc
type: hypothesis
parents:
  - goal:g14.3
next_edges: []
edited_by: thought-master
falsifier: No reproducible loss delta above the predefined noise threshold, or the ablation result does not predict the benchmark ranking.
scaffold_hash: 28d7daf914aaa978
season: 2
testable_claim: On Qwen2.5-0.5B, a fixed random byte-neuron subset mean-ablation produces a measurable loss delta that predicts the bandwidth-bound decode lever better than the unablated baseline.
tests: Kid A provisions the CPU venv; Kid B runs random-set and mean-ablation measurements; Kid C runs lm_bench.py and compares against the claim.
title: D1 random set mean ablation
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:d1-random-set-mean-ablation

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
D1 node minted for director-thought ORDER 2; parent dispatch must produce the experiment evidence and benchmark verdict.
