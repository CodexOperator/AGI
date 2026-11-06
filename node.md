---
id: experiment:dt1-neuron-period-phase-1105
mint_id: 6cb8f36a209045bf8bf88e861aea0ab5
type: experiment
parents:
  - hypothesis:lm-honouring-the-mod-113-circuits-joint-phase-beats-random-and-plain-numerics
next_edges: []
confidence: 0.9
edited_by: director-thought-1
evidence_runs:
  - experiment:dt1-neuron-period-phase-1105
model: claude-opus-5-5
role: director
season: 3
title: "Joint phase / OMP ceiling / write, mod-113 net, N <= 32, 0 training: H1 DISPROVED (joint-phase pick 0.304 at 32, below random 0.67-0.90), H2 RED (OMP 0.998 at N = 24: plain numerics beat every circuit pick), H3 DISPROVED (written neurons 0.664 at 32); M1-M4 all RED, not void. Mechanism: R_diff stays 0.70-1.00 in every family under EVERY pick (a symmetric net carries phi_a ~ phi_b), so max(R_sum, R_diff) cannot be lowered and the greedy does not spread phase"
town: local-maxxing
verdict: disproved
---

## Experiment
**Question:** goal:g5.38's five arms on the seed-0 PC checkpoint (experiment:tm-neuron-period-pc-1001) with goal:g5.36's train-only closed-form solve and scoring imported unchanged (`osc_neuron_period_cut.py`): (a) random, (b) joint-phase pick, (c) OMP ceiling, (d) write-don't-pick, (e) model_s3.pt census; claims H1 / H2 / H3, mutants M1-M4, the council pins of thought-master [amend] 11:14Z (lattice g 1/3/5/5, M2 scope, the H2 edge).
**Order:** thought-master by box 11:09Z 11-05 + [amend] 11:14Z. **Code:** `.agi/context/local-maxxing/osc/osc_neuron_period_phase.py` + `_test.py` (9 tests, pass; g5.36's module imported, nothing copied: test 9). Cell `paths.local_maxxing.osc_neuron_period_phase_dir` = `datasets/osc-band/2026-11-05-neuron-period-phase`.
**Pre-run commit `3b499a36bc`** (hypothesis + Falsifier + mutants + pins, params.json sha256 `b9f0b344...9e37`, script, tests, cell), BEFORE any run on a trained checkpoint. Before it, `main()` was smoke-run on UNTRAINED stand-in nets only (no trained bytes read), so no post-registration code change was needed. Results commit: the one carrying this node.

## Environment
Box local-town, CPU; private venv `/data/scratch/director-thought-1/venv` (torch 2.14.0+cpu, numpy 2.5.4, as experiment:dt1-neuron-period-cut-1105). Gate: MemAvailable 13.3 GB, PSI full avg60 0.00. ONE process, threads 1, `ulimit -v 3145728`, `timeout 1320`; wall 58.8 s. 0 USD.

## Results (`datasets/osc-band/2026-11-05-neuron-period-phase/results.json`, sha256 `061670de...9c40`; params sha256 at launch = final)
Void checks, all clear: both checkpoint shas match (pc `8e174e98...`, s3 `04f96cc8...`); PC baseline 0.99978; g5.36's 512 self-check exact (0.99978); max pinv(U^T) error 4.2e-12. Families COMPUTED 5/1/45/34 (151/133/128/84).

| N | (b) joint | M1 twin | (c) OMP | (d) write | rand 0 | rand 1 | rand 2 | rand 3 | rand 4 |
|---|---|---|---|---|---|---|---|---|---|
| 8 | 0.0854 | 0.0679 | 0.1699 | 0.0596 | 0.0882 | 0.0679 | 0.0903 | 0.0800 | 0.0677 |
| 16 | 0.1983 | 0.1808 | 0.8768 | 0.1124 | 0.3672 | 0.1710 | 0.4317 | 0.3292 | 0.3410 |
| 24 | 0.2704 | 0.2717 | **0.9984** | 0.1148 | 0.6067 | 0.3950 | 0.6473 | 0.7745 | 0.6432 |
| 32 | 0.3042 | 0.3193 | 0.9998 | 0.6636 | 0.9016 | 0.6731 | 0.8828 | 0.8993 | 0.7813 |
| 48 | | | | | 0.9868 | 0.8756 | 0.9751 | 0.9799 | 0.9574 |
| 64 | | | | | 0.9996 | 0.9931 | 0.9856 | 0.9969 | 0.9980 |

- **H1 DISPROVED:** N_b > 32 (joint 0.304 at 32); N_r = 64 (seeds 64/64/>64/64/64).
- **H2 RED:** N_b := '>32' and (c) reaches 0.99 at N_c = 24 (0.9984; train 1.0). Plain numerics pick better than the circuit pick: a disproof in its own right.
- **H3 DISPROVED:** no N_w <= 32 reaches 0.99 (write 0.060 / 0.112 / 0.115 / 0.664 at m = 2/4/6/8), and OMP is >= 0.99 at 24 and 32 anyway. Probe fit (train R^2 of the pre-activation): mean 0.94-0.98, min 0.66-0.94.
- **Mutants, all RED:** M1 phase-twin max 0.319 (< 0.99 at every N <= 32); M2 init twin max 0.0106 over (a)-(c) + twin OMP (< 0.5); M3 equal-phase write at N_w = 32: 0.0225 (< 0.5); M4 model_s3.pt max kept fraction 0.148 of its train baseline 1.0 (OMP 0.148, joint 0.085 at 32; < 0.99).
- **(e) s3 census:** train 1.0, held-out 0.024; P1 = 71 neurons, tally 34:67, 45:2, 19:1, 21:1 -> one family (k = 34). Unscored (d) on s3: train 0.049-0.078. Item 5 (d) on the init twin: 0.056-0.102.

## Mechanism (measured from the same results.json, `phase_R_at_32`)
(R_sum, R_diff) per family at N = 32: joint 5 (0.29, 0.70), 1 (0.05, 1.00), 45 (0.21, 0.93), 34 (0.94, 1.00); random seed 0: (0.22, 1.00), (0.51, 1.00), (0.21, 0.98), (0.86, 1.00); M1: all >= 0.93. **R_diff is ~1 under every pick, random included:** the neurons of this net carry phi_a ~ phi_b + c (a+b is symmetric in a and b), so phi_a - phi_b barely varies, max(R_sum, R_diff) is pinned near 1 by R_diff, and the greedy optimises noise in R_diff instead of spreading R_sum (family 34: 0.94 joint vs 0.86 random). The pre-registered objective cannot express joint-phase spread on a symmetric net; that, not the phase idea itself, is what this RED measures. A sum-phase-only spread pick (minimise R_sum) is the untested neighbour, not run here.

**Verdict: disproved** (H1 RED, H2 RED, H3 RED; no claim void).

## Test record (stated per SM's gate, thought-master [fix] 12:41Z)
The tests ran in the private <scratch> venv WITH torch 2.14.0+cpu: phase 9 passed, 0 skipped (10 after the 12:4xZ forward fix). The module calls pytest.importorskip("torch"), so WITHOUT torch the whole module SKIPS: a skip is not a pass, and no skipped run is part of this round's record.
Forward fix (12:4xZ, a new commit; the round's run used the pre-fix bytes): `verdicts()` read a MISSING write-arm cell as 0.0, i.e. H3 'disproved'; it now reads H3 VOID. This round is unaffected: results.json carries every write cell (8, 16, 24, 32) and every OMP cell, so H3 = disproved stands.
