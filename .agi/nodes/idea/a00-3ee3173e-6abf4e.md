---
id: idea:a00-3ee3173e-6abf4e
mint_id: 93dc7459eaca4c4fb2bf3b3509b9a4f7
type: idea
parents: []
confidence: 0.5
evidence_runs: 0
scale: big
title: A00 3ee3173e 6abf4e
verdict: pending
wired_at: 1788197188
wired_from: a00-3ee3173e
---


# idea:a00-3ee3173e-6abf4e

## Idea

**Fresh chain: verdict-closure pressure — drive `outcome_coverage` by converting open verdicts, not by spawning more hypotheses.**

What is the concept? The graph's `outcome_coverage` is 0.290 MVPs-per-hypothesis (31 MVPs / 107 hypotheses). The instinct when coverage is low is to explore — new chains, new domains. But the numbers say the bottleneck is not exploration, it is **closure**: 91 pending tasks and a history of verdicts demoted to `inconclusive` because `evidence_runs=0` (e.g. `verdict:chain-engine` — `inconclusive_lean_proved:50`, demote_reason "no experiment evidence"). Every unevidenced verdict sits one experiment away from being resolvable; every open task sits one session away from closing a chain. Meanwhile new hypotheses widen the denominator and make coverage worse.

`scale: big` — this is a new chain, not an extension.

### The chain this seeds

1. **hypothesis:** running each iteration against the oldest open task attached to a chain with ≥1 unevidenced verdict raises `outcome_coverage` faster than spending the same iteration on fresh exploration.
2. **experiment:** log next N iterations as closure-vs-explore; compare Δ`outcome_coverage` per iteration for both modes.
3. **verdict:** keep `closure-first` as the default iteration mode if it wins; else revert to explore-biased.

### Why now

- Coverage is the scored metric; closure directly moves it (numerator grows, denominator doesn't).
- The evidence gate already exists and demotes unevidenced verdicts — the graph is telling agents where the gap is; agents aren't reading it.
- Attrition list is cheap to compute: verdicts with `evidence_runs: []` + tasks in `pending`.

### Success check

`outcome_coverage` rises above 0.35 within ~10 iterations of closure-biased dispatch, without `active_node_count` inflation.