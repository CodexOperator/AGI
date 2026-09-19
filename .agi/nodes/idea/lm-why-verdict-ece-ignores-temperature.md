---
id: idea:lm-why-verdict-ece-ignores-temperature
mint_id: ad9e528c452048948a9b4a3b2a927b2f
type: idea
parents:
  - hypothesis:lm-jev-ece-is-a-pooling-artifact
next_edges: []
edited_by: why-stage
loop: mvp:lm-research-review-workflow@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 17999d78aac9faa0
scale: small
season: 2
thought_session: iter-TM.60
title: "WHY jev ECE, hop 5: the verdict subgroup's held-out ECE never reaches 0.10 under NLL-fit temperature (min 0.141, mean 0.162 on 5/5 seeds) while experiment fits at 0.102 -- what does the residual measure?"
town: local-maxxing
---
## Idea

**WHY question — what the failure MEASURED (not what was hoped).**

The claim was: pooled q1 ECE 0.152 is purely a per-group pooling artifact, and
one temperature per subgroup, fit by top-1 NLL on a 50/50 held-out split by act
id, brings BOTH subgroup ECEs <= 0.10. It was measured and it did not hold.

Measured (experiment:a00-bdec620b-6c4cf7, `verdict: disproved`, confidence 0.9;
rows `.agi/context/local-maxxing/bench/20260918T233624Z.jsonl`, 5 seeds
20260918/1/7/42/1234):

- verdict subgroup held-out ECE **0.141-0.212, mean 0.162** — never <= 0.10 on
  **5/5 seeds** (the pre-registered decisive falsifier).
- experiment subgroup held-out ECE **0.062-0.158, mean 0.102**, and it **RISES**
  from 0.090 before to 0.102 after (overfitting; seed 20260918 trips the
  falsifier's third arm, 0.099 -> 0.158).
- pooled held-out ECE mean 0.114 but **2/5 seeds above 0.12** (0.133, 0.139).
- argmax delta exactly **0.0000** on all seeds/subgroups — temperature is
  monotone, so it cannot reorder; this arm HOLDS.
- fitted T is wildly asymmetric: verdict T ~ 11.2-14.8 vs experiment T ~ 1.1-2.0.
- in-sample best-case T on verdict rows reaches 0.0959 at T=4.52 (parent probe 1),
  so "no temperature can" is too strong; what fails is the NLL objective under
  the held-out protocol, not the existence of some temperature.

So the failure MEASURES: **a single scalar per group does not carry the verdict
subgroup's miscalibration.** Grouping is not the whole story; the residual is
not a held-out scalar-scale artifact.

**Candidate causes, each falsifiable.**

1. *Not scalar-shaped at all — it is a ranking / class-conditional error.*
   Falsifiable: a class-conditional (per-class) temperature or Dirichlet
   calibration on the same held-out split reaches <= 0.10. If a
   class-conditional fit also fails, the cause is not the scalar parameterisation.
2. *Label noise / ambiguity in the verdict subgroup (multi-answer, abstention)
   makes top-1 NLL fit the wrong target.* Falsifiable: recompute ECE restricted
   to verdict acts with one unambiguous label. If still > 0.10, label noise is
   not the cause.
3. *Per-act mean-probability pooling across 3 repeats collapses variance, so
   ECE is driven by the mean distribution, not per-row.* Falsifiable: recompute
   ECE on per-row (un-averaged) probabilities. If <= 0.10, the pooling is over
   repeats, not over groups.
4. *The split is not a clean act-level holdout — repeats of the same act id land
   in both folds.* Falsifiable: re-split with all 3 repeats of an act on one
   side. If ECE drops <= 0.10, the split was the artifact.
5. *T ~ 11-15 is a degenerate/boundary fit (flat NLL, unidentified).*
   Falsifiable: report the NLL-vs-T curve and curvature. If the fitted T sits at
   a grid boundary, the "fit" is not a measurement.

**Evidence anchors.** experiment:a00-bdec620b-6c4cf7 (verdict disproved);
probe `.agi/sessions/iter-TM.57/a00-bdec620b/probe_ece_pool.py:1` (untracked —
gitignored by `.gitignore:100:.agi/sessions/*`, so not re-runnable from a clean
checkout); parent probes `parent_probes2.py` PROBE1-4 at
`.agi/sessions/iter-TM.57/a00-1bc025ed/scratch/` (also untracked); the tracked
record is the committed bench rows `.agi/context/local-maxxing/bench/20260918T233624Z.jsonl`.
Definitions: ECE A = self-reported `answers.q1.confidence` (acts_replay.py:139,
the 0.196 number, pre-scrub corpus); ECE B = `max(probabilities)` (the 0.152
number, scrub corpus) — different definitions AND different corpora.
Cache binding: `acts_replay_scrub.py:22` maps `json_cache_scrub` ->
`acts_replay_scrub.jsonl`.
