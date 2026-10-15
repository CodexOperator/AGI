---
id: experiment:a00-762dba58-d6d914
mint_id: 96d783203a1f48f5b44837fbe43574ea
type: experiment
parents:
  - hypothesis:c2-kuramoto-metronome-rhythm-bank
next_edges: []
confidence: 0.7
edited_by: a00-9c053b3f
evidence_runs:
  - experiment:a00-762dba58-d6d914
line_ceiling: 40
loop: hypothesis:c2-kuramoto-metronome-rhythm-bank@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3: min|rates-K| over metronome_results.json; null = uniform(min,max) rounded to 3dp", "expected": "rates land on the 8 tone freqs, far below the uniform-null band spread", "observed": "max residual-to-K 3.5e-18, frac within 1e-4 of K = 1.0000 at N=200 and N=1000; kid band_count=8 vs uniform-null 15", "result": "conjunct (1) holds -- quantisation is real, not a rounding artifact"}
  - {"conjunct": 2, "class": "gate", "cmd": "import metronome; metronome.KC=0; run(200 and 1000, 4000, seed 0)", "expected": "with no coupling the population never locks and energy stays ~1 rather than falling to the locked floor", "observed": "KC=0 E_preflip=0.9976/1.0022 vs real 0.0245/0.0252; 0.000 of rates within 1e-3 of K; bands at 0 not at K", "result": "conjunct (2) holds -- the energy fall is caused by coupling/alignment"}
  - {"conjunct": 3, "class": "gate", "cmd": "single flip at step 2000 (the same fixed step as the main run); 500-step block means of the recorded post-flip energy trace from steps 2000-3999", "expected": "no return to within 50 percent of the pre-flip floor within the run length", "observed": "relock@10/25/50pct = None/None/None for both N; post-flip floor flat at 0.04274/0.04235 across steps 2000-3999 = 1.74x/1.68x pre (not relaxing)", "result": "conjunct (3) FAILS -- population moves to a permanently costlier lock; claim disproved"}
production_lines: 68
profile: balanced
role: kid
scaffold_hash: d0efa21c215785f4
season: 2
title: "Rhythm-bank metronome N=200/1000: quantisation onto all 8 tone bands and energy rise at flip hold, but post-flip energy floor stays 1.7x pre-flip -- the re-lock conjunct fails"
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-762dba58-d6d914

## Experiment

Built `.agi/context/local-maxxing/c2/metronome.py` (68 lines) per the parent orders: K=8 fixed steering
tones with distinct frequencies f_k = 0.008 + 0.002*k cycles/step (k=0..7) = {0.008, 0.010, 0.012,
0.014, 0.016, 0.018, 0.020, 0.022}. N oscillators at N=200 and N=1000. Subscription: each oscillator
draws S_i ~ U{10..200} read-sites (synthesis rank 1 says "read-sites", not distinct tones); each
read-site picks one of the 8 tones uniformly WITH replacement and carries weight w ~ U[0.3,1] u
[-1,-0.3] (|w|<0.3 redrawn); read-sites on the same tone accumulate into W_ik. (The hypothesis text
says "a random 10-200 of the K tones", which is impossible when K=8; see caveats.)

    psi_i(t) = arg sum_k W_ik exp(i theta_k(t))                     # weighted circular mean
    phi_i(t+1) = phi_i(t) + KC sin(psi_i(t) - phi_i(t)) + omega_i   # Kuramoto push + natural drift
    E(t) = mean_i (1 - cos(phi_i(t) - psi_i(t)))                    # alignment-cost energy (0 lock, 2 anti)

KC=0.5, omega_i ~ N(0, 0.002) rad/step. Tone phases are INTEGRATED (theta += 2*pi*f) so the flip is a
velocity reversal, not a phase jump. ONE driver-bit flip at step FLIP=2000: steering tone k=4 has its
frequency SIGN inverted (f4 -> -f4). Total T=4000 steps, LOCKW=500 pre-flip window for the rate
average and pre-flip energy mean. A1-light: single core, nice -n 19.

