---
id: hypothesis:lm-pufferlib-oscillator-policy
mint_id: e7a4b3c86386417dbec299c4ad01cfc4
type: hypothesis
parents:
  - idea:lm-hybrid-oscillator-readout
  - goal:g14.12
next_edges: []
ceiling: $1 OpenRouter; $0 compute; downloads <= 1.5 GB (clone + wheels); CPU <= 30 min per training run, counted against the A1 share; file scope = .agi/context/local-maxxing/puffer/{cmds.md, rhythm_bank_env.py, rows.jsonl} + bench/<utc>.jsonl + the kid experiment node + this node.
edited_by: thought-master
falsifier: PufferLib does not build CPU-only on aarch64 or x86 without CUDA, or the env cannot exceed 0.1M steps/s on 16 threads (the readout is not RL-trainable at this scale on CPU), or the learned policy is within noise of random subscription sets after 30 min on 5 seeds -- then the readout stays a hand-designed subscription set and RL training moves to a Camber XS hour (banked, spend).
scaffold_hash: e5bf85fb93fbf3fa
season: 2
testable_claim: (1) PufferLib 5.0 installs from a shallow clone on ARM4C (aarch64, no GPU) and on local-town (x86-64, 16 threads) and puffer train breakout runs CPU-only (vec num-threads N, no CUDA) to a scoring agent -- wall-clock and steps/s recorded at 1 and 4 threads (A1) and 1 and 16 threads (local-town), the blog 1M-4M sps numbers as the reference and the release-body line (reproduce on a single GPU) as the expected falsifier; (2) a custom env rhythm_bank (a bank of K Kuramoto oscillators driven by recorded head-activation / KV-bit traces from the served 9B -- the C2 digital-Kuramoto flip-mode traces reused as the observation; action = which read sites each of M readout neurons subscribes to from a fixed menu of 10-200 sites; reward = phase coherence of the readout with a held-out target rhythm) runs at >= 0.5M steps/s on 16 threads and >= 0.1M on 4; (3) after <= 30 min of CPU training the learned subscription policy beats random subscription sets on the coherence reward by >= 2x (mean of 5 seeds, held-out traces); env source, policy sizes (hidden_size, num_layers) and seeds committed.
tests: ONE pi parent + ONE kid, A1-light slot first (install + breakout CPU timing, digest seeds P1/P2), then the off-box slot for the 16-thread run; $1 OpenRouter cap, $0 compute; shallow clone only (repo 926 MB -> depth 1), puffer5_models.zip only if <= 500 MB; rows to bench/<utc>.jsonl labelled puffer-*; env under .agi/context/local-maxxing/puffer/; rollback = rm the venv + clone; kid line_ceiling 150.
title: PufferLib 5.0 trains the rhythm-bank readout as a tiny RL policy CPU-only (A1 4 threads / local-town 16 threads) at >= 0.5M steps/s on a custom oscillator env and beats random subscription sets >= 2x after 30 min, $0 -- the subscription set IS the weight, learned by RL not backprop
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-pufferlib-oscillator-policy

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-18 03:5xZ (thought-master pane), verbatim: "Bend and puffer lib are critical. Used for efficient fine tuning and oscillator and spiking neural net optimization imo. We can off load to cpu and use it for speculative decode and hybrid system both and even launch cup cores between it and the other encryption box even if we have to. We just gotta use the compute we have. Later we can also run experiments on the big arm box as well. Check the Doppler for setup." APPLY: PufferLib 5.0 = tag 5.0-experiments 2026-09-13 (6,451 stars; blog 2.0 = 1M sps, 3.0 = 4M sps; the 'under a second' claim is video-only and the release body says reproduce on a single GPU -- the CPU-only run IS the falsifier target). The readout being trained = idea:lm-hybrid-oscillator-readout (subscription set as the weight; rhythm-neuron subnetwork as the metronome); the observation traces come from the C2 digital-Kuramoto chain (hypothesis:c2-digital-kuramoto-flip-mode). A1-light slot first, then 16 threads; $0 by construction.

CEILING CLARIFIED (thought-master 05:20Z): two halves (ARM4C half: install + breakout CPU timing; local-town half: 16 threads + the rhythm_bank env + training) --  OpenRouter per half-round,  for the node in total, /bin/bash compute.

ACCEPT (thought-master 18:1xZ; gate passed, landed f2dacfaae): ARM4C half DISPROVED (experiment:a00-dc84f156-eb0a1d, TM.38): PufferLib 5.0-experiments has no CPU-only trainer path on aarch64 -- the native trainer needs nvcc (absent), the --cpu target links a raylib binary pinned to x86-64 (EM:62, cannot link on aarch64), and the tag ships no pyproject/setup.py. This is arch-specific, not a CPU-only impossibility: the x86-64 off-box half (GPU2070S, 16 threads + GPU) decides the node and is dispatched next. CEILING CLARIFIED (same reading as bend2, thought-master 05:21Z): 1 USD OpenRouter PER HALF, 2 per node, 0 compute -- the off-box half runs at 1 USD, not 0.50. Director error recorded: TM.38 was dispatched without --branch and ran in the shared main checkout; rescued onto a proper loop branch with only its 4 files; every kid its own worktree, always.
