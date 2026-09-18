---
id: idea:lm-why-no-gpu-load-bend2-cuda
mint_id: 6a358909f64f400dadb080460592a869
type: idea
parents:
  - goal:g14
next_edges: []
edited_by: thought-master
scaffold_hash: f3563d2f8e49adc5
season: 2
title: "WHY did the Bend 2.0.5 CUDA lane show 0 percent GPU utilization on the LIF workload (TM.35: 47.77 s vs 1.264 s OpenMP-C on GPU2070S)? The disproved hypothesis:lm-bend2-spiking-sim hangs this idea: disproved means try something else, starting from a why"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# idea:lm-why-no-gpu-load-bend2-cuda

## Idea

What is the concept? `scale:` big (new chain) or small (extension)?

## Agent Notes
OWNER 2026-09-18 17:4xZ (thought-master pane), verbatim: "disproved in hard research just means lets try something else instead. So hang a new idea on the disproved hypothesis, usually a why question as a starter. So we had no GPU load, but WHY no gpu load?" HANGS ON hypothesis:lm-bend2-spiking-sim (disproved both halves; the [idea] schema allows only goal/vision parents, so the edge is recorded here + as a note on the hypothesis; schema question raised with the SM). THE QUESTION: the CUDA lane built, ran, produced the right spike counts (19983, drift 0) and never moved utilization.gpu -- so the work was not on the GPU. CANDIDATE CAUSES, each one experiment: (1) the binary never launched kernels -- HVM CUDA runtime fell back to the host path (check: nsys/nvprof kernel count = 0 vs > 0; cuda-gdb break on cudaLaunchKernel); (2) kernels launched but the program is one long sequential reduction (1000 LIF steps, each depending on the last) so a single interaction-net redex is live at a time -- the GPU runs one thread (check: utilization sampled at 10 ms with nvidia-smi dmon; count redexes per step in the HVM stats output); (3) the .bend program allocates the whole 10000x100 synapse graph as interaction nodes and the runtime spends its time in host-side allocation/GC between kernel launches (check: cudaMemcpy/host time vs kernel time in the nsys timeline); (4) float ops are not native in HVM (f24/u24 encodings) so the LIF arithmetic expands into many interactions per neuron per step -- 37.8x slower could be interaction count, not placement (check: HVM interaction counter per run vs the C op count). The FIRST experiment is (1): a kernel-launch count on the existing lif_gpu.bend binary on GPU2070S, 0 USD, 10 min. What answering it buys: whether Bend/HVM is a dead lane for spiking sims (kernels never launch / one redex live) or a fixable one (interaction blowup -> rewrite the LIF as parallel-per-neuron folds). Source-level understanding of the HVM CUDA runtime is the long road: goal:g14.5.

thought-master 20:0xZ 09-18 -- BRAINSTORM REVIEW (director hand-fallback 19:58Z, 5 items): KEPT as hypothesis:lm-bend2-cuda-lane-launches-zero-kernels (item 1 = the claim; items 2 + 3 = the conditional rows of the SAME rig job: dmon at 10 ms, nsys host/kernel split) and hypothesis:lm-hvm-float-encoding-blows-up-lif-interactions (item 4, MOVED from off-box to ARM4C: the HVM interaction counter needs no GPU, so cause 4 runs at 0 USD while the rig is down). DEFERRED item 5 (a from-scratch neuron-parallel Bend rewrite): contradicts the no-further-Bend-rounds call until hops 1/1b say the lane is fixable, and needs the driven fixture from idea:lm-why-the-lif-fixture-is-silent first; revisit ONLY if kernels launch with < 10 percent utilization AND no interaction blowup.
