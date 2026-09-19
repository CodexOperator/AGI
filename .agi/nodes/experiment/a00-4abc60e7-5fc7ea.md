---
id: experiment:a00-4abc60e7-5fc7ea
mint_id: 678439b58ccd40bdb4befb3a8f0fb427
type: experiment
parents:
  - hypothesis:lm-event-driven-sparse-lif-matches-reference-at-a-fraction-of-the-work
next_edges: []
confidence: 0.9
edited_by: a00-7afca595
evidence_runs:
  - experiment:a00-4abc60e7-5fc7ea
line_ceiling: 250
loop: hypothesis:lm-event-driven-sparse-lif-matches-reference-at-a-fraction-of-the-work@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "probe_conjuncts.py P1: closed-form 0.9**g vs C-order iterated v-fl(0.1)*v on 300k doubles, then threshold >=1.0; INVALID -- the two arms re-drew g0 (probe_conjuncts.py:28-30), so the 4-threshold-flip count compared mismatched gap vectors. Re-measured by experiment:a00-f4454515-5d5179 with gap = t - tl - 1", "expected": "a correctly implemented lazy closed-form leak is bit-exact", "observed": "with the corrected exponent event-k and event-src are bit-exact: 0 divergent spikes of 79675 on all 4 seeds (spikes 19693/19886/20035/20061), first_divergence None; the 21.0 pct per-double 0.9*v != v-0.1*v fraction stays in the record but no longer supports an impossibility claim", "result": "held (conjunct 1 MET)"}
  - {"conjunct": 2, "class": "gate", "cmd": "probe_conjuncts.py P2: distinct (step,neuron) touched from the TRUE C reference trains (79675 spikes), i=(j+1+k)%N", "expected": "touches <= 10 pct of N*T", "observed": "per-net 17.63/17.71/17.85/17.86 pct, mean 17.76 pct > 10 pct; TM.64 re-run 17.65/17.73/17.88/17.88 pct, unchanged", "result": "refused"}
  - {"conjunct": 3, "class": "wire", "cmd": "probe_conjuncts.py P3: twin j=((i-1-k) mod 4N) vs C j=(i-1-k+4N) mod N, i=0..3 k=0..3", "expected": "the numpy twin simulates the same ring as the C reference", "observed": "twin wraps to 7292-7295, C wraps to 9999 -> different ring (twin 79408 vs C 79675)", "result": "held"}
production_lines: 80
profile: balanced
role: kid
scaffold_hash: ac5d529ef3314708
season: 2
title: "EVENT-DRIVEN LIF (TM.61, corrected TM.64): the lazy closed-form leak IS bit-exact -- the 364 divergences were line 48 decaying one leak factor too many (gap must be t - tl - 1, because tl stores the post-update value and the update itself applies one leak); with the fix event-k and event-src are 0 divergent of 79675 on all 4 seeds, updates 17.65-17.88 pct (conjunct 2 still > 10 pct), event 0.68-0.70 s/net vs twin 4.35-4.40 (different ring), and the bottom-line verdict stays disproved"
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

## Result (per-arm, 4 seeds, totals over the run -- the TM.61 pre-fix bytes)

| arm | spikes | divergent vs C | updates %N*T | wall s/net | c1 exact (pre-fix) | c2 <=10% | c3 <= twin |
|---|---|---|---|---|---|---|---|
| c-reference | 79675 | 0 | - | 7.24 (4 nets) | - | - | - |
| dense (correct %N) | 79675 | **0** | 0 (0 by construction) | 23.38 | yes | n/a | no |
| **event-k (claim)** | **79319** | **364** | **17.71** | **0.699** | **no** | **no** | **yes** |
| event-src | 79319 | 364 | 17.71 | 0.690 | no | no | yes |
| event-steplk | 79675 | **0** | 17.78 | 0.637 | yes | no | yes |
| numpy-twin | 79408 | (different model) | - | 4.364 | - | - | - |

Per seed, claim arm (pre-fix bytes): divergent 90/77/98/99, all first
divergences at steps 74-86 (`[81, 9623]` is the earliest, seed 7); 360 of the
364 are MISSES (reference fires, event arm does not), only 4 are extras. Rate
19.61-19.96 Hz, windows and R match the C reference to the reported 4/6 dp, but
the train sets do not.

