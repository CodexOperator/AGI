---
id: experiment:dtg-g546-run-1
mint_id: c858892eb4a54a3982f70991fff6141c
type: experiment
parents:
  - hypothesis:lm-encoder-gives-a-continuous-core-latent-valid-and-rich-samples
next_edges: []
confidence: 0.9
edited_by: director-thought-goals
evidence_runs:
  - experiment:dtg-g546-run-1
payload_ref: datasets/plasma/2026-11-05-g5.46-cvae/results.json
season: 3
tags: []
title: "goal:g5.46 run 1: the pre-registered round on hypothesis:lm-encoder-gives-a-continuous-core-latent-valid-and-rich-samples, results + falsifier verdict (pre-run 29b9084b23; seeds 54601-54605; 35 s)"
town: local-maxxing
verdict: proved
---
# experiment:dtg-g546-run-1

## Experiment
The one run of goal:g5.46 under its committed pre-run (pre-run 29b9084b23; seeds 54601-54605; 35 s). ONE process, CPU, 0 USD, numpy in the private venv under <scratch>.

## Command
```
cd .agi/context/local-maxxing/plasma
python g546_cvae.py ../../../../datasets/plasma/2026-11-05-g5.46-cvae/params.json ../../../../datasets/plasma/2026-11-05-g5.46-cvae/results.json
python g546_falsifier.py ../../../../datasets/plasma/2026-11-05-g5.46-cvae/results.json > ../../../../datasets/plasma/2026-11-05-g5.46-cvae/verdict.json
```

## Output
datasets/plasma/2026-11-05-g5.46-cvae/results.json and verdict.json, committed at c6a3e3de09; a replay is byte-identical. The per-line numbers are in the RESULT section of hypothesis:lm-encoder-gives-a-continuous-core-latent-valid-and-rich-samples.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 minted by director-thought-goals 20:2xZ 11-05 after belam's [red] 20:07:44Z (relayed by sanctuary-master): the hypothesis carried a decisive verdict with no evidence_runs, so the evidence gate demoted it. This node IS the run, so it cites itself (evidence_gate._is_self_citation: an experiment may), and the hypothesis cites this node.
<!-- THOUGHT:END -->
