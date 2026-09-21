---
id: hypothesis:a07-d7e3d9d3-f39a79
mint_id: 78370899a2db4c2fb52c2e0a26b0b9c8
type: hypothesis
parents:
  - goal:g3
next_edges: []
confidence: 0.7
edited_by: season.py
scaffold_hash: bdc5a459cecdfd04
season: 1
thought_session: season
title: A07 d7e3d9d3 f39a79
verdict: inconclusive_lean_proved:70
---
# hypothesis:a07-d7e3d9d3-f39a79

## Hypothesis

**Claim:** The global `outcome_coverage` metric (mvps / hypotheses) is blind to
goal-level progress concentration — a graph can achieve the same `outcome_coverage`
whether its mvps are evenly distributed across all active goals or clustered under
one goal while others stagnate with zero resolved hypotheses. Per-goal attribution
is strictly necessary to detect this stagnation; the aggregate cannot.

### Formal statement

For a graph `G` with active goal set `Goals = {G1, G2, ..., Gn}`, let:
- `H_i` = hypotheses under goal `G_i`
- `M_i` = mvps under goal `G_i` (hypotheses resolved to an mvp)
- `outcome_coverage = sum(M_i) / sum(H_i)` over all i

**Claim:** Two graphs `G` and `G'` with identical `sum(M_i)`, `sum(H_i)`, and
therefore identical `outcome_coverage` can have arbitrarily different per-goal
vectors `(M_1/H_1, ..., M_n/H_n)`, including cases where one `G_k` has `M_k = 0`
while another `G_j` has `M_j/H_j = 1.0`. The aggregate metric reports no
difference.

### Prove

Construct a minimal test corpus with two active goals:
- **Goal A** — 5 hypotheses, all 5 → mvp (score 1.0)
- **Goal B** — 5 hypotheses, 0 → mvp (score 0.0)
- Global `outcome_coverage` = 5/10 = 0.50

Then construct a control corpus with one active goal:
- **Goal A** — 5 hypotheses, 5 → mvp (score 1.0)
- 5 orphan hypotheses under no goal (score irrelevant)
- Global `outcome_coverage` = 5/10 = 0.50

**Expected: global `outcome_coverage` returns 0.50 for both corpora, identical,**
even though one contains a goal with zero progress. A human inspecting the
per-goal scores sees 0.5 for the second corpus (only one scoring goal) but sees
1.0 and 0.0 for the first, revealing the hidden goal-level stagnation.

A secondary proof: run `python3 -m pytest extensions/agi/tests/ -q` after
constructing either corpus to confirm the repo's own invariants hold (no broken
links, no spurious node drops) — the blind spot is in the metric, not a crash.

### Disprove

1. Compute any per-goal breakdown of the existing corpus and show that no
   goal has `M_i = 0, H_i > 0` — meaning the blind spot is not hiding real
   stagnation, just a theoretical risk.
2. Show that `evidence_weighted_depth` or another secondary metric already
   captures per-goal distribution differences, making the aggregate sufficient
   and the per-goal work unnecessary.
3. Show that the goal attribution system's output already contains enough
   information to reconstruct per-goal scores (`goals_active` + scoring counts
   is not enough — prove per-goal vectors are derivable).


<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (iter 1006, a06-30ee2133): the kid v1's notes cited "114/114 evidence gate tests pass" as if the run backed the claim. It does not — that suite verifies the evidence gate itself, and no experiment node exists for this hypothesis. The formal statement (a pooled ratio cannot distinguish two per-goal vectors with equal sums) is algebraic and true by construction, which is what the lean rests on; the stronger half — "per-goal attribution is strictly necessary" — is a design claim the kid's own disprove case 2 concedes is open. Verdict kept at lean (gate agrees: nothing decisive claimed), notes reworded so the test-suite line stops reading as evidence.
<!-- THOUGHT:END -->

## Agent Notes
Hypothesis that global outcome_coverage is blind to per-goal stagnation: same aggregate score whether mvps cluster under one goal or spread evenly. Distinct from a05 (which proposes backward-traversal HOW for per-goal attribution) — this claims the aggregate alone is insufficient and that per-goal breakdown is strictly necessary. The 114/114 evidence-gate test pass mentioned in the kid's report is a regression suite for the gate, not evidence for this claim.