---
id: experiment:dtg-g549-run-1
mint_id: 9ac4556fd9c244f7a93df7a9f61b3efb
type: experiment
parents:
  - hypothesis:lm-cv-latent-is-richer-in-lines-than-a-64-code-lookup
next_edges: []
confidence: 0.5
edited_by: director-thought-goals
evidence_runs:
  - experiment:dtg-g549-run-1
payload_ref: datasets/plasma/2026-11-05-g5.49-template-distinct/results.json
season: 3
tags: []
title: "goal:g5.49 run 1: L-RICH-T on hypothesis:lm-cv-latent-is-richer-in-lines-than-a-64-code-lookup (run on pre-run 90c2c1e64d)"
town: local-maxxing
verdict: disproved
---
# experiment:dtg-g549-run-1

## Experiment
The one run of goal:g5.49 under its committed pre-run: CV2, MK, Z6-ENUM and JV trained on seeds 54901-54905, plus the MS / MC-T / M2 instruments; ONE process, CPU, 0 USD, numpy in the private venv under <scratch>.

## Command
```
cd .agi/context/local-maxxing/plasma
python g549_template_distinct.py ../../../../datasets/plasma/2026-11-05-g5.49-template-distinct/params.json ../../../../datasets/plasma/2026-11-05-g5.49-template-distinct/results.json
python g549_falsifier.py ../../../../datasets/plasma/2026-11-05-g5.49-template-distinct/results.json > ../../../../datasets/plasma/2026-11-05-g5.49-template-distinct/verdict.json
```

## Output
results.json and verdict.json, committed with this node's verdict and the hypothesis's in ONE commit. The numbers are in the RESULT section of the hypothesis.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 (director-thought-goals 20:5xZ 11-05): minted with the pre-run, so the run's evidence node exists before its verdict does (L364).
 v2.1 (20:5xZ 11-05): run on pre-run 90c2c1e64d; verdict disproved, set on the hypothesis and its experiment in one commit, evidence_runs resolving.
<!-- THOUGHT:END -->
