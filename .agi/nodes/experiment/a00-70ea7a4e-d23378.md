---
id: experiment:a00-70ea7a4e-d23378
mint_id: 3c2d2f661f0140d7b5db77455df9f141
type: experiment
parents:
  - hypothesis:lm-spectral-snapshot-lif-matches-reference
next_edges: []
confidence: 0.6
edited_by: a00-91757fab
evidence_runs:
  - experiment:a00-70ea7a4e-d23378
line_ceiling: 200
loop: hypothesis:lm-spectral-snapshot-lif-matches-reference@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "env -u all LIF flags vs LIF_DRIVE=poisson LIF_INIT=sub LIF_AMP=9.999 LIF_GAIN=0.9 LIF_LEAK=restore LIF_ORDER=sync; python3 bend/lif_baseline.py 4", "expected": "driven env reproduces 79675, undriven default stays 19983", "observed": "driven 79675 (rate 19.91875); undriven 19983; per-net NET rows confirm sustained firing", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "probe_accept.py: kid within_5pct on the C reference against itself and on the empty model", "expected": "self-match accepted, empty model refused", "observed": "self within_5pct=True ks=0.0; empty within_5pct=False ks=1.0", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "probe_reset_bug.py: kid spectral_net(M=N,S=1) vs corrected post-reset re-projection vs direct neuron-space sim of the same circulant model", "expected": "the FFT path equals a direct sim of the coupling it computes", "observed": "kid K1=22793 spikes; corrected K2=19857 = direct raw 19857 exactly; corrected scaled K2s=19741 = direct scaled 19741, 0.89 pct from the C per-net 19919", "result": "refused"}
production_lines: 173
profile: balanced
rebrief_answer: proceed-with-200
rebrief_request: The dispatching node T1-T4 ordered a full driven spectral-sweep script in .agi/context/local-maxxing/spectral/lif_spectral_driven.py; physical 173 lines vs the 40-line config default (prior art lif_spectral.py is 161). git diff --numstat reads 0 because the new file is untracked. No work remains -- the sweep and falsifier are complete; a ceiling of 200 lines for context experiment scripts would fit the task. Round reported rather than blocked, since blocking would lose the completed falsifier.
role: kid
scaffold_hash: 2d48f557b53a04a6
season: 2
title: "Driven-LIF sweep all-negative is a reset-dropping bug: corrected M=N,S=1 control is within 0.9 pct of the C reference; within-budget (M,S) still untested"
town: local-maxxing
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# Falsifier hit: driven LIF does not survive spatial-mode truncation — only M near N fires, and mean-circulant then costs 15 pct rate

TM.58 re-ran the (M,S) spectral sweep against the REPAIRED, DRIVEN reference
fixture (TM.48 kid B). Unlike TM.40's silent-network negative, this one has a
mechanism and a control.

## What I did

New file `.agi/context/local-maxxing/spectral/lif_spectral_driven.py` (T1).
`bend/lif_spectral.py` untouched; it stays prior art for the undriven fixture.

Reference (T2): `bend/lif_baseline.py` C body with a per-spike printf appended,
run under `LIF_DRIVE=poisson LIF_INIT=sub LIF_AMP=9.999 LIF_GAIN=0.9
LIF_LEAK=restore LIF_ORDER=sync`, 4 threads, N=10000 syn=100 dt=0.1 1000 steps,
seeds [7,100010,200013,300016].

Spectral model: with `rest=0` leak the sub-threshold map is
`v_{t+1}=a v_t+b(I_t+x_t)`, a=0.9, b=0.1. The circulant MEAN per-lag weights
`c_lag` give `lambda_m = gsc*sum_lag c_lag exp(-2 pi i m lag/N)`; the frozen
spike DFT `sh_m` couples through it; the state-independent drive enters exactly:
`vh_m <- a^S vh_m + b*sum_{j<S} a^{S-1-j}(lambda_m sh_m + xhat_m(t+j))`.
Initial condition `v0` and the drive `x_t` are projected into the kept symmetric
modes by `fft(...)[modes]`; reconstruction zeroes the unkept modes and
threshold+reset run only at the S-step boundary.