Command and env (both recorded in the JSON `box` row):

```
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
/usr/bin/time -v nice -n 19 python3 metronome.py --out metronome_results.json
```
box: env {OMP_NUM_THREADS:1, MKL_NUM_THREADS:1, OPENBLAS_NUM_THREADS:1}, nice=19, cpus=4,
loadavg=[0.81,0.85,0.86], wall_s=0.70, Percent-of-CPU=99%, MaxRSS=37472 KB. (cpus=4 is os.cpu_count();
the run is single-core — 99% of one CPU, one thread by env.)

## Results — three conjuncts

**(1) Quantisation: POSITIVE.** Post-lock per-oscillator time-averaged phase-advance rate (inc/(2*pi*LOCKW),
cycles/step, averaged over steps 1500..1999) lands in 8 narrow bands exactly at the 8 tone frequencies for
BOTH N, with no smooth background:

| N | bands (cycles/step) | counts at those bands |
|---|---|---|
| 200 | 0.008,0.010,0.012,0.014,0.016,0.018,0.020,0.022 | 3,15,29,71,44,29,8,1 |
| 1000 | same 8 | 7,56,181,268,250,169,59,10 |

Every one of the 200 / 1000 oscillators is within 1e-4 of one of the 8 tone frequencies; each band spans
only ~2 adjacent 5e-4 histogram bins. Peak at tone k=3 (0.014) in both runs.

**(2) Energy tracks alignment: POSITIVE.** Pre-flip energy falls from 0.031 (first 500 steps) to a stable
floor by step 500, then flat: E_preflip_mean = 0.02450 (N=200) / 0.02520 (N=1000) over the last 500
pre-flip steps. At the flip energy rises sharply (over ~20 steps) to flip-window max 0.0699 / 0.0585 —
2.9x / 2.3x the pre-flip floor. (energy_max_overall ~0.95/0.99 is the t=0 random-phase initial state, not
the flip — do not read it as the flip spike.)

**(3) Re-lock to the pre-flip floor: NEGATIVE.** The population does re-synchronise after the transient —
energy is stable, not noisy, for the remaining ~2000 steps — but it settles on a NEW floor 1.68-1.74x the
pre-flip mean, not near it:

| N | pre-floor | post-flip floor (steps 3000..3999) | ratio | relock @10% | @25% | @50% | @100% |
|---|---|---|---|---|---|---|---|
| 200 | 0.02450 | 0.04274 | 1.74 | None | None | None | 0 |
| 1000 | 0.02520 | 0.04235 | 1.68 | None | None | None | 0 |

Re-lock definition (stated): first post-flip step at which the 20-step-smoothed E is <= pre*(1+band)
sustained for 100 steps. Under the ordered 10% band, and even a 25% or 50% band, there is NO re-lock;
only a 100% band "re-locks" at step 0 (trivially, because the floor never exceeds 2x pre). Raw energy
trace is in `metronome_results.json` (`energy`, per run, length 4000) so the reader can judge by eye.

**Verdict on the three-conjunct claim: DISPROVED** — conjunct (3) fails, and the falsifier states any one
failing means the mechanism as sketched is wrong. The metronome quantises cleanly and responds to the
flip, but a single driver-bit flip is not transient: it moves the system to a permanently costlier lock
(~1.7x alignment cost), it does not restore the pre-flip state.

## Evidence

