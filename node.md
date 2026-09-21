---
id: hypothesis:lm-rpc-cpu-split-pays
mint_id: 7ef48e115ae5405ab7fcbd459467b8a7
type: hypothesis
parents:
  - idea:lm-two-node-vram-split
  - goal:g14.6
next_edges: []
ceiling: $0.50 OpenRouter; $0 compute; 0 downloads on CPU8G (the GGUF copied by scp and removed after); file scope = .agi/context/local-maxxing/rpc/{cmds.md, rows.jsonl} + bench/<utc>.jsonl + the kid experiment node + this node.
edited_by: thought-master
falsifier: Measured tg >= 5 tok/s with >= 4 GB resident on CPU8G (the bandwidth estimate wrong by 2x), or the owner names a use where 2-3 tok/s is enough (an offline batch quality probe of a 50B-class model) -- then one measured round is queued; otherwise this node stands as the reason no round runs.
scaffold_hash: cd98752c99b653dc
season: 2
testable_claim: "ARITHMETIC (ESTIMATE from the Prime inventory ruling 04:08Z + public part specs): CPU8G class memory bus ~21 GB/s theoretical, 13-15 GB/s practical; decode is bandwidth-bound, so W bytes of weights resident on CPU8G cost W / 14 GB/s per token: 5 GB (the most its 8 GB hosts beside the OS) = 0.36 s/token = 2.8 tok/s CEILING for the whole pipeline, because pipeline stages are serial per token and the GPU stage waits; prefill is compute-bound: an AVX-only ISA (no AVX2, no FMA), 2 cores, ~40-70 GFLOPS -> 2 x 10B params (5 GB at Q4) = 20 GFLOP/token = 2-3 tok/s prefill, i.e. a 2k-token kid prompt = 11-17 min; the LAN adds ~0.3-0.5 ms per token per hop (hidden state 4-10 KB at d_model 4096-5120) -- negligible. The kid-tier bar (hypothesis:lm-bonsai2-27b-kid-tier) is tg >= 20 tok/s and pp >= 200 tok/s: the split sits 7-10x below it on decode and 70-100x below on prefill under EVERY ratio that puts real weight on CPU8G, and a ratio that puts < 1 GB there adds nothing the 16 GB RAM of local-town (DDR4, ~40 GB/s, 3x faster than the remote worker) does not already hold. CLAIM: the split pays ONLY when the target does not fit local-town at all (8 GB VRAM + ~14 GB usable RAM = ~22 GB; a dense 50B at Q4 = ~28 GB, the qwen3.8-50b line of the charter) and then only at <= 3 tok/s as an offline capacity/quality probe, never as a kid service. MEASURED test, if ordered: rpc-server on CPU8G (CPU build, same llama.cpp commit, no secrets, off the Doppler path), llama-server on local-town with --rpc <prime>:<port> and a tensor split putting 4-5 GB of the target on CPU8G; tg128 + pp512, 3 reps warm, beside the same model local-only (or the local OOM line): proved if tg >= 5 tok/s (2x the estimate), disproved if <= 3 tok/s. SECOND READING of the owner line (CPU sims): CPU8G adds 2c/4t of AVX-only x86 = ~10-15% of the local-town 16-thread throughput and < 40% of the 4 cores of the ARM4C -- a spare test node, not a compute partner; the compute the owner wants used is the 16 threads + the A1, already in the queue (Bend2, PufferLib, spec-decode)."
tests: "NO ROUND by default. If ordered: ONE pi parent + ONE kid, off-box slot, $0.50 OpenRouter, $0 compute; the same llama.cpp commit built CPU-only on CPU8G (AVX only), never a secret or Doppler value in any file, the worker stopped and removed after the run (rollback logged); rows to bench/<utc>.jsonl labelled rpc-*; kid line_ceiling 120."
title: "A llama.cpp rpc-server CPU worker on CPU8G (2c/4t x86, 8 GB, wired 1 Gbit LAN) caps any pipeline it joins at ~2-3 tok/s decode and ~2-3 tok/s prefill: the cross-box CPU split does NOT pay for kid-tier serving and pays only as a capacity probe for a model that does not fit local-town alone -- arithmetic first, one measured round only if the owner names such a model"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-rpc-cpu-split-pays

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-18 03:5xZ (thought-master pane), verbatim: "Bend and puffer lib are critical. Used for efficient fine tuning and oscillator and spiking neural net optimization imo. We can off load to cpu and use it for speculative decode and hybrid system both and even launch cup cores between it and the other encryption box even if we have to. We just gotta use the compute we have. Later we can also run experiments on the big arm box as well. Check the Doppler for setup." PRIME RULING (belam, VERIFIED 04:08Z, doc:l5-owner-decisions): CPU8G = 2c/4t x86, 8 GB, an iGPU (no compute GPU), the secret keeper (Doppler agi/* only there); local-town = x86-8c/16t, 16 GB, 8 GB GPU; both on the farm LAN; no bigger ARM box in the inventory (banked for the owner). A llama.cpp rpc-server CPU worker on CPU8G is inside remit, never on the Doppler path, no secrets stored there; NO round until the thought-town feasibility node says the split pays. THIS NODE IS THAT NODE (thought-master 04:2xZ): by the arithmetic it does not pay for kid-tier; no round is queued; the owner can override by naming a model that does not fit local-town (then one $0.50 measured round, off-box slot).
