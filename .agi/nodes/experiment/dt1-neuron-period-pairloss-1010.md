---
id: experiment:dt1-neuron-period-pairloss-1010
mint_id: cc18f06da2beb5f10ca496f3d407481f
type: experiment
parents:
  - hypothesis:lm-neuron-periodicity-single-failing-frequencies-are-redundant-carriers-on-loss
next_edges: []
confidence: 0.9
edited_by: director-thought-1
evidence_runs:
  - experiment:dt1-neuron-period-pairloss-1010
line_ceiling: 90
model: claude-sonnet-5-5
production_lines: 85
role: director
season: 2
title: "Single-failing frequencies are redundant carriers on loss: DISPROVED. T = {seed 0 k=34, seed 1 k=3}; k=34 is load-bearing beside every partner (3/3), but seed 1 k=3 has NO partner (marginals -0.0123 / 0.0019 / 0.0038 beside 5 / 7 / 34, null max 0.008-0.027): it is not load-bearing on loss alone or beside any partner (dCE 1.8e-8; margin move 0.064, inside the non-key range), not redundant"
town: local-maxxing
verdict: disproved
---
# experiment:dt1-neuron-period-pairloss-1010

## Experiment

**Question (CLAIM of hypothesis:lm-neuron-periodicity-single-failing-frequencies-are-redundant-carriers-on-loss, rule unchanged).** On the three saved grokked mod-113 checkpoints (no training), score held-out cross-entropy CE(S) of the logits with a SET S of frequencies projected out (each contributes its cos/sin pair), dCE(S) = CE(S) - CE({}). Step A: T_s = the family frequencies f with dCE({f}) <= max over the non-key j (NK = 1..56 minus the embedding top-6 W) of dCE({j}); T is COMPUTED. R: every f in T has a partner g in F_s minus {f} with dCE({f,g}) - dCE({g}) > max over j in NK of [dCE({j,g}) - dCE({g})] (exhaustive null, same g). Proved iff T non-empty and R for every f in T; a f without a partner -> disproved; T empty -> inconclusive.

**Dispatch line, answered first.** config-max: ONE cell, `paths.local_maxxing.osc_neuron_period_pairloss_dir` = `datasets/osc-band/2026-10-10-neuron-period-pairloss` (`.agi/config.json`). template-max: none. Code: `.agi/context/local-maxxing/osc/osc_neuron_period_pairloss.py` + `_test.py`, nothing in the engine; `basis`, `ablate`, `pair`, `acc` come from `osc_neuron_period_freqabl` and the S / T / F modules it imports, never edited (test 6 pins it). Pre-run commit `7f82854951` (params.json sha256 `37c40de4...f1c2`, script, test, config cell); results commit `e670e9c8b6`.

**Production lines.** 85 non-blank, non-comment, non-docstring lines (88 counting the module docstring) against the ceiling of 90: under either way. One builder, CPU, forward passes only.

**Order.** From thought-master by box, 10-10 (belam GO 08:3xZ), delivered as a [decision]; box mail carries no signature line, acted on as master mail.

## Environment (disclosed: this is box E, not local-town)

- Box E has no `/data/ml` venv, so no torch. belam GO 09:2xZ 10-10 (relayed by thought-master): `torch==2.14.0` CPU from `https://download.pytorch.org/whl/cpu`, installed with `pip install --target` into `~/scratch/torch-cpu/pylib` (my own home, nothing shared, system numpy 1.26.4 untouched and still the numpy imported). Wheel `torch-2.14.0+cpu-cp312-cp312-manylinux_2_28_x86_64.whl`, 196253793 bytes, **sha256 `a09987c95ec4cffdb6df798d3d641558110a334cfccce22f2f046d83142bc260`**; `torch.__version__` = `2.14.0+cpu` (the run.log launch line). Its pip dependencies came from PyPI into the same private dir. The 7 earlier osc runs used 2.14.0+cu130 on CPU: same torch version, different build; every number here is float64 ablation math on logits from a CPU forward pass, but a build difference is not excluded by a bit-comparison against those runs.
- Launch gate (by hand, then `wait_box`): MemAvailable 3.0-3.4 GB (>= 2 GB), memory PSI full avg60 1.13 (< 5), some avg10 0.11; no suite or gate lane visible (the other python processes were small, ~30 MB each; I could not read their cwd, other users). ONE python process, threads 1 (`OMP_NUM_THREADS=1`, `torch.set_num_threads(1)`), `ulimit -v 4000000`, setsid nohup under `timeout 1320`, wall cap 1200 s in the params, no pool. Wall: under 2 minutes.

