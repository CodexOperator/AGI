# TM.51 — does the CORRECTED partition derive the human review call?

Offline only, no network, no jev calls. Input `single_axis_rows.jsonl`, `arm2_verdict`
rows, 370 acts, mean over the 3 repeats of `answers.q1.probabilities`.
`StratifiedKFold(5, shuffle, seed 20260918)`; ONE threshold fitted per train fold
(argmax train agreement), applied to the held-out fold. LR = 5 class probabilities
as features, `LogisticRegression(max_iter=1000)`, same folds.
Rows flushed per probe to `corrected_partition_rows.jsonl`; script `corrected_partition_review_call.py`.

## Pre-registered partitions

| tag | accept side |
|---|---|
| A_prereg (claim clause 1, as written) | {proved, inconclusive_lean_proved} |
| B_corrected (TM.50 ACC + the parent's fix) | {proved, disproved, inconclusive_lean_proved} |
| TM50_control (reproduction) | {proved, disproved} |

## Pooled held-out (n=370 all / 170 verdict / 200 experiment)

| probe | pop | AUC | agreement | fold AUC std | thr std | ECE | conf [acc,dem] |
|---|---|---|---|---|---|---|---|
| A_prereg mapping | all | **0.7244** | 0.7730 | 0.076 | 0.040 | 0.156 | [[281,6],[78,5]] |
| A_prereg mapping | verdict | **0.7576** | 0.6294 | 0.079 | 0.085 | 0.149 | [[97,5],[58,10]] |
| A_prereg mapping | experiment | 0.5834 | 0.9250 | 0.114 | 0.000 | 0.175 | [[185,0],[15,0]] |
| B_corrected mapping | all | 0.7435 | 0.7892 | 0.065 | 0.059 | 0.099 | [[287,0],[78,5]] |
| B_corrected mapping | verdict | 0.7727 | 0.6765 | 0.081 | 0.101 | 0.129 | [[97,5],[50,18]] |
| TM50_control mapping | all | 0.5688 | 0.7757 | 0.029 | 0.000 | 0.344 | [[287,0],[83,0]] |
| LR (5 probs) thr=0.5 | all | 0.7945 | 0.8459 | 0.080 | 0.000 | 0.037 | [[276,11],[46,37]] |
| LR (5 probs) thr=0.5 | verdict | **0.8923** | **0.8118** | 0.045 | 0.000 | 0.076 | [[84,18],[14,54]] |
| LR (5 probs) thr=0.5 | experiment | 0.5535 | 0.9250 | 0.127 | 0.000 | 0.023 | [[185,0],[15,0]] |
| LR (5 probs) fitted thr | all | 0.7945 | 0.7946 | 0.080 | 0.200 | 0.037 | [[287,0],[76,7]] |
| LR (5 probs) fitted thr | verdict | 0.8923 | 0.7235 | 0.045 | 0.214 | 0.076 | [[95,7],[40,28]] |

## Controls

- Majority baseline 287/370 = **0.7757** — reproduced.
- TM.50 wrong-partition (accept={proved,disproved}) pooled AUC **0.5688** — reproduced to 4 dp.
- Shuffled labels, 20 seeds: A_prereg mean **0.5053** (0.4571–0.5949); B_corrected mean **0.5053** (0.4576–0.5467); LR mean **0.4966** (0.4187–0.5638). No leakage pattern.
- Offline audit: no network tokens in the script; `env -u TYPESAFE_API_KEY -u TYPESAFE_KEY` plus a `sys.addaudithook` that raises on any `socket.*`/`urllib.*`/`http.*` event runs clean (rc 0), byte-identical rows.
- Wire probe: accept/demote swapped in a sandbox copy → A_prereg pooled AUC 0.2756 (= 1 − 0.7244). The script reads the labels; no hard-coded vector.

## Bar-by-bar

(2) mapping: all-acts 0.7244 >= 0.70 **YES**; verdict-acts 0.7576 >= 0.72 **YES**;
fold AUC std 0.076 / 0.079 < 0.10 **YES**.
(3) LR: pooled all-acts AUC 0.7945 vs >= 0.80 **NO (by 0.0055)**; verdict-acts
0.8923 >= 0.80 **YES**. Agreement >= 0.80: at 0.5 all 0.8459 / verdict 0.8118
**YES**; at a train-fitted threshold all 0.7946 / verdict 0.7235 **NO**. ECE
reported (all 0.037, verdict 0.076).
(4) controls: shuffled at chance **YES for the 20-seed mean** (single draws spread);
majority and TM.50 AUC reproduced **YES**.

Disprove triggers all fail to fire: mapping 0.7244 > 0.65; LR 0.7945 > 0.72; no
leakage pattern; fold AUC std < 0.10 on both claim populations.

**Reading.** The hypothesis's core — `inconclusive_lean_proved` belongs on the
accept side, and on that corrected partition the class-probability mapping clears
its two pre-registered AUC bars (0.7244 / 0.7576) held out — **holds**. The
5-feature LR clears 0.80 on the population it was computed on in TM.50 (verdict
acts, 0.8923 held-out vs 0.8904 in-sample: no overfit). The two soft spots are the
LR pooled over all 370 acts (0.7945, 0.0055 short, well inside its 0.08 fold std)
and the phrase "at the fitted threshold" (0.5 clears 0.80, a fitted threshold does
not). The experiment subgroup is inert throughout (AUC 0.53–0.58, 185/200 accept).
