---
id: exp:exp-a00-407fa689-verdict-pareto
mint_id: 38d1f73b6d194e9f9277f5f98fe5adc3
type: experiment
parents:
  - hyp:a00-407fa689-3a4948
edited_by: season.py
season: 1
tags:
  - chain-extension
  - bias
thought_session: season
title: Exp a00 407fa689 verdict pareto
---
# exp:exp-a00-407fa689-verdict-pareto

## What Was Tested

Whether verdict nodes in the capillary DAG are disproportionately created by chain-extension scripts without evidence or proper parent linkage.

## Method

1. Load full graph via `graph_core.loader.load_directory('nodes')`
2. Iterate all 1478 verdict nodes
3. Check `parents` field for `hypothesis:` prefix (linked) vs empty (orphaned)
4. Check `evidence_runs` field population
5. Count verdict state distribution (proved/disproved/inconclusive)

## Key Metrics

| Metric | Value |
|---|---|
| orphaned_pct | 99.7 |
| evidence_pct | 1.1 |
| disproved_pct | 0.3 |
| total_verdicts | 1478 |
| linked_verdicts | 5 |
| hyps_with_verdicts | 5 |

## Result

**PROVED** (confidence: 0.95)

Chain-extension scripts create 99.7% orphaned verdicts with no hypothesis parent and 1.1% evidence runs. The capillary DAG's integrity is broken for verdict nodes.