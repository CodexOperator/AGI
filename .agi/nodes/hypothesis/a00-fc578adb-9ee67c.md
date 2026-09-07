---
id: hypothesis:a00-fc578adb-9ee67c
mint_id: eafec7a511cc479b8c3403dc6078754a
type: hypothesis
parents:
  - goal:g3
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 05363717a7ff04b5
season: 1
testable_claim: For any `proved` or `disproved` hypothesis node H with `evidence_runs` citing specific experiment nodes, measure **evidence integrity** as the fraction of those experiment nodes whose forward chain (through `next_edges` and `parents`) still connects back to H at the current graph state. A decay threshold exists T such that hypothesis nodes whose evidence is older than T iterations have integrity < 0.5 (majority of evidence is disconnected or stale).
thought_session: season
title: Evidence decay — proved hypotheses disconnect from their support over time
verdict: pending
---
# hypothesis:a00-fc578adb-9ee67c

## Hypothesis

**Evidence decay** — a `proved` hypothesis whose `evidence_runs` resolve to
real experiment nodes is assumed to hold indefinitely, but the graph evolves:
experiment nodes get deprecated, their parent chains get restructured, and the
hypotheses they once supported may no longer trace back to the same claim.
If evidence is not periodically re-verified, the scoring system built on it
reports stale results as current.

### Testable claim

For any `proved` or `disproved` hypothesis node H with `evidence_runs` citing
specific experiment nodes, measure **evidence integrity** as the fraction of
those experiment nodes whose forward chain (through `next_edges` and `parents`)
still connects back to H at the current graph state. A decay threshold exists
T such that hypothesis nodes whose evidence is older than T iterations have
integrity < 0.5 (majority of evidence is disconnected or stale).

Specifically: for each hypothesis H with verdict `proved`:
1. Resolve each entry in `evidence_runs` to its node (requires G3.1's resolution).
2. For each experiment node E, walk forward along `next_edges` to find whether
   any subsequent node in the chain is an mvp or build node that still lists H
   (or H's parent goal) in its `parents:` field.
3. If yes, the evidence is "live". If no (path broken, node deprecated, parent
   chain rerouted), the evidence is "decayed".
4. Compute `integrity(H) = live_count / total_count`.
5. Compute `iteration_age(H) = current_iteration - iteration_when_verdict_written`.

Hypothesis holds if: across all `proved` hypotheses with `age > T`, the mean
integrity is < 50%.

### What would prove it

An audit of the real corpus shows:
1. At least one `proved` hypothesis where `integrity(H) < 1.0` — i.e. a concrete
   case of decay exists.
2. The Pearson correlation between `age` and `integrity` is negative and
   significant (r < -0.3, p < 0.05).
3. There exists an age threshold T where `mean(integrity[H with age > T]) < 0.5`.
4. A hypothesis whose evidence has decayed can be trivially re-proved (same
   claim, same experiment, just re-wiring the parent chain) — showing the decay
   is structural, not logical.

### What would disprove it

1. Every `proved` hypothesis in the corpus has `integrity(H) = 1.0` — evidence
   never decays, the graph is stable enough.
2. `age` and `integrity` show zero or positive correlation — older proofs are
   *more* connected, not less (counterintuitive but possible if old proofs
   survived heavy curation while new ones are transient).
3. No age threshold produces mean integrity < 0.5 — decay exists but never
   reaches a majority.
4. Evidence decay is always repaired by the same agent that wrote the verdict
   (no structural gap — just a temporary state during a multi-step edit).

### Why this matters for G3

G3's invariant is that *no primary metric can be shifted by appending hops.*
But if evidence decays silently, then even a correctly-attributed goal score
(G3-L4's open problem) can be inflated: old outcomes that are no longer backed
by live evidence count as if they were current. The score is *stable under new
hops* but *unstable under time* — a different axis of vulnerability that the
current formulation does not address.

If evidence decay is real, the implication for L4 goal-attribution scoring is:
any implementation must include a **evidence freshness weight** that decays
the contribution of an outcome proportionally to how long since its supporting
evidence was last verified.

### Edge cases

- **Self-citing experiments**: an experiment node citing itself has `integrity`
  trivially 1.0 (it *is* the evidence, no forward walk needed). These should
  be excluded from decay analysis or scored separately.
- **Bare-int evidence**: `evidence_runs: 1` is a direct attestation, not a
  reference. Such hypotheses cannot participate in forward-chain integrity
  checking. They report `integrity = N/A` and are excluded from the mean.
- **Deprecated intermediate nodes**: a build node on the path from experiment
  to hypothesis may be `status: deprecated`. Proposal: count as decayed —
  a deprecated node is no longer part of the active graph.
- **Multiple hypotheses per experiment**: one experiment may serve as evidence
  for multiple hypotheses. Decay of the experiment affects all of them equally.

## Agent Notes
Filed hypothesis on evidence decay — proved hypotheses may lose forward-chain connectivity to their supporting experiments as the graph evolves. Testable via forward-walk audit from evidence_runs through next_edges and parents.