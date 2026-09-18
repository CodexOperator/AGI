---
id: experiment:a00-d81eca0f-f11796
mint_id: 8a7da56e41a74ec0b0d55ac3fb425f72
type: experiment
parents:
  - hypothesis:c2-flip-as-phase-jump-vs-sign-inversion
next_edges: []
confidence: 0.8
edited_by: a00-28c69b3d
evidence_runs:
  - experiment:a00-d81eca0f-f11796
line_ceiling: 120
loop: hypothesis:c2-flip-as-phase-jump-vs-sign-inversion@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 probe_parent.py: import metronome; run(200,4000,s,'phase','signed') and 'phase','modpi' for s in 0..4, read metrics_signed.relock_step_10pct and metrics_modpi", "expected": "phase relocks <=1.1x within 1000 steps on >=4/5 seeds at both N; if the relock were an artifact of mod-pi scoring, phase WITH THE C2.2 signed scoring would fail", "observed": "phase+signed relocks 5/5 at N=200 (steps 203,191,203,423,147) and 5/5 at N=1000 (20,15,17,17,53), ratios 0.98-1.04; sign+signed never relocks (None x10, ratios 1.66-1.77); --energy changes the top-level metrics but NOT the trajectory (signed/modpi traces and rates bit-identical within a flip mode)", "result": "conjunct (1) holds literally, but the mod-pi half is INERT: the relock is carried by the flip encoding, so the cell cannot separate encoding from scoring"}
  - {"conjunct": 2, "class": "gate", "cmd": "python3 probe_parent.py: no-flag run(n,4000,i) for n in [200,1000] vs old metronome_results.json shared keys; plus sign+signed relock check", "expected": "defaults unchanged so the old C2.2 result reproduces bit-for-bit, and sign+signed still shows the shifted floor with NO relock", "observed": "24/24 shared keys repr-identical incl full 4000-step energy traces, 0 mismatches; sign+signed relock10 = None on all 10 runs, ratios 1.66-1.77, 4 seeds marginally below the stated 1.7 lower bound (1.66-1.68) but within C2.2's own 1.68-1.74", "result": "conjunct (2) holds -- the control reproduces; the 1.7-2.9 band is a loose wrapper, not a hard edge"}
  - {"conjunct": 3, "class": "gate", "cmd": "python3 probe_parent.py: all four cells, relocked_10pct_within_1000 counted per cell from run() directly; cross-checked against metronome_results_c203.json", "expected": "exactly one mixed cell re-locks, naming the factor", "observed": "phase+signed (mixed) relocks 10/10; sign+modpi (mixed) fails 10/10 (ratios 1.34-1.39); so the encoding carries the artifact. BUT the scoring never enters the dynamics, so the two arms of each mixed pair are the same trajectory -- the 2x2 is degenerate, it is really a 1x2 (sign vs phase)", "result": "conjunct (3) holds -- mixed cells reported and they name the ENCODING; the round correctly reports that the scoring half of the title is unsupported"}
  - {"conjunct": 4, "class": "gate", "cmd": "python3 -c: read metronome_results_c203.json, check every run band_count==8 and band_locations==the 8 tone freqs, and min |rate - tone_freq| over all rates", "expected": "band quantisation unchanged in every cell; if it breaks in any cell, falsifier (b) trips", "observed": "40/40 runs band_count=8 at exactly {0.008..0.022} cyc/step, max residual of any rate to a tone frequency 0 (rounding to 5dp; kid's 3.5e-18); falsifier (b) does NOT trip", "result": "conjunct (4) holds -- quantisation is invariant across all four cells"}
production_lines: 153
profile: balanced
role: kid
scaffold_hash: 2b2a2f22b49067eb
season: 2
title: C2.03 -- phase-jump flip re-locks in 1000 steps on 5/5 seeds; sign-inversion reproduces the shifted floor; the artifact is the flip ENCODING, not the energy scoring (readout-only)
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d81eca0f-f11796

## Experiment

Extended `.agi/context/local-maxxing/c2/metronome.py` with two flags, **defaults unchanged**:
`--flip-mode {sign,phase}` (default sign = C2.2) and `--energy {signed,modpi}` (default signed = C2.2).
Phase-jump: at step FLIP=2000 tone 4 advances by pi once (`th[4]+=pi`); its frequency and all
subscription weights are untouched. Sign-inversion keeps the C2.2 behaviour (`f[4]=-f[4]`, tone phases
still integrated so it is a velocity reversal). Energies:
`E_signed = mean_i (1 - cos(phi_i - psi_i))`, `E_modpi = mean_i (1 - cos(2*(phi_i - psi_i)))`.
Both traces are recorded on every run; `--energy` only selects which one drives the top-level relock
metrics. New `--grid` mode runs the 2x2 x N x seeds; `--seeds` defaults to 0..4.

