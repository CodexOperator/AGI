---
id: hypothesis:lm-bend2-spiking-sim
mint_id: f8007b7f031047dba8535d17a08ef618
type: hypothesis
parents:
  - idea:lm-hybrid-oscillator-readout
  - goal:g14
next_edges: []
ceiling: $1 OpenRouter; $0 compute; downloads <= 500 MB (Bun + Bend); runs <= 10 min each; file scope = .agi/context/local-maxxing/bend/{cmds.md, lif.bend, lif_baseline.py, rows.jsonl} + bench/<utc>.jsonl + the kid experiment node + this node.
edited_by: thought-master
falsifier: Bend 2 does not install on either box, or 16-thread scaling < 4x (the assign-once no-work-stealing scheduler starving on the sparse loop), or the LIF loop is > 5x slower than the NumPy baseline -- then Bend 2 is not the sim substrate and the spiking sim stays NumPy/C (or Brian2) with multiprocessing.
scaffold_hash: 45cea0bd0fa50baf
season: 2
testable_claim: "(1) Bend 2.0.x installs into a user prefix on local-town (x86-64 Linux; Bun + C compiler) and on this box (aarch64 Linux; no Metal/CUDA -> CPU path only) -- install command, version, failing steps recorded; (2) the shipped Game-of-Life fixture reproduces the upstream shape: 16-thread wall-clock <= 1/8 of 1-thread on local-town and 4-thread <= 1/3 of 1-thread on the A1 (upstream laptop bench, MEASURED in the digest, not rerun: 7.803 s -> 0.647 s parallel CPU -> 0.063 s GPU; the lexer LOSES on GPU 0.198 s -> 1.075 s); (3) a sparse LIF network (N = 10,000 neurons, ~100 synapses each, f32 Euler at dt 0.1 ms -- Bend 2 has 32-bit numbers only, no f64 -- 1,000 steps, seeded) written in Bend scales the same way and its neuron-steps/s are within 2x of a NumPy/C baseline on the same box, spike-count drift vs the f64 baseline reported; (4) the same source runs unchanged with --gpu on the local-town GPU and the GPU vs 16-thread ratio is reported -- which side of the Game-of-Life/lexer crossover the LIF loop falls on is the number the town needs."
tests: ONE pi parent + ONE kid, A1-light slot (install + fixture + LIF on 4 threads) then the off-box slot for 16 threads + --gpu; $1 OpenRouter cap, $0 compute; install via the bend-lang.com script into a user prefix, never system-wide, rollback = rm the prefix; sources under .agi/context/local-maxxing/bend/; rows to bench/<utc>.jsonl labelled bend-*; kid line_ceiling 150.
title: Bend 2 (BendRT flat-C parallel runtime, no GC, no work stealing, f32 only) runs a sparse LIF spiking-net loop on the 16 threads of local-town at >= 8x the 1-thread rate and on the 4 A1 threads at >= 3x, within 2x of a NumPy/C baseline -- the sim substrate for the oscillator readout, $0
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-bend2-spiking-sim

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-18 03:5xZ (thought-master pane), verbatim: "Bend and puffer lib are critical. Used for efficient fine tuning and oscillator and spiking neural net optimization imo. We can off load to cpu and use it for speculative decode and hybrid system both and even launch cup cores between it and the other encryption box even if we have to. We just gotta use the compute we have. Later we can also run experiments on the big arm box as well. Check the Doppler for setup." APPLY: Bend 2.0.5 at github.com/bendlang/bend (Apache-2.0, 20,546 stars, pushed 2026-09-18T03:03Z; install script at bend-lang.com; papers BendTT + BendRT). MEASURED limits from the digest: 32-bit numbers only (no u64/f64), BendRT compiles to a flat C evaluator (no interaction nets), the scheduler assigns tasks once without work stealing, GPU = Metal/CUDA only (none on the A1); upstream laptop bench: GPU wins Game of Life 10x but LOSES the lexer 5x to 16 CPU threads -- the crossover this node measures for a spiking loop. A1-light slot then 16 threads + --gpu on the local-town GPU; $0 by construction.

CEILING CLARIFIED (thought-master 05:20Z, on the director's question): the tests field names two halves (ARM4C half: install + fixture + LIF on 4 threads; local-town half: 16 threads + --gpu) -- the ceiling is  OpenRouter PER HALF-ROUND,  for the node in total, /bin/bash compute both. TM.32 (ARM4C half, parent a00-f29e25f2, cap 0.55) runs under the first half; the local-town half may be dispatched at up to  when the off-box slot frees behind Bonsai + the schedule fix. Same reading applies to hypothesis:lm-pufferlib-oscillator-policy (two halves,  each).

ACCEPT (thought-master 11:3xZ, gate passed, landed eea005dd4 + scrub 0d5084d9a: the cmds.md host line named the provider/hardware, now the ARM4C alias): the ARM4C half is inconclusive_lean_disproved:60 -- Bend 2.0.5 LIF (N=10000, syn=100, 1000 steps, 4 nets) is 13.0x slower than the gcc -O3 -fopenmp f64 baseline (baseline 1.72 s at 4 threads), past the > 5x falsifier; the parent rebuilt and reran both fixtures itself. The install + Game-of-Life fixture are real and stay as the runbook. RE-SCOPE for the queued off-box half (16 threads + GPU on GPU2070S): it now DECIDES the node -- Bend/HVM on CUDA must come within 5x of a CUDA (or the OpenMP C) LIF baseline on the same rig, same workload, or the node closes disproved and the spiking-sim line moves to plain C/CUDA (PufferLib stays its own node). Ceiling unchanged: 1 USD OpenRouter for that half, 0 compute.

ACCEPT + CLOSED DISPROVED (thought-master 13:4xZ; gate: merge-base 863ad9329 live, 0 deletions, round-file scrub 0 hits, landed c102dc404): both halves fail the falsifier -- ARM4C half 13.0x slower than OpenMP-C (TM.32, lean_disproved:60), GPU half on GPU2070S 37.8x slower (Bend 2.0.5 CUDA LIF 47.77 s vs OpenMP-C 16-thread 1.264 s; the CUDA lane builds and engages but offloads nothing, utilization.gpu 0 pct; spikes 19983, drift 0; TM.35, verdict disproved, parent re-ran the kid binaries itself). No further Bend rounds. What survives: the LIF fixture + OpenMP-C baseline (bend/lif_baseline.py) as the spiking-sim reference implementation; the spiking-sim line continues in plain C/CUDA under idea:lm-hybrid-oscillator-readout, and hypothesis:lm-pufferlib-oscillator-policy stays its own node (owner CRITICAL) -- its ARM4C half is the next ARM4C dispatch.

OWNER 17:4xZ: a disproved hypothesis hangs a new idea, starting from a WHY -> idea:lm-why-no-gpu-load-bend2-cuda (why 0 percent GPU utilization; four candidate causes, first experiment = kernel-launch count on the existing binary, 0 USD). The Bend lane is not dead, it is a why.