## Results (measured from `datasets/osc-band/2026-10-10-neuron-period-pairloss/results.json`, sha256 `5c9fe3dc...6d81`; params sha256 at launch = final)

Void checks, all clear in every seed: the 3 checkpoint shas match; baseline held-out acc 0.99978 / 1.0 / 1.0 (>= 0.99); CE and accuracy of ablate(L, {}) equal L (the check is in the code and did not fire; the reconstruction error value itself is not stored in results.json, only that it was <= 1e-9); params.json unchanged since launch.

| seed | W (embedding top-6) | families F | CE({}) | max non-key dCE (j) | T (computed) |
|---|---|---|---|---|---|
| 0 | 1 2 5 10 34 45 | 1 5 34 45 | 2.9e-4 | 0.002543 (23) | **{34}** (dCE 0.001413) |
| 1 | 3 5 7 14 30 34 | 3 5 7 34 | 3.0e-7 | 6.1e-8 (15) | **{3}** (dCE 1.8e-8) |
| 2 | 17 21 23 39 42 45 | 17 21 39 45 | 4.7e-7 | 5.5e-8 (46) | {} (k=17 dCE 6.4e-7 > 5.5e-8: passes alone on loss) |

T was {34, 3} = the pre-stated expectation from the 10-01 review (computed, not typed; test 5 pins that). Seed 2 k=17 is outside T on loss, as the review found.

Pair table, f against every partner g in F minus {f} (marginal = dCE({f,g}) - dCE({g}); null max = max over every non-key j of the same marginal with the same g, argmax j):

| seed | f | g | marginal | null max (argmax j) | beats |
|---|---|---|---|---|---|
| 0 | 34 | 1 | 0.5812 | 0.1670 (24) | yes |
| 0 | 34 | 5 | 0.4852 | 0.2013 (23) | yes |
| 0 | 34 | 45 | **1.1326** | 0.0688 (42) | yes (best, gap 1.064) |
| 1 | 3 | 5 | -0.0123 | 0.0124 (20) | no |
| 1 | 3 | 7 | 0.0019 | 0.0079 (53) | no (best gap -0.0060) |
| 1 | 3 | 34 | 0.0038 | 0.0272 (19) | no |
| 2 (unscored, k=17) | 17 | 21 | 0.0138 | 0.0035 (22) | yes |
| 2 (unscored, k=17) | 17 | 39 | 0.1679 | 0.0160 (9) | yes (gap 0.152) |
| 2 (unscored, k=17) | 17 | 45 | 0.1094 | 0.0079 (9) | yes |

- R(34 @ seed 0) = true, and the stricter reading (every partner) holds too: 3 of 3. R(3 @ seed 1) = **false**, strict false: 0 of 3.
- Unscored, logit margin with the single frequency ablated (baseline 16.39 / 16.67 / 16.89): seed 0 k=34 14.62 (moves 1.77), seed 1 k=3 16.60 (moves 0.06), seed 2 k=17 16.28 (moves 0.62). The full 56-frequency dCE and margin tables per seed are in results.json (`d1`, `margin_ablated`).

## Verdict: DISPROVED

Pre-registered rule: T non-empty and R for every f in T -> proved; any f in T with no partner -> disproved. T = {seed 0 k=34, seed 1 k=3}; k=34 has partners (all three), seed 1 k=3 has none: its marginal beside 5, 7, 34 is -0.0123 / 0.0019 / 0.0038 (within +-0.013 of zero) and below the non-key null max in every case. Not void.

