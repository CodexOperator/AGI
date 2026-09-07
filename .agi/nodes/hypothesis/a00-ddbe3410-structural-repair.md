---
id: hyp:a00-ddbe3410-structural-repair
mint_id: feaf4a2e88d34e27ac192074295a68ea
type: hypothesis
parents:
  - idea:domain-chain-bootstrap
next_edges:
  - exp:a00-ddbe3410-exp002-structural-repair
acceptance_criteria: []
blocked_by: []
cavekit_req: structural-bias/synthetic-repair
edited_by: season.py
effort: L
season: 1
status: open
tags:
  - structural-bias
  - repair
  - synthetic-flag
  - iteration-1
thought_session: season
title: "Hypothesis: synthetic verdict nodes lack evidence_runs and synthetic flag"
---
## Hypothesis

The capillary DAG has 7794 verdict nodes. Most are synthetic (created by chain-extension scripts without running real experiments). These synthetic verdicts lack:
1. `evidence_runs: ["synthetic"]` — can't distinguish script-generated from experiment-generated
2. `synthetic: true` — no flag marking script-generated nodes

**Claim**: Adding `synthetic: true` and `evidence_runs: ["synthetic"]` to all chain-extension verdict nodes will enable quality filtering and prevent future repair analysis from miscounting evidence-backed verdicts.

## What would prove it?

1. Scan all verdict nodes in `nodes/verdict/`
2. Identify synthetic verdicts (those created by extend scripts — have `status: proved`, `confidence: 0.85-1.0`, no `evidence_runs`)
3. Add `synthetic: true` and `evidence_runs: ["synthetic"]` to each
4. Verify `find_chains()` still reports same chain count/length
5. Verify `evidence_runs` field is now populated for all synthetic nodes

## What would disprove it?

- Adding fields breaks the YAML schema (unrealistic — schema is permissive)
- `find_chains()` reports different chain count after update
- Some verdict nodes are genuinely experiment-backed and should NOT have synthetic flag