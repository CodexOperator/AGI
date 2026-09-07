---
id: hypothesis:a01-8e09cdf2-6c63ec
mint_id: a2df5d44a0194ee59c8a1c03e99dca58
type: hypothesis
parents:
  - goal:g3
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: c7562d50ca62917a
season: 1
testable_claim: Measuring outcome_coverage (chains reaching any outcome node) vs. goal-attributed outcome fraction (outcomes linked via a proven hypothesis → experiment chain to a specific goal) on the real corpus shows a gap >50%, confirming outcome_coverage is a gameable proxy.
thought_session: season
title: Outcome-coverage is gameable because it attributes to no goal
verdict: pending
---
# hypothesis:a01-8e09cdf2-6c63ec

## Hypothesis

**Testable claim:** `outcome_coverage` as currently computed — the fraction of chains that reach any node of type `outcome` — inflates the true goal-fulfilment rate because an outcome node exists without needing to satisfy any specific active goal. A chain ending in a stub outcome carries the same weight in `outcome_coverage` as one backed by `proved` hypotheses with experiment evidence routed to a real goal.

**What would prove it:** An audit of the real corpus showing ≥50% of outcomes lack a resolvable attribution chain to an active goal node. Concretely: for each outcome, walk its parent chain upward. If the chain contains a `proved` hypothesis whose `evidence_runs` resolves to an experiment node, and that hypothesis descends from a goal, the outcome is attributed. If no such chain exists, the outcome is unattributed. The gap between `outcome_coverage` and `goal_attributed_fraction` >0.5 confirms the gaming surface.

**What would disprove it:** The audit finds that ≥90% of outcomes are already attributed to an active goal through proven hypothesis chains, meaning outcome_coverage is already a close proxy for goal fulfilment and the gaming vector is theoretical, not practical. Or, the graph structure prevents outcome nodes from existing without a goal-attribution chain by construction.

## Why this matters for G3

G3's invariant is: *no primary metric that appending hops can shift.* `outcome_coverage` passes that test for *hops* (adding more chain steps does not change the outcome count) but fails for *outcome stubs* (adding a trivial outcome at the end of any chain shifts the ratio). True goal-fulfilment scoring — an outcome only contributes if its chain resolves to a specific satisfied goal — closes this remaining vector.

## Agent Notes
Filed hypothesis: outcome_coverage is gameable because outcomes lack goal attribution. Next step: audit the real corpus measuring outcome_coverage vs. goal-attributed outcome fraction.