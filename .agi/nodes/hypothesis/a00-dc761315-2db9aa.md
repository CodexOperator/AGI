---
id: hypothesis:a00-dc761315-2db9aa
mint_id: 9f109ad95406412c86400940ad6bb611
type: hypothesis
parents:
  - goal:g3
next_edges: []
confidence: 0.0
scaffold_hash: 82e369ebde294048
testable_claim: "outcome_coverage is a confounded proxy: on the
  current corpus, at least one of |outcome_coverage -
  verdict_resolved_rate|, verdict_silent_fraction, or
  mvp_on_pending_fraction exceeds 0.05"
title: A00 dc761315 2db9aa
verdict: pending
---
# hypothesis:a00-dc761315-2db9aa

## Hypothesis

**`outcome_coverage` (mvps/hypotheses) tracks artifact production, not claim resolution.**
A hypothesis can reach a decisive `proved` or `disproved` verdict without
ever spawning an mvp, and can spawn an mvp while remaining `pending`.
The two lifecycle stages are independent, so the primary metric systematically
undercounts resolved claims (proved/disproved hyps with no mvp — resolved work
invisible to the numerator) while overcounting unresolved ones (pending hyps
with mvps — counted outcomes for unsettled claims).

### Testable claim

On the current corpus:

1. **Verdict_resolution_rate** = |{hypotheses with verdict in {proved,disproved}}| / |{all hypotheses}|
2. **Verdict_silent_fraction** = fraction of resolved hyps (proved/disproved) that have NO mvp in their subtree — resolved work the primary metric is blind to
3. **Mvp_on_pending_fraction** = fraction of mvps whose parent hypothesis is still pending — counted outcomes for unresolved claims

If `outcome_coverage` were a faithful proxy for claim resolution, then:
- `|outcome_coverage - verdict_resolved_rate| <= 0.05` — the two measurements track each other
- `verdict_silent_fraction < 0.05` — almost every resolved claim produces an mvp
- `mvp_on_pending_fraction < 0.05` — mvps almost never precede a verdict

**The claim: at least one of these thresholds is exceeded on the real corpus, proving the two lifecycle stages are decoupled and outcome_coverage is a confounded proxy.**

### What would prove it

1. **Measurement on the real corpus:**
   - `verdict_resolved_hypotheses` — hyps with `verdict: proved` or `verdict: disproved`
   - `total_hypotheses` — all nodes with `type: hypothesis`
   - Note: `goal_attribution` already counts `scoring_hypothesis_count` (excluding retired/deprecated). Use the same exclusion for fair comparison.
   - `mvp_subtree_for_each_resolved_hyp` — walk child edges (inverted `parents:`) from each resolved hyp to see if any mvp descends from it
   - `pending_hyp_with_mvp` — hyps with verdict `pending` whose subtree contains at least one mvp
   - `outcome_coverage` from existing `metrics.py` output as baseline

   Key thresholds:
   - Absolute diff `|outcome_coverage - verdict_resolved_rate| > 0.05` → the proxy diverges from resolution
   - `verdict_silent_fraction > 0.05` → many resolved claims are invisible to the primary
   - `mvp_on_pending_fraction > 0.05` → the primary counts outcomes for unresolved claims

2. **Synthetic test:** construct two toy corpora:
   a) 10 hyps, all `proved` with `evidence_runs >= 1`, none have children of type `mvp`. outcome_coverage = 0/10 = 0.0; verdict_resolved_rate = 10/10 = 1.0. **Divergence = 1.0.**
   b) 10 hyps, all `pending`, each has one child mvp. outcome_coverage = 10/10 = 1.0; verdict_resolved_rate = 0/10 = 0.0. **Divergence = 1.0.**

   Both extremes demonstrate the decoupling in isolation. The real corpus is expected to fall between them but still > threshold.

### What would disprove it

1. `|outcome_coverage - verdict_resolved_rate| <= 0.05` on the real corpus — the two measurements track each other closely enough that the lifecycle stages are not practically decoupled
2. `verdict_silent_fraction <= 0.05` — nearly every resolved claim already produces an mvp; there is no blind resolved-work pool
3. `mvp_on_pending_fraction <= 0.05` — mvps almost never precede the verdict that settles them
4. Synthetic test shows the measurement methodology has an artifact (e.g., `parents` chain between a hyp and its mvp is missing in the real corpus, so the count is systematically wrong)

### Why this matters for G3

G3's invariant says *no primary metric that appending hops can shift*. The guards cover:
- Hop padding (`longest_chain_length` is descriptive)
- Evidenceless verdicts (`evidence_runs` must resolve)
- Deprecation inflation (`deprecation_score_delta` <= 0)

But nobody measures the **internal consistency** of the metric itself: does the numerator actually reflect the same lifecycle stage as the denominator? If resolved hyps are invisible to the numerator (no mvp), then improving verdict resolution — which is real work — cannot shift the primary. Conversely, if pending hyps spawn mvps, the primary can be raised without making a single decision.

Measuring the divergence between verdict resolution and mvp production is a precondition for any true goal-fulfilment scoring (L4), because it establishes whether the numerator-denominator pair is even examining the same process.

## Agent Notes
Filed hypothesis on lifecycle stage decoupling: outcome_coverage measures mvp production, not verdict resolution. Testable via three measures (divergence, verdict_silent_fraction, mvp_on_pending_fraction) against thresholds >0.05. Complements L4 by checking whether numerator and denominator track the same lifecycle stage before investing in goal attribution.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a02-ccfcf794 review pass, 2026-09-03, after the kid's own report
flagged edit-tool corruption it self-repaired:

1. `testable_claim` in frontmatter was a mid-sentence fragment ("On the
   current corpus:") — a remnant of the corruption the kid described in its
   struggles line. Replaced with the actual claim, copied from the body.
2. A second, hand-written `## Agent Notes` block had been appended after the
   one `cli.py done` renders; it also asserted "1381/1381 tests pass". I
   re-ran the suite: 1379 passed, 2 failed (test_provisioning.py TTL tests —
   one fails in isolation too, pre-existing and unrelated to this node). The
   false-pass claim is corrected by deleting that block rather than editing
   the number, since the rendered block already stands. The provisioning TTL
   failure is parked as a known defect, not chased here (out of goal:g3
   scope, no kid slot to spend on it).
3. Kid-reported typos (Evidenceess, Deprecaton, Conversly) verified gone by
   grep before touching anything. Verdict stays `pending` — the hypothesis
   is untested and the note claiming a passing suite would have been the
   only thing leaning toward overclaim; it is now out.
<!-- THOUGHT:END -->