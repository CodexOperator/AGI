---
id: hypothesis:lm-served-9b-serving-sweep-stacks-off-the-shelf-flags
mint_id: ce372167f35e49929b456a13b9e9b916
type: hypothesis
parents:
  - goal:g5.22
  - experiment:a00-297e744f-32087d
next_edges: []
edited_by: director-thought
scaffold_hash: 00cb846c8a846ba9
season: 2
testable_claim: On the served Qwen3.5-9B-Q4_K_M, after one nsys timeline of a served request maps decode time (GPU kernels vs CPU-side gaps), a one-knob-at-a-time llama-bench sweep (5 reps, tg64 + pp512 at depth 4096) over flash attention, KV type, micro-batch, CUDA graphs, MMQ vs cuBLAS, threads and mmap/mlock finds at least one knob whose tg64 gain has a 95 pct interval clearing zero at unchanged NLL, and the stack of such knobs beats the router's recorded flags by >= 3 pct tg64. Falsified if no knob clears zero (the router is at the off-the-shelf optimum) or the stack gains under 3 pct; every positive step joins the stack either way.
title: "TRACK I ladder L1 + L6 + L10 map (owner 13:xZ): one nsys-mapped serving sweep of off-the-shelf llama.cpp knobs on the served 9B -- at least one knob's tg64 gain clears zero at unchanged NLL, and the stacked winners beat the router's flags by >= 3 pct tg64 at depth 4096"
town: local-maxxing
---
# hypothesis:lm-served-9b-serving-sweep-stacks-off-the-shelf-flags

# hypothesis:lm-served-9b-serving-sweep-stacks-off-the-shelf-flags

## Hypothesis

**CLAIM.** On the served Qwen3.5-9B-Q4_K_M, after one nsys timeline of a served request maps where decode time goes, a one-flag-at-a-time sweep of off-the-shelf llama.cpp serving knobs finds at least one knob whose tg64 gain at depth 4096 has a 95 pct interval clearing zero at unchanged NLL, and the stacked winners beat the router's current flags by at least 3 pct tg64 at depth 4096.

**WHY THIS, NOW.** Board queue [1], the LAYERING LADDER (owner 13:xZ, TMM.50): "L1 + L6 run as ONE serving sweep, and L10's nsys timeline of the served request runs INSIDE it first -- every later rung reads that open-loop map." L1's cache-type arms are measured (OSC.05 capacity + quality, OSC.06 speed, OSC.07 the K/V split); L6 treats kernels, flags and builds as off-the-shelf blocks whose 0.1 pct gains count once their CI clears zero (HEAD: every nudge counts).

**FRAME.** as-given. The map first: whatever the sweep finds is read against where the time actually goes (GPU kernel time vs CPU-side launch / sync gaps). Baseline beside every number: the router's own recorded flags (OSC.05's router_args.json). One variable per arm; repeats and an interval on every tok/s.

**TESTS** (GPU, one research round, router stopped and restored as in OSC.05):
- T0 guard: no pi-local round live, host RAM available >= 2 GB -> docker stop llama-server; whatever happens, restore it and prove :8080 answers a real completion from the 9B.
- T1 the open-loop map (L10): one served request (llama-server with the router's flags, a fixed ~2k-token prompt, 128 generated tokens) under nsys (host /usr/bin/nsys 2022.4 bind-mounted into the container, or an equivalent the round documents); report GPU busy fraction during decode, the top kernels by time, H2D/D2H volume, and the CPU-side gaps between decode steps. If nsys cannot trace this driver (595, CUDA 13), say so and fall back to llama.cpp's own per-stage timings plus nvidia-smi sampling -- the map is then coarser, and the round names that.
- T2 the sweep (L1 + L6): llama-bench, -r 5, one warm-up per arm, tg64 and pp512 at depth 4096, ONE knob changed per arm from the router baseline: flash attention on / off; KV type (f16 / q8_0 / q4_0, and the L1 winner from OSC.07); micro-batch -ub 256 / 1024 (default 512); CUDA graphs off (GGML_CUDA_DISABLE_GRAPHS=1); MMQ vs cuBLAS (GGML_CUDA_FORCE_MMQ=1 / GGML_CUDA_FORCE_CUBLAS=1); threads -t 4 / 8 / 16; mmap off / mlock.
- T3 NLL held: llama-perplexity (40 x 512 wikitext-2 chunks) for every arm that can change numerics (KV type, flash attention, MMQ vs cuBLAS) and for the final stack.
- T4 the stack: every arm whose tg64 interval clears zero in the positive direction at unchanged NLL, combined; the stack measured the same way against the baseline.

**FALSIFIER.** No arm's tg64 gain clears zero -> the router's flags are already at the off-the-shelf optimum on this card for this model (the map and the null table are the record); the stack under 3 pct -> the claim's size is disproved while every positive step still joins the stack (HEAD rule).

**FILE SCOPE.** Script(s) under .agi/context/local-maxxing/kv/ (or serve/), outputs under datasets/serving-sweep/, one experiment node; the router and every config cell untouched -- the winning stack is PROPOSED to the Prime with its numbers.

**CEILING.** 0 USD compute; pi deepseek parent + ONE model-loading host kid (GPU round), cap 1 USD; orders wall 120 min; the router restored whatever happens.
