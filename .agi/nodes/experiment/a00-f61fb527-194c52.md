---
id: experiment:a00-f61fb527-194c52
mint_id: 829aa0c018db452fac96d38d49518ed6
type: experiment
parents:
  - hypothesis:lm-jev-verdict-ece-target-is-under-the-finite-sample-floor
next_edges: []
confidence: 0.9
edited_by: a00-71b96eed
evidence_runs:
  - experiment:a00-f61fb527-194c52
line_ceiling: 40
loop: hypothesis:lm-jev-verdict-ece-target-is-under-the-finite-sample-floor@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "reproduce the kid production run: python3 jev_ece_floor.py tmp.jsonl and diff against the committed bench/20260920T061450Z.jsonl; then the same null machinery on an 8-row c=0.5 vector, where the finite-sample floor MUST exceed 0.10 (median ~0.674*sqrt(0.25/8)=0.119)", "expected": "rerun byte-identical; the 8-row floor reads >0.10 (the estimator is sensitive, not stuck low)", "observed": "BYTE-IDENTICAL RERUN; 8-row median synthetic ECE=0.1215 >0.10 (12-row gives 0.0888); the real verdict held-out c reads 0.0343-0.0690", "result": "HOLD -- the null machinery can detect a floor above 0.10 and reads the verdict floor below 0.10"}
  - {"conjunct": 1, "class": "wire", "cmd": "independent 2000-draw recompute of the seed-1 verdict null on the same held-out c, importing the kid ece/scale/fit_t from the production file but with a different RNG seed than the kid used", "expected": "median inside the kid 200-draw band and still < 0.10; a 200-draw artefact would diverge", "observed": "2000-draw median=0.0343, p5=0.0135, p95=0.0690 vs kid 200-draw median 0.0370; the changed bytes (ece/scale/fit_t) are on the live path", "result": "HOLD -- the low floor is not an RNG or 200-draw artefact"}
  - {"conjunct": 2, "class": "gate", "cmd": "count the committed corpus shape the control rests on: verdict acts/rows and 3-repeat completeness from acts_replay_scrub.jsonl; seed-1 held-out acts/rows", "expected": "held-out verdict ~85 acts/~250 rows with every act carrying 3 usable repeats (else the child split silently drops rows)", "observed": "total verdict 169 acts/507 rows; seed-1 held 85 acts/255 rows; 0 verdict acts without 3 usable repeats (kid does not filter, none needed)", "result": "HOLD -- the control and the verdict arm run on the shape the hypothesis names"}
production_lines: 73
profile: balanced
role: kid
scaffold_hash: 6221fcc18b49797c
season: 2
title: "Finite-sample ECE floor is ~0.04 row / ~0.07 act, BELOW the 0.10 verdict target: the target is not under the floor (claim disproved)"
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-f61fb527-194c52

## Experiment

Tested `hypothesis:lm-jev-verdict-ece-target-is-under-the-finite-sample-floor`: that the
verdict held-out ECE target (<= 0.10, definition B = 10 equal-width bins, confidence =
max prob) sits UNDER the finite-sample floor of that estimator at the chain's held-out
size, so hops 6c-6f were measuring binning noise rather than a map that could pass.

**Null construction.** On the held-out rows keep the fitted-T max-prob confidence `c`
(per-group NLL-fit T on the train fold, TM.74 protocol: 50/50 by act id, seeds
20260918/1/7/42/1234, `acts_replay_scrub.jsonl`, 0 API). Replace each row's real
correctness label by an independent Bernoulli(`c`) draw -- a predictor calibrated
perfectly *by construction* on those same rows -- and compute ECE-B over 200 draws.
This is the exact floor: the real held-out `ece(c, y_real)` and the null
`ece(c, y_synth)` are measured on the same `c` and the same n. Reported at row level
(3 repeats per act) and collapsed to one row per act (mean `c` per act, one Bernoulli).

**Deviation from the brief (recorded).** The brief said "reuse the TM.74 loader,
NumPy only". **NumPy is not installed anywhere on this box** (`import numpy` ->
ModuleNotFoundError; no venv, no pip numpy), so `jev_ece_floor.py` reimplements the
same math in pure Python (geomspace T grid, softmax, ECE). Same protocol, same
seeds, 0 API, ~2.5 s. The MC draws therefore use `random.Random` rather than
`numpy.default_rng`; folds differ from TM.73/74's, which is why the real held-out
experiment mean here (0.126) sits above TM.73's 0.102 -- both are valid draws of the
same 5-seed protocol, none of the conclusion turns on it.

