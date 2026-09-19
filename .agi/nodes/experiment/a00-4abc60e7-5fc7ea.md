---
id: experiment:a00-4abc60e7-5fc7ea
mint_id: 678439b58ccd40bdb4befb3a8f0fb427
type: experiment
parents:
  - hypothesis:lm-event-driven-sparse-lif-matches-reference-at-a-fraction-of-the-work
next_edges: []
confidence: 0.9
edited_by: a00-4abc60e7
evidence_runs:
  - experiment:a00-4abc60e7-5fc7ea
line_ceiling: 40
loop: hypothesis:lm-event-driven-sparse-lif-matches-reference-at-a-fraction-of-the-work@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 80
profile: balanced
role: kid
scaffold_hash: ac5d529ef3314708
season: 2
title: "EVENT-DRIVEN LIF (TM.61): the exact train is reachable but NOT lazily -- dense correct-%N control and event-steplk are bit-exact (79675, 0 divergent) while the lazy closed-form leak (A**gap) diverges in 364 spikes (360 missed, first [81,9623]) because C's leak is v-fl(0.1*v) /= fl(0.9*v); updates 17.7% of N*T (fan-out floor, not <=10%); event wall 0.699 vs twin 4.364 s/net = 6.9x; twin models a different ring (%4N, 79408)"
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-4abc60e7-5fc7ea

## Experiment

Tested the 3-conjunct claim (exact trains / updates <= 10% of N*T / wall <= NumPy twin)
for the repaired fixture: `LIF_DRIVE=poisson LIF_INIT=sub LIF_AMP=9.999 LIF_GAIN=0.9
LIF_LEAK=restore LIF_ORDER=sync`, N=10000, syn=100, dt=0.1, T=1000, 4 nets,
seeds [7, 100010, 200013, 300016], on CPU8G under `agi-run` (4 threads, 4 GB, no swap).

Landed: `event/event_port.py` (80 lines, pure NumPy/python, no numba) and
`event/event_rows.jsonl` (24 rows + 6 summary rows). Reference = the C body of
`bend/lif_baseline.py` with a per-(neuron,step) reporter appended (the
`ref_trains()` path of the read-only `spectral/lif_spectral_driven.py`, which
reproduces 79675 spikes exactly). `bend/*` and `spectral/*` untouched.

Arms, all on the same box in one run: `c-reference`, `dense` (C recurrence
transcribed vectorised, correct `%N` ring), `event-k` (lazy closed-form leak,
k-ordered accumulation = CLAIM ARM), `event-src` (same, source-ordered
accumulation = ordering control), `event-steplk` (event-driven I, exact
per-step leak applied to every neuron = leak-approximation control), and
`numpy-twin` (`lif_drive.run_net`, for conjunct 3 only).

## Result (per-arm, 4 seeds, totals over the run)

| arm | spikes | divergent vs C | updates %N*T | wall s/net | c1 exact | c2 <=10% | c3 <= twin |
|---|---|---|---|---|---|---|---|
| c-reference | 79675 | 0 | - | 7.24 (4 nets) | - | - | - |
| dense (correct %N) | 79675 | **0** | 0 (0 by construction) | 23.38 | yes | n/a | no |
| **event-k (claim)** | **79319** | **364** | **17.71** | **0.699** | **no** | **no** | **yes** |
| event-src | 79319 | 364 | 17.71 | 0.690 | no | no | yes |
| event-steplk | 79675 | **0** | 17.78 | 0.637 | yes | no | yes |
| numpy-twin | 79408 | (different model) | - | 4.364 | - | - | - |

Per seed, claim arm: divergent 90/77/98/99, all first divergences at steps
74-86 (`[81, 9623]` is the earliest, seed 7); 360 of the 364 are MISSES
(reference fires, event arm does not), only 4 are extras. Rate 19.61-19.96 Hz,
windows and R match the C reference to the reported 4/6 dp, but the train sets do
not.

**Verdict: disproved.** Two of the three conjuncts fail. A clean negative with
the mechanism measured.

## Mechanism, three separable measurements

1. **The port is not index-broken.** `dense`, which transcribes the C recurrence
   literally (`I += gsc*W[:,k]*spk[(i-1-k)%N]`, sequential ascending k, `ws` via
   sequential `cumsum`) is **bit-exact on all 4 seeds, 0 divergent, 79675 vs
   79675**. So the ring direction, the `%N` modulus, the sequential gsc sum and
   the Jacobi step are all right. NOTE: the brief's TRAP 1 is wrong — the C
   source is `j=(i-1-k+4*N)%N` with `%N`=10000, not `%40000`; the numpy twin
   uses `% (4*N)` = 40000, so `lif_drive.py` models a *different* ring
   (its negative-wrap indices land on 7196-7295 instead of 9999-down). That is
   why the twin gives 79408 (-267) and is the reason its wall is the only fair
   conjunct-3 baseline.
