---
id: "outcome:a00-ddbe3410-outcome002-structural-repair"
mint_id: fae435ae1b9d4cbd9ba71c4da164d246
next_edges:
  - bigger_outcome:a00-ddbe3410-bo002-structural-repair
parents:
  - mvp:a00-ddbe3410-mvp002-structural-repair
tags:
  - structural-bias
  - repair
title: "OUTCOME002: synthetic verdict nodes now quality-filterable"
type: outcome
---

## Input
Verdict nodes with `status: proved`, `confidence >= 0.8`, no `evidence_runs`, `chain-extension` tag.

## Output
- `synthetic: true` field added to all synthetic verdict nodes
- `evidence_runs: ["synthetic"]` populated for 3235 verdict nodes
- `find_chains()` unchanged (21 chains, 708 hops)

## Behavior
1. Scan verdict files in `nodes/verdict/`
2. Identify synthetic nodes via heuristic (proved + high confidence + no evidence_runs + chain-extension tag)
3. Add `synthetic: true` and `evidence_runs: ["synthetic"]`
4. Write updated files

## Edge Cases
- Already-repaired nodes: skip (no change needed)
- Genuine experiment-backed verdicts: NOT repaired (have non-synthetic evidence_runs)
