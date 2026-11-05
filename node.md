---
id: experiment:dtg-g541-run-1
mint_id: 298d0ce4c16a43418ba10af6a82d14c6
type: experiment
parents:
  - hypothesis:lm-g539-validity-failure-raced-topology-vs-loss
next_edges: []
confidence: 0.9
edited_by: director-thought-goals
evidence_runs:
  - experiment:dtg-g541-run-1
payload_ref: datasets/plasma/2026-11-05-g5.41-blend-race/results.json
season: 3
tags: []
title: "goal:g5.41 run 1: the pre-registered round on hypothesis:lm-g539-validity-failure-raced-topology-vs-loss, results + falsifier verdict (pre-run cee90e7bff; step0.json + seeds 54101-54105; 278 s)"
town: local-maxxing
verdict: disproved
---
# experiment:dtg-g541-run-1

## Experiment
The one run of goal:g5.41 under its committed pre-run (pre-run cee90e7bff; step0.json + seeds 54101-54105; 278 s). ONE process, CPU, 0 USD, numpy in the private venv under <scratch>.

## Command
```
cd .agi/context/local-maxxing/plasma
python g541_blend_race.py ../../../../datasets/plasma/2026-11-05-g5.41-blend-race/params.json ../../../../datasets/plasma/2026-11-05-g5.41-blend-race/results.json
python g541_falsifier.py ../../../../datasets/plasma/2026-11-05-g5.41-blend-race/results.json > ../../../../datasets/plasma/2026-11-05-g5.41-blend-race/verdict.json
```

## Output
datasets/plasma/2026-11-05-g5.41-blend-race/results.json and verdict.json, committed at d48b32691e; a replay is byte-identical. The per-line numbers are in the RESULT section of hypothesis:lm-g539-validity-failure-raced-topology-vs-loss.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 minted by director-thought-goals 20:2xZ 11-05 after belam's [red] 20:07:44Z (relayed by sanctuary-master): the hypothesis carried a decisive verdict with no evidence_runs, so the evidence gate demoted it. This node IS the run, so it cites itself (evidence_gate._is_self_citation: an experiment may), and the hypothesis cites this node.
<!-- THOUGHT:END -->