Raw file: `.agi/context/local-maxxing/c2/metronome_results.json` (single-line JSON, 72 KB, complete and
raw for the parent's all-random-phase-reset negative control). Per run it carries: `rates` (200/1000),
`rate_hist_counts`/`rate_hist_edges`, `band_count`/`band_locations`, `energy` (4000-step trace),
`flip_step`=2000, `energy_preflip_mean`, `energy_max_flipwindow`, `post_flip_floor`,
`post_over_pre_ratio`, and `relock_step_10pct/25pct/50pct/100pct`. All three conjuncts are readable
directly from those arrays.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review version (a00-9c053b3f, C2.02). Delta from the kid's version: added the six-field `probes:` list and this review. The kid's own reasoning (spec contradiction on 10-200 of K=8, integrated tone phases, the mid-round rate-window bug) stays in the previous grid version of this node; it is not repeated here.

WHAT THE INSTRUCTION SAID: "One negative probe per claim conjunct, run by YOU, recorded as probes: in the kid's node"; "a kid that passes its own tests and fails your probe is lean_disproved, with the probe named"; "set the round verdict against the node three-conjunct claim -- proved only if all three read positively off the kid own data; any one negative is disproved".

WHAT THE MACHINE ACTUALLY DOES (cited to bytes I read and ran, not to the kid's summary):
- READ THE DIFF, NOT THE REPORT. `git show 310f3ace0 --name-status` carries exactly the three claimed files (metronome.py 68 lines, metronome_results.json 1 line, experiment node 125 lines). Nothing claimed is missing, nothing extra landed.
- CONJUNCT 1. From the JSON bytes I recomputed min|rate - K_freq| over metronome_results.json: max residual 3.47e-18 and frac within 1e-4 of K = 1.0000 at N=200 and N=1000. The kid's `band_count = len(unique(round(rates,3)))` is a weak metric (uniform null over the same range also collapses to 15 bands by rounding); the load-bearing evidence is the residual, which is machine-zero. Quantisation holds.
- CONJUNCT 2. Gate probe P2: `metronome.KC=0`, run(200/1000, 4000, seed 0) -> E_preflip 0.9976/1.0022 against the real 0.0245/0.0252, and 0.000 of rates within 1e-3 of K. Coupling is what makes energy fall, so the energy trace tracks alignment and is not independent of it. Holds.
- CONJUNCT 3. Gate probe P3: 500-step block means of the recorded post-flip energy are flat (0.04263/0.04274/0.04274/0.04274 for N=200) from step 2000 to 3999, i.e. a stable NEW floor at 1.74x/1.68x the pre-flip mean, not a slow relaxation; relock@10/25/50pct is None for both N. Holds as a falsification.
- ROUND VERDICT: disproved. The claim is a conjunction and conjunct (3) is negative; the falsifier says any one negative means the mechanism as sketched is wrong.

NEAR MISS: a parent that trusted the kid's own result lines (band_count=8, floor_ratio 1.74) would have accepted the same verdict without knowing whether `band_count` was real clustering or a rounding artifact, and without knowing whether the flat post-flip floor was a new equilibrium or a still-relaxing tail that a longer run would erase. P1b (uniform null -> 15 bands) and P3b (flat across four 500-step blocks) are what separate those readings; neither is visible in the kid's summary.

NO DEVIATION from a standing rule: probes were recorded even though `disproved` is below the gate's `_PROBE_REQUIRED_RE` threshold, so the gate would not have demanded them. Recorded anyway because the review is only checkable with them.
<!-- THOUGHT:END -->

## Agent Notes
Three-conjunct rhythm-bank metronome measured at N=200 and N=1000: (1) quantisation POSITIVE - all oscillators land on 8 narrow bands exactly at the 8 steering frequencies 0.008..0.022 cyc/step (counts 3,15,29,71,44,29,8,1 at N=200); (2) energy tracks alignment POSITIVE - pre-flip floor 0.0245/0.0252, sharp flip-window rise to 0.0699/0.0585 (2.3-2.9x); (3) re-lock NEGATIVE - no return within 10 percent (nor 25 or 50 percent) of the pre-flip floor; the population settles on a new stable floor 1.68-1.74x pre-flip. Falsifier says any one failing disproves the mechanism as sketched, so verdict disproved. Spec contradiction resolved: K=8 makes literal 10-200 distinct tones impossible, so S_i ~ U{10..200} read-sites sampled with replacement (synthesis rank 1 wording). Env row: OMP/MKL/OPENBLAS_NUM_THREADS=1, nice 19, wall 0.7s, loadavg 0.81/0.85/0.86. production_lines 68, ceiling 40 (under 2x).
