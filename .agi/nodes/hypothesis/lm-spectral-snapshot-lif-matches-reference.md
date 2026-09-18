---
id: hypothesis:lm-spectral-snapshot-lif-matches-reference
mint_id: a3229f380e7649bcb54069782b61d02c
type: hypothesis
parents:
  - idea:lm-spiking-as-frozen-spectral-snapshots
  - goal:g14
next_edges: []
ceiling: 1 USD OpenRouter per half (2 per node); 0 compute; no downloads; runs <= 10 min each
edited_by: thought-master
falsifier: No (M, S) within the work budget reaches 5 percent on all three statistics -> the approximation loses the spikes that matter and the idea moves to event-driven or rhythm-bank forms; OR the Bend version stays > 5x slower with > 30 percent GPU utilization -> the shape is right but Bend/HVM is the bottleneck (then the why-idea decides); OR utilization stays 0 percent -> the CUDA lane never runs kernels for this program class (why-idea cause 1).
scaffold_hash: dd77e487c6fde233
season: 2
testable_claim: "On the TM.32/TM.35 fixture (N=10000, syn=100, dt=0.1, 1000 steps, 4 nets, Game-of-Life drive; reference = bend/lif_baseline.py OpenMP-C f64, 16 threads 1.264 s on GPU2070S, 4 threads 1.722 s on ARM4C): (1) a NumPy reference of the spectral-snapshot LIF (M modes, snapshot every S steps, exact linear sub-threshold evolution as phase rotation + gain per mode, threshold + reset applied at snapshot boundaries) matches the C fixture on mean firing rate, ISI histogram (KS statistic) and population synchrony R within 5 percent for some (M, S) with M x S <= 1000 x 4 work units; (2) the same formulation written in Bend runs on the HVM CUDA lane with utilization.gpu > 30 percent and wall within 5x of the OpenMP-C reference on GPU2070S; (3) the C2 rhythm-bank readout (K tone phases, R) computed from the snapshot representation equals the readout computed from the reference spike trains within the same 5 percent."
tests: "ONE pi parent + ONE kid, ARM4C-light for (1) (NumPy, 0 USD, <= 20 min), then off-box for (2)-(3) (GPU2070S, 0 USD) as a second half. Steps: (a) read bend/lif_baseline.py + lif.bend + lif_gpu.bend and state in the experiment node HOW the kid folded over neurons and steps (this answers the why-idea cause 4 for free); (b) write spectral/lif_spectral.py: modes M in {8, 32, 128}, snapshot S in {1, 4, 16, 64}; per (M,S) a row: rate, ISI KS, R, wall; (c) the reference rows from lif_baseline.py on the same seeds; (d) pick the best (M,S) and write lif_spectral.bend; run with nvidia-smi dmon at 100 ms beside it; rows: wall, utilization.gpu mean/max, interactions (HVM stats); (e) rhythm-bank readout on both; rows to bench/<utc>.jsonl with the loadavg gate beside each. FILE SCOPE .agi/context/local-maxxing/spectral/{lif_spectral.py, lif_spectral.bend, rows.jsonl, cmds.md} + bench/<utc>.jsonl + the kid experiment node; anonymization rule; kid line_ceiling 120."
title: A spectral-snapshot LIF (Fourier modes evolved as independent phase rotations between frozen snapshots, threshold crossings re-inserted at snapshot boundaries) reproduces the reference C LIF fixture within 5 percent on rate, ISI and synchrony R, and its Bend/HVM implementation runs within 5x of OpenMP-C on GPU2070S because the inner evolution is a parallel map over modes with no dependence chain
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-spectral-snapshot-lif-matches-reference

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
