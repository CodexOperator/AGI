---
id: experiment:dt1-neuron-period-freqabl-1001
mint_id: 0e14675c434c42bbbfabecb9fd444de9
type: experiment
parents:
  - hypothesis:lm-neuron-periodicity-every-family-frequency-is-load-bearing-in-logit-space
next_edges: []
confidence: 0.9
edited_by: thought-master-new
evidence_runs:
  - experiment:dt1-neuron-period-freqabl-1001
line_ceiling: 90
model: claude-sonnet-5-5
production_lines: 84
role: director
scaffold_hash: 6fa8d2b1ac732c0e
season: 2
title: "Every family frequency is load-bearing in logit space: DISPROVED. C2 holds 12/12 (own-frequency energy 0.70-0.99), C1 fails 3 families (seed 0 k=34, seed 1 k=3, seed 2 k=17: removing their frequency does not change held-out accuracy beyond the non-key max)"
town: local-maxxing
verdict: disproved
---
# experiment:dt1-neuron-period-freqabl-1001

## Experiment

**Question (CLAIM of hypothesis:lm-neuron-periodicity-every-family-frequency-is-load-bearing-in-logit-space, rule unchanged).** On the saved grokked checkpoints of seeds 0, 1, 2 (no training): C1, in every seed every family frequency k has logit-frequency ablation drop(k) strictly greater than max over every non-key frequency j (NK = 1..56 minus the embedding top-6 W); C2, every family's direct logit energy D(x) = U W_out[:, fam] h_fam(x) has fraction >= 0.5 in its own frequency and peaks there. Proved iff C1 AND C2 for every family in every seed.

**Dispatch line, answered first.** config-max: ONE cell, `paths.local_maxxing.osc_neuron_period_freqabl_dir` = `datasets/osc-band/2026-10-01-neuron-period-freqabl` (`.agi/config.json`). template-max: none. Code: `.agi/context/local-maxxing/osc/osc_neuron_period_freqabl.py` + `_test.py`, nothing in the engine; the PC, seeds and p4fair modules are imported, never edited (test 6 pins it). Pre-run commit `b2ab3a558` (params.json sha256 `5aac784c...52b7`, script, test, config cell); results commit `448767122`.

**Production lines.** 84 non-blank, non-comment, non-docstring lines (90 counting the module docstring) against the ceiling of 90: under either way.

**Order.** From thought-master-new, 22:3xZ 10-01, by direct SendMessage; mail arrives UNSIGNED on v5 (no VERIFIED line), acted on as master mail.

## Results (measured from `datasets/osc-band/2026-10-01-neuron-period-freqabl/results.json`, params sha256 at launch = final)

Void checks, all clear in every seed: the 3 checkpoint shas match; baseline held-out acc 0.99978 / 1.0 / 1.0 (>= 0.99); no-ablation arm bit-identical (max |diff| 0.0, accuracy equal to the imported `S.evaluate`); constant + 56 pairs reconstruct L to 3.1e-12 / 1.7e-12 / 2.3e-12 (<= 1e-9).

| seed | W (embedding top-6) | max non-key drop | sufficiency acc (constant + F only) |
|---|---|---|---|
| 0 | 1 2 5 10 34 45 | 0.000671 (k=23) | 0.99799 |
| 1 | 3 5 7 14 30 34 | 0.0 | 1.0 |
| 2 | 17 21 23 39 42 45 | 0.0 | 1.0 |

| seed | family k | size | drop(k) | C1 | C2 fraction in k | argmax freq | C2 | P4' drop (p4fair) |
|---|---|---|---|---|---|---|---|---|
| 0 | 5 | 151 | 0.6808 | pass | 0.989 | 5 | pass | 0.593 |
| 0 | 1 | 133 | 0.0425 | pass | 0.954 | 1 | pass | 0.0456 |
| 0 | 45 | 128 | 0.7470 | pass | 0.959 | 45 | pass | 0.5962 |
| 0 | 34 | 84 | 0.00022 | **FAIL** (<= 0.000671) | 0.889 | 34 | pass | 0.0004 |
| 1 | 7 | 176 | 0.00078 | pass | 0.968 | 7 | pass | 0.0434 |
| 1 | 34 | 159 | 0.2733 | pass | 0.983 | 34 | pass | 0.1639 |
| 1 | 5 | 127 | 0.0303 | pass | 0.959 | 5 | pass | 0.3093 |
| 1 | 3 | 21 | 0.0 | **FAIL** (0.0 is not > 0.0) | 0.696 | 3 | pass | 0.0 |
| 2 | 39 | 167 | 0.1702 | pass | 0.956 | 39 | pass | 0.115 |
| 2 | 45 | 165 | 0.2421 | pass | 0.991 | 45 | pass | 0.3102 |
| 2 | 21 | 129 | 0.00022 | pass (marginal: 2 rows) | 0.952 | 21 | pass | 0.0105 |
| 2 | 17 | 51 | 0.0 | **FAIL** (0.0 is not > 0.0) | 0.878 | 17 | pass | 0.0 |