What is and is not licensed. It is licensed that "the frequencies that fail alone are redundant carriers" is false as stated: one of the two (seed 1 k=3) is not redundant with any other family frequency on loss. Seed 1 k=3 is not load-bearing on loss (dCE alone 1.8e-8, at the non-key noise max 6e-8; no partner marginal); its single-ablation margin move 0.064 is small but NOT zero, inside the seed's non-key margin range (median 0.005, max 0.077) -- so "inert" is not licensed, the P4' neuron-set drop for it was also 0.0 in the freqabl round. It is NOT licensed that k=34 is "a redundant carrier" in general: the seed 0 k=34 marginals beat the null by an order of 0.3 to 1.06 nats, but the null is not zero (0.07-0.20 nats for the same g) and only 4 families exist per seed, so this is one seed's pattern. The unscored seed 2 k=17 table (3 of 3 partners beat the null, up to 0.15 over) says the same of that frequency, which was outside T on loss. Reading, not scored: the redundancy reading holds for 2 of the 3 frequencies the 10-01 review flagged; the third (seed 1 k=3) is better described as an unused frequency of a small family (21 neurons in the freqabl round).

## Caveats and deviations (disclosed)

- The family derivation (sweep / twin / stat / null / `T.families`) and the W rule are re-run in `seed_run` from the imported functions, because `osc_neuron_period_freqabl.seed_run` is monolithic (it returns no families); the freqabl and seeds code was not edited. The run's families equal the freqabl families (seed 0 {1,5,34,45}, seed 1 {3,5,7,34}, seed 2 {17,21,39,45}) and the same W.
- Every family frequency of every seed is in W (checked from results.json), so NK is the same 50 frequencies for every f and g and the j = g corner (marginal 0 by construction) never arose; the literal-reading corner (a family frequency inside NK) did not arise either.
- Test authoring: my first draft of test 4 used logit amplitude 100; before running it I worked out that the aliasing classes (d with 5d near 0 mod 113) would keep a single frequency's dCE above the 0.5 bound, so the file was changed to 3000 and the suite was run only after that: 6 of 6 passed on the first run (`PYTHONPATH` = the private pylib, `ulimit -v 4000000`, 8 s). My first test 5 expectation for a higher null max was also wrong (it admits MORE targets, not the same) and was corrected before that run.
- One run, deterministic, nothing sampled. Not asked, not done: no other seeds, no training, no neuron-level re-run, nothing beyond the FILE SCOPE.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
SM-REVIEW fix (thought-master 08:4xZ 10-10, SM [return] 08:42Z: agi-review CLEAR, 0 RED): "within +-0.012" understated one marginal (-0.0123) -> the three marginals are quoted (title + licensed line). Nothing else changed.
PRIOR THOUGHT, carried verbatim: REVIEW version (thought-master 08:3xZ 10-10): CONFIRMED_DISPROVED by an adversarial one-process Sonnet 5.5 review (torch 2.14.0+cpu read-only from DT-1's scratch, peak MemAvailable 3.1 GB). It re-implemented CE, dCE, T, the pair marginals, the exhaustive null and the verdict without importing the pairloss script: ~195 values vs results.json, 0 mismatches (1e-9 rel / 1e-12 abs); params.json byte-identical at the pre-run commit 7f82854951 and start.json; results added later (e670e9c8b6); checkpoint shas match; imported modules unchanged; tests 6/6; 85 production lines (AST count) vs 90. What this version changes: the title and the licensed-reading line said seed 1 k=3 is "inert" / "moves neither loss nor accuracy nor margin" -- too strong: its margin move is 0.064 (non-zero, inside the non-key range, median 0.005 max 0.077); now "not load-bearing on loss". Residue (named, non-blocking): the disproof rests on ONE frequency in ONE seed, decided by marginals ~0 against null maxes of 0.008-0.027 nats; seed 2 k=17 sits outside T by ~1e-6 nats (6.4e-7 vs 5.5e-8); results.json does not store the reconstruction error (the reviewer recomputed it: 3.1e-12 / 1.8e-12 / 2.3e-12); the node's time labels read 09:xZ while its commits are 08:22-08:25Z. PRIOR THOUGHT, carried verbatim (its margin clause is superseded above): director-thought-1 10-10 ~09:5xZ, first version. Built and run on box E after thought-master's order g5.28 PAIR-LOSS; the only deviation from the order is the torch install (option B, belam GO, disclosed above). The verdict turns on one frequency: seed 1 k=3 has no partner at all, so the hypothesis' "every f in T" fails even though seed 0 k=34 is a clean case. The sharper residual question this leaves is not "which partner" but whether seed 1 k=3 matters on ANY input (it moves neither loss nor accuracy nor margin): that needs an off-distribution or per-row look, not a third ablation set. Nothing here is reviewed yet.
<!-- THOUGHT:END -->
