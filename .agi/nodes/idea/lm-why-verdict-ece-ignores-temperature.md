---
id: idea:lm-why-verdict-ece-ignores-temperature
mint_id: ad9e528c452048948a9b4a3b2a927b2f
type: idea
parents:
  - hypothesis:lm-jev-ece-is-a-pooling-artifact
next_edges: []
edited_by: thought-master
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

## Agent Notes
thought-master review 05:11Z 09-19 of the 01:21Z research-review auto-mint (rescued to the trunk by the Prime at d042bac44): this why-stage idea is the CANONICAL WHY for TM.57 (experiment:a00-bdec620b-6c4cf7 disproved); the kid dup idea:lm-why-jev-verdict-confidence-misfits-one-scalar and the empty stub idea:lm-why-jev-verdict-confidence-is-uncalibrated are deprecated into it. Folded from the dup, three candidate causes the four minted hypotheses do not cover: (1) SHAPE not scale -- per-group isotonic regression on the held-out train fold reaches verdict ECE <= 0.10 where temperature cannot; (3) disagreement-conditioned overconfidence -- split verdict rows by 3-repeat label agreement, the agree-only subset calibrates; (4) elicitation channel -- the self-reported scalar (acts_replay.py:139, definition A) vs max-prob (definition B): refit on A. Of the four minted hops: 6a and 6b have FALSE premises against the TM.57 record (split was 50/50 BY ACT ID so all 3 repeats sit on one side; ECE was scored over 1107 per-repeat ROWS, 507 verdict, no per-act averaging) and are deprecated unrun; 6c (T degenerate) and 6d (per-class T) are KEPT and queued with cause (1) as ONE 0-USD ARM4C-light round on the committed rows (BATCH 10).

thought-master 06:02Z 09-19: TM.72 (hypothesis:lm-jev-class-conditional-t-recovers, experiment:a00-2bfe6e45-9d9f08) DISPROVED 0.9 -- per-class temperature leaves both verdict-class sub-ECEs > 0.10 on 5/5 seeds; the demote class fails on RANKING not scale (argmax agreement 0.025-0.100, NLL-optimal T degenerate at 870-3e4); parent reproduced with a different grid, a random-2-arm control also fails, and a q2-vs-q1 crosstab shows q2 is not a relabel of q1. Cause (2) class composition is therefore the WRONG description of the residual; cause (1) shape/ranking stands and is decided by hypothesis:lm-jev-isotonic-per-group-fixes-verdict-ece (TM.73, running). No new WHY node: the disproof sharpens this one.

thought-master 06:05Z 09-19: TM.73 (hypothesis:lm-jev-isotonic-per-group-fixes-verdict-ece, experiment:a00-fb3ab94b-01f359) DISPROVED 0.85 -- per-group isotonic leaves verdict held-out ECE at 0.057-0.203, <= 0.10 on 2/5 seeds only (experiment subgroup 4/5, so not a global overfit); parent re-implemented PAVA by hand and matched the table; oracle fit ON the held-out rows gives 0.000-0.006, so the failure is generalization, not method capability. Cause (1) shape is refuted with cause (2) class composition: no monotone map of the max-prob channel carries held-out information on verdict rows. Next lever, minted: hypothesis:lm-jev-verdict-ece-floor-is-label-disagreement (cause 3 -- the contested ~20 pct of verdict acts set the floor); cause 4 (channel A) stays queued behind it. Chain so far: 6c T-degenerate (TM.71, pending), 6d per-class T disproved (TM.72), 6e isotonic disproved (TM.73), 6f label-disagreement (next).

thought-master 06:24Z 09-19: TM.71 (hypothesis:lm-jev-verdict-t-is-degenerate; experiments a00-c522b82d-5f20fe + a00-f191e0d6-f87268, two kids sharing no code) CLOSED inconclusive_lean_proved:60 -- two conjuncts refuted as worded (the argmin is interior at T~11-15 on 5/5 seeds and the held-out ECE-vs-T curve is not flat, 0.096-0.54), but the crux holds: argmin curvature is 0.3 pct of bootstrap noise, the 90 pct CI spans T~5.5-28 (factor 3.3-3.7), profile-likelihood CI factor 11-18 and 32-41 pct of disjoint half-splits disagree by > 2x; the parent corrected the magnitude with a regime-matched control (T0=12 resolves only to factor 6.6): verdict rows are ~2x looser than the control, not ~5x. CHAIN CLOSED for scalar/shape levers: 6c degenerate-but-real (TM.71, 60), 6d per-class T disproved (TM.72, 0.9), 6e isotonic disproved (TM.73, 0.85). The residual is not fixable by any map of the max-prob channel; hypothesis:lm-jev-verdict-ece-floor-is-label-disagreement (cause 3) is next, cause 4 (channel A) behind it.

thought-master 04:47Z 09-20: TM.74 (hypothesis:lm-jev-verdict-ece-floor-is-label-disagreement, experiment:a00-f8aca319-427816, kid a00-2b8b1432, parent-accepted in-node) DISPROVED -- hop 6f: on verdict acts whose 3 repeats agree unanimously, held-out ECE under per-group temperature still exceeds 0.10 on 5/5 seeds in all four agreement splits (gold split degenerate: labels.q1 constant per act; self/corr contested 3-4 pct; graph contested 17.5 pct, n=40); T_fit unstable (gold 7.6-17.3, graph 1.1-7.9) as t-is-degenerate predicts; full-corpus verdict ECE B 0.3234 (507 rows) replicates TM.57 0.3169. Four hops now fail the same question: not scale (6d), not shape (6e), not the labels (6f), and T is location-unidentified (6c, lean_proved:60 by two methods). The one thing no hop measured is the METRIC: ECE definition B on ~85 held-out verdict acts has a finite-sample floor that no map can go under. Next hop 6g = hypothesis:lm-jev-verdict-ece-target-is-under-the-finite-sample-floor (0 USD, committed rows). If 6g is proved the line closes as a target-definition error; if disproved the residual is real and the max-prob channel is abandoned for verdict acts (the triage LR already carries the review call). Merged to the trunk on local-town at 74271855e.

thought-master 13:3xZ 09-20 (WHY sharpened by 6g, hypothesis:lm-jev-verdict-ece-target-is-under-the-finite-sample-floor DISPROVED 0.9, experiment:a00-f61fb527-194c52, merged 8d558a2eb): the 0.14-0.20 verdict-group residual that 6c-6f kept hitting is NOT a finite-sample artefact of ECE definition B -- a perfectly calibrated predictor with the same fitted-T max-prob confidences on the same held-out rows scores median 0.037-0.045 (row) / 0.060-0.076 (act) on 5/5 seeds, and the real verdict ECE is 0.059-0.265 (mean 0.152), i.e. 1.3x-7.1x the row null median (seed 7 sits inside its null band; act-level 0.8x-4.4x). So the miscalibration of the max-prob channel on verdict acts is real and systematic, and no calibration map tried so far (temperature 6c, per-class T 6d, isotonic 6e, label-disagreement 6f, floor 6g) removes it. DECISION (the chain's pre-registered disproved branch): the max-prob channel is abandoned for verdict acts; the review call rides the triage LR. OPEN, not a round now (owner 'slow down'): WHERE the verdict miscalibration comes from -- prompt structure, act-type skew, or something upstream of the confidence extraction -- is the next question on this idea if the town ever returns to the max-prob channel; the live triage check at >= 20 fresh VERDICT acts remains the cheaper test.
