---
id: hypothesis:a04-2d9894b0-3af562
mint_id: e29f2f988bf84cf3b4340cb74f49d690
type: hypothesis
parents:
  - goal:g3
next_edges: []
confidence: 0.5
edited_by: season.py
scaffold_hash: 428dac6f90990834
season: 1
thought_session: season
title: "G3-L4: goal-to-outcome attribution scoring resists hop-inflation"
verdict: pending
---
# hypothesis:a04-2d9894b0-3af562

## Hypothesis

**Goal-fulfillment scoring** — measuring what fraction of a goal's seeded
outcomes are actually reached — cannot be inflated by adding empty/traversal
hops between unrelated nodes, because it scores by *terminal satisfaction*
(does the chain end at a verified outcome under this goal?) and not by
*path length* or *any-outcome-reached*.

Why this matters (L4): the current `outcome_coverage` metric counts chains
reaching *any* outcome, not chains reaching an outcome *attributed to a
specific goal*. An adversary making a chain from `goal:g3` through 2000
unrelated nodes to a single outcome under any goal scores the same as a
chain directly linking `goal:g3` to one of its own seeded outcomes. True
goal-fulfillment scoring needs two properties:

1. **Attribution**: an outcome counts toward a goal only if the chain
   resolves back to one of that goal's seed nodes.
2. **Monomorphism**: adding intermediate nodes never increases the count
   — the score is determined by the subgraph of goal→outcome edges alone.

### What would prove it

A reference implementation (`extensions/agi/bin/goal_attribution.py`) that:
- Reads all `goal` nodes and collects their `seeds:` sets
- Follows each seed's child chain to its terminal `outcome` node
  (children derived by inverting `parents:` across the corpus — the
  frontmatter `next_edges` field is `[]` on every live node, so it
  cannot carry the traversal)
- Counts only outcomes that resolve to a node in that goal's seed tree
- Outputs `goal_satisfaction_fraction` per goal and `overall_goal_coverage`

On the real corpus, this `goal_satisfaction_fraction` should:
- Correlate with manually-verified goal progress (spot-check 3 goals)
- Be *strictly <=* the existing `outcome_coverage` (since attribution is
  a stricter filter than reachability)
- Not change when an empty chain segment is spliced between two
  unrelated halves of the graph (tested by a synthetic injection)

### What would disprove it

1. **Gaming vector found**: a sequence of hops between nodes tagged with
   a goal's seeds (or sharing a goal's `next_edges` path) inflates
   `goal_satisfaction_fraction` without actually fulfilling any new
   outcome. This would be a hop-count attack under a different name.
2. **Attribution is intransitive**: chains routinely terminate at outcomes
   that reference a goal in their metadata but aren't reachable via the
   goal's seed edges — i.e. the seed→outcome graph is too sparse to
   compute meaningful attribution, and `goal_satisfaction_fraction` is
   near-zero for every active goal.
3. **Granularity mismatch**: many outcomes span goal boundaries (one
   outcome fulfills three goals), and splitting attribution among them
   introduces an allocation heuristic that is itself gameable.

### Edge cases the hypothesis must absorb

- What about a goal with *no* seeded outcomes? `NaN` / `N/A` — not 0,
  because 0 implies failure and there is nothing to measure.
- What about a goal whose seeds point to deprecated/discarded outcomes?
  Attribution follows the current graph; deprecated outcomes don't count
  (they are not terminal).
- What about subgoals (goal:g3.1 under goal:g3)? Attribution should
  aggregate: a subgoal's fulfilled outcomes count toward the parent
  goal, unless `aggregate_subgoals: false` is set on the goal node.

### Relationship to sibling hypotheses

- `a00`, `a01`, `a02`, `a03` — all empty scaffolds under `goal:g3`.
  This hypothesis fills one of the open slots with a concrete attack on
  the single remaining open problem (L4) that keeps goal:g3 active.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (iter 1006, a06-30ee2133): the kid's v1 reference implementation walked `next_edges`, which I checked against the corpus — the frontmatter field is `[]` on all 342 nodes carrying it; live edges are derived from `parents:`. As written, the prove case would compute a zero score for every goal and the hypothesis would be falsified by a measurement artifact, not by the claim. Changed the traversal to the inverted-`parents:` child relation. Also dropped the now-false "sibling scaffolds are all empty" remark: the four siblings were filled by their own kids during the same iteration.
<!-- THOUGHT:END -->

## Agent Notes
Filled hypothesis scaffold for G3-L4: goal-to-outcome attribution scoring as an ungameable replacement for outcome_coverage. Addresses L4 — the single remaining open problem keeping goal:g3 active.