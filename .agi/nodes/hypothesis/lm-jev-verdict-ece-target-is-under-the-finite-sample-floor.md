---
id: hypothesis:lm-jev-verdict-ece-target-is-under-the-finite-sample-floor
mint_id: 2387479779214a22b02f52a792ecd0de
type: hypothesis
parents:
  - idea:lm-why-verdict-ece-ignores-temperature
next_edges: []
edited_by: thought-master
scaffold_hash: c8d5d167b0b16ba4
season: 2
testable_claim: "On the committed q1 rows (acts_replay_scrub.jsonl, 0 API calls), the TM.57 50/50 by-act-id split and the 5 seeds (20260918/1/7/42/1234): take the held-out VERDICT rows with their fitted-T (per-group NLL fit on the train fold, as in TM.74) max-prob confidence c, and for each of 200 label draws per seed replace the real correctness label by a Bernoulli(c) draw -- a predictor calibrated perfectly by construction. Compute ECE definition B (10 equal-width bins, confidence = max prob) exactly as the chain did. CLAIM: the median synthetic ECE over draws is >= 0.10 on >= 3/5 seeds for the verdict subgroup (the floor is above the target). CONTROL that must resolve: the same construction on the EXPERIMENT held-out rows (600 rows) gives median synthetic ECE < 0.10 on >= 4/5 seeds (the floor is below the target where the chain did pass). FALSIFIER: verdict median synthetic ECE < 0.10 on >= 3/5 seeds, OR the experiment control fails to resolve. Report per seed: n rows, n acts, real held-out ECE, synthetic median and 5/95 pct over draws, at row level AND with one row per act (mean confidence per act). Cost: 0 USD, NumPy only, reuse the TM.74 loader (jev_label_disagreement_split.py); runs on any CPU in minutes. CEILING: one kid, one script, one bench jsonl, one experiment node."
title: "WHY hop 6g (after 6c-6f all failed the same question): the verdict-subgroup held-out ECE target 0.10 sits UNDER the finite-sample floor of ECE definition B at ~85 held-out acts -- a predictor that is perfectly calibrated by construction on the same rows scores >= 0.10, so no post-hoc map could ever have passed"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-verdict-ece-target-is-under-the-finite-sample-floor

## Hypothesis

**Claim.** The verdict-subgroup held-out ECE target (<= 0.10, definition B: 10 equal-width bins, confidence = max prob) is below the finite-sample floor of that estimator at the chain's held-out size (~85 verdict acts, ~250 rows). A predictor that is perfectly calibrated by construction on those same rows and confidences scores >= 0.10, so hops 6c-6f (temperature, per-class temperature, isotonic, label-agreement split) were measuring binning noise, not a map that could pass.

**Method (0 USD, NumPy, committed rows).** `acts_replay_scrub.jsonl`, TM.57 50/50 by-act-id split, seeds 20260918/1/7/42/1234, per-group NLL-fit T on the train fold exactly as TM.74 (`jev_label_disagreement_split.py` loader). On the held-out verdict rows keep the fitted-T max-prob confidence c per row; for 200 draws per seed replace the real correctness label by Bernoulli(c); compute ECE-B per draw. Report per seed: n rows, n acts, real held-out ECE, synthetic median and 5/95 pct, at row level AND collapsed to one row per act (mean c per act, one Bernoulli per act).

**Control that must resolve.** The same construction on the EXPERIMENT held-out rows (600 rows, where the chain reached 0.102) gives median synthetic ECE < 0.10 on >= 4/5 seeds. If the control does not resolve the construction is wrong and the round is inconclusive, not proved.

**Proved when** verdict median synthetic ECE >= 0.10 on >= 3/5 seeds AND the control resolves: the line closes as a target-definition error; the follow-up is a debiased or equal-mass estimator (a NOTE on the WHY, not a new map).

**Disproved when** verdict median synthetic ECE < 0.10 on >= 3/5 seeds (the floor is under the target, so the 0.14-0.20 residual is real miscalibration): the max-prob channel is then abandoned for verdict acts -- the review call already rides the triage LR (mvp:lm-jev-review-triage-feature, outcome proved) -- and the WHY gets its closing note.

**Ceiling.** One kid, one script (`.agi/context/local-maxxing/typesafe/`), one bench jsonl (`.agi/context/local-maxxing/bench/`), one experiment node. No API calls. Any CPU.

## Agent Notes
thought-master 05:32Z 09-20: OWNER GO (pane, verbatim on goal:g14): 'have at it, use pi with deepseek that's fine' -- round ordered to director-thought as TMM.03 on --harness pi, cap 1 USD, first round dispatched from local-town.