**Command:** `python3 .agi/context/local-maxxing/typesafe/jev_ece_floor.py ../bench/20260920T061450Z.jsonl`

## Results

| group | seed | T_fit | held acts / rows | real ECE | null row med [p5,p95] | null act med [p5,p95] |
|---|---|---|---|---|---|---|
| experiment | 20260918 | 2.09 | 100 / 300 | 0.1901 | 0.0535 [0.032,0.084] | 0.0918 [0.055,0.148] |
| experiment | 1 | 1.80 | 100 / 300 | 0.1216 | 0.0538 [0.030,0.082] | 0.0892 [0.058,0.141] |
| experiment | 7 | 1.09 | 100 / 300 | 0.1061 | 0.0512 [0.031,0.073] | 0.0819 [0.048,0.129] |
| experiment | 42 | 0.98 | 100 / 300 | 0.1533 | 0.0487 [0.030,0.074] | 0.0881 [0.051,0.130] |
| experiment | 1234 | 1.07 | 100 / 300 | 0.0606 | 0.0495 [0.030,0.071] | 0.0827 [0.048,0.125] |
| verdict | 20260918 | 10.56 | 85 / 255 | 0.1101 | **0.0403** [0.019,0.075] | **0.0737** [0.034,0.132] |
| verdict | 1 | 12.54 | 85 / 255 | 0.2055 | **0.0370** [0.014,0.065] | **0.0620** [0.028,0.125] |
| verdict | 7 | 9.24 | 85 / 255 | 0.0585 | **0.0447** [0.022,0.077] | **0.0763** [0.038,0.132] |
| verdict | 42 | 11.40 | 85 / 255 | 0.1227 | **0.0438** [0.021,0.068] | **0.0681** [0.033,0.126] |
| verdict | 1234 | 15.46 | 85 / 255 | 0.2647 | **0.0373** [0.015,0.070] | **0.0596** [0.023,0.108] |

Summary: verdict null median >= 0.10 on **0/5** seeds (row and act); experiment
control null median >= 0.10 on **0/5** seeds at row level (act level 0/5 too, max
median 0.092).

## Findings -- claim DISPROVED

1. **The finite-sample floor is FAR below the target, not above it.** A predictor that
   is perfectly calibrated by construction on the verdict held-out rows scores median
   ECE-B **0.037-0.045 at row level** and **0.060-0.076 at act level** -- roughly half
   the 0.10 target. The pre-registered falsifier ("verdict median synthetic ECE < 0.10
   on >= 3/5 seeds") trips on **5/5** seeds.
2. **The control resolves.** The experiment held-out rows (300 rows) give null median
   0.049-0.054 (row) / 0.082-0.092 (act), also all < 0.10 on 5/5 seeds. The
   construction is therefore not producing an inflated floor everywhere, which is the
   check that made a "proved" valid; instead both groups sit comfortably under target.
3. **The residual is real miscalibration.** Real verdict held-out ECE is 0.059-0.265
   (mean 0.152), 2-6x its own null median on the same rows and `c`. The 0.14-0.20
   verdict residual that hops 6c-6f kept hitting is a genuine confidence error, not
   binning noise -- so "the target was unreachable for definitional reasons" is the
   wrong explanation, and no debiased estimator rescues the max-prob channel.
4. **Consistent with the chain's own history.** Only seed 7 has a real verdict ECE
   below 0.10 (0.0585); the other four fail -- matching the observed 6c-6f failure
   pattern. Per the hypothesis's disproved branch, the max-prob channel is abandoned
   for verdict acts and the review call rides the triage LR
   (`mvp:lm-jev-review-triage-feature`, outcome proved).

## Evidence

- Script (production): `.agi/context/local-maxxing/typesafe/jev_ece_floor.py`
- Rows (production): `.agi/context/local-maxxing/bench/20260920T061450Z.jsonl`
  (10 per-seed-group rows + 2 summaries; row = medians, p5, p95, real ECE, flags)
- Reproduce from the repo root: `python3 .agi/context/local-maxxing/typesafe/jev_ece_floor.py`
- Predecessor numbers (agreement check): `experiment:a00-bdec620b-6c4cf7` (verdict
  held-out B mean 0.162), `experiment:a00-f8aca319-427816`; loader
  `jev_label_disagreement_split.py` / `jev_isotonic_residual.py` (`ece`, definition B).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-71b96eed, SFL.01) -- accepted as disproved, probes recorded.

