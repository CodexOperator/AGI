---
id: hypothesis:a01-2a74553c-ae68b4
mint_id: 203b2b25319c4429a328f9b076b66aa2
type: hypothesis
parents:
  - goal:g4.8
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 3294874fda810824
season: 1
testable_claim: "With one delegator (director) and P parents, each parent having spawned K kids and produced one parent summary node:"
thought_session: season
title: "Delegator token spend is sub-linear in loops: parent summaries replace kid re-reads"
verdict: pending
---
# hypothesis:a01-2a74553c-ae68b4

## Hypothesis

A delegator reviewing N parent-level summaries spends tokens proportional to
N (each parent writes a brief), not to the sum of each parent's kids — so token
growth is sub-linear in the total number of loops when each parent runs M kids.

### Testable claim

With one delegator (director) and P parents, each parent having spawned K kids
and produced one parent summary node:

- The delegator reads **P summary nodes** (one per parent), not P×K kid nodes.
- The delegator's token cost to ingest and produce a verdict on the round
  is **O(P)** with respect to the total kid count P×K.
- Each parent's summary node is **structurally shorter** than the union of its
  kids' nodes: it states verdicts and flags anomalies, not re-derives evidence.

Stated as a ratio: with P=2 parents each running K=3 kids, the delegator reads
2 nodes (P) rather than 6 (P×K). The token ratio `tokens_delegator / tokens_kids`
should be approximately `1/K` — one parent summary replaces K kid reads.

### What would prove it

An experiment with 1 delegator, 2 parents, 3 kids each (6 total kids):

1. Each kid writes a hypothesis body of typical length (~500 tokens).
2. Each parent reads its 3 kids and writes a **parent review summary node**
   (~500 tokens) listing verdicts, defects, and actions for the delegator.
3. The delegator reads both parent summaries and no kid nodes directly.
4. Delegator produces a top-level assessment without opening any kid node.

Proof criteria:
- Delegator's ingested tokens ≤ 2× parent-summary length < 6× kid length.
- Delegator assessment is correct: it reports the same verdicts the experiment
  would yield if the delegator read all 6 kids directly.
- The accuracy check is automated: extract the verdict from each kid's node,
  compare to the delegator's assessment — if ≥5 of 6 match, the parent-summary
  structure preserved enough information.

### What would disprove it

- Delegator must read kid nodes to resolve ambiguities the parent summary
  left open → actual read count > P.
- Parent summaries grow linearly with K (each summary re-states all kids'
  evidence) → the ratio never approaches 1/K.
- Delegator assessment misses a material defect that parent summary hid →
  summary loses information, gains tokens, keeps no advantage.
- The `O(P)` property holds only because summaries are produced by an LLM,
  which itself costs P×tokens_parent tokens — shifting the cost upstream
  without reducing system-wide spend. (This does not disprove the hypothesis
  but limits its value: delegator spend is sub-linear in loops, but total
  system spend including parent review may not be.)

### Relation to g4.8

Tests falsifier **clause 4**: the delegator's own token spend is sub-linear
in the number of loops. If a delegator must read every kid node to judge a
round, then adding loops costs linearly — the hierarchy has bought nothing.
If parent summaries replace kid re-reads, the delegator's cost grows with the
number of parents, which for K≥2 is sub-linear in total loops.

**This clause is what makes the delegator tier worth its model cost.**
A director on the largest model ($/token) earns its cost only by multiplying
what the tiers below produce — and that multiplication fails if the director
reads every node the tiers below wrote.

Also tests the final sentence of clause 3: "Parents review kids and report
deltas; the delegator reviews parents." The mechanism assumes summaries that
compress; this hypothesis tests whether they actually do.

## Agent Notes

Hypothesis: parent summaries compress K kid reads into 1 read for the
delegator, making delegator token spend O(P) rather than O(P×K). Targets
g4.8 falsifier clause 4 — the whole economic argument for the hierarchy.



## Agent Notes
Delegator token spend O(P) vs O(PxK) via parent summaries — tests g4.8 falsifier clause 4, sub-linear in loops