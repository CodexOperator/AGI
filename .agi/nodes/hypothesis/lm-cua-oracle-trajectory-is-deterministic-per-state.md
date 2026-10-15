---
id: hypothesis:lm-cua-oracle-trajectory-is-deterministic-per-state
mint_id: 3a5ba6dc15964b2b9b1e4fc2408b706c
type: hypothesis
parents:
  - idea:lm-cua-bench-as-typed-acts-source
next_edges: []
edited_by: thought-master
scaffold_hash: 99324f092ec90eea
season: 2
testable_claim: "10 identical headless runs of the cua-bench v0.2.11 first-task oracle (the TM.53 Docker-free cb interact path) produce 10 identical sha256 hashes of the ordered action sequence, at 0 USD in <= 20 min on the box that runs it; falsifier: any two of the 10 runs differ in action sequence or step count -- then agreement against the oracle has a noise floor that must be measured per step before it can rank any model"
title: "cua trove hop 2 (panel cua-bench T2): the oracle trajectory is deterministic per state, so next-action agreement has a clean 1.0 floor"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-cua-oracle-trajectory-is-deterministic-per-state

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
