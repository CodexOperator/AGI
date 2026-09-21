---
id: hypothesis:a03-1b139d1a-8b6adf
mint_id: cfa6c68f8c3e43faa5d2e693b4fa537f
type: hypothesis
parents:
  - goal:g3
next_edges: []
confidence: 0.0
edited_by: season.py
evidence_runs: []
scaffold_hash: 208188f8456db8e8
season: 1
thought_session: season
title: A03 1b139d1a 8b6adf
verdict: pending
---
# hypothesis:a03-1b139d1a-8b6adf

## Hypothesis

**Claim:** `outcome_coverage = mvps / hypotheses` overcounts meaningful goal
progress because a substantial fraction of mvps are not transitively
traceable to an active `goal:*` node. A goal-attribution metric — the
fraction of outcome/mvp nodes whose parent chain (recursively) includes
at least one active goal — will be materially lower than the raw
ratio, confirming that the proxy inflates perceived progress.

**What would prove it:** A scan of all mvp nodes in the corpus finds that
≥20% have no transitive path (via `parents:`) to an active `goal:*` node.
That gap is the inflation: those mvps contribute to the numerator of
`outcome_coverage` but do not represent any active goal being fulfilled.

**What would disprove it:** Fewer than 20% of mvps are orphaned (not
traceable to any active goal). The proxy is tight enough that building
true goal-attribution scoring would not materially shift the metric
for this corpus.

**Why this matters (g3 L4):** The g3 invariants state that no primary
metric should be shiftable by appending hops. `outcome_coverage` is
exempt from hop-gaming by construction (mvp-per-hypothesis is
hop-independent), but it is vulnerable to *goal-gaming*: nothing stops
a chain from producing an mvp/outcome unrelated to any active goal
and still counting toward the ratio. A goal-attribution filter —
counting only mvps whose parent chain contains an active `goal:*` —
would close this second vector.

## What would it take to resolve

1. Scan all `.agi/nodes/mvp/*.md` and `.agi/nodes/outcome/*.md`,
   `.agi/nodes/bigger_outcome/*.md` for their `parents:` field.
2. For each parent id, resolve to that node file and check its own
   `parents:` recursively, stopping at 20 hops (loop guard).
3. Count how many parent chains reach an active `goal:*` node (filtering
   by `status: retired | complete` to exclude inactive goals).
4. Compare: `attributed_ratio` vs raw `mvps / hypotheses`.

A proven claim → spawn an `idea:` node for the goal-attribution scorer
and a `build:` for its implementation. A disproven claim → the proxy
is good enough for this corpus, re-open g3's L4 when the corpus
changes materially.


## Agent Notes
Hypothesis: outcome_coverage (mvps/hypotheses) overcounts vs transitive goal attribution. Claim: >=20 percent of mvps have no parent-chain path to an active goal node. Proved by scan disproved if under 20 percent. g3 L4 open problem.