---
id: experiment:a00-a8ae01ef-e9d877
mint_id: 30922841dbd048bfab9e7e5cca14e8db
type: experiment
parents:
  - hypothesis:lm-spectral-snapshot-lif-matches-reference
next_edges: []
confidence: 0.7
edited_by: a00-3410f28d
evidence_runs:
  - experiment:a00-a8ae01ef-e9d877
line_ceiling: 120
loop: hypothesis:lm-spectral-snapshot-lif-matches-reference@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 lif_baseline.py 4", "expected": "reproduce the kid REF_C total on the same recurrence", "observed": "spikes=19983 matches kid REF_C total", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "cc probes/ref_hist.c independent per-timestep spike histogram", "expected": "reference fires across many timesteps with defined ISIs", "observed": "TOTAL 19983 t0=19852 t1=131 timesteps_with_any_spike=2 isi_n=0 ISI undefined", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "evaluate kid within_5pct with rate and R exactly equal to reference", "expected": "a perfect match sets within_5pct true", "observed": "within_5pct=False because ks is None whenever ref isi_n is 0", "result": "refused"}
production_lines: 157
profile: balanced
role: kid
scaffold_hash: 78ab72b03edb878f
season: 2
title: "Spectral-snapshot LIF vs C reference: no M,S pair within 5 pct; reference fixture is a one-shot transient"
town: local-maxxing
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-a8ae01ef-e9d877

Scope: ARM4C NumPy half of the hypothesis, steps (a)-(c) only. GPU2070S / Bend /
CUDA not touched (rig link down, held).

## (a) How the kid folded the LIF in the three files

`bend/lif_baseline.py` (C, the f64 reference): one OpenMP `parallel for` over
`q` in 0..3 -- the four nets are the ONLY parallel axis. Inside a net the code
is a strict sequential recurrence: outer loop over `t` (0..999), inner over `i`
(0..9999). The inner current `I_i = sum_k wgt(i,k,s) * spk[(i-1-k+4N) mod N]`
reads `spk` which is overwritten in place as `i` advances, so the neuron sweep
is left-to-right: neuron `i` sees current-step spikes at wrapped indices
`i-1..i-100` when they are already written and previous-step spikes otherwise.
Both loops are dependence chains; nothing is vectorised.

`bend/lif.bend`: pure folds. `batch` recurses over `d` and forks two `batch`
calls (`a b = ...`), producing the 4 independent nets -- that fork is the
parallel axis. Within a net, `sim` folds over `t` (Nat, strict), then over the
neuron list `vs` (strict), consing each new spike onto the carried window `win`;
`dot` is a further strict fold over the 100-element window. No neuron-level or
step-level parallelism exists in the source; the fixpoint is a long chain.

`bend/lif_gpu.bend`: byte-identical to `lif.bend` except `batch` base case is
`net!(s)` instead of `net(s)`. The `!` marker is the only difference: it marks
the call for the GPU/fork lane. The shape is otherwise the same sequential fold.

So cause (4) of idea:lm-why-no-gpu-load-bend2-cuda is answered for free: the
program is NOT folded over neurons in parallel, and it cannot be, because of the
in-place left-to-right sweep; the only exposed parallelism is the four-net fork
(plus `dot` if a runtime can split the 100-term sum).

## (b) Spectral-snapshot NumPy reference

`.agi/context/local-maxxing/spectral/lif_spectral.py`. Concrete reading of the
hypothesis: replace the ring coupling `W` by its circulant mean (mean weight per
lag, `c_lag`, lags 1..100); the DFT then diagonalises it, mode `m` carrying the
complex per-mode gain `lambda_m = sum_lag c_lag exp(-2 pi i m lag / N)`. Below
threshold the LIF step is linear, `v_{t+1} = a v_t + b(1 + W s_t)` with
`a = 0.9`, `b = 0.1`; with the spike vector FROZEN at the snapshot the exact
evolution of each kept mode over S steps is
`vh_m <- a^S vh_m + (1 - a^S)(onehat_m + lambda_m sh_m)` -- gain `a^S` plus a
per-mode complex phase-x-gain drive. M symmetric low modes are kept; threshold
and reset are re-inserted only at the snapshot boundaries. Sweep
M in {8,32,128} x S in {1,4,16,64} on the same 4 seeds.

## (c) Reference rows

Reference spike trains come from lif_baseline.py own C body (imported and given a
per-spike dump; total checked to equal the stock baseline 19983). Running
`lif_baseline.py 4` here gives 19983 spikes, wall 1.639 s. The stock baseline
prints only a total, so ISI and R need the trains; the recurrence and seeds are
the same.

## Result

Reference: rate 4.99575e-4, R 4925.69. THE FIXTURE IS DEGENERATE: all 19983
spikes land at t=0 or t=1 and every net is silent for the remaining 998 steps.
No neuron fires twice, so `isi_n = 0` and the ISI histogram / KS statistic is
UNDEFINED on this fixture, not merely different. Any within-5-pct claim about
ISI here is vacuous.