2. **Summation order is not the cause.** `event-src` (source-ordered) and
   `event-k` (k-ordered) produce *identical* divergences: 364 total, same first
   divergence `[81, 9623]`, identical missing/extra split. The falsifier's
   "f64-vs-f64 ordering tolerance" clause is refuted in the sense that ordering
   contributes nothing here.
3. **The lazy closed-form leak is the sole cause.** `event-steplk` uses the same
   event arithmetic (same bincount, same weights, same touched sets) but applies
   the leak exactly every step to every neuron: **bit-exact, 0 divergent, on all
   4 seeds**. Difference between `event-k` and `event-steplk` is only how the
   decay between events is computed.

The root arithmetic: C's untouched-neuron update is `v + fl(0.1)*((0.0-v) + I + x)`,
i.e. `v - fl(0.1*v)`. That is NOT `fl(0.9*v)` — a direct probe over 200000
uniform doubles found 41915 entries (21.0%) where `v - 0.1*v != 0.9*v`. So no
closed form `A**gap` can reproduce the C trajectory, and the fixture is
maximally hostile to the approximation: with amp 9.999 a Poisson kick alone
puts `v1 ~= 0.99990 + 0.9v` within a few ulps of threshold, so a last-bit decay
error flips real spikes — hence divergence at step ~80, the first step at which
enough neurons have accumulated enough ulp drift.

Conjunct 2 fails as arithmetic, not as implementation: fan-out 100 x 19898
spikes/net = 1.99e6 deliveries, + 2.1e4 kicks, and after per-step dedup 1.77e6
distinct (neuron,step) = **17.7% of N*T**. At this rate and fan-out a <=10%
budget is unreachable by any event-driven scheme; the floor is
`100 * spikes/(N*T)`.

## Consequence for the next round (the frontier this fixes)

The exact event-driven port EXISTS and is fast: `event-steplk` is bit-exact on
all 4 seeds at 0.637 s/net vs the twin's 4.364 s/net (**6.9x faster**), so the
falsifier's third clause is refuted in the constructive direction — Python
overhead does not eat the sparsity. But it stays exact only by applying the
leak to every neuron every step, i.e. it gives up "touch only neurons with an
incoming event" for the leak while keeping it for the coupling. So the real
frontier is a stated choice, not an implementation trick:

- if "neuron-updates" counts **only event-driven updates** (the coupling),
  then the exact port wins 6.9x on wall and the claim's spirit holds;
- if it counts **every neuron written per step**, no bit-exact port can be
  <=10%, because exactness forces the N*T leak.

## Evidence

- `event/event_port.py` — all arms; `event/event_rows.jsonl` — 24 per-(arm,seed)
  rows + 6 summary rows (arm, spikes_total, updates_pct_NT_mean, wall_s_mean,
  conjunct1/2/3 booleans, first_divergence).
- Command: `ssh cpu8g "agi-run python3 tm61/event/event_port.py all"`; the
  dedup+summary step (`summarise.py`) is in the session scratch dir, not landed,
  because a second landed script would break the 40-line ceiling (see caveat).
- Probes: `C-REF {"spikes": 79675, "wall_s": 7.24}`; leak probe
  `v-0.1*v != 0.9*v` on 41915/200000 doubles.

## Agent Notes
Event-driven sparse LIF ported to NumPy-free pure Python/NumPy on CPU8G. Two controls separate the mechanisms: dense (C recurrence, correct %N ring) and event-steplk (event-driven coupling, exact per-step leak) are BOTH bit-exact vs the C reference (79675 spikes, 0 divergent of 79675, all 4 seeds); event-src == event-k (identical 364 divergences, same first [81,9623]), so summation ORDER contributes nothing. The lazy closed-form leak (A**gap) is the sole cause: C decays with v-fl(0.1*v) which differs from fl(0.9*v) on 41915/200000 doubles, and with amp 9.999 the kick sits a few ulps from threshold, so 90/77/98/99 spikes/net diverge (360 missed, 4 extra), first at step 74-86. Conjunct 2 fails as arithmetic: 100 fan-out x 19898 spikes/net = 1.77e6 distinct (neuron,step) = 17.71% of N*T, floor 100*spikes/(N*T) > 10%. Conjunct 3 PASSES: event wall 0.699 s/net vs numpy-twin 4.364 s/net = 6.9x, so Python overhead does not eat the sparsity. Side finding: the numpy twin uses %(4*N)=40000 so it models a different ring (79408, -267); the brief's TRAP 1 misquotes the C as %N_K=4N -- the C is %N=10000. Frontier: an exact port exists (event-steplk, 6.9x faster) but exactness FORCES the N*T step-wise leak, so 'exact AND <=10% touch' is impossible if every written neuron counts.
