---
id: hypothesis:a00-003fffb0-388249
mint_id: 4723b37526d144d7be87f48acf2ef480
type: hypothesis
parents:
  - goal:g4.8
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 168fb6b5cc705e84
season: 1
testable_claim: The delegator's token spend (input tokens to read + output tokens to judge) scales with the **number of parent-level summary reports**, not with the total number of nodes produced across all loops. If P parents each produce one structured summary report reviewing K kids each, the delegator reads O(P) reports rather than O(P×K) full kid nodes — spending fewer tokens per unit of graph growth as P×K grows.
thought_session: season
title: Delegator spend is sub-linear in loop count if review is by-summary not by-node
verdict: pending
---
# hypothesis:a00-003fffb0-388249

## Hypothesis

### Testable claim

The delegator's token spend (input tokens to read + output tokens to judge) scales with the **number of parent-level summary reports**, not with the total number of nodes produced across all loops. If P parents each produce one structured summary report reviewing K kids each, the delegator reads O(P) reports rather than O(P×K) full kid nodes — spending fewer tokens per unit of graph growth as P×K grows.

### Formal statement

Let:
- P = number of concurrent parent loops
- K = kids per parent (uniform, for analysis)
- T_kid = tokens to read one full kid node (body + frontmatter, ~2-8KB)
- T_report = tokens to read one parent summary (~0.5-1KB, structured)
- S_delegator = delegator's total input tokens per iteration

**Claim:** S_delegator(P, K) = P × T_report + c, where c is constant overhead (brief + instructions), and critically:
- S_delegator grows O(P), not O(P×K)
- The ratio S_delegator / (P×K) → 0 as P×K grows
- The ratio S_delegator / P is bounded (constant per parent, regardless of K)

### What would prove it

An analytical measurement — not a live loop — that demonstrates the structural property:

1. Take two static configurations:
   - Config A: 1 parent, 10 kids. Delegator reads 1 parent report + 1 brief + instructions.
   - Config B: 5 parents, 2 kids each (10 kids total). Delegator reads 5 parent reports + 1 brief + instructions.

2. Measure T_kid (mean tokens to read a full kid node from the existing graph) and T_report (mean tokens to read a parent summary, estimated from the existing `hypothesis:a00-a54f694b-b20b78` parent review node).

3. **Proved if:**
   - S_delegator(B) < 5 × S_delegator(A) — sub-linear in loop count vs a naive 5× scaling.
   - S_delegator(B) / S_delegator(A) < B's parent count / A's parent count — delegator grows slower than parent count.
   - S_delegator(B) / (5×2) < S_delegator(A) / (1×10) — cost per kid node is lower when more parents are present.

4. The strongest version: a linear regression of S_delegator against P×K that shows delegator spend is explained by P (parent count) and not by K (kids per parent).

### What would disprove it

- S_delegator(B) ≈ S_delegator(A) — delegator reads every kid node regardless of hierarchy (the structural compression does not exist).
- S_delegator(B) ≈ 5 × S_delegator(A) — delegator's cost grows linearly with loop count, proving no sub-linear advantage exists.
- S_delegator grows with total nodes (P×K) rather than with parent count (P) — the hierarchy buys nothing in token terms.
- A parent summary is not meaningfully smaller than a kid node (T_report ≈ T_kid), so reading P reports costs the same as reading P×K kids — compression failed.

### Relation to g4.8

Directly tests **falsifier clause 4**: "the delegator's own token spend is sub-linear in the number of loops." This clause exists because if the delegator reads everything linearly, the tiered architecture has no cost advantage over flat dispatch — every loop adds the same per-node read cost regardless of hierarchy. A proved hypothesis here means the tier has structural efficiency; a disproved one means a parent's summary must be engineered explicitly for compression (e.g., fixed-format checksum review, not free-text analysis).

### Precedent

`hypothesis:a00-07b2223d-b21977` (parent review gate, clause 3) already argues that structural review — checking frontmatter fields rather than re-reading hypotheses — is what keeps parent review sub-linear. This hypothesis extends the same principle one level up: the delegator reviews parent summaries structurally rather than re-reading every kid. The two clauses together describe the review hierarchy: kids produce structured verdicts → parents check structure (clause 3) → parents produce structured summaries → delegator checks structure (clause 4).


## Agent Notes
Hypothesis testing g4.8 falsifier clause 4: delegator token spend scales O(P) via parent summaries, not O(P×K). Novel claim — no prior hypothesis covers clause 4. Targets the whole value proposition of the tiered architecture.