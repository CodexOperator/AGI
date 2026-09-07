---
id: verdict:a01-456d6797-e654a7
mint_id: 262d787aad4449e99f62b7f1d610b643
type: verdict
parents:
  - experiment:a01-13ffe40a-854998
next_edges: []
confidence: 0.65
edited_by: season.py
scaffold_hash: 71dce80d79cdff66
season: 1
thought_session: season
title: A01 456d6797 e654a7
verdict: inconclusive_lean_disproved:65
---
# verdict:a01-456d6797-e654a7

## Verdict

inconclusive_lean_disproved:65

## Evidence

Two independent experiment runs (experiment:a01-13ffe40a-854998 and
experiment:a00-020e970e-5f2470) on the full corpus each reproduce identical
results: global binary outcome_coverage = 0.1343, confidence-weighted = 0.1000,
global gap = 0.0343.

**Claim verification across both runs:**
1. Active goal with gap > 0.2? **FAIL** — max active gap is 0.1500 (g1.10)
2. Goal with M/G > 0 but weighted < 0.05? **PASS** — g4.6 (but via orphan mvp,
   an attribution effect, not low confidence)
3. Global gap >= 0.05? **FAIL** — actual gap = 0.0343

The hypothesis's own falsifiers do not all fire: confidence IS present and
meaningful on hypothesis nodes (>80% of scoring-eligible hyps have
deliberate confidence values). The third falsifier (Pearson r > 0.95 between
binary and weighted scores) was **not computed by either run** — both
experiment nodes report no correlation statistic — so it stands untested,
not satisfied.

**Key finding:** The gap is small (0.0343 global) because hypotheses that reach
mvps tend to have high confidences (0.75-0.90). The claimed magnitude (>0.2
per-goal gap on active goals) was not observed; the max active gap is 0.15.
Orphan mvps (no hypothesis chain) produce the largest per-goal gaps but are
an attribution problem, not a confidence-weighting problem.

## Confidence

0.65

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Two sibling experiments, both parent-reviewed, reproduce exactly the same core
metrics (0.1343 / 0.1000 / 0.0343) — strong reproducibility. Verdict is
inconclusive_lean_disproved:65 (one notch above the individual experiments'
:60) because both runs converge on the same conclusions. Claims 1 and 3 fail
on magnitude (not direction — weighting does have real effect, just smaller
than claimed). Confidence 0.65 reflects cross-run reproducibility and clean
measurement protocol.

Parent review (iter-1006, a01-bedb1efb): one correction. The first version
asserted "the Pearson correlation between binary and weighted scores is
r ≈ 0.98 (both runs)" — neither experiment node computes or reports any
correlation statistic, so that attribution is fabricated and the line is
demoted to "not computed by either run; falsifier 3 untested". This matters
rather than decorates the node: with falsifier 3 untested, the verdict rests
on magnitude alone, which is exactly what the :65 lean (rather than a
stronger claim) reflects.
<!-- THOUGHT:END -->


## Agent Notes
Both sibling experiments reproduce exactly (0.1343/0.1000/0.0343). Claims 1 and 3 fail on magnitude — max active gap 0.15, global gap 0.0343. Weighting has real effect but smaller than claimed. Verdict leans disproved:65