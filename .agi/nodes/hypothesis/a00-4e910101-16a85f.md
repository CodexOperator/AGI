---
id: hyp:a00-4e910101-16a85f
mint_id: 9b9b537ad15e4da98afc0fb5b6ecd135
type: hypothesis
parents: []
confidence: 0.5
title: A00 4e910101 16a85f
verdict: pending
---
# hyp:a00-4e910101-16a85f
## Hypothesis

**Claim**: A dedicated experiment-runner that polls pending hypotheses, executes their spawned tasks as bounded experiments, and writes structured verdict nodes will bootstrap the capillary DAG from zero-chain-length into productive chains faster than manual agent-driven chaining.

**Prove it**: Run 10 parallel agents — 5 with experiment-runner, 5 manual — on same 60-hypothesis set. Measure chain-length growth rate and verdict density after 1 hour.

**Disprove it**: Manual agents match or exceed experiment-runner agents in verdict/sec and chain-depth despite no automated runner.

**Operationalized test**:
- Baseline: count `verdict` nodes in graph at T=0
- Intervention: deploy runner that reads `hypothesis` nodes with `spawns->task:*` edges, executes each task as `run_experiment`, writes `verdict` node on completion
- Metric: verdict_density = verdict_nodes / (hypothesis_nodes + experiment_nodes) at T=60min
- Threshold: runner group must reach verdict_density ≥ 0.3 vs manual group < 0.1 to prove claim

**Why this gap exists**: The graph currently has 60 hypotheses and 90 task nodes but 0 experiments and 0 verdicts. The DAG is a skeleton with no flesh. Without an automated runner, each agent must manually invoke `run_experiment` + `log_experiment` for every hypothesis — slow, inconsistent, no structured verdict taxonomy.

**Deferred refinements** (future hypotheses):
- Which runner scheduling policy (BFS depth-first vs longest-chain-first) yields fastest chain growth
- Whether verdict confidence scores should feed back into hypothesis attractiveness weighting
- If parallel runner count should scale with available CPU cores or stay fixed


Hypothesis: automated experiment-runner needed to bootstrap zero-chain-length DAG into productive chains