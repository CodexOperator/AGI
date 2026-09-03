---
id: hypothesis:a06-4714fa2c-c75aec
mint_id: 01eec8b2134542cc8944ef7f97c2e26d
type: hypothesis
parents:
  - goal:g4.8
next_edges: []
scaffold_hash: a4cc57f4a421ff27
title: "Delegator token spend is sub-linear in loop count via structural delta review"
testable_claim: "When a delegator directs N concurrent parent loops, its per-loop token consumption decreases as N grows because parents report structural deltas (verdict changes, metric diffs, exit codes) rather than full node bodies — the delegator reads full content only for anomalous deltas, so marginal cost per additional loop approaches zero."
confidence: 0.0
verdict: pending
---

# hypothesis:a06-4714fa2c-c75aec

## Hypothesis

The delegator (director) in `goal:g4.8`'s three-tier model reviews N concurrent parent loops.
For delegator token spend to be sub-linear in N, it cannot read all N parent briefs fully.
The mechanism is: **each parent reports a structural delta** — a machine-readable block
listing which kids changed status, which verdicts shifted, which metrics moved — and the
delegator inspects only the deltas flagged as anomalous. Routine completions cost roughly
fixed tokens (verify exit code, log the delta), while anomalous ones cost full reading.

Thus as N grows, the marginal delegator cost per loop approaches zero because the share
of anomalous completions is small and bounded, not proportional to N.

### Testable claim

With N concurrent parent loops, each producing a structural delta at completion:

- Delegator token consumption for N loops is **sub-linear** — measurable as
  `cost(N) / cost(1) < N` for all N > 1.
- The fraction of parents whose delta is anomalous (triggering a full read) is
  bounded by a constant `A < 0.2`, independent of N.
- Delegator review quality (measured by detection rate of real issues) does not
  degrade as N grows — sub-linear spend is not achieved by skipping important content.

### What would prove it

An experiment simulating a delegator reviewing N parent deltas at N ∈ {1, 4, 16}:

- **N=1 (baseline):** delegator reads one parent brief fully. Record total tokens.
- **N=4 (linear check):** each parent reports a structural delta. Delegator must
  read at most 1 full brief (the one anomalous one). Token cost < 2× baseline.
- **N=16 (sub-linear stretch):** all 16 parents return deltas, 1-2 anomalous.
  Delegator reads 1-2 full briefs. Token cost < 3× baseline.
- Quality: the anomalous parents are correctly detected (no false negatives);
  routine parents are not accidentally read (no false positives).

Pass if `cost(16) / cost(1) ≤ 3` and detection rate ≥ 0.8.

### What would disprove it

- Delegator reads every parent brief fully at any N — token cost grows linearly with N.
- `cost(16) / cost(1) > 5` — the sub-linear property fails.
- Anomalous rate grows with N (e.g., 5/16 anomalous at N=16, forcing proportional reads).
- Delegator misses real anomalies because it only reads deltas (detection rate < 0.5).

### Relation to g4.8

Directly tests falsifier **clause 4** — "the delegator's own token spend is sub-linear
in the number of loops" — which is the last remaining untested clause in g4.8's
falsifier. Clause 3 (parent review gate) has its own hypothesis; clause 2
(concurrency bound) is proved. This hypothesis isolates clause 4 as a separately
falsifiable claim with a concrete mechanism.

### Why not tested as part of an end-to-end parent loop run

The delegator's review cost is a property of the review protocol (delta format +
anomaly detection), not of the parent's spawning machinery. An end-to-end run with
real parent loops would mix process overhead, spawn cost, and kid token spend into
the measurement. This hypothesis isolates the delegator's marginal cost by substituting
simulated parent deltas — the review protocol is the variable, not the harness.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted iter-1005 as agent a06-4714fa2c. Targets g4.8 falsifier clause 4, the only
remaining untested clause. The mechanism is structural delta reporting, chosen over
batching or sampling because it preserves review quality (anomalies still trigger full
read) while letting routine completions cost near-zero tokens. The 0.8 detection
threshold in proof clause is lenient by design — the first experiment should measure
the baseline, not set a bar that forces a false disproval.
<!-- THOUGHT:END -->

## Agent Notes
Hypothesis for g4.8 falsifier clause 4: delegator token spend is sub-linear in loop count via structural delta review — last remaining untested clause