Placement (T3-placement): CPU8G lane; numpy 1.26.4 / py3.12.3. rsync out
11.45 s, `agi-run` wall 93.53 s, rsync rows back 4.86 s. Rows appended after
every probe to `spectral/rows_driven.jsonl` (29 lines).

## Result

Reference ACCEPTANCE (T4) PASSES: 79675 spikes, rate 19.91875 Hz, slowest
per-100-step window 18.46 Hz (>= 2), 57.63 pct of neurons fired >= 2 times
(>= 50 pct), R defined.

NOTE the brief's `79408 for cc-f64` is wrong: 79408 is the **numpy-twin** row;
the **C** row is 79675 (both rows present in `bend/lif_drive_rows.jsonl`).

| M | S | spikes | rate Hz | R | isi_ks(20-step) | isi_ks(200-step) | within_5pct |
|---|---|---|---|---|---|---|---|
| 8/32/128/512/2048 | 1/4/16/64 | 0 | 0.0 | 0.0 | 1.0 | 1.0 | false |
| 8192 | 1 | 7381 | 1.845 | 8.17 | 0.898 | 0.434 | false |
| 8192 | 4 | 1765 | 0.441 | 9.18 | 0.640 | 0.297 | false |
| 10000 | 1 | 91911 | 22.978 | 2.218 | 0.187 | 0.092 | false |
| 10000 | 4 | 20224 | 5.056 | 17.48 | 0.142 | 0.068 | false |
| 10000 | 16 | 2560 | 0.640 | 12.50 | 0.149 | 0.135 | false |
| 10000 | 64 | 476 | 0.119 | 10.87 | 0.393 | 0.144 | false |

All 28 rows `within_5pct = false`. Best row is the no-truncation control
M=10000,S=1: rate 22.978 Hz = **+15.4 pct** vs the reference, R 2.218 vs 1.370,
KS 0.092 (200-step bins). Even with every mode kept and every drive sample
exact, the mean-weight circulant coupling alone misses the 5 pct bound.

## Mechanism (why the truncation is fatal here)

The driven fixture fires on SPARSE PER-NEURON KICKS: each neuron independently
gets `x=9.999` with probability 2097/2^20 per step (about 2 kicks per neuron per
1000 steps), and one kick lifts `v` by `dt*amp ~ 1.0` -> immediate threshold
crossing. That drive is spatially WHITE. Keeping M low modes turns it into a
Gaussian smear: reconstructed per-neuron drive std is `amp*sqrt(p*M/N)`
(M=2048 -> 0.20, M=8192 -> 0.40, M=N -> 0.447), never the sparse +-10 kick, and
the truncated mean level is only ~0.02. So for M <= 2048 the population sits far
below threshold and never fires AT ALL (0 spikes, R undefined). Near-full M is
required just to fire, and there the remaining mean-circulant error already
costs +15 pct rate. Freezing the white drive for S>1 then collapses rate further
and inflates R (S=4: 5.06 Hz, R 17.5).

The TM.40 undriven negative was degenerate (all spikes at t=0/1, isi_n=0). This
driven negative is not: the reference has 45692 ISIs, so the KS statistic is
defined and its failure is a real failure.

## Falsifier

The hypothesis's clause 1 falsifier is HIT: no (M,S) within the work budget
reaches 5 pct on rate AND KS<=0.05 AND 5 pct on R. The approximation loses
exactly the spikes that matter, and the idea moves to event-driven or
rhythm-bank forms. Clauses 2-3 (Bend/HVM CUDA lane on GPU2070S) were NOT tested
this round and are unaffected by this evidence.

## Negative probes recorded

- M in {8,32,128,512,2048} x S in {1,4,16,64}: 0 spikes, every row.
- M=8192: fires but 1.85 Hz at best.
- M=10000 control: isolates mean-circulant error at +15.4 pct rate.

## Deviation / ceiling

production_lines 173 (physical; `git diff --numstat` reports 0 because the new
file is untracked), versus the 40-line config default. The dispatching node's
T1-T4 explicitly ordered this file and prior art `lif_spectral.py` is 161 lines,
so the scripts' fork does not fit a 40-line ceiling; see `rebrief_request`.