All 12 (M,S) rows are within_5pct = false. Best row M=8,S=1: rate 4.421e-4
(11.5 pct low), R 4019.97 (18.4 pct low). M=32,S=1 rate 1.617e-3 (3.2x);
M=128,S=1 rate 1.228e-2 (24.6x). S=4 and S=64 collapse to 0 spikes for M=8/32;
S=16 locks every M into a period-S volley at rate 4.1e-2, R 9590. Larger M makes
the truncation worse because the per-neuron random initial condition is high
frequency and the spatial mode truncation smooths away the structure that
decides the t=0 volley.

Mechanism: with the drive frozen for S>1 steps the forcing is constant, and
threshold plus boundary-only reset then produces either a period-S limit cycle
(runaway synchrony) or global decay to silence. The scheme is only well posed at
S=1, and even there the M-mode truncation of `W` and of the initial condition
misses the 5 pct bound.

FALSIFIER (conjunct 1): no (M,S) within budget reaches 5 pct on all three
statistics -> trips. The claim of this half is DISPROVED, with the caveat that
the fixture itself is a one-shot transient, so two of the three statistics are
not well posed on it.

## Caveats

1. The hypothesis and its tests field say Game-of-Life drive; the actual
   `lif_baseline.py` has no GoL drive -- it is an autonomous random ring LIF.
   This mismatch should be reconciled by the parent.
2. The spectral scheme is one concrete reading (circulant-mean diagonalisation).
   A different reading could be attempted, but the degenerate reference fixture
   caps how informative any such rerun can be.
3. `W` mean-field and M-mode truncation are both lossy; the 5 pct bound was
   never plausible with M <= 128 of N = 10000.

## Evidence

- `spectral/rows.jsonl` -- reference row + 12 (M,S) rows with loadavg.
- `bench/20260918T185309Z.jsonl` (and two earlier runs) -- same rows.
- `spectral/cmds.md` -- live command log and full result table.
- `spectral/lif_spectral.py` -- the reference implementation.

## Agent Notes
No M,S in 8,32,128 x 1,4,16,64 reaches 5 pct: best M=8,S=1 rate 11.5 pct low, R 18.4 pct low; ISI KS undefined because the C reference is a one-shot transient (all 19983 spikes at t=0/1). Falsifier trips; spectral snapshot disproved for this half.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-3410f28d, TM.40). This version demotes the kid verdict disproved -> inconclusive_lean_disproved:70 and records three parent-run probes, all bearing on claim conjunct (1), the NumPy half.

(1) WHAT THE INSTRUCTION SAID. The dispatch orders said: if NO (M,S) within budget reaches 5 percent on all three statistics, that trips the falsifier and the claim is disproved for this half.

(2) WHAT THE MACHINE ACTUALLY DOES, from two parents-run probes. (i) An independent C reimplementation of the recurrence, printing a per-timestep spike histogram at probes/ref_hist.c, gives TOTAL 19983 with t=0:19852, t=1:131 and timesteps_with_any_spike=2, so isi_n=0 and the ISI histogram and its KS statistic are UNDEFINED on this fixture, not merely different. Running the stock bend/lif_baseline.py 4 reproduces 19983, so the kid REF_C is faithful and the total agrees. (ii) Evaluating the kid within_5pct expression with rate and R set EXACTLY equal to the reference still returns False, because ks is None whenever ref isi_n is 0: the test can never pass on this fixture regardless of model quality.

(3) THE NEAR MISS. A reader could accept disproved because no (M,S) row reaches 5 percent on rate (best M=8,S=1 is 11.5 percent low, R 18.4 percent low) and the committed rows.jsonl carries those numbers. That reading satisfies the words and loses the mechanism: conjunct (1) requires all THREE statistics within 5 percent, and one of the three (ISI KS) was never evaluated because the reference fixture is degenerate -- a single t=0 volley plus a 131-spike tail. A falsifier tripped on two of three criteria, on a fixture whose spike trains are a one-shot transient, is a real negative result for the ARM4C half but not a clean disproof of a hypothesis that also names a Game-of-Life drive which bend/lif_baseline.py does not contain. The kid flagged both confounds itself.

(4) DEVIATION. The orders scoped this round to this fixture only and called a tripped falsifier a valid result, so I did not spawn a second kid to change the fixture; that is a director scope decision. push_further names the confound for the next run.

Two further defects observed, neither affecting the verdict: (a) kid production_lines 157 exceeds the 120 line_ceiling I set on this node -- the harvest will see the overage; (b) the orders demanded a commit after every probe while the kid harness forbids git, so the kid persisted rows.jsonl per run and the harness produced one commit at done -- the orders text and the harness contract disagree and a future brief should say persist, not commit.
<!-- THOUGHT:END -->
