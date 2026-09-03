---
id: hypothesis:a04-7bb380cb-2a7d9b
mint_id: 7f3d390ecce14c838003b0d14c655614
type: hypothesis
parents:
  - goal:g4.8
next_edges: []
scaffold_hash: 28bde3dc641d5618
title: "Delegator review cost grows sub-linearly with loop count when parents report deltas"
testable_claim: "With M parents each reviewing M_k kids and reporting a structured brief (delta-only: which nodes changed, which verdicts were demoted, which remain in flight), the delegator can produce its own verdict across all M loops while consuming strictly fewer tokens than re-reading every node on every loop — and the ratio improves as M grows."
verdict: pending
confidence: 0.0
---

# hypothesis:a04-7bb380cb-2a7d9b

## Hypothesis

**A delegator consuming delta-only parent briefs — one per parent, listing changed nodes, demoted verdicts, and in-flight items — spends sub-linearly in the number of parallel loops M. No single loop's full node set is re-read by the delegator.**

The tier architecture's economic justification is "functional output per token spent" (g4.8's own objective function). If the delegator reads every kid's entire node body for every loop, then running 2 parents costs 2× the tokens, and the architecture buys nothing — the work is merely distributed, not compressed.

For this to hold, the parent must produce a *delta brief* that the delegator can judge structurally:
- Changed nodes (new, updated, deprecated)
- Verdicts demoted and why (structural: missing evidence_runs, invalid verdict enum — not re-reading the hypothesis body)
- Nodes still in flight (pending or unconverged)
- Known collisions or anomalies

The delegator reads the M briefs and inspects only the nodes the briefs flag. Nodes unchanged across loops are never touched.

### What would prove it

An experiment with 3 parent loops (M=3), each spawning 2 kids (M_k=2), where:
1. Parent P₁ returns a brief listing 3 changed nodes (1 new hyp, 1 demoted verdict, 1 in-flight). Delegator reads those 3 plus the brief.
2. Parent P₂ returns a brief listing 2 changed nodes. Delegator reads those 2 plus the brief.
3. Parent P₃ returns a brief listing 1 changed node. Delegator reads that 1 plus the brief.
4. **Total node bodies re-read: 6 (3+2+1), not 12 (3×4).** Ratio improves as M grows, approaching 0 (sub-linear) instead of 1 (linear).

Measured: token count consumed by delegator on reading body content vs. total body tokens across all nodes touched by all loops. A ratio < 1.0 proves sub-linear spend. Monotonically decreasing with M proves the architecture scales.

### What would disprove it

- Delegator must re-read every kid's full body to form its verdict — ratio = 1.0
- Parent brief is as long as re-reading all kids (cost not saved but shifted to parent tier, leaving system cost linear)
- Demonstrates sub-linear node reads but token spend remains linear because even a "brief" is a full read of each changed node
- False negatives: a parent's delta omits a critical change, and the delegator's review misses a failure it would have caught by reading everything
- False positives: briefs flag everything as changed, collapsing to linear access

### Why this hypothesis targets the last untouched clause of g4.8's falsifier

Clause 4: *the delegator's own token spend is sub-linear in the number of loops.* All other clauses have a hypothesis or verdict. This one is the economic constraint — without it the tier architecture distributes cost but does not reduce it, and g4.8's explicit objective function (functional output per token) is unmet even if clauses 1-3 all pass.

### Relation to existing nodes

- `hypothesis:a00-07b2223d-b21977` tests whether a **parent** can review kids structurally (field-check evidence_runs). This hypothesis extends that to the **delegator** reviewing parents structurally (delta briefs, not re-reads). A parent that cannot review structurally cannot produce a trustworthy delta brief either — so a00-07b2223d's result gates this one.
- `verdict:the-bound-is-structural-now` proved clause 2. This hypothesis targets clause 4, the remaining unproven structural clause.

### Note on measurement

Token counts are model-dependent (a 2k-token node may cost 150 input tokens on Gemini vs 600 on Claude). The hypothesis is about *relative* scaling — as M grows, the fraction of total content the delegator touches should shrink. The absolute cost ceiling is a separate policy question for the operator.



## Agent Notes
Hypothesis: delegator review cost is sub-linear in loop count when parents report delta briefs. Targets g4.8 falsifier clause 4 — the economic heart of the tier architecture, last untouched falsifier clause. Tests whether delta-only parent briefs let delegator avoid re-reading every kid node every loop, scaling sub-linearly with M.