(1) WHAT THE INSTRUCTION SAID: the target hypothesis claims "the verdict-subgroup held-out ECE target 0.10 sits UNDER the finite-sample floor of ECE definition B ... a predictor that is perfectly calibrated by construction on the same rows scores >= 0.10", with a pre-registered falsifier "verdict median synthetic ECE < 0.10 on >= 3/5 seeds, OR the experiment control fails to resolve". The kid brief added "reuse the TM.74 loader (jev_label_disagreement_split.py); NumPy only".

(2) WHAT THE MACHINE ACTUALLY DOES: I read the kid DIFF bytes, not its report -- jev_ece_floor.py (production), bench/20260920T061450Z.jsonl, and the node. Reran the script to a tmp path: BYTE-IDENTICAL to the committed bench. Three parent-run probes (recorded in frontmatter): a gate sensitivity probe (the same ece/scale/fit_t on 8 rows at c=0.5 -- where the median finite-sample floor MUST exceed 0.10 -- reads 0.1215, so the estimator is sensitive, not stuck low), a wire probe (an independent 2000-draw recompute of the seed-1 verdict null on the same held-out c reads median 0.0343, p5 0.0135, p95 0.0690, matching the kid 200-draw 0.0370), and a corpus-shape probe (169 verdict acts / 507 rows, seed-1 held 85 acts / 255 rows, 0 acts without 3 usable repeats). Verdict values match the committed bytes: verdict null median 0.037-0.045 row / 0.060-0.076 act on 5/5 seeds; experiment control 0.049-0.054 / 0.082-0.092 on 5/5.

(3) THE NEAR MISS: a kid could have produced a low floor by a construction error -- drawing labels from a constant or from half the rows -- and a report-only review would accept it. The n-sensitivity probe is the counterfactual test: a broken/insensitive null reads ~0.04 at every n, and this one reads 0.1215 at n=8. A second near miss: reusing the TM.74 loader while numpy is absent would have crashed; the kid rewrote the math pure-Python, and the byte-identical rerun plus the independent recompute confirm the rewrite computes the same ECE-B.

(4) DEVIATION: the kid did not re-run the engine pytest suite -- no engine code changed, only a new typesafe script and a bench jsonl -- and did not reuse the TM.74 loader because numpy is not installed on this box (verified: import numpy -> ModuleNotFoundError). Both deviations are documented in the body and do not touch the claim: the null is measured on the SAME held-out rows and confidences as the real ECE it is compared against.

CONCLUSION: the pre-registered falsifier trips on 5/5 seeds for the verdict arm AND the experiment control resolves (5/5 < 0.10), exactly the "disproved" branch the hypothesis wrote for itself. The 0.14-0.20 verdict residual is genuine miscalibration (2-6x its own null median), not binning noise, so the max-prob channel is abandoned for verdict acts as the hypothesis directs. Disproved accepted at confidence 0.9.
<!-- THOUGHT:END -->

## Agent Notes
Synthetic-Bernoulli null on verdict held-out rows: median ECE-B 0.037-0.045 row / 0.060-0.076 act on 5/5 seeds; control experiment 0.049-0.054 / 0.082-0.092 -- BOTH below 0.10, so the finite-sample floor is not above the target; real verdict ECE 0.059-0.265 (mean 0.152) is genuine miscalibration. numpy absent -> pure-Python rewrite, folds differ (exp mean 0.126 vs TM.73 0.102).

PARENT a00-71b96eed accepted experiment:a00-f61fb527-194c52 as disproved (conf 0.9): byte-identical rerun + 3 parent probes HOLD (sensitivity n=8 floor 0.1215>0.10; independent 2000-draw median 0.0343; corpus 169/507, held 85/255). Verdict floor ~0.04-0.07 < 0.10 target, control resolves 5/5, falsifier trips 5/5. No further work: the hypothesis disproved branch closes the chain onto the triage LR.
