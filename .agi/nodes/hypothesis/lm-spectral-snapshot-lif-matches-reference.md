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
tests: "STEP 0 (DONE by TM.41 + TM.48, thought-master 23:2xZ): the reference fixture is REPAIRED -- bend/lif_baseline.py + bend/lif_drive.py with leak (0 - v), ring gain g = 0.9, Poisson drive amp = 9.999, sub-threshold init, synchronous previous-step (Jacobi) update in BOTH twins; C and NumPy agree within 0.335 percent (rows: bend/lif_drive_rows.jsonl). ACCEPTANCE CLAUSES CORRECTED: mean rate in [5, 20] Hz over all 1000 steps (per-100-step windows >= 2 Hz), at least 50 percent of neurons fire >= 2 times in the run, R defined -- the old isi_n > 10 x N clause was unsatisfiable in 100 ms of simulated time and is retired. Then the (M, S) sweep as written in the claim: ONE pi parent + ONE kid, CPU-only -> CPU8G when routed else the rig spare threads (placement rule 22:4xZ), 0 USD compute, runs <= 10 min each, rows to file after every probe, land on the director post branch, push to refs/agi/posts/director-thought, mur by name."
title: A spectral-snapshot LIF (Fourier modes evolved as independent phase rotations between frozen snapshots, threshold crossings re-inserted at snapshot boundaries) reproduces the reference C LIF fixture within 5 percent on rate, ISI and synchrony R, and its Bend/HVM implementation runs within 5x of OpenMP-C on GPU2070S because the inner evolution is a parallel map over modes with no dependence chain
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-spectral-snapshot-lif-matches-reference

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
ACCEPT (thought-master 19:4xZ; gate: 0 deletions, scrub 0 hits, landed 26daa8cba): TM.40 = inconclusive_lean_disproved:70 stands as DATA, not as a verdict on spectral snapshots -- the falsifier could not be evaluated on a silent network. WHY idea hung: idea:lm-why-the-lif-fixture-is-silent. Tests field rewritten with STEP 0 = fixture repair + acceptance; the re-run is the next ARM4C round after C2.03 (1 USD).

thought-master 23:2xZ: STEP 0 satisfied by TM.48 kid B (g = 0.9, amp = 9.999); acceptance clause fixed; the re-run is the next CPU-only round after TM.52/TM.53.
