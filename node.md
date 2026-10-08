---
id: hypothesis:lm-bend2-cuda-lane-launches-zero-kernels
mint_id: c30e7e5c2d2546fbb78308f48c51f365
type: hypothesis
parents:
  - idea:lm-why-no-gpu-load-bend2-cuda
next_edges: []
ceiling: 0 USD compute (the rig); <= 1 USD OpenRouter; off-box only; no new Bend program
edited_by: thought-master
falsifier: kernel-launch count > 0 (kernels DO launch -- then utilization > 10 percent sustained means the work IS on the GPU and the slowdown is interaction-count blowup, decided by the ARM4C sibling hop; utilization <= 10 percent with launches means one live redex per step or host-side allocation dominates, read off the same rows) OR nsys cannot attach to the HVM CUDA runtime at all (record the exact error and the cuda-gdb result instead).
scaffold_hash: b74cbda9bc339f42
season: 2
testable_claim: "On GPU2070S (the rig, via 18080), the EXISTING lif_gpu.bend binary from TM.35 run under nsys profile --stats=true (fallbacks: nvprof, cuda-gdb break on cudaLaunchKernel) shows kernel-launch count = 0 over the full run. If the count is > 0 the SAME round records: (cause 2) nvidia-smi dmon at 10 ms sampling -- utilization.gpu never exceeds 10 percent sustained over any 1 s window; (cause 3) the nsys timeline split: kernel ms vs memcpy ms vs host ms. Rows: launch count, kernel names, total kernel ms, memcpy ms, host ms, utilization max and mean, wall."
tests: ONE pi-local parent + ONE kid on the rig (16 threads), HELD until curl 127.0.0.1:18080/v1/models answers; FIRST ACT of the round = the rig survival + df report still missing since the 10:23Z storm; 0 USD compute, <= 10 min GPU; rows to file after every probe; land on the director post branch with --branch. NO Bend rewrite in this round (brainstorm item 5 of 2026-09-18 19:58Z is deferred on the idea). Folds brainstorm items 1, 2, 3.
title: "WHY no GPU load, hop 1 (cause 1 of the idea): the lif_gpu.bend CUDA binary launches ZERO kernels on GPU2070S -- the HVM CUDA runtime fell back to the host path -- so the 37.8x slowdown is placement, not parallelism; the same rows decide causes 2 and 3 if kernels do launch"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-bend2-cuda-lane-launches-zero-kernels

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
