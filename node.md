---
id: exp:exp-a00-407fa689-verdict-repair
mint_id: 6790ca32192049f7bbfd5db2151b3e70
type: experiment
parents:
  - hyp:a00-407fa689-verdict-repair
edited_by: season.py
season: 1
tags:
  - chain-extension
  - repair
thought_session: season
title: Exp a00 407fa689 verdict repair
---
# exp:exp-a00-407fa689-verdict-repair

## What Was Tested

Whether orphaned verdict nodes can be automatically repaired by tracing their IDs back to parent hypotheses.

## Method

1. Load full graph (3184 nodes, 1478 verdict nodes)
2. Attempt repair via two strategies:
   - **experiment_parent**: trace verdict→experiment→hypothesis via next_edges
   - **domain_match**: extract domain from verdict ID, link to domain base hypothesis
3. Count repairable vs unrepairable

## Key Metrics

| Metric | Value |
|---|---|
| total_verdicts | 1478 |
| before_orphaned_pct | 99.7 |
| repairs_experiment_parent | 0 |
| repairs_domain_match | 346 |
| unrepairable | 6 |
| repairable_pct | 23.5 |
| simulated_orphaned_pct | 76.3 |

## Result

**inconclusive_lean_proved:60** — partial repair (23.5% orphan reduction) via domain_match. experiment_parent strategy failed (0 repairs) because extend scripts don't populate next_edges.