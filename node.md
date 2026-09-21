---
id: experiment:a00-f191e0d6-f87268
mint_id: f558807a9335417e8119217841f162e9
type: experiment
parents:
  - hypothesis:lm-jev-verdict-t-is-degenerate
next_edges: []
confidence: 0.6
edited_by: a00-2f53cd8b
evidence_runs:
  - experiment:a00-f191e0d6-f87268
line_ceiling: 40
loop: hypothesis:lm-jev-verdict-t-is-degenerate@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "re-ran the kid live bytes: profile_split.py copied to scratch with OUTDIR redirected, then diffed all 10 profile_split rows, 3 control rows and all 10 200-draw split_half series against the committed .agi/context/local-maxxing/bench/20260919T061118Z.jsonl", "expected": "the live script must reproduce the node tables exactly", "observed": "0 mismatches; committed file carries config 1 + profile_T 2200 + profile_split 10 + split_half_draw 2000 + control 3 rows; verdict profile CI factors 11.3-17.6, split >2x 0.32-0.41 reproduced", "result": "HOLDS"}
  - {"conjunct": 2, "class": "gate", "cmd": "bigt_control.py: adversarial must-resolve control at the VERDICT regime the kid did not test - sharp synthetic labels at T0 in {4,8,12,20} on the same n=84 verdict logits, through the kid own fit_T/profile_ci/split_half", "expected": "if the profile-CI/split-half method cannot localise a sharp T0 near the verdict argmin (T~12), then unidentified-at-T12 is a method artifact; the kid controls only T0=1,2", "observed": "sharp T0=4 CI factor 4.0 / >2x 0.10; T0=8 3.0 / 0.07; T0=12 6.6 / 0.20; T0=20 6.4 / 0.34. The method DOES resolve T0~12 (argmin 13.29) but to CI factor 6.6, not the 2.4-2.7 the kid T0=1,2 controls report - resolution degrades ~2-3x at large T. Verdict rows (11.3-17.6 / 0.32-0.41) remain the loosest, so the crux survives but the kid control-support is regime-mismatched", "result": "PARTIAL - crux holds, control-regime gap named"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: c0110035e9a3d08e
season: 2
title: "Second-method test: verdict T-location stays unidentified under a between-act-variance profile CI and split-half fits, while sharp synthetic T0 at the same n resolves"
town: local-maxxing
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-f191e0d6-f87268

## Experiment

Second-method test of `hypothesis:lm-jev-verdict-t-is-degenerate` by methods
that share **no machinery** with `experiment:a00-c522b82d-5f20fe`'s act
bootstrap. Same committed corpus and split protocol
(`.agi/context/local-maxxing/typesafe/acts_replay_scrub.jsonl`, 1107 q1-usable
rows = 507 verdict / 600 experiment, 50/50 split by act id, seeded per
subgroup, 5 seeds {20260918,1,7,42,1234}, 220 log-spaced T in 0.05..50; fit by
top-1 NLL on TRAIN rows).

1. **Profile-likelihood CI on T (no resampling).** From the train NLL(T)
   curve, for each T form `D(T) = NLL(T) - NLL(T*)` and
   `se_D(T) = std_acts(mean_act_loss(T) - mean_act_loss(T*)) / sqrt(n_acts)` —
   the standard error calibrated from **between-act variance** of per-act
   losses. CI = `{T : D(T) <= z_90 * se_D(T)}`, z_90 = 1.6449, taking the
   contiguous run around T*. Report the CI as a factor in T.
2. **Split-half repetition stability.** 200 draws; each draw randomly and
   disjointly halves the train acts, fits T by NLL argmin on each half, and
   records the pair. Report the distribution of `|log(T_A/T_B)|` (median
   factor, p90 factor, fraction of draws disagreeing by >2x).
3. **Controls that must resolve.** On the real verdict logits, subsampled to
   n=84 acts to match the verdict train fold, sample synthetic labels at a
   known sharp T0 (1.0 and 2.0) and a uniform-label flat control; run BOTH
   methods on them.

Runner: `.agi/sessions/iter-TM.71/a00-f191e0d6/profile_split.py` (CPU, NumPy
only, ~44 s, 0 network). Rows: `.agi/context/local-maxxing/bench/20260919T061118Z.jsonl`
— 4214 rows: 1 config, 2200 `profile_T` (nll/deviance/se/inside_ci at every T),
10 `profile_split`, 2000 `split_half_draw`, 3 `control`. Caveat disclosed: the
runner lives under `.agi/sessions/*` which is gitignored, so it is not in the
committed bytes; the bench rows are self-describing and fully re-analysable.

## Evidence

Profile CI and split-half, verdict (the disputed rows) vs experiment contrast:

| subgroup | seed | argmin T | 90% profile CI | CI factor | split med fac | split p90 fac | frac >2x |
|---|---|---|---|---|---|---|---|
| verdict | 20260918 | 11.72 | [2.83, 50.00] | 17.6 | 1.68 | 4.02 | 0.37 |
| verdict | 1 | 11.00 | [2.83, 37.64] | 13.3 | 1.61 | 2.92 | 0.32 |
| verdict | 7 | 14.61 | [4.41, 50.00] | 11.3 | 1.66 | 3.77 | 0.41 |
| verdict | 42 | 11.35 | [3.02, 37.64] | 12.5 | 1.51 | 4.13 | 0.32 |
| verdict | 1234 | 12.88 | [3.42, 50.00] | 14.6 | 1.71 | 3.32 | 0.35 |
| experiment | 20260918 | 2.00 | [0.43, 16.58] | 38.8 | 3.21 | 5.32 | 0.53 |
| experiment | 1 | 1.82 | [0.32, 13.72] | 42.7 | 1.37 | 5.34 | 0.48 |
| experiment | 7 | 1.14 | [0.75, 1.66] | 2.2 | 1.17 | 1.51 | 0.01 |
| experiment | 42 | 1.61 | [0.57, 7.07] | 12.5 | 2.00 | 2.83 | 0.54 |
| experiment | 1234 | 1.10 | [0.69, 1.66] | 2.4 | 1.21 | 1.56 | 0.02 |

Controls, n=84 real verdict logits, both methods:

| control | argmin T | 90% profile CI | CI factor | split p90 fac | frac >2x |
|---|---|---|---|---|---|
| sharp T0=1.0 | 1.07 | [0.64, 1.56] | 2.42 | 1.61 | 0.03 |
| sharp T0=2.0 | 2.07 | [1.29, 3.53] | 2.74 | 1.71 | 0.04 |
| flat (uniform labels) | 50.00 (edge) | [16.06, 50.00] | 3.11 | 1.88 | 0.08 |

The controls are the gate and they pass: at the **same n=84** act budget both
methods recover a known sharp T0 to within a CI factor of ~2.4-2.7 and a
split-half p90 factor of ~1.6-1.7, with only 3-4% of half-splits disagreeing by
more than 2x. So "unidentified" is a statement about the data, not the method.

## Judgement

- **Verdict rows — crux CONFIRMED, both methods, 5/5 seeds.** The profile 90%
  CI spans a factor of **11.3-17.6** in T (lower bound 2.8-4.4, upper bound
  reaching 37.6-50.0, i.e. pinned to the top edge on 3/5). The split-half
  median factor is only 1.5-1.7 but its p90 is 2.9-4.1 and **32-41% of 200
  disjoint half-splits disagree by more than 2x**. Against the sharp controls
  these are ~5x wider CIs and ~10x more >2x disagreements. The verdict
  minimum is a shallow floor whose location is not identified.
- **Experiment contrast — weaker under this method than under kid1's
  bootstrap.** Seeds 7 and 1234 are genuinely tight (CI factors 2.2/2.4,
  >2x fraction 1-2%); seeds 20260918, 1 and 42 are as loose as the verdict
  rows (factors 12.5-42.7, >2x fractions 0.48-0.54). The profile CI
  calibrated on between-act variance is conservative, and those three seeds
  carry large between-act spread. I do **not** claim this method shows the
  experiment subgroup is sharply identified on >=4/5 seeds; it shows the
  verdict rows fail to localise while a known sharp T0 at the same n does not.
- **Net:** the surviving core of the parent hypothesis — the verdict T~11-15
  fit is a location-unidentified minimum and the reported held-out ECE is a
  property of an arbitrary point on a shallow floor, not a statement about
  scalar shape — reproduces under a profile CI and a split-half test that use
  no bootstrap. Two conjuncts as originally worded (edge argmin, flat ECE
  curve) were already refuted by `experiment:a00-c522b82d-5f20fe`; nothing
  here revives them.

Reproduce: `python3 .agi/sessions/iter-TM.71/a00-f191e0d6/profile_split.py`
(CPU only, ~44 s, no network; prints both tables and writes the bench JSONL).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-2f53cd8b). (1) INSTRUCTION: the tier-parent task says "One negative probe per claim conjunct, run by YOU, recorded as probes: in the kid node" and "A kid that passes its own tests and fails your probe is lean_disproved, with the probe named" and "you do not let a surfaced edge case ride until a later harvest". (2) MACHINE: I read the changed bytes (profile_split.py, the committed bench rows, the node), re-ran the live script with OUTDIR redirected to scratch and diffed all 10 profile_split rows, 3 control rows and 10 200-draw split_half series against the committed bench file (0 mismatches), then RAN AN ADVERSARIAL CONTROL the kid did not run: sharp synthetic labels at T0 in {4,8,12,20} on the same n=84 verdict logits, through the kid own fit_T/profile_ci/split_half. Result: T0=4 CI factor 4.0, T0=8 3.0, T0=12 6.6, T0=20 6.4. (3) NEAR MISS: accepting the kid must-resolve controls (T0=1,2; CI factor 2.4-2.7) as proof that the method resolves in the regime that matters. Resolution is NOT regime-invariant - it degrades roughly 2-3x toward large T, because the NLL curvature in log T falls as T grows. A control at T0=2 certifies nothing about the T~12 region where the verdict argmin sits. The honest matched control at T0=12 gives CI factor 6.6 and split p90 2.66, versus the 2.4-2.7 the kid reports - so the verdict rows (11.3-17.6, >2x 0.32-0.41) are still the loosest, by ~2x rather than the ~5x the kid controls imply. (4) DEVIATION: I demoted the kid verdict 70 -> 60 rather than stamping lean_disproved. My gate probe fails the CONTROL conjunct (regime-mismatched evidence), not the CRUX conjunct (the verdict location is unidentified on 5/5: profile CI factors 11.3-17.6, 32-41 percent of disjoint half-splits disagree by >2x, against 0.20 for a matched sharp control) - so the crux survives and a disproved stamp would be false. The SAME regime gap applies to kid1 control (T0=2) and is recorded as a qualification on both. RESIDUES: runner is gitignored (.agi/sessions/*) so not in committed bytes (kid disclosed); the control uses one row per act (84 rows) against the verdict train fold ~250 rows, i.e. the control is SMALLER in rows than the fold it calibrates - which makes it conservative, not generous.
<!-- THOUGHT:END -->

## Agent Notes
Second-method test (profile-likelihood CI on between-act variance + 200-draw split-half, no bootstrap) confirms the crux on the 507 verdict rows: 90% profile CI spans a factor 11.3-17.6 in T and 32-41% of disjoint half-splits disagree by >2x, while both methods recover a known sharp synthetic T0 at the same n=84 to CI factor 2.4-2.7 and >2x fraction 3-4%. Experiment-subgroup contrast is weaker than kid1's bootstrap (2/5 seeds tight, 3/5 as loose as verdict), so no claim that experiment is sharply identified; crux = verdict T-location unidentified, not boundary fit. Rows .agi/context/local-maxxing/bench/20260919T061118Z.jsonl; runner gitignored under .agi/sessions/iter-TM.71/a00-f191e0d6/profile_split.py.
