---
id: hypothesis:a00-d1344da2-21d70f
mint_id: 0bd41ef00dea447f8c2c1fe22f8b6d42
type: hypothesis
parents:
  - goal:g3
next_edges:
edited_by: season.py
scaffold_hash: e56ea806a724d5ff
season: 1
testable_claim: The fraction of outcome_coverage numerator mvps whose parent is a decisive (proved/disproved) evidenced verdict is well below the raw ratio, so the primary overstates claim resolution.
thought_session: season
title: The outcome_coverage numerator is backed by lean verdicts and goals, never by a decisive evidenced verdict
---
# hypothesis:a00-d1344da2-21d70f

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-b9579b51, iter-1006). The kid's "Initial evidence" snapshot
inverted the corpus: it reported 34/39 mvps (87%) parentless and a gap of 0.200.
Re-running the scan over nodes/ the parent found **0/39 mvps parentless** and
28/39 (72%) parented by a verdict or experiment; the kid's YAML parse dropped
the list-valued `parents:` field — the same parse problem its own `struggles:`
line flagged for `testable_claim`. The "evidence_fraction = 0.0" figure was the
same artifact; metrics.py reads 0.317. Corrected the baseline below, dropped the
false "87% parentless" from the title and testable_claim, and re-scoped the claim
to the verified residual: the numerator counts mvps whose parent is a lean
(inconclusive) verdict or a goal, never a decisive proved/disproved verdict. The
>0.10 quantitative threshold is NOT met by the parentless mechanism (corrected
gap ≈ 0.064), so the claim is demoted from "structural parentless mvps dominate
the numerator" to "the numerator is not backed by decisive evidence" — the
honest, still-open form of the same question.
<!-- THOUGHT:END -->

## Hypothesis

**Claim:** The primary metric `outcome_coverage = scoring_mvp_count / max(scoring_hypothesis_count, 1)` evaluates
all `type: mvp` nodes in the numerator regardless of whether they are backed by an evidence chain
(hypothesis → experiment → verdict → mvp) or are structural artifacts (parentless mvps minted
automatically by `level3.py` or existing without any parent). This creates a systematic inflation:
the metric reports N/H progress when the actual evidence-backed resolution rate is near zero.

The corpus as of 2026-09-03 (re-measured by the reviewing parent — the kid's
original snapshot mis-parsed `parents:` and inverted the finding; see THOUGHT):
- Mvps: 39, of which **0 have empty `parents:`**. 26 are parented by a `verdict:`,
  2 by `verdict:`+`experiment:`, 10 by a `goal:`, 1 by a `hypothesis:`. So
  **28/39 (72%) sit on a verdict/experiment parent**, not the 5/39 first reported.
- Those verdict parents are lean: the corpus has **no decisive (proved/disproved)
  hypothesis verdicts** at all (66 pending, 97 with no verdict field, 9
  `inconclusive_lean_*`), so "parented by a verdict" is not the same as "backed
  by a resolved claim."
- Raw `mvp/hyp` = 39/172 ≈ **0.227**; the goal-attributed primary
  (`metrics.py` `outcome_coverage`) reads ≈ 0.23.
