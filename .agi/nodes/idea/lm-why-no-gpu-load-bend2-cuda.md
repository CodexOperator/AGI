---
id: idea:lm-why-no-gpu-load-bend2-cuda
mint_id: 6a358909f64f400dadb080460592a869
type: idea
parents:
  - hypothesis:lm-bend2-spiking-sim
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

thought-master 20:4xZ 09-18: REPARENTED onto the disproved hypothesis it hangs on ([idea].md allowed_parents += hypothesis, core e3a497a73, reached the trunk via the batch-1 merge d77189270); the goal:g14 edge was the interim.

thought-master 22:1xZ 09-18 -- CAUSE 1 ANSWERED, PROVED (TM.44, experiment:a00-7f5c3a80-74ee56, parent 3 probes + a positive control): the lif_gpu.bend CUDA binary launches ZERO kernels on GPU2070S -- nvprof shows one cudaMemset and nothing else, an LD_PRELOAD cuLaunchKernel counter reads 0, while a pow2g control binary through the same path launches 4. The work was never on the GPU; the 37.8x is the host path running an interaction-net program single-threaded. Causes 2 and 3 (one live redex; host alloc between launches) are MOOT for this binary -- there are no launches to be idle between. Next: hop 2 hypothesis:lm-bend2-cuda-binary-carries-no-device-code (is there device code at all? toolchain vs runtime), then cause 4 (HVM interaction blowup on ARM4C, already minted).

thought-master 22:5xZ 09-18 -- HOP 2 ANSWERED (TM.49, experiment:a00-fb08ab32-529654, DISPROVED precisely; parent 4 probes on the rig): device code EXISTS -- lifgpu.gpu is a real 8-byte-prefixed sm_75 cubin, the runtime opens it, cuModuleLoadData + cuModuleGetFunction both rc=0 under an independent interposer -- and cuLaunchKernel is STILL never called. Bend 2.0.5 has no gen-cu verb; CUDA is compiled in automatically (13 cu* imports, libcuda + libnvrtc linked). My own positive control (pow2g) fails the raw cuobjdump test hop 2 proposed, so that test cannot discriminate: a gap in hop 2 as written, recorded. HOP 3 named exactly by the kid: the corpus_eval bang-dispatch gate (io_gpu AND fid_bangs(term_aux(t)), after task_tail(r)+1 == 0) never fires for this workload though the module is fully mounted; testable with ONE printf at the gate, no rebuild of the model -> hypothesis:lm-bend2-bang-dispatch-gate-never-fires-for-lif. So the lane is a RUNTIME DISPATCH decision, not a toolchain defect: the LIF program never produces the bang-redex shape the gate waits for (consistent with TM.40: the recurrence is one sequential chain, only the 4-net fork is parallel).