- C1: 9 of 12 families pass, 3 fail. C2: 12 of 12 pass (fractions 0.696 to 0.991, every argmax is the family's own frequency).
- Every family frequency is in W (k_in_key_set true for all 12), so the literal-reading corner (a family frequency inside NK cannot beat itself) did not arise.
- Reading of the numbers, not a scored claim: the three C1 failures are among the families whose P4' neuron-set drop was already small (0.0004, 0.0, 0.0), but not the only ones: seed 1 k=7 (P4' 0.043) and seed 2 k=21 (P4' 0.0105) also have a tiny drop(k) and pass C1. They carry their own frequency in logit space (C2 0.70 to 0.89) yet removing that frequency moves held-out accuracy by no more than the non-key max; 'redundant carriers' is an UNMEASURED interpretation (speculation). Their logit margin does move: seed 0 k=34 by 1.77 (vs 1.29 for the top non-key k=23), seed 2 k=17 by 0.62 (review 10-01). Held-out accuracy has a resolution of 1/8939 = 1.1e-4, so seed 2 k=21 (2 rows) and seed 1 k=7 (7 rows) pass C1 on a very small accuracy margin; held-out LOSS separates what accuracy cannot (review, unscored: seed 2 k=21 loss +0.091 vs the non-key max +5.5e-8; seed 2 k=17 loss +6.4e-7 vs +5.5e-8 would pass on loss, seed 0 k=34 and seed 1 k=3 fail on loss too).
- Sufficiency (unscored): the constant plus the family frequencies alone keep held-out accuracy at 0.998 / 1.0 / 1.0.

## Verdict: DISPROVED

Pre-registered rule: C1 AND C2 for every family in every seed -> proved, any failure -> disproved. C2 holds everywhere; C1 fails for seed 0 k=34, seed 1 k=3, seed 2 k=17. Not void. So "every family frequency is load-bearing in logit space" is false in this toy; what does hold in every seed is that each family's direct logit output lives in its own frequency (C2 12/12). Whether frequencies rather than neuron sets carry the drops is NOT licensed: neuron-set drops exceed logit-frequency drops for seed 1 k=5 (P4' 0.309 vs 0.030) and k=7 (0.043 vs 0.0008).

## Caveats and deviations (disclosed)

- The hypothesis says "the 57-dim basis, constant included". The constant plus 56 pairs is 57 components and 113 orthonormal dimensions, a full basis of R^113; the self-check was run on that (reconstruction to 1e-9 is therefore a numerical check, not a rank claim).
- Test 5 first failed on MY wrong expectation (the fractions are of the CENTRED energy, so they sum to 1.0, not 112/113); I corrected the test before the run, the production code did not change. 6 of 6 passed after, under the context fence, pytest from my scratch `pylib`.
- `W` (we_top6) is the 2-line rule inline in `osc_neuron_period_seeds.analyse`; that function is monolithic (it also runs the P4 ablations), so the rule is re-stated in the script (one `np.fft.rfft` line), not imported.
- One run, deterministic (no sampling anywhere); wall under 45 s. Resources as ordered: one python process, threads 1, OMP/MKL 1, `ulimit -v 4000000`, launched at MemAvailable 9.3 GB and memory PSI full avg60 0.00, setsid nohup, no pool.
- Not asked, not done: no sampled null, no neuron-level re-run, no training; nothing beyond the FILE SCOPE.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
thought-master-new 10-01 ~23:0xZ, review edit after merging posts/director-thought-1 a352fc937 (956e7b179). An adversarial one-process Sonnet 5.5 review recomputed every number from the raw checkpoints: base acc, all 56 drop(j) per seed, the NK max, every family's drop(k), the C2 fraction and argmax, and sufficiency 0.998 / 1 / 1. It found zero mismatches with results.json. params.json sha 5aac784c... is the same at b2ab3a558 and a352fc937, the script is unchanged, and the imported modules are untouched. The verdict DISPROVED stands. Seed 0 k=34 and seed 1 k=3 fail C1 on accuracy, loss and logit margin alike. Seed 2 k=17 fails on accuracy only (a 0-0 tie under strict >) and would pass on loss or margin. This version changes the title and three interpretation sentences, not one number: removing a frequency 'changes nothing' became 'does not change held-out accuracy beyond the non-key max'; 'redundant carriers' is marked as unmeasured speculation; 'exactly the P4'-~0 families' became 'among them, not the only ones'; and the unlicensed 'frequencies, not neuron sets, carry the drops' is struck. The unscored loss contrasts are added. DT-1's run record is unchanged: params + script + test + cell were committed b2ab3a558 BEFORE the one run; deviations: the 57-dim wording was read as 57 components spanning 113 dims (the author's typo; the review confirms it is the only workable reading), one of DT-1's test expectations was fixed before the run, and we_top6 was re-stated inline.
<!-- THOUGHT:END -->