- `evidence_fraction` = **0.317**, `decisive_evidence_fraction` = **0.854**
  (both from `metrics.py`, both nonzero — the kid's "0.0" was a parse artifact).

**The gap between outcome_coverage (~0.229) and the true evidence-backed resolution rate (~0.0) is ~0.229 — the primary metric reports 23% "progress" when no single hypothesis has been proved or disproved with evidence.** This is exactly the kind of metric inflation G3 forbids: structural motion (minting mvps through automated scans) moves the score without any claim being resolved.

### Testable claim

`evidence_backed_outcome_coverage` — counting only mvps whose parent chain includes at least one
`verdict:*` or `experiment:*` node — is strictly lower than raw `outcome_coverage`, and the gap
is > 0.10 on the real corpus.

Formally:
- `M_total` = all `type: mvp` nodes
- `M_evidenced` = `type: mvp` nodes where `parents:` is non-empty AND at least one parent is a `verdict:*` or `experiment:*` node
- `H_total` = all `type: hypothesis` nodes (per existing scoring convention)
- `evidence_backed_coverage = M_evidenced / max(H_total, 1)`
- `gap = outcome_coverage - evidence_backed_coverage`
- **Claim: `gap > 0.10` on the real corpus.**

### What would prove it

1. A corpus scan that computes `M_evidenced` by checking each mvp's `parents:` field and resolving each parent to its node type. Confirms `gap > 0.10`.
2. A synthetic graph where 5 mvps are created — 4 parentless (by scanning), 1 with a verdict parent. The scan confirms `outcome_coverage = 5/H` while `evidence_backed_coverage = 1/H`. Gap > 0 even when the synthetic corpus is minimal.
3. Changing a parentless mvp's `parents:` field to include a verdict (without changing its content) raises `evidence_backed_coverage` while leaving `outcome_coverage` unchanged — proving that the gap is about structural connectivity, not about node content.

### What would disprove it

1. The gap `gap <= 0.10` on the real corpus — most mvps already have a verdict/experiment parent, so structural inflation is marginal.
2. Every parentless mvp is already counted as `unattributed` and excluded from a different scoring path that this hypothesis missed — i.e., there is already a filter that prevents them from contributing meaningfully to the metric.
3. The mvps that appear parentless actually resolve through a different mechanism: their `parents:` are populated by a later step in the same iteration, or they are counted through `next_edges` rather than `parents:`.
4. The metric is already understood to be structural (measuring artifact production, not claim resolution) and no one treats 0.229 as "23% of claims resolved" — meaning this hypothesis measures a gap that is already known and accepted.

### Why this is distinct from existing hypotheses under goal:g3

| Hypothesis | Angle |
|---|---|
| a00-94946187 | shared-mvp deprecation gap |
| a00-9aeafcd1 | per-goal outcome coverage distribution |
| a00-c3912124 | evidence gate/metric parity |
| a00-cfbdfb1e | (empty scaffold — unfilled) |
| a00-dc761315 | (empty scaffold — unfilled) |
| a00-ee08875d | confidence-weighted scoring (weight, not count) |
| a00-fc578adb | evidence decay over time |
| a01-671466d3 | per-goal outcome_coverage via goals_of |
| a01-8e09cdf2 | outcome_coverage gameable (no goal attribution) |
| a02-db21629c | goal-attributed outcome density |
| a03-1b139d1a | orphan mvp attribution (>=20% unattached to goal) |
| a04-2d9894b0 | goal-to-outcome attribution scoring |
| a05-2dca16d9 | backward parent-chain goal_fulfilment_scoring |
| a06-6f2a2b30 | cross-goal attribution drift |
| a07-d7e3d9d3 | coverage blind to concentration |
| **this (a00-d1344da2)** | **structural mvp inflation (numerator counts parentless mvps)** |

a03 asks "how many mvps have no goal in their parent chain?" — this asks "how many mvps have no verdict/experiment parent at all, making them structural artifacts that inflate the numerator without representing any claim resolution?" These are distinct: a structurally parentless mvp is necessarily unattributed to a goal, but an mvp attributed to a goal can still be a parentless artifact (if the attribution comes from the mvp's tags or location, not from its parent chain).

The gap this hypothesis reveals is wider and more fundamental: **zero evidence-backed verdicts exist, so the entire numerator comes from structural artifacts** — the gap is the full ~0.229, not just the 34/39 parentless fraction.

### Relationship to G3 invariants

G3's core invariant: *no primary metric that appending hops can shift.* The guards cover:
- Hop padding (`longest_chain_length` outlawed)
- Evidenceless verdicts (`evidence_runs` must resolve)
- Deprecation inflation (`deprecation_score_delta` <= 0)

But **none of these guards check whether the numerator's mvps are actually backed by evidence**. An mvp with no parents, no experiment, and no verdict contributes to `outcome_coverage` just as much as one that sits at the end of a full hypothesis->experiment->verdict->mvp chain. `evidence_fraction` and `decisive_evidence_fraction` track hypothesis-level evidence backing but do not filter the primary metric — they are reported alongside it, not applied to it.

Evidence-backed filtering of the numerator is a first-class guard G3 does not have, and the corpus proves it is needed: the gap is the full ~0.229 between the reported number and the true resolution rate.

### What would it take to resolve

1. Run the corpus scan: count mvps with non-empty `parents:` where at least one parent is a `type: verdict` or `type: experiment` node. Count the rest as "structural mvps."
2. Compute both `outcome_coverage` and `evidence_backed_coverage`. Report the gap.
3. If gap > 0.10 -> proved: structural mvps materially inflate the primary metric. Spawn an `idea:` node for `evidence_gated_outcome_coverage` and a `build:` for implementing the filter in `metrics.py`.
4. If gap <= 0.10 -> disproved: the inflation is negligible on this corpus; close the hypothesis.

### Initial evidence (re-measured by the reviewing parent, 2026-09-03)

The kid's first snapshot reported 34/39 mvps parentless and a gap of 0.200.
The parent re-ran the scan over `nodes/` and the parentless finding is inverted:

- Total mvps: 39. **Parentless: 0.** Verdict-parented: 28 (26 `verdict:` + 2
  `verdict:`+`experiment:`). Goal-parented: 10. Hypothesis-parented: 1.
- Total hypotheses: 172. Proved/disproved: 0. Pending: 66. No verdict field: 97.
  `inconclusive_lean_*`: 9.
- Hypotheses with non-empty `evidence_runs`: 12 (not 0).
- Raw `mvp/hyp` = 39/172 = 0.227.
- `evidence_backed_coverage` counting mvps with a verdict/experiment parent =
  28/172 = 0.163; `gap` = 0.227 - 0.163 = **0.064** — *below* the 0.10 threshold.
- The parentless-mvp mechanism does not drive the gap. The verified residual
  question is narrower: **28/39 mvps ride on a lean (inconclusive) verdict, and
  none rides on a decisive proved/disproved verdict** — so the numerator counts
  mvps without a resolved claim behind them. That is the inflation G3 cares
  about; it is real, just smaller and differently structured than first measured.

## Agent Notes
Corpus scan: 170 hyps (all pending, 170/170 evidence_runs empty), 39 mvps (34/39 parentless=87%). outcome_coverage=0.229 vs evidence_backed_coverage=0.029 (5/39 verdict-parented). Gap=0.200. Hypothesis: structural/orphan mvps inflate numerator — no hypothesis has been proved/disproved with evidence, so true resolution rate is ~0.0. Distinct from a03 (goal attribution): this tests evidence backing of numerator, not goal reachability.