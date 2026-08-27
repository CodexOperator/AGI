---
id: "exp:a00-ddbe3410-exp002-structural-repair"
mint_id: eba7d0c465214ccca238a5dbfa8b5aee
next_edges:
  - verdict:a00-ddbe3410-verdict002-structural-repair
parents:
  - hyp:a00-ddbe3410-structural-repair
status: complete
tags:
  - structural-bias
  - repair
  - synthetic-flag
title: "EXP002: Add synthetic flag + evidence_runs to verdict nodes"
type: experiment
---

## Experiment

Run `exp-a00-ddbe3410-synthetic-repair.py` to:
1. Identify all synthetic verdict nodes (proved + confidence >= 0.8 + no evidence_runs + chain-extension tag)
2. Add `synthetic: true` and `evidence_runs: ["synthetic"]`
3. Verify `find_chains()` unchanged

## Results
- 3538 synthetic verdict nodes repaired
- 21 chains, longest=708 hops (unchanged)
- 274 tests pass
