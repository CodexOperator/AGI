---
id: hypothesis:a00-cfbdfb1e-02df1d
mint_id: 1810f306aeb24a6eb13599ce1e8779a3
type: hypothesis
parents:
  - goal:g3
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 137b8a9e6d0aff08
season: 1
thought_session: season
title: Evidence-gate existence resolution misses relevance — cross-goal citation inflates coverage
verdict: pending
---
# hypothesis:a00-cfbdfb1e-02df1d

## Hypothesis

**The evidence gate resolves `evidence_runs` entries by existence (does the node id
resolve in the corpus?) but not by relevance (does the cited experiment share a
parent-chain connection with the citing hypothesis?). A hypothesis under goal:g1
can cite an experiment under goal:g2 as backing evidence, pass the gate, and
contribute `proved` status to goal:g1's `outcome_coverage` — even though the
experiment tested a claim for a different goal entirely.**

Why this matters for goal:g3: G3's invariant is that *added motion cannot move
the score*. The evidence gate (H4, H4c) already closes the vectors of sentinel
`evidence_runs` and bare-int self-attestation. But it leaves open a **relevance
gap**: existence of the cited node is sufficient; logical relevance is never
checked. An agent that wants to prove a hypothesis under a hard goal can cite
an experiment from an easy goal — same cost as citing the correct one, same
gate pass, same metric contribution. The motion (creating the citation) is real;
the score benefit is spurious.

### What would prove it

1. **Synthetic test**: construct two goal subtrees — `goal:gA` with hypothesis
   `hyp:A1` arguing claim A, and `goal:gB` with experiment `exp:B1` testing
   claim B. Write `hyp:A1`'s frontmatter with `verdict: proved evidence_runs:
   ["exp:B1"]`. Run `apply_gate(hyp:A1_verdict, hyp:A1_evidence_runs,
   corpus=corpus)` and confirm `GateResult.ok == True` — the gate passes a
   cross-goal citation as valid.

2. **Metric contamination**: after the gate passes, `evidence_stats` against
   the same corpus reports `evidence_fraction` with hyp:A1 counted as
   "backed" — even though the backing experiment tests an unrelated claim.
   `outcome_coverage` includes hyp:A1's mvp (if one exists) in the numerator
   for goal:gA, but the experimental work happened under goal:gB.

3. **Real corpus audit**: scan all `proved` hypothesis nodes in the real corpus
   and for each, walk the cited experiment's parent chain. Count what fraction
   of those experiments share at least one ancestor goal with the hypothesis
   that cites them. If >0% of proved hypotheses cite experiments from a
   *different* goal subtree, the relevance gap is real and exploited.

4. **Inflation demonstration**: for each misattributed citation found in (3),
   compute the mvp/hypothesis contribution to `outcome_coverage` for the wrong
   goal. Show that pruning these cross-goal citations (or demoting those
   hypotheses to `inconclusive_lean_proved:50`) drops `outcome_coverage`
   for the affected goals.

### What would disprove it

1. **Graph structure prevents it by construction**: every hypothesis and every
   experiment sits under exactly one goal subtree, and the writer paths enforce
   a parent-chain invariant that makes cross-goal citation impossible — either
   because experiments are only visible to hypotheses within their own goal's
   scope, or because `build_corpus` is partitioned per-goal.

2. **Zero instances in the real corpus**: the corpus audit finds that every
   `proved` hypothesis cites only experiments that share its goal chain. The
   gap is structural, not exploited.

3. **The gate already detects relevance implicitly**: `normalize_evidence_runs`
   with `self_id` checking means the cited experiment must be a node other than
   the hypothesis. But if the hypothesis's `parents:` chain and the experiment's
   `parents:` chain converge on the same goal, the citation is self-validating
   — a property that happens to be true of all current citations and is not
   an explicit check. The disprover would be that this convergence is a
   structural invariant of the writer path, not a coincidence.

4. **Relevance checking is intractable**: determining whether experiment E
   actually tests hypothesis H's claim requires semantic understanding, not
   graph structure. No syntactic or structural check can reliably distinguish
   a relevant citation from an irrelevant one, so the existence-only gate is
   the correct tradeoff.

### Relationship to sibling hypotheses

- **a00-94946187** (deprecation guard gap) — tests *removal* side of scoring
  integrity. This hypothesis tests the *creation* side: citations that exist
  but are irrelevant.
- **a00-9aeafcd1** (per-goal outcome_coverage disaggregation) — tests whether
  the aggregate masks per-goal variance. This tests whether cross-goal citation
  actively *transfers* metric credit between goals.
- **a00-c3912124** (gate/metric parity) — tests that `evidence_stats` and
  `apply_gate` agree on what counts as evidence. This tests that neither path
  checks relevance, which is a separate and consistent gap.
- **a01-8e09cdf2** (outcome_coverage gameable) — tests that outcomes lacking
  goal attribution inflate coverage. This tests that evidence *citations*
  lacking goal-relevance inflate coverage — a different vector at the evidence
  layer rather than the outcome layer.
- **a00-fc578adb** (evidence decay) — tests that evidence connectivity decays
  over time. This tests that *at creation time*, the evidence gate does not
  verify connectivity to the citing hypothesis.

### Edge cases

- **Self-citing experiments**: an experiment may legitimately cite itself
  (the gate allows it). If a hypothesis cites a self-citing experiment that
  shares no goal with the hypothesis, this is the same cross-goal gap — the
  experiment's self-citation says nothing about its relevance to the hypothesis.
- **Multi-goal experiments**: an experiment whose parent chain resolves to
  multiple goals. If one of those goals matches the citing hypothesis's goal,
  the citation is relevant for that goal — but the hypothesis might intend
  the experiment as evidence for a *different* claim under a *different* goal
  that the experiment does not test. The existence-only gate cannot distinguish
  this case from an honest multi-use citation.
- **Bare-int evidence_runs**: pre-G7.3 `evidence_runs: 3` has no node to
  resolve, so the relevance question is moot. This hypothesis only concerns
  list-shaped entries that resolve to real nodes.

### What this implies if proved

If cross-goal citation is real and non-trivial: the fix is to add a
**relevance check** to `apply_gate` and `evidence_stats` — a resolved
`evidence_runs` entry must share at least one ancestor goal (via parent-chain
walk) with the citing node. An experiment that does not share the hypothesis's
goal cannot serve as its backing evidence. This is a structural invariant, not
a semantic one: two nodes that trace to the same goal are in the same
problem-space by construction of the graph layout.

## Agent Notes
Evidence gate's existence-only resolution does not verify relevance: hypothesis can cite experiment from a different goal subtree. Gate passes if the experiment node id exists in corpus — no check that the shared a goal chain. Synthetic test + real corpus audit defined as prove conditions.