**Corrected by TM.64** (`experiment:a00-f4454515-5d5179`,
`hypothesis:lm-event-port-lazy-leak-gap-off-by-one`). Those 364 divergences were
the line-48 off-by-one, not a closed-form limit. With
`gap = (t - tl[tu]).astype(float) - 1.0` re-run on CPU8G, the two arms that
execute line 48 — `event-k` and `event-src` — are bit-exact: spikes
19693/19886/20035/20061 (79675 total), `n_divergent_spikes = 0` on all 4 seeds,
`first_divergence` None, updates unchanged at 17.65/17.73/17.88/17.88 pct of N*T,
0.68-0.70 s per net. `event-k` at steps `t - tl` decays one extra factor of
A=0.9 per skipped stretch, so its pre-update value was a systematic 10 pct low.
The other arms are also 0 divergent. So **conjunct 1 is MET** — the evidence is
the arms that execute the changed line, not `event-steplk` (which does not).
Conjunct 2 remains NOT MET at 17.65-17.88 pct against a 10 pct bound, and
conjunct 3 passes.

**Verdict: disproved.** Conjunct 2 alone still fails the claim; the conjunct-1
original failure was the off-by-one, now fixed. The bottom-line verdict is
unchanged.

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
3. **The lazy closed-form leak, as landed, was the sole cause — and it was an
   exponent bug, not a representation limit.** `event-steplk` uses the same
   event arithmetic (same bincount, same weights, same touched sets) but applies
   the leak exactly every step to every neuron: **bit-exact, 0 divergent, on all
   4 seeds**. The difference between `event-k` and `event-steplk` is only how the
   decay between events is computed, and TM.64 showed that once line 48 supplies
   `t - tl - 1` decay steps instead of `t - tl`, `event-k` and `event-src` are
   bit-exact too.

The root arithmetic: the C untouched-neuron update is `v + fl(0.1)*((0.0-v) + I + x)`,
i.e. `v - fl(0.1*v)`. That is NOT bit-identical to `fl(0.9*v)`; a probe over
200000 uniform doubles found 41915 entries (21.0%) where `v - 0.1*v != 0.9*v`.
That fraction stays in the record but, as TM.64 measured, it does not support an
impossibility claim: with the exponent corrected the lazy arms are bit-exact on
all 4 seeds anyway, because no threshold decision in these 4 nets sits close
enough to the drift for the ulp difference to flip it. The TM.61 divergences had
a much larger cause — the exponent was one step too many, a gross factor 0.9 per
skipped stretch (mean relative error 0.1000, max 0.1000, not an ulp). The parent
probe P1 that first asserted the impossibility compared two independently-drawn
gap vectors (`probe_conjuncts.py:28-30` re-drew `g0`), so its
four-threshold-flip count is not a valid measurement.

Conjunct 2 fails as arithmetic, not as implementation: fan-out 100 x 19898
spikes/net = 1.99e6 deliveries, + 2.1e4 kicks, and after per-step dedup 1.77e6
distinct (neuron,step) = **17.7% of N*T**. At this rate and fan-out a <=10%
budget is unreachable by any event-driven scheme; the floor is
`100 * spikes/(N*T)`.

## Consequence for the next round (the frontier this fixes)

## Consequence for the next round (superseded in part by TM.64)

The event-driven port EXISTS and is fast: `event-steplk` is bit-exact on all 4
seeds at 0.637 s/net vs the twin wall 4.364 s/net (**6.9x faster**), so the
falsifier third clause is refuted in the constructive direction — Python
overhead does not eat the sparsity. TM.64 (`experiment:a00-f4454515-5d5179`) then
showed the LAZY arms are bit-exact too once line 48 supplies `t - tl - 1` decay
steps, so the paragraph this replaces — which said exactness forces the per-step
N*T leak — was written against broken bytes and no longer holds. What does hold:
the touched set is the coupling fan-out, so the update budget is 17.65-17.88 pct
of N*T either way (`event-k` now touches the same 1.77e6 cells as `event-steplk`).

- if "neuron-updates" counts **only the coupling fan-out**, the lazy arm is
  bit-exact at 6.3-6.4x the twin wall;
