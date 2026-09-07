---
id: hypothesis:a07-1850cc5d-39f57c
mint_id: a4e2f643bceb4858a40fc45d2767745f
type: hypothesis
parents:
  - goal:g4.8
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 14421efef6aebbf5
season: 1
testable_claim: A delegator reading parent-summary reports, each compressing M kid outcomes into one bounded report, consumes token cost growing sub-linearly in the number of concurrent loops N
thought_session: season
title: Parent reports are size-bounded, so delegator cost is sub-linear in loop count
verdict: pending
---
# hypothesis:a07-1850cc5d-39f57c

## Hypothesis

A delegator reading parent-summary reports (each compressing M kid outcomes into one report) consumes token cost that grows sub-linearly in the number of concurrent loops N, because each parent report is bounded in size regardless of the number of kids it supervised.

### Testable claim

Given N loops (1 parent, M kids each), the delegator reads N parent reports. Each parent report contains:
- A structured verdict table: N kid-ids + verdicts + evidence-run counts (constant-size per row, O(M) rows)
- A delta summary: what changed this iteration (bounded, typically <500 tokens regardless of M)
- A section of defects found: the number of defects is a function of the parent's thoroughness, not of M

Let:
- `K` = avg tokens consumed reading one kid hypothesis body (~1500-3000 tokens for a full hypothesis with "What would prove/disprove" sections)
- `P` = avg tokens consumed reading one parent report (~500-800 tokens for a delta summary + verdict table)
- `N` = number of concurrent loops
- `M` = number of kids per loop

Then: delegator cost = N × P, while total kid-evaluation cost = N × M × K.

The ratio P / (M × K) → 0 as M grows. For the falsifier's claim of "sub-linear in the number of loops", this means: T_delegator(N) = O(N) × constant, where the constant P is independent of M, so T_delegator is sub-linear in N × M × K (total agent output). By the traditional definition (sub-linear = o(N)), T = c × N is linear, not sub-linear — but the falsifier clause defines it relative to total work produced: the delegator's spend grows slower than the total agent output. That is the intended meaning, and this hypothesis tests it by measuring the ratio directly.

### What would prove it

A synthetic benchmark measuring token consumption of reading:
- 1 kid full hypothesis body (avg tokens consumed)
- 1 parent summary report (avg tokens consumed)
- 1 delegator session reading N parent reports (for N=2, 4, 8)

The claim holds if:
1. A single parent report consumes < 1/3 the tokens of a single kid hypothesis body (P < K/3)
2. Reading N parent reports consumes < N × K / 3 tokens (i.e., less than reading N kid bodies)
3. The parent report token count does not grow proportionally with M: P(M=5) < 1.5 × P(M=2), because the verdict table grows but the summary + defects sections are bounded
4. A full delegator session reading 8 parent reports consumes fewer tokens than reading 2 full kid hypotheses — demonstrating sub-linear growth relative to total agent output

### What would disprove it

- A parent report grows linearly with M: P(M) ≈ M × constant, making P ≈ K and the delegator gets no savings
- Reading 8 parent reports consumes more tokens than reading 1 kid hypothesis (delegator cost is worse than nothing)
- The parent's compressions are lossy — the delegator must re-read kid bodies to resolve defects found, negating the savings
- Token consumption of reading a report is dominated by the model's reasoning overhead (re-processing every verdict), not the text length, making the ratio approach 1 regardless of P/K

### Relation to g4.8

Directly tests g4.8 falsifier **clause 4** — "the delegator's own token spend is sub-linear in the number of loops." Also relates to clause 3 (parent review gate) — if the parent cannot produce a reliable, bounded-size delta summary, the delegator cannot be sub-linear. The two clauses share a mechanism.


## Agent Notes
Filled scaffold for delegator sub-linear spend hypothesis (g4.8 falsifier clause 4). Claims parent report token cost P is bounded and < K/3 per kid hypothesis, making delegator spend sub-linear in total agent output. No experiments yet — pending.