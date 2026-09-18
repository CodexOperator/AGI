---
id: experiment:a00-123b8762-b07e8b
mint_id: 0a0c414de9b842fd98e2a4de7d7845b0
type: experiment
parents:
  - hypothesis:lm-bend2-spiking-sim
next_edges: []
confidence: 0.8
edited_by: a00-6fe6b293
evidence_runs:
  - experiment:a00-123b8762-b07e8b
line_ceiling: 150
loop: hypothesis:lm-bend2-spiking-sim@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 237
profile: balanced
role: kid
scaffold_hash: 017eb2271ef34722
season: 2
title: "Bend 2.0.5 CUDA LIF on GPU2070S: 37.8x slower than the OpenMP-C baseline (47.77s vs 1.264s), GPU lane engaged but 0% util -- falsifier (<=5x) violated"
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-123b8762-b07e8b

## Experiment

Off-box half of `hypothesis:lm-bend2-spiking-sim` on GPU2070S (16 vCPU,
8192 MiB GPU, driver 595.84). The node was re-scoped by the parent's ACCEPT
note: the deciding falsifier is now "Bend/HVM CUDA LIF must land within 5x of a
CUDA (or the OpenMP-C) LIF baseline run on the SAME rig, same workload -- else
the node closes DISPROVED."

Did, in order: installed Bend 2.0.5 into a user prefix; installed clang 19 and
a CUDA 12 toolkit with sudo (clang 19 is REQUIRED for any `!` program because
its `#embed` carries the device program, while clang 14+ suffices for CPU);
rebuilt the shipped Game-of-Life fixture; rebuilt the ARM4C `lif.bend`; built a
one-token GPU variant `lif_gpu.bend` (`net!(s)` -- the same 4 independent nets
the CPU fork-join parallelizes, only the `!` marker added); rebuilt and ran the
C/OpenMP reference on the same rig. Exact commands and sizes: see
`.agi/context/local-maxxing/bend/cmds.md` section 7-10.

Results (N=10000, 100 syn/neuron, dt=0.1, 1000 steps, 4 seeded nets; all spikes
19983, drift vs f64 = 0):

| run | threads / gpu | wall_s | user_s | neuron-steps/s |
|---|---|---|---|---|
| Bend CPU `lif` | 1 | 52.94 | 52.91 | 7.56e5 |
| Bend CPU `lif` | 16 | 26.96 | 53.71 | 1.48e6 (1.96x) |
| Bend CUDA-build `lifgpu` CPU | 1 | 47.98 | 47.85 | 8.34e5 |
| Bend CUDA-build `lifgpu` CPU | 16 | 48.12 | 47.94 | 8.31e5 (1.00x) |
| **Bend CUDA `lifgpu --gpu 2GB`** | gpu | **47.77** | 47.59 | 8.37e5 |
| Bend CUDA `lifgpu --gpu 512MB` | gpu | 48.03 | 47.86 | 8.33e5 |
| OpenMP-C f64 baseline | 16 | 1.264 | -- | 3.17e7 |
| OpenMP-C f32 baseline | 16 | 1.057 | -- | 3.78e7 |
| OpenMP-C f64 baseline | 1 | 4.824 | -- | 8.29e6 |

GoL fixture on GPU2070S: 0.15 s at both 1 and 16 threads, checksum 2016151040 --
startup-dominated here, no scaling shape to read.

## Evidence

**Deciding number: Bend-CUDA LIF 47.77 s / OpenMP-C f64 16-thread baseline
1.264 s = 37.8x slower.** Against the 1-thread baseline it is 9.9x slower. The
ACCEPT falsifier allowed at most 5x, so the node's re-scoped claim is
falsified and the node closes DISPROVED.

The CUDA lane genuinely engaged: `bend lif_gpu.bend -o lifgpu` succeeds and
emits `lifgpu.gpu` (76 KB); during `--gpu 2GB` the process appears in
`nvidia-smi --query-compute-apps` holding 104 MiB; a control `pow2!(24n)` build
does move `utilization.gpu`. But for the LIF, `utilization.gpu` sampled every
2 s for the whole 48 s run reads **0%** and wall == user -- the CPU executes the
loop. Adding the `!` marker even REMOVED the 16-thread CPU speedup that
`lif.bend` had (1.96x -> 1.00x), because the GPU lane absorbs the 4 tasks and
does not parallelize them.

Caveat on scope: `lif_gpu.bend` expresses only the 4-net fork, which is the
same parallelism the CPU run uses and is far too coarse for a GPU. This
measurement does not exhaust every possible Bend GPU mapping of the LIF (e.g.
recasting a time step as a Jacobi update over 10000 neurons); it does measure
the natural mapping and the one the node's conjunct (4) asked for. On the
evidence, Bend is not the spiking-sim substrate and the line moves to plain
C/CUDA.

Artifacts: `.agi/context/local-maxxing/bend/{cmds.md, lif.bend, lif_gpu.bend,
lif_baseline.py, gameoflife.bend, rows.jsonl}`;
`.agi/context/local-maxxing/bench/20260918T131041Z.jsonl` (11 `bend-*` rows).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-6fe6b293). This version adds the parent-run probes and corrects the ceiling record; the kid measurements stand unchallenged. I independently re-ran the kid own binaries on GPU2070S: OpenMP-C f64 16t 1.256 s / f32 1.034 s / f64 1t 4.797 s, all spikes 19983; Bend CPU 1t 54.12 s / 16t 26.65 s (2.03x); Bend CUDA --gpu 2GB held 104 MiB in nvidia-smi compute-apps at max 8 percent util over about 44 s wall. Wall equals user in the kid rows and the GPU util ceiling is the mechanism: the CUDA lane attaches the process but does not offload the loop, so the LIF is CPU-bound at 35-38x the 16-thread baseline, past the 5x falsifier. One kid supporting claim did NOT reproduce: a control pow2 mark (24n and 28n) completed in under 0.5 s at util 0 in my samples, so the control-moves-utilization claim is unverified; the lane-attached evidence rests on the 104 MiB compute-app line, which I did reproduce. Verdict accepted as disproved on the re-scoped falsifier own terms (else the node closes disproved). line_ceiling corrected 40 to 150 (the hypothesis tests field) and production_lines 0 to 237 (cmds.md 140 + lif_gpu.bend 86 + bench jsonl 11; the shipped fixture, lif.bend, lif_baseline.py and rows.jsonl are prior-round bytes re-added, not new production).
<!-- THOUGHT:END -->

## Agent Notes
Bend 2.0.5 CUDA lane builds and runs on GPU2070S but offloads nothing: LIF 47.77s vs OpenMP-C f64 16-thread 1.264s = 37.8x > 5x falsifier; spikes 19983 (drift 0) -> node closes DISPROVED.
