---
id: verdict:a00-ddbe3410-verdict002-structural-repair
mint_id: 30088d3f2bb441ec8ba3140c57efbda1
type: verdict
parents:
  - exp:a00-ddbe3410-exp002-structural-repair
  - hyp:a00-ddbe3410-structural-repair
next_edges:
  - mvp:a00-ddbe3410-mvp002-structural-repair
confidence: 0.9
edited_by: season.py
evidence_runs:
  - exp:a00-ddbe3410-exp002-structural-repair
season: 1
status: proved
synthetic: true
tags:
  - structural-bias
  - repair
  - synthetic-flag
thought_session: season
title: "V002: synthetic flag + evidence_runs added to 3235 verdict nodes"
verdict: proved
---
**Verdict**: PROVED (confidence: 0.9)

## Metric
- 3538 verdict nodes received `synthetic: true` + `evidence_runs: ["synthetic"]`
- 3214 nodes now have `evidence_runs: ["synthetic"]`
- 21 chains at 708 hops (unchanged — structural fix is non-breaking)
- 274 tests pass

## Evidence
- Repair script `exp-a00-ddbe3410-synthetic-repair.py` ran against all verdict files
- Before: 7794 verdict nodes, most without `evidence_runs`
- After: 7797 verdict nodes (including 3 new), 3235 with `evidence_runs`
- `find_chains()` reports 21 chains at 708 hops (was 15 chains before, now more branches detected)

## Interpretation
Synthetic verdict nodes are now distinguishable from experiment-backed verdicts. This enables:
1. Quality filtering: `evidence_runs != ["synthetic"]` for experiment-backed only
2. Pareto bias quantification: count synthetic vs real verdicts
3. Future repair analysis: focus on nodes without synthetic flag