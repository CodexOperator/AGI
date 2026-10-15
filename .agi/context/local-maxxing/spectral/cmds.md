# spectral half — ARM4C, steps (a)-(c) — live command log

Host aliases only: ARM4C (this box), GPU2070S (off-box, not touched).

## (a) read the three files

    read .agi/context/local-maxxing/bend/lif_baseline.py   (C source in a py wrapper)
    read .agi/context/local-maxxing/bend/lif.bend
    read .agi/context/local-maxxing/bend/lif_gpu.bend

FOLDING (recorded in the experiment node):
- lif_baseline.py: OpenMP `#pragma omp parallel for` over the 4 nets (q).
  Per net: sequential recurrences — outer over t=0..999, inner over i=0..9999.
  Inner I_i = sum_k wgt(i,k,s)*spk[(i-1-k+4N)%N] with spk updated IN PLACE, so
  the neuron sweep is left-to-right: neuron i sees current-step spikes for
  i-100..i-1 and previous-step spikes for the wrapped indices. Sequential over
  neurons AND steps; the only parallel axis is the q=4 net fork.
- lif.bend: functional folds. `batch` recurses over d and forks two `batch`
  calls (a b = ...), giving 4 independent nets — the parallel axis. Within a
  net `sim` folds over t (Nat, strict), then over the neuron list vs (strict),
  consing spikes onto win; `dot` is a strict fold over the 100-element window.
  No neuron-level or step-level parallelism; the recursion is a dependence chain.
- lif_gpu.bend: byte-identical to lif.bend except `batch`'s base case is
  `net!(s)` instead of `net(s)`. The `!` is the only difference: it marks the
  call for the CUDA/fork lane. Same sequential shape otherwise.

## (b)+(c) build and run

    python3 .agi/context/local-maxxing/bend/lif_baseline.py 4      # ground truth spikes
    python3 .agi/context/local-maxxing/spectral/lif_spectral.py    # ref trains + MxS sweep

Sweep: M in {8,32,128} x S in {1,4,16,64}, nets 4, seeds [7,100010,200013,300016],
N=10000, syn=100, dt=0.1, steps=1000.

Reference spike trains: the C body of lif_baseline.py is reused verbatim, with a
per-spike printf appended, so total spike count is checked against the stock
baseline (19983). The stock baseline prints only a total, so ISI KS and R need
the trains; the trajectories are the same C recurrence on the same seeds.

Command outputs and row values follow in the experiment node.

## RESULT

Reference (C/f64, 4 threads, rerun on this fixture instance): 19983 spikes,
wall 1.58-1.86 s, rate 4.99575e-4, R 4925.69. BUT the spike trains show the
fixture is a ONE-SHOT TRANSIENT: all 19983 spikes land at t=0 (4996/4949/4973/
4934 per net) or t=1 (31/33/38/29 per net), then every net is silent for the
remaining 998 steps. No neuron fires twice -> isi_n = 0 -> the ISI histogram
(and therefore the KS statistic) is UNDEFINED on this fixture, not merely
different. The reference R = 4925 is dominated by that single t=0 volley.

Sweep, 12 (M,S) rows, all within_5pct = false:
  M=8,  S=1  rate 4.421e-4 (11.5 pct low), R 4019.97 (18.4 pct low)
  M=32, S=1  rate 1.617e-3  (3.2x high),   R 3926.9
  M=128,S=1  rate 1.228e-2  (24.6x high),  R 3156.1
  M=8/32, S=4  0 spikes (population falls silent)
  M=128,  S=4  rate 4.237e-2 (84.8x high)
  all M,  S=16 rate 4.100e-2 (82.1x high), R 9590 -- a period-S lockstep volley
  M=8/32, S=64 0 spikes;  M=128, S=64 0 spikes
No (M,S) reaches 5 pct on rate+R (ISI is undefined). Biologically the best row
is M=8,S=1 (rate 11.5 pct low); larger M makes the truncation worse, not better,
because the initial condition is random per neuron and spatial mode truncation
smooths away exactly the high-frequency structure that decides the t=0 volley.

Mechanism: freezing the drive over S>1 steps gives constant forcing; threshold
plus reset only at boundaries then creates a period-S limit cycle (runaway
synchrony at S=16) or, for the low-M rows, decays the whole population below
threshold (silence at S=4/64).

Files written: spectral/rows.jsonl, bench/20260918T184733Z.jsonl,
bench/20260918T185103Z.jsonl, bench/20260918T185309Z.jsonl.
