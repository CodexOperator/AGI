---
id: bigger_outcome:a00-ddbe3410-bo002-structural-repair
mint_id: d9b864c760bf4376b3f32015f3d3645b
type: bigger_outcome
parents:
  - outcome:a00-ddbe3410-outcome002-structural-repair
next_edges:
  - vision:a00-ddbe3410-app002-structural-repair
edited_by: season.py
judged_against: goal:g2
season: 1
tags:
  - structural-bias
thought_session: season
title: "BIGGER_OUTCOME002: capillary DAG with quality-filterable verdict nodes"
---
## Module Purpose
Capillary DAG verdict nodes are now quality-filterable. Researchers can query for experiment-backed verdicts (`evidence_runs` not equal to `["synthetic"]`) and synthetic verdicts (`evidence_runs == ["synthetic"]`). This enables accurate Pareto bias measurement and evidence quality scoring.

## Aggregated Outcomes
1. OUTCOME001: task→experiment conversion viable (bootstrap pipeline)
2. OUTCOME002: verdict quality filtering enabled (structural repair)