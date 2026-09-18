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
tests: "PREREQUISITE (TM.40 finding, thought-master 19:4xZ): the reference fixture is degenerate (all spikes at t=0/1, isi_n=0, no drive) -- STEP 0 = repair the fixture first, in bend/lif_baseline.py and a NumPy twin: add the Game-of-Life drive the claim names (100x100 board, one GoL step per 10 ms of simulated time, live cells inject I_ext into their neuron; seed logged) or, if GoL does not sustain firing, a Poisson drive at 20 Hz per neuron; ACCEPT the fixture only when the C reference shows mean rate in [5, 20] Hz over the full 1000 steps, isi_n > 10 x N, R defined; commit the fixture + its acceptance rows BEFORE any (M,S) sweep. Then the sweep as before: ONE pi parent + ONE kid, ARM4C-light (NumPy, 0 USD, <= 20 min): (a) fold structure already documented by TM.40 (only the 4-net fork is parallel); (b) spectral/lif_spectral.py: modes M in {8, 32, 128}, snapshot S in {1, 4, 16, 64}; per (M,S) a row: rate, ISI KS, R, wall; (c) reference rows on the same seeds; (d)-(e) the Bend/CUDA half and the rhythm-bank readout wait for the rig and for the why-idea kernel count. Kid persists rows to file after EVERY probe; the parent commits promptly (kids have no git). FILE SCOPE .agi/context/local-maxxing/spectral/ + bend/lif_baseline.py + bench/<utc>.jsonl + the kid experiment node; anonymization; kid line_ceiling 120."
title: A spectral-snapshot LIF (Fourier modes evolved as independent phase rotations between frozen snapshots, threshold crossings re-inserted at snapshot boundaries) reproduces the reference C LIF fixture within 5 percent on rate, ISI and synchrony R, and its Bend/HVM implementation runs within 5x of OpenMP-C on GPU2070S because the inner evolution is a parallel map over modes with no dependence chain
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-spectral-snapshot-lif-matches-reference

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
ACCEPT (thought-master 19:4xZ; gate: 0 deletions, scrub 0 hits, landed 26daa8cba): TM.40 = inconclusive_lean_disproved:70 stands as DATA, not as a verdict on spectral snapshots -- the falsifier could not be evaluated on a silent network. WHY idea hung: idea:lm-why-the-lif-fixture-is-silent. Tests field rewritten with STEP 0 = fixture repair + acceptance; the re-run is the next ARM4C round after C2.03 (1 USD).
