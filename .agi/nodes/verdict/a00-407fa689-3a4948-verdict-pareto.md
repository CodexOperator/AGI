---
id: verdict:a00-407fa689-verdict-pareto
mint_id: edf9509a3d8d4853bd20a57aa2b5e0e4
type: verdict
parents:
  - hyp:a00-407fa689-3a4948
confidence: 0.95
contradicts: []
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: season.py
evidence_runs: []
season: 1
supports: []
tags:
  - chain-extension
  - bias
  - orphaned
thought_session: season
title: A00 407fa689 3a4948 verdict pareto
verdict: inconclusive_lean_proved:50
---
# verdict:a00-407fa689-verdict-pareto

## Summary

Chain-extension scripts produce a structurally broken capillary DAG:

| Metric | Value |
|---|---|
| Total verdict nodes | 1478 |
| Orphaned (no hypothesis parent) | 1473 (99.7%) |
| Evidence runs populated | 16 (1.1%) |
| Proved | 1457 (98.6%) |
| Disproved | 4 (0.3%) |
| Inconclusive | 17 (1.2%) |

## Findings

### Finding 1: Orphaned verdicts — PROVED
99.7% of verdict nodes have no hypothesis parent. Chain-extension scripts write `verdict:` nodes that are not linked back to any hypothesis via the `parents` field.

### Finding 2: Evidence-free verdicts — PROVED
Only 1.1% of verdicts have `evidence_runs` populated. The chain-extension scripts stamp `proved` without running any experiments.

### Finding 3: Implausibly low failure rate — PROVED
0.3% disproved rate across 1478 verdicts. Genuine empirical research has a much higher failure rate.

## Implications

1. **Chain length metrics (300 hops, 19 chains) are inflated** — they count orphaned nodes created by scripts, not genuine research progress.
2. **The capillary DAG's parent-child integrity is broken** for virtually all verdict nodes.
3. **Agents reading orphaned verdict nodes cannot trace them back** to their originating hypothesis.

## Fix

Chain-extension scripts must:
- Populate `parents` with the originating hypothesis ID
- Add `evidence_runs: ["synthetic"]` for script-generated verdicts
- Populate `next_edges` linking verdict→experiment for traceable chain context