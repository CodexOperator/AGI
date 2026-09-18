---
id: experiment:a00-bdec620b-6c4cf7
mint_id: dabb4a87071a4f77b37d4056b2a61886
type: experiment
parents:
  - hypothesis:lm-jev-ece-is-a-pooling-artifact
next_edges: []
confidence: 0.9
edited_by: a00-bdec620b
evidence_runs:
  - experiment:a00-bdec620b-6c4cf7
line_ceiling: 40
loop: hypothesis:lm-jev-ece-is-a-pooling-artifact@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 1
profile: balanced
role: kid
scaffold_hash: 0a746209c1bee7b8
season: 2
title: "Per-group temperature does NOT calibrate the verdict subgroup: held-out ECE 0.141-0.212 on 5/5 seeds (pooling artifact disproved)"
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-bdec620b-6c4cf7

## Experiment

Tested `hypothesis:lm-jev-ece-is-a-pooling-artifact`: that pooled q1 ECE
(0.152) is purely a per-group pooling artifact, and one temperature per
subgroup fit on a held-out fold brings BOTH subgroup ECEs <= 0.10.

Data: `.agi/context/local-maxxing/typesafe/acts_replay_scrub.jsonl`,
0 API calls, 0 network. 1110 rows = 370 acts x 3 repeats; 1107 rows usable
for q1 (n_experiment=600 rows, n_verdict=507 rows; 1 verdict act has no q1
label). Per-act probability vectors rebuilt from `answers.q1.probabilities`.
Probe: `.agi/sessions/iter-TM.57/a00-bdec620b/probe_ece_pool.py`.
Rows: `.agi/context/local-maxxing/bench/20260918T233624Z.jsonl`
(one row per full-corpus probe, per seed x subgroup, plus pooled, plus summary).

**Metric pinned.** Two ECE definitions exist:
- **A** = confidence is the self-reported scalar `answers.q1.confidence`
  (this is acts_replay.py:139, which reported 0.196).
- **B** = confidence is `max(probabilities)`, the probability of the argmax class.

A temperature rescales the probability vector only, so it cannot rescale the
self-reported scalar: **before/after under definition A, and after under
definition B only** — the after-fit ECE is definition B by construction.

Split: 50/50 by act id, seeded shuffle per subgroup; fit ONE T per subgroup by
top-1 NLL on TRAIN rows (grid + bounded scalar refine); ECE on HELD-OUT rows.
5 seeds (20260918, 1, 7, 42, 1234).

### Full-corpus before (all rows, no split)

| group | n_rows | ECE A | ECE A (acts_replay bins) | ECE B |
|---|---|---|---|---|
| experiment | 600 | 0.0672 | 0.0682 | 0.0730 |
| verdict | 507 | 0.3172 | 0.3152 | 0.3169 |
| pooled | 1107 | 0.1569 | 0.1563 | **0.1524** |

**Provenance of the two disputed numbers.** 0.152 reproduces as definition B
(max-prob) on the *scrub* corpus = 0.1524. 0.196 reproduces as definition A
(self-reported scalar) on the *pre-scrub* `acts_replay.jsonl` = 0.196 (verified).
The claim's "0.152" and acts_replay.md's "0.196" therefore come from **different
definitions AND different corpora** — they are not the same measurement. The
claim's subgroup numbers (exp 0.078, verdict 0.326) match definition B on the
scrub rows (0.073 / 0.317).

### Held-out after per-group fit (definition B)

| seed | T_exp | exp A->B before | exp B after | T_ver | ver A->B before | ver B after | pool A->B before | pool B after | argmax d |
|---|---|---|---|---|---|---|---|---|---|
| 20260918 | 1.999 | 0.085/0.099 | 0.158 | 11.806 | 0.287/0.301 | 0.141 | 0.156/0.174 | 0.133 | 0.000 |
| 1 | 1.810 | 0.070/0.116 | 0.081 | 11.158 | 0.343/0.346 | 0.148 | 0.175/0.207 | 0.098 | 0.000 |
| 7 | 1.143 | 0.110/0.082 | 0.087 | 14.830 | 0.292/0.285 | 0.212 | 0.163/0.158 | 0.139 | 0.000 |
| 42 | 1.595 | 0.079/0.082 | 0.122 | 11.214 | 0.287/0.315 | 0.163 | 0.137/0.181 | 0.116 | 0.000 |
| 1234 | 1.099 | 0.051/0.069 | 0.062 | 12.741 | 0.338/0.352 | 0.146 | 0.170/0.191 | 0.082 | 0.000 |
| **mean** | 1.529 | — / 0.090 | **0.102** | 12.350 | — / 0.320 | **0.162** | — / 0.182 | **0.114** | 0.000 |
| min..max | 1.10..2.00 | | 0.062..0.158 | 11.2..14.8 | | 0.141..0.212 | | 0.082..0.139 | 0.000 |

## Evidence

Assertions against the claim:

- **(a) exp held-out <= 0.10** — FAILS: mean 0.102, 2/5 seeds above (0.158, 0.122),
  and the ECE **rises** from 0.090 to 0.102 on the mean (overfitting; the falsifier's
  third arm trips on seed 20260918, 0.099 -> 0.158).
- **(b) verdict held-out <= 0.10** — FAILS on 5/5 seeds, min 0.141, mean 0.162.
  This is the pre-registered decisive falsifier: "if (b) fails on a majority of
  seeds, the claim is disproved".
- **(c) pooled held-out <= 0.12** — marginal fail: mean 0.114 but 2/5 seeds above
  (0.133, 0.139).
- **(d) argmax unchanged within +/-0.02** — HOLDS EXACTLY: delta = 0.0000 on all
  5 seeds, all subgroups (temperature is monotone in logits, so this is identity).

Verdict: **disproved**. Per-group temperature fitting reduces the verdict
subgroup from 0.320 to 0.162 but never reaches 0.10 on any seed. Grouping is
**not** the whole story. The fitted verdict T ~ 12 against experiment T ~ 1.5
shows the residual is not a scalar-scale artifact: the verdict probability
vector is peaked (max ~0.95) while its argmax accuracy is ~0.59, so no single
temperature can both flatten and reorder it. A class-conditional / ranking fix
is required, not a temperature.

Reproduce: `python3 .agi/sessions/iter-TM.57/a00-bdec620b/probe_ece_pool.py`
(CPU only, ~10 s, no network).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First pass on this node. Chose to compute ECE over rows (repeats) to match
acts_replay.py's pooling, and reported both definitions because the claim's
"0.152" and the cited "0.196" are different measurements (B-on-scrub vs
A-on-pre-scrub) — pinning that provenance is what lets the falsifier be read
honestly. The falsifier was pre-registered, and (b) tripped on every seed, so
the strong verdict is warranted rather than the lean the brief suggested.
<!-- THOUGHT:END -->

## Agent Notes
Per-group temperature on held-out: verdict ECE 0.141-0.212 (mean 0.162) on 5/5 seeds, never <=0.10; exp ECE rises 0.090->0.102 (overfit); pooled 0.114 mean, 2/5 >0.12; argmax delta exactly 0. Claim disproved: grouping is not the whole story. 0.152=def B on scrub rows, 0.196=def A on pre-scrub rows — different definitions AND corpora.