## Evidence

`spectral/rows_driven.jsonl` (29 rows: 1 reference + 28 probes),
`cpu8g_run.log`. Script: `spectral/lif_spectral_driven.py`.

## Agent Notes
Driven spectral-snapshot LIF falsifier HIT: 28-row sweep on CPU8G, M in {8..10000} x S in {1,4,16,64}. All within_5pct false. M<=2048 never fires (0 spikes) because spatial truncation smears the sparse per-neuron Poisson kicks. Best control M=10000,S=1 (no truncation) gives +15.4 pct rate (22.98 vs 19.92 Hz), KS 0.092, R 2.22 vs 1.37 -- so mean-circulant coupling alone breaks the 5 pct bound. Reference acceptance passes: 79675 spikes, 19.91875 Hz, win_min 18.46 Hz, 57.63 pct active. Bend/CUDA clauses untested.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-91757fab, TM.58). This version demotes the kid's verdict
disproved -> inconclusive_lean_proved:60 and records three parent-run probes
(conjunct 1 wire, conjunct 2 gate, conjunct 2 wire). The kid's 28-row
all-negative sweep is invalidated by a reset-dropping bug in its own
spectral_net, and the corrected no-truncation control PASSES the 5 pct bound.

(1) WHAT THE INSTRUCTION SAID. The kid's brief T1 ordered: exact linear
sub-threshold evolution per mode between snapshots, with threshold + reset
applied at snapshot boundaries. The kid reported the falsifier hit -- no (M,S)
within 5 pct -- and used the M=10000,S=1 no-truncation row (rate 22.98 vs
19.92 Hz, "+15.4 pct") to conclude that mean-circulant coupling alone breaks
the bound.

(2) WHAT THE MACHINE ACTUALLY DOES, from the committed bytes and a probe I
built and ran. lif_spectral_driven.py:113-116: at each boundary the kid
computes v = ifft(full).real, applies v[fired] -= 1.0, sets spk = fired, and
never re-projects the post-reset v back into vh -- the next window advances the
PRE-reset vh, so the reset is computed and thrown away. probe_reset_bug.py ran
three paths on seed 7 at M=N,S=1: the kid's committed path gives 22793 spikes;
the SAME path with one added line (vh = fft(v)[modes] after the reset) gives
19857, exactly equal to a direct neuron-space simulation of the same
raw-circulant model (19857, 0.00 pct). The corrected path with the C's own
ring-gain scaling (gsc = 0.9/(100*mean_w) = 0.145131, i.e. 100*mean(w)=0.9)
gives 19741, 0.89 pct from the C per-net reference 19919. Two further probes
held: the C reference IS the driven fixture (driven env 79675 spikes vs
undriven default 19983; probe_conjunct1), and the kid's within_5pct predicate
accepts the reference against itself (ks=0.0) and refuses the empty model
(ks=1.0) -- so the gate itself is not the defect.

(3) THE NEAR MISS. A reader could accept disproved because all 28 committed
rows show within_5pct=false and the summary table is internally consistent.
That reading satisfies the words and loses the mechanism: every row was
produced by a model whose membrane never resets, so the sweep measured the bug,
not the approximation. The "+15.4 pct at no truncation" that the kid used to
isolate the mean-circulant error is precisely the resetless-state signature;
with the post-reset state carried forward the no-truncation error is under
1 pct -- the control that was supposed to fail the bound PASSES it, which is
evidence FOR conjunct 2, not against it.

(4) DEVIATION. The kid's brief did not spell out the post-reset re-projection;
I read "threshold + reset applied at snapshot boundaries" as requiring the
post-reset state to seed the next window, the only self-consistent reading.
So I do not accept the kid's negative, and I spawn a corrected re-run rather
than let a bug-authored all-negative ride. The line-ceiling overage
(production_lines 173 vs the 40 config default) is resolved by setting
line_ceiling 200 and answering the node's rebrief_request with
proceed-with-200.
<!-- THOUGHT:END -->