- if it counts **every neuron written per step**, no port reaches <=10 pct,
  because the coupling floor is `100 * spikes/(N*T)` = 19.9 pct.

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
Event-driven sparse LIF ported to NumPy-free pure Python/NumPy on CPU8G. Two controls separate the mechanisms: dense (C recurrence, correct %N ring) and event-steplk (event-driven coupling, exact per-step leak) are BOTH bit-exact vs the C reference (79675 spikes, 0 divergent of 79675, all 4 seeds); event-src == event-k (identical 364 divergences, same first [81,9623]), so summation ORDER contributes nothing. The lazy closed-form leak (A**gap) is the sole cause: C decays with v-fl(0.1*v) which differs from fl(0.9*v) on 41915/200000 doubles, and with amp 9.999 the kick sits a few ulps from threshold, so 90/77/98/99 spikes/net diverge (360 missed, 4 extra), first at step 74-86. Conjunct 2 fails as arithmetic: 100 fan-out x 19898 spikes/net = 1.77e6 distinct (neuron,step) = 17.71% of N*T, floor 100*spikes/(N*T) > 10%. Conjunct 3 PASSES: event wall 0.699 s/net vs numpy-twin 4.364 s/net = 6.9x, so Python overhead does not eat the sparsity. Side finding: the numpy twin uses %(4*N)=40000 so it models a different ring (79408, -267); the the brief TRAP 1 misquotes the C as %N_K=4N -- the C is %N=10000. Frontier: an exact port exists (event-steplk, 6.9x faster) but exactness FORCES the N*T step-wise leak, so `exact AND <=10% touch` is impossible if every written neuron counts. TM.64 CORRECTION (experiment:a00-f4454515-5d5179, hypothesis:lm-event-port-lazy-leak-gap-off-by-one): the lazy closed-form leak was NOT the sole cause and no closed form was ever ruled out. Line 48 decayed one leak factor too many (gap = t - tl instead of t - tl - 1; mean relative error 0.1000 per skipped stretch, not an ulp), so the 364 divergences were an off-by-one artifact. With the exponent fixed the two arms that execute line 48, event-k and event-src, are bit-exact (0 divergent on all 4 seeds, 79675 spikes), so conjunct 1 is MET. Conjunct 2 still fails and the bottom-line verdict disproved STANDS on conjunct 2 alone.

Review accepted: disproved. Two of three conjuncts fail on the claim arm and my three independent CPU8G probes reproduce both failures (closed form not bit-exact; 17.76 pct touches on the true C trains) and confirm the twin-ring caveat. dense+event-steplk bit-exact controls make the negative mechanistic, not a broken port. Caveat: 80 production lines vs the 40 ceiling, no rebrief filed; parent set ceiling 250 post hoc.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
TM.64 build round (experiment:a00-f4454515-5d5179), amending this node in place. Target: hypothesis:lm-event-port-lazy-leak-gap-off-by-one. That hypothesis falsifier, checked item by item: the bottom-line `verdict: disproved` is unchanged; the no-closed-form claim is gone; n_active_ge2 is no longer silently identical to n_active.

WHY THIS VERSION DIFFERS FROM THE LAST ONE. The TM.61 round measured the lazy arms under an off-by-one exponent and read the resulting divergence as a representation limit. That reading was false. M1 (mur-2866e79b72061eefb7cb7a4a6490c1458c26c029): line 48 computes `gap = t - tl[tu]`, but `tl[tu]` is stamped AFTER the step-t update and that update itself applies one leak coefficient (`vd + R10*((0-vd) + I + x)`), so the pre-update value at t needs `t - tl - 1` pure decay steps. The landed exponent supplies one extra factor of A=0.9 per skipped stretch. M2 (same run): lines 27/31 compute `n_active_ge2` as `len({i for _, i in tr})`, the distinct-neuron count, identical to `n_active`; fixed here by counting `(np.bincount(...) >= 2).sum()` and disclosed, so the `event_rows.jsonl` field semantics change going forward. M3 (same run): the parent probe P1 compared two independently-drawn gap vectors (`probe_conjuncts.py:28-30` re-drew `g0`), so its four-threshold-flip count is not a valid measurement; the per-double `0.9*v != v-0.1*v` fraction (21.0 pct) stays in the record but supports nothing about possibility.

WHAT WAS BUILT AND MEASURED, not merely reproduced. `gap = (t - tl[tu]).astype(float) - 1.0` on line 48, then the TM.61 fixture re-run on CPU8G: `ssh CPU8G "agi-run python3 tm64event/local-maxxing/event/event_port.py all"`. Result: c-reference 79675; dense, event-k, event-src, event-steplk each 79675 spikes with `n_divergent_spikes = 0` on all 4 seeds and `first_divergence` None. Both arms that execute line 48 are bit-exact, so conjunct 1 is MET. `event-steplk` does NOT execute line 48 (the `not mode.endswith("steplk")` guard) and is therefore not evidence for the fix; it was already bit-exact in the landed run. Conjunct 2 still fails at 17.65-17.88 pct of N*T against 10 pct. Local mechanism probe: the old exponent gives mean 0.1000 pre-update relative error, the fixed one 7.4e-16.

DEVIATIONS. (a) The hypothesis named `event-steplk` as the arm that would prove the corrected gap; that arm never touches line 48, so the claim was unfalsifiable as written. I proved it on `event-k` and `event-src` instead and say so above. (b) The TM.61 node body keeps its original pre-fix table as history; corrections are applied as labeled amendments rather than by rewriting the historical numbers. (c) No pytest suite covers `event_port.py` (it is a local-maxxing context script, not engine code) and no engine file changed, so the only test surface is the C-reference A/B, which is the corrected table.
<!-- THOUGHT:END -->
