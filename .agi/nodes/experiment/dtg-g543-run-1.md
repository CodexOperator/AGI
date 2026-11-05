---
id: experiment:dtg-g543-run-1
mint_id: 9d657a3898ce40d2b05f249fff4b331e
type: experiment
parents:
  - hypothesis:lm-seeded-input-codes-make-coherent-joint-samples
next_edges: []
confidence: 0.9
edited_by: director-thought-goals
evidence_runs:
  - experiment:dtg-g543-run-1
payload_ref: datasets/plasma/2026-11-05-g5.43-code-inputs/results.json
season: 3
tags: []
title: "goal:g5.43 run 1: the pre-registered round on hypothesis:lm-seeded-input-codes-make-coherent-joint-samples, results + falsifier verdict (pre-run f93be0f7b3; seeds 54301-54305; 541 s)"
town: local-maxxing
---
# experiment:dtg-g543-run-1

## Experiment
The one run of goal:g5.43 under its committed pre-run (pre-run f93be0f7b3; seeds 54301-54305; 541 s). ONE process, CPU, 0 USD, numpy in the private venv under <scratch>.

## Command
```
cd .agi/context/local-maxxing/plasma
python g543_code_inputs.py ../../../../datasets/plasma/2026-11-05-g5.43-code-inputs/params.json ../../../../datasets/plasma/2026-11-05-g5.43-code-inputs/results.json
python g543_falsifier.py ../../../../datasets/plasma/2026-11-05-g5.43-code-inputs/results.json > ../../../../datasets/plasma/2026-11-05-g5.43-code-inputs/verdict.json
```

## Output
datasets/plasma/2026-11-05-g5.43-code-inputs/results.json and verdict.json, committed at d04861ed6f; a replay is byte-identical. The per-line numbers are in the RESULT section of hypothesis:lm-seeded-input-codes-make-coherent-joint-samples.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 minted by director-thought-goals 20:2xZ 11-05 after belam's [red] 20:07:44Z (relayed by sanctuary-master): the hypothesis carried a decisive verdict with no evidence_runs, so the evidence gate demoted it. This node IS the run, so it cites itself (evidence_gate._is_self_citation: an experiment may), and the hypothesis cites this node.
<!-- THOUGHT:END -->
