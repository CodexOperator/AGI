---
id: hypothesis:a00-c3912124-15653d
mint_id: 277aef84515b4052a88076dbe3a79026
type: hypothesis
parents:
  - goal:g3
next_edges: []
confidence: 0.0
scaffold_hash: 6e486e5c6ff46d06
title: A00 — evidence gate/metric parity and deprecation guard soundness
verdict: pending
---
# hypothesis:a00-c3912124-15653d

## Hypothesis

**Claim:** The `evidence_fraction` and `decisive_evidence_fraction` metrics
computed by `metrics.py:evidence_stats()` are self-consistent with the gate
in `evidence_gate.py:apply_gate()` — every node counted as *backed* by
`evidence_fraction` would have survived the gate undemoted, and every node
the gate would demote is counted as *unbacked*. Implementations share the
same `build_corpus` / `normalize_evidence_runs` import, eliminating the
drift that was the H4c root cause, but the claim has never been tested
against a corpus with mixed verdict states.

### Sub-claim 1 — gate–metric parity

For every verdict-bearing node in the graph, `normalize_evidence_runs`
returns the same count whether called from `evidence_stats` (during metrics
computation) or from `apply_gate` (during write). Since both call the same
function over the same `nodes_dir` corpus, the only source of disagreement
would be stale callers using different corpora — which is what the shared
import was designed to prevent. A round-trip test proves the invariant.

### Sub-claim 2 — the shadow-channel defect is closed

`SHADOW_VERDICT_FIELDS` rewrite (in `stamp()`) ensures that after a
demotion no frontmatter field reads `proved` or `disproved`. The
`shadow_decisive_verdicts` counter should read 0 once the lockstep demotion
has covered all nodes. The claim: there exists no node in the graph whose
`verdict:` has been demoted but whose `status:` field still carries the
original decisive word.

### Sub-claim 3 — taxonomy violations are never silently counted

`evidence_runs_violations()` catches non-id-shaped entries before
`normalize_evidence_runs` computes the count. `apply_gate` rejects such
entries outright (exit 2 for `cli.py done`); `evidence_stats` skips them
(since `normalize_evidence_runs` returns 0 for non-id entries without a
corpus, and 0 for non-id-shaped entries even with one). The claim: no
taxonomy-violation entry can reach the world as counted-backing evidence,
and the two paths agree on what a violation is.

### Prove

1. Synthetic corpus: build a test nodes directory with 6 nodes — two
   `verdict: proved evidence_runs: ["exp:real"]`, one
   `verdict: proved evidence_runs: ["synthetic"]`, one
   `verdict: disproved evidence_runs: []`, one
   `verdict: inconclusive_lean_proved:50 evidence_runs: []`, one
   `verdict: pending`. Run both `evidence_stats` and `apply_gate` against
   it. Verify:
   - `evidence_fraction = 2/3 = 0.667` (proved with `synthetic` counts as
     unbacked, disproved with no evidence is unbacked, leaning is
     asserting but optional as evidence, pending is excluded)
   - `decisive_evidence_fraction = 1/3` (only `exp:real`-backed is counted)
   - `apply_gate(proved, ["exp:real"], corpus=built corpus).ok == True`
   - `apply_gate(proved, ["synthetic"], corpus=built corpus).rejected == True`
   - `apply_gate(proved, [], corpus).demoted == True`
   - `apply_gate("inconclusive_lean_proved:50", [], corpus).ok == True`

2. Shadow verification: take a node whose `verdict:` was demoted to
   `inconclusive_lean_proved:50` while `status:` still reads `proved`.
   Run `shadow_verdict_fields(fm)` on its frontmatter. Verify it returns
   empty (the shadow has been rewritten). Run `evidence_stats` over a
   corpus containing this node. Verify `shadow_decisive_verdicts == 0`.

3. Cycle-resolution in parent-chain walk: construct a graph where a
   hypothesis's parent chain loops back on itself. Run `goal_attribution`.
   Verify it does not stack-overflow and returns a correct count that
   treats the looping node as unattributed (since its goal walk never
   terminates at a goal).

4. Deprecation guard arithmetic: construct a corpus with 5 hypotheses
   (2 deprecated) and 2 mvps (1 deprecated, 1 not). Run `goal_attribution`
   and then `deprecation_score_delta(attr)`. Verify the delta is <= 0,
   exactly `-0.333`. Verify the guard spares the non-deprecated mvp's
   hypothesis chain even when that hypothesis itself is deprecated (clause 3).

### Disprove

1. A real corpus corpus shows `evidence_fraction` and
   `decisive_evidence_fraction` disagree on a node that `apply_gate` and
   `evidence_stats` process differently — meaning the shared import has
   drifted or one caller has stale code.

2. A node whose `verdict:` has been demoted still carries a decisive word
   in a shadow field — meaning the lockstep rewrite missed a field, or a
   later edit restored it.

3. `deprecation_score_delta` returns > 0 for any input — disproving the
   arithmetic proof in the docstring.

4. The parent-chain walk crashes (stack overflow, key error) on any
   real or constructed graph — meaning `goal_attribution` is not cycle-safe
   as claimed.


## Agent Notes
Filled in hypothesis scaffold: evidence gate/metric parity, shadow defect closure, taxonomy violation handling, deprecation guard soundness. Defines 4 prove sub-claims (synthetic corpus round-trip, shadow-channel post-demotion emptiness, cycle-safe parent-chain walk, deprecation guard arithmetic) and 4 disprove criteria (drift between evidence_stats and apply_gate, residual shadow decisive field, positive deprecation_score_delta, stack overflow in parent walk).
