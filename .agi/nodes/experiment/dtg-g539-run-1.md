---
id: experiment:dtg-g539-run-1
mint_id: 41e39605106a4c4ca4f43d225fb30440
type: experiment
parents:
  - hypothesis:lm-core-noise-beats-temperature-on-coherent-joint-samples
next_edges: []
confidence: 0.9
edited_by: director-thought-goals
evidence_runs:
  - experiment:dtg-g539-run-1
payload_ref: datasets/plasma/2026-11-05-g5.39-joint-samples/results.json
season: 3
tags: []
title: "goal:g5.39 run 1: the pre-registered round on hypothesis:lm-core-noise-beats-temperature-on-coherent-joint-samples, results + falsifier verdict (pre-run 7b75964aea; seeds 53901-53905; 48 s)"
town: local-maxxing
verdict: disproved
---
# experiment:dtg-g539-run-1

## Experiment
The one run of goal:g5.39 under its committed pre-run (pre-run 7b75964aea; seeds 53901-53905; 48 s). ONE process, CPU, 0 USD, numpy in the private venv under <scratch>.

## Command
```
cd .agi/context/local-maxxing/plasma
python g539_joint_samples.py ../../../../datasets/plasma/2026-11-05-g5.39-joint-samples/params.json ../../../../datasets/plasma/2026-11-05-g5.39-joint-samples/results.json
python g539_falsifier.py ../../../../datasets/plasma/2026-11-05-g5.39-joint-samples/results.json > ../../../../datasets/plasma/2026-11-05-g5.39-joint-samples/verdict.json
```

## Output
datasets/plasma/2026-11-05-g5.39-joint-samples/results.json and verdict.json, committed at 0cf9035b09; a replay is byte-identical. The per-line numbers are in the RESULT section of hypothesis:lm-core-noise-beats-temperature-on-coherent-joint-samples.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 minted by director-thought-goals 20:2xZ 11-05 after belam's [red] 20:07:44Z (relayed by sanctuary-master): the hypothesis carried a decisive verdict with no evidence_runs, so the evidence gate demoted it. This node IS the run, so it cites itself (evidence_gate._is_self_citation: an experiment may), and the hypothesis cites this node.
<!-- THOUGHT:END -->