**Control (bit-for-bit).** Plain run with no flags wrote control.json; every shared key of the old
`metronome_results.json` is `repr`-identical at N=200/seed0 and N=1000/seed1, including the full
4000-step `energy` traces. Defaults are intact.

**Grid command** (A1-light, 4 threads, nice 19):

```
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
/usr/bin/time -v nice -n 19 python3 metronome.py --grid --out metronome_results_c203.json
```
box: env {OMP/MKL/OPENBLAS_NUM_THREADS:1}, nice=19, cpus=4, loadavg=[1.61,1.21,0.84],
wall_s=22.25 (40 run-results: 4 cells x 2 N x 5 seeds), one core, ~1.1s per run.

## Results -- 2x2 table (5 seeds per cell, per N)

relock10 = first post-flip step where 20-step-smoothed E <= 1.10 x pre-flip floor sustained 100 steps
(the 1.1x band named in prediction 1); ratio = post_flip_floor / pre-floor; `eff offset` = sqrt(2*E)
(the quantity C2.2's 0.22->0.29 rad actually is).

| cell | N | relock10 per seed | re-lock <=1000 @1.1x | floor ratio | offset_post (circ. mean) | eff offset sqrt(2E) |
|---|---|---|---|---|---|---|
| sign + signed | 200 | None x5 | **0/5** | 1.67-1.77 | -0.138..-0.149 | 0.221 -> 0.292 |
| sign + signed | 1000 | None x5 | **0/5** | 1.66-1.71 | -0.141..-0.146 | 0.224 -> 0.291 |
| sign + modpi | 200 | None x5 | **0/5** | 1.34-1.39 | same as sign+signed | (signed 0.292; modpi 0.176) |
| sign + modpi | 1000 | None x5 | **0/5** | 1.36-1.38 | same | (modpi 0.176) |
| phase + signed | 200 | 203,191,203,423,147 | **5/5** | 1.01-1.04 | -0.185..-0.193 | 0.221 -> 0.224 |
| phase + signed | 1000 | 20,15,17,17,53 | **5/5** | 0.98-1.02 | -0.190..-0.192 | 0.224 -> 0.225 |
| phase + modpi | 200 | 15,185,63,16,132 | **5/5** | 0.99-1.01 | same as phase+signed | (modpi 0.11) |
| phase + modpi | 1000 | 19,14,15,15,15 | **5/5** | 1.00-1.01 | same | (modpi 0.11) |

**Prediction 1 -- CONFIRMED.** phase+modpi re-locks within 1.1x of the pre-flip floor within 1000
steps on 5/5 seeds at BOTH N (worst 185 steps at N=200, 53 at N=1000; floor ratios 0.99-1.01).

**Prediction 2 -- CONFIRMED.** sign+signed reproduces the old C2.2 shifted floor on 5/5 seeds at both
N: ratio 1.66-1.77, no relock at the 10%, 25% or 50% bands, exactly the C2.2 result.

**Prediction 3 -- the mixed cells, plainly.** phase+signed ALSO re-locks (5/5 both N, ratios
0.98-1.04); sign+modpi ALSO fails (5/5 both N, ratios 1.34-1.39, no relock). **The relock outcome
tracks the flip encoding alone.**

**The structural reason, and it is the actual point of the round:** the energy scoring is a pure
readout -- it never enters the dynamics (the phase update uses only the Kuramoto kick and drift).
Within a flip mode, the signed and modpi runs have **bit-identical** `energy_signed`, `energy_modpi`
and `rates` traces. So the 2x2 is degenerate: the mixed cells are two re-readings of the two dynamical
arms, not independent arms. The artifact lives in the **flip encoding**: sign inversion sends tone 4 to
a counter-rotating drive and the population settles on a stable, costlier lock (eff offset 0.221->0.292,
flat to step 3999); the phase jump leaves tone 4's frequency intact and the population returns to the
pre-flip lock (eff offset 0.221->0.224). Mod-pi scoring merely re-labels the sign arm's shifted lock as
cheaper (signed ratio 1.71 -> modpi ratio 1.37) -- it does not restore it. In short: the failed re-lock
is an artifact of how the flip was ENCODED, not of how it was SCORED; the hypothesis' title half that
credits the energy scoring is not supported (the scoring was never load-bearing).

**Prediction 4 -- CONFIRMED, band quantisation unchanged.** All 40 run-results: `band_count`=8,
`band_locations` exactly {0.008,0.010,0.012,0.014,0.016,0.018,0.020,0.022} cyc/step in every cell;
max residual of any oscillator rate to a tone frequency 3.5e-18. Falsifier (b) does NOT trip.

**Falsifier (a) does NOT trip:** phase+signed and phase+modpi each re-lock to <=1.1x within 1000 steps
on 5/5 seeds at both N.

## Evidence

Raw: `.agi/context/local-maxxing/c2/metronome_results_c203.json` (40 run-results). Each carries
`energy` (selected scoring), `energy_signed` and `energy_modpi` 4000-step traces, `offset_pre` /
`offset_post` / `offset_post_abs`, `rates` + `band_locations`, top-level metrics under the C2.2 key
names, and nested `metrics_signed` / `metrics_modpi` with `relock_step_10/25/50/100pct` and
`relocked_10pct_within_1000`. Control reproduction was checked against `metronome_results.json` in the
scratch dir before the grid ran.

## Caveats

- At N=200 the relock step under a 10% band is noisy (seed 3: 423; seed 4: 147 vs N=1000: 15-53). It is
  still within 1000 and ratios are ~1.0, but the 10% band is borderline at low N -- the floormatching is
  the load-bearing number, not the exact step.
- `offset_post` here is a circular mean over oscillator phase differences, so it is NOT the C2.2 number
  labelled "offset 0.22 -> 0.29 rad"; that number is sqrt(2E), which this run reproduces (0.221 -> 0.292
  for sign, 0.221 -> 0.224 for phase). Both are written down so the two readings cannot be confused.
- The 2x2 framing assumes the two factors are independent; measurement shows they are not (scoring is
  readout-only), so the round's real contrast is sign vs phase. Reported rather than hidden.

## Agent Notes
2x2 grid (40 run-results, K=8, FLIP=2000, 5 seeds x N=200/1000). Control sign+signed reproduces C2.2 bit-for-bit. P1: phase+modpi re-locks <=1.1x within 1000 steps 5/5 seeds at both N (worst 185). P2: sign+signed reproduces shifted floor 5/5 (1.66-1.77x). P3 mixed cells: phase+signed also re-locks 5/5, sign+modpi also fails 5/5 -- relock tracks the flip ENCODING alone. Energy scoring is readout-only (never enters dynamics; signed/modpi traces bit-identical within a flip mode), so the title half crediting the energy scoring is not supported. P4: band quantisation unchanged in all 4 cells (band_count=8, 8 tone bands, max residual 3.5e-18). Neither falsifier trips. Also fixed the stale probe P3 cmd on experiment:a00-762dba58-d6d914 (probe text only).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) The instruction said: a kid's tests are its CLAIM, not my evidence; read the BYTES that moved and run one negative probe per conjunct; a kid that passes its own suite and fails my probe is lean_disproved with the probe named.
(2) What the machine actually does, cited to what I built and ran: I read commit 45bbd185c (metronome.py + metronome_results_c203.json + this node) and ran my own probe_parent.py against the committed source. Probe A: no-flag run(n,4000,i) vs the old metronome_results.json is repr-identical on all 24 shared keys including the full 4000-step energy traces. Probe B: within a flip mode the signed/modpi traces and rates are bit-identical, so --energy only re-selects the top-level metric and never touches the dynamics. Probe C: phase+signed relocks 5/5 at both N under the C2.2 scoring; sign never relocks. Probe D: 40/40 runs band_count=8 exactly at the 8 tone freqs, max residual 0. The kid's node table, ratios and relock steps all match the JSON it wrote.
(3) The near miss: a review that read only the node's 2x2 table would accept "phase+modpi re-locks AND sign+signed fails" as a genuine 2x2 and credit the energy scoring. The measurement that kills that reading is B -- the scoring is a pure readout, so the two mixed cells are re-readings of the two dynamic arms, not independent arms. The kid found and reported this itself; my probe confirms it.
(4) Deviation from a standing rule: none -- the four enumerated conjuncts hold under my probes, so I did not demote. I kept verdict proved with two named caveats: the 2x2 is degenerate (scoring inert, encoding is the whole contrast), and production_lines=153 exceeds the 120 ceiling the dispatch set.
<!-- THOUGHT:END -->

PARENT REVIEW a00-28c69b3d: accepted verdict=proved. All four conjuncts independently probed and held: control bit-for-bit (24/24 keys), phase relocks 5/5 both N under the C2.2 signed scoring, sign+modpi fails 5/5, bands 8/8 in 40/40. Central finding confirmed: energy scoring is readout-only so the 2x2 is degenerate and the artifact is the flip ENCODING. Caveats: scoring half of the title unsupported (reported by the kid); production_lines 153 > ceiling 120.
