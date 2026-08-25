---
id: "bigger_outcome:a00-ddbe3410-bo002-structural-repair"
mint_id: d9b864c760bf4376b3f32015f3d3645b
next_edges:
  - app_purpose:a00-ddbe3410-app002-structural-repair
parents:
  - outcome:a00-ddbe3410-outcome002-structural-repair
tags:
  - structural-bias
title: "BIGGER_OUTCOME002: capillary DAG with quality-filterable verdict nodes"
type: bigger_outcome
---

## Module Purpose
Capillary DAG verdict nodes are now quality-filterable. Researchers can query for experiment-backed verdicts (`evidence_runs` not equal to `["synthetic"]`) and synthetic verdicts (`evidence_runs == ["synthetic"]`). This enables accurate Pareto bias measurement and evidence quality scoring.

## Aggregated Outcomes
1. OUTCOME001: task→experiment conversion viable (bootstrap pipeline)
2. OUTCOME002: verdict quality filtering enabled (structural repair)
