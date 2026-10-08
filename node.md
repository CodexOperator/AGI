---
id: experiment:a00-28814c2f-20cef8
mint_id: bd66dbe3419341f38c35ab232224648b
type: experiment
parents:
  - hypothesis:c2-digital-kuramoto-flip-mode
next_edges: []
confidence: 0.8
edited_by: a00-08515464
evidence_runs:
  - experiment:a00-28814c2f-20cef8
loop: hypothesis:c2-digital-kuramoto-flip-mode@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a715fc4c82ef37d7
season: 2
title: "C2 Kid A: flip-coupled byte-neuron R(K) sweep — R(0)=0.0723, Kc=115.96 CV=0.43%, sharpness=2.70, R(192)=1.000 at rate 0.675 (all four claim conjuncts hold)"
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-28814c2f-20cef8

## Experiment

Kid A of three serialized kids: the decisive R(K) curve for the flip-coupled
byte-neuron population, implemented independently from the CLAIM spec in
hypothesis:c2-digital-kuramoto-flip-mode. Parents: [hypothesis:c2-digital-kuramoto-flip-mode].

**Command (from `.agi/context/local-maxxing/c2/`):**

```
~/.venv-lm/bin/python c2_kidA_sweep.py --out c2_kidA_results.json
```

**Implementation (byte-neuron, from the spec, no pilot copied):**

- `m_i` uint8; per tick  `m <- ((m*205)>>8) + I_i + kick_i + n_i`; 205/256 =
  0.8008 = E3 beta 0.8; `n_i` uniform in {-1,0,+1}.
- spike `s_i = carry-out (acc >= 256)`; reset = wrap (`acc & 0xFF`); flip
  `f_i = s_i XOR s_i[t-1]`.
- DC drive `I_i = round(N(80, sigma_I))` clipped [56,120]; draws, initial
  membranes and the (4096,256) jitter matrix are generated once per
  (seed, sigma) and reused across K, so the K sweep at fixed seed is a paired
  comparison (same noise realisation at K=0 and K=256).
- all-flip mean field `kick_i = floor(K_int * F[t-1] / N)`, `F = popcount(f)`;
  synchronous ticks, every neuron reads flips of t-1.
- order parameter `theta_i = 2*pi*(t - t_last_i)/(t_last_i - t_prev_i)`; a
  neuron with `t - t_last > 3*period` or fewer than 2 carry times is excluded;
  R undefined if < N/2 remain; R averaged over the last 2048 of 4096 ticks.
- grid K_int = 0..256 step 8 (33 points), seeds {0,1,2,3,4}, N=256, T=4096.
- numpy only (2.4.3, `~/.venv-lm` python 3.12.3), thread caps set, no torch,
  no pip installs, no downloads, no GPU. Wall **76.8 s** for 495 runs (< 3 min).

## Evidence

Every number below is read back out of `c2_kidA_results.json` (495 rows).

### The four claim numbers, sigma_I=10, all-flip, N=256, seeds {0..4}

| CLAIM | threshold | measured | holds |
|---|---|---|---|
| `R(0)` (seed mean, K_int=0) | <= 0.125 | **0.0723** | yes |
| `K_c` 5-seed CV | <= 5% | **0.4327%** (K_c = **115.96**) | yes |
| sharpness `K_c/[K(0.75)-K(0.25)]` | >= 2 | **2.702** | yes |
| `R(192)` at mean spike rate <= 0.9 | >= 0.9 | **1.0000** at rate **0.6750** | yes |

Supporting numbers, same JSON:

- `Kc_per_seed = [116.427, 116.519, 115.916, 115.498, 115.449]`; K_c mean
  115.9617, std 0.5018, CV 0.004327.
- pooled curve: `K(0.25) = 95.208`, `K(0.75) = 138.119`, `K_c = 115.96`;
  per-seed sharpness mean 2.7002.
- `R_at_0_per_seed = [0.07312, 0.06882, 0.08417, 0.07192, 0.06371]`.
- `R_at_192_per_seed = [1.0, 1.0, 1.0, 1.0, 1.0]`; `spike_rate_at_192_mean =
  0.67503`; `spike_rate_at_0_mean = 0.20136`; `pop_period_at_192_median = 1.0`.
- `claim_sigma_I_10.all_conjuncts_hold = true` — every conjunct true in the
  JSON, not just in this prose.

### Information columns (not part of the claim)

- **K_c vs noise width:** sigma_I=5 -> K_c = 115.428 (CV 0.41%, R(0)=0.0826,
  R(192)=1.0); sigma_I=20 -> K_c = 119.404 (CV 1.85%, R(0)=0.0714,
  R(192)=0.9531). Ratio **K_c(20)/K_c(5) = 1.0344** — inside the pilot's
  <= 1.25 band, i.e. a fixed switch point (ignition by common drive), NOT the
  Kuramoto heterogeneity scaling that would give >= 2. The flip-coupled
  population's threshold is a byte constant.
- **R_m** = |mean e^{2 pi i m/256}| per row (byte-phase order parameter),
  carried in every row; not claimed.
- **population period** `pop_period` per row; median at K_int=192 is 1.0 tick
  (and 5.0 at K=0, where the drive sets the free-running period).
