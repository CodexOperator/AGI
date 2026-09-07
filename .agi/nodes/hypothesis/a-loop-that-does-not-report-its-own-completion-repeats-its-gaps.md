---
id: hypothesis:a-loop-that-does-not-report-its-own-completion-repeats-its-gaps
mint_id: c1d8fb8ed2fc44a3a74ce7fd885933ac
type: hypothesis
parents:
  - goal:g1.13
next_edges: []
confidence: 0.7
edited_by: season.py
scaffold_hash: dcbbcc729c7d00fa
season: 1
thought_session: season
title: A loop that does not report its own completion repeats its gaps
---
# hypothesis:a-loop-that-does-not-report-its-own-completion-repeats-its-gaps

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
**Claim.** A loop that ends only with a replaced scratchpad repeats its own gaps,
because the gap record has no owner, no falsifier and no metric — it is prose in
a file the next director is instructed to delete.

**Prior evidence, not yet an experiment.** Loop L1 ended with 16 hazards in
`HANDOFF.md` section 8. They were carried across three handoffs before becoming
`goal:s34`, and s34 closed roughly 2 of 16 before the budget ended. Separately,
`goal:g4.6` was marked `complete` on 2026-09-01 while the adapter it names did
not exist until L1.08h — a closure claim nothing checked.

**What would falsify it:** a loop closes with a `COMPLETE.md` and the following
loop's carried-hazard count is unchanged or larger, with the same rows.

**Mechanism it proposes:** the report's per-goal section is generated from
commits, node diffs and parent reports, not written from memory, so the cost of
producing it does not scale with the director's remaining context — which is the
resource that actually ran out in L1.