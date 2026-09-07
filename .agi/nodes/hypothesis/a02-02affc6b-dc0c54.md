---
id: hypothesis:a02-02affc6b-dc0c54
mint_id: 2a54415179764754aae2be4ccea55621
type: hypothesis
parents:
  - goal:g4.8
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 82e64f9e6774bd2e
season: 1
testable_claim: A delegator reviewing P parent briefs -- each parent reviewing its own kids -- spends tokens sub-linearly in total loops L = P x M, because it reads P short parent briefs rather than L kid nodes
thought_session: season
title: Delegator token cost is O(P) in parent count, not O(L) in total loops
verdict: pending
---
# hypothesis:a02-02affc6b-dc0c54

## Hypothesis

A delegator (director) reviewing P parent briefs — each parent's review of its own kids — spends tokens sub-linearly in total loops L = P×M, because the delegator reads only P short parent briefs rather than L kid nodes. Specifically: delegator token cost ≈ O(P) where P << L, not O(L).

### Testable claim

With P parents each managing M kids (total L = P×M loops), the delegator reading only the P parent briefs:
- Delegator token spend per review cycle < (P × max_brief_tokens) where max_brief_tokens is bounded (e.g., < 4K tokens per brief).
- Delegator token spend < (L × min_hypothesis_tokens) where min_hypothesis_tokens is what a single kid hypothesis requires to read — demonstrating sub-linear scaling.
- The delegator correctly catches at least one defect the parent missed (or correctly passes a parent brief with no missed defects), proving the brief is sufficient for oversight.
- The delegator does NOT need to read any kid node to produce its verdict on the parent's quality.

### What would prove it

An experiment running 2 parents (P=2), each spawning 3 kids (M=3, L=6 total), where:
- Parent A produces a brief of ~2K tokens (summarizing 3 kids, flagging one issue).
- Parent B produces a brief of ~3K tokens (summarizing 3 kids, passing all cleanly).
- Delegator reads both briefs and produces oversight verdict in < 10K tokens total.
- Total delegator cost: ~5K tokens. Cost to read all 6 kid hypotheses directly: ~30K+ tokens (6 × ~5K each). Ratio: 5K/30K = ~0.17, clearly sub-linear.
- Delegator correctly identifies the issue Parent A flagged (or independently spots a gap) — proving the brief contains enough signal.

### What would disprove it

- Delegator token spend is ≥ O(L) because it must re-read every kid node to verify parent claims — the brief is too lossy to stand alone.
- Parent briefs grow linearly with M (each parent must describe every kid in full), so P briefs together ≈ L kid nodes — no savings.
- Delegator misses a defect the parent also missed, and the only way to catch it was reading kid nodes — proving the brief provides insufficient signal for oversight.
- Delegator cannot produce a verdict from briefs alone without escalating to the full kid tree.

### Relation to g4.8

Directly tests g4.8 falsifier **clause 4** ("the delegator's own token spend is sub-linear in the number of loops"). This is the largest untested gap in g4.8's falsifier — clauses 2 and 3 are covered by sibling hypotheses (`shared-lease-bounds-the-tree`, `a00-07b2223d-b21977`), clause 1 is g4.1 territory, clause 5 is model-tier verification by inspection. Clause 4 is the economic claim that makes the delegator tier worthwhile: if the director must read everything anyway, the tier buys nothing.

## Agent Notes
Hypothesis: delegator achieves sub-linear token spend by reading P parent briefs rather than L kid nodes. Tests g4.8 falsifier clause 4 — largest untested gap. Pending: no experiment yet.