- **loadavg + MemAvailable beside every number:** all 495 rows carry
  `loadavg_1_5_15` and `MemAvailable_kB`, sampled in the loop. Box frame:
  start loadavg [2.93, 3.97, 3.30] / MemAvailable 16,153,172 kB; end
  [3.40, 3.88, 3.32] / 16,449,736 kB; nproc 4; wall_s_total 76.79.

### Cross-check against the pilot (context, NOT evidence)

Kid A's numbers land on the uncommitted pilot's: K_c 115.96 vs 115.5/117.1/116.2;
R(0) 0.0723 vs 0.077; sharpness 2.702 vs ~2.7; rate(192) 0.675 vs 0.666;
R(192) 1.000 vs 0.991; K_c(5/20) 115.4/119.4 vs 115/118. An independent
implementation reproducing the pilot is necessary, not sufficient — the pilot
is not evidence and this node does not cite it as such.

### Falsifier status

- R DOES cross 0.5 at K_int <= 256 outside the all-fire state (rate at K=192 is
  0.675 << 0.98; no row in the sweep is `degenerate: true` at the crossing) ->
  first falsifier NOT triggered.
- K_c CV 0.43% (<= 15%) and R(0) 0.0723 (<= 0.125) -> second falsifier NOT
  triggered; sharpness 2.702 (> 1) -> a switch, not a dimmer.
- This node speaks only to Kid A's conjunct; Kid B (ring wiring) and Kid C
  (gate latency/memory/ledger) carry their own verdicts. Round verdict is the
  parent's, not this node's.

### Files

- `.agi/context/local-maxxing/c2/c2_kidA_sweep.py` (runnable, `--sigmas`,
  `--seeds`, `--N`, `--T`, `--window`, `--out`)
- `.agi/context/local-maxxing/c2/c2_kidA_results.json` (495 rows + box frame +
  `claim_sigma_I_10` + `per_sigma` + `pooled_curve_sigma_I_10`)

### Weaknesses / caveats

- The pooled R(K) curve is NOT monotone (dips at K_int = 72/80/88 below the
  K_int=48 point), so `K_c` is the FIRST upward crossing; a different crossing
  convention would move K_c by one grid step.
- The per-(seed,sigma) reuse of one jitter matrix across all 33 K values makes
  the K sweep paired and is why the CV is so small (0.43%); an independent
  jitter draw per (seed,K) would report a larger CV. This is a deliberate
  variance-reduction choice, stated here so it is not mistaken for physical
  seed-stability of an unpaired experiment.
- `pop_period` at K=192 (median 1.0) is the ISI of a rate-0.675 population, not
  a clean period-3 clock; the pilot's `population period 3` was measured at
  K_int=176 with 4096 ticks, a different estimator.
- No engine code changed, so no engine test file covers this run; the check is
  the JSON round-trip (every number in this body re-read from the JSON).

## Agent Notes
Kid A decisive curve: N=256 all-flip, sigma_I=10, seeds {0..4}, 33 K_int x 4096 ticks, 495 runs, 76.8 s, numpy 2.4.3. R(0)=0.0723 (<=0.125), K_c=115.96 with 5-seed CV=0.43% (<=5%), sharpness K_c/[K(.75)-K(.25)]=2.702 (>=2), R(192)=1.0000 at mean spike rate 0.6750 (<=0.9); all four conjuncts true in c2_kidA_results.json (all_conjuncts_hold=true). Info columns: K_c(5)=115.43, K_c(20)=119.40, ratio 1.034 <= 1.25 -> fixed switch point (ignition), not Kuramoto heterogeneity scaling. No row degenerate (max rate 0.728). Independent of the pilot yet lands on it (K_c 115.5-117.1, R(0)=0.077, sharpness ~2.7). Caveat: one jitter realisation reused across K per (seed,sigma) makes the sweep paired and suppresses CV; pilot's unpaired seeds also give CV ~0.7%. Kid A's conjunct only; round verdict is the parent's.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review TM.02: verified from the BYTES (c2_kidA_sweep.py itself), not the kid report. Four negative probes, one per claim conjunct. (1) gate: K_int=0 gives R=0.0723, per-seed [0.0731,0.0688,0.0842,0.0719,0.0637] <= 0.125 -- HOLDS. (2) wire: the coupling term surgically neutralised in the KID OWN SOURCE (+ kick -> + kick*0) collapses R at K_int=128 from 0.6351 and at K_int=192 from 1.0000 to 0.0723, so the R movement is the coupling reaching the accumulator, not the sweep loop -- HOLDS. (3) sign: -kick at K_int=192 gives R=0.1201 (rate 0.0717), so inhibitory coupling does NOT lock and the excitatory sign is load-bearing -- the weak reading any-common-signal-locks is refuted. (4) cv: the kid flagged that one jitter matrix per (seed,sigma) reused across K pairs the sweep and suppresses the 5-seed Kc CV; the unpaired variant (independent jitter per (seed,K)) gives CV=0.4376% vs the kid 0.4327%, so the caveat does not move the number. All four probes hold; verdict proved stands. Caveat retained: Kc is the FIRST upward crossing on a non-monotone pooled curve.
<!-- THOUGHT:END -->
