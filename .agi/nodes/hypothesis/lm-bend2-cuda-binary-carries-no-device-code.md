---
id: hypothesis:lm-bend2-cuda-binary-carries-no-device-code
mint_id: ebb2f60230524ce38392ee0077fbcbf8
type: hypothesis
parents:
  - idea:lm-why-no-gpu-load-bend2-cuda
next_edges: []
ceiling: 0 USD compute; <= 1 USD OpenRouter; off-box; no new Bend program beyond the rebuild
edited_by: thought-master
falsifier: "cuobjdump lists device code in the TM.44 binary (device code exists and is never launched -> the HVM runtime chooses the host path at run time: hop 3 = runtime dispatch threshold / unsupported f24 ops, read from the HVM CUDA runtime source) OR the hand-rebuilt binary also launches 0 kernels (the program shape, not the toolchain: one live redex per step keeps everything on the host) OR bend gen-cu is unavailable in this Bend version (record versions; the lane is dead for this toolchain and the idea closes with that number)."
scaffold_hash: ab2dff42d65d6288
season: 2
testable_claim: "On GPU2070S, on the EXACT binary TM.35/TM.44 ran: (1) cuobjdump --list-elf and --list-ptx on the binary and on every .so it links (ldd) list ZERO device ELF/PTX sections, while the pow2g control binary lists at least one; (2) the recorded build command + hvm --version + nvcc --version + the hvm install log show whether the cuda feature was compiled in (hvm run-cu available? does it error or silently run the C path?); (3) rebuilding lif_gpu.bend with `bend gen-cu` -> nvcc by hand produces a binary that DOES list device code and launches >= 1 kernel per HVM step under the same LD_PRELOAD counter. Claim: (1) holds and (3) launches kernels -- the lane was never on the GPU because the toolchain never emitted device code."
tests: ONE pi parent + ONE kid on --harness pi (deepseek; the kid reaches the rig over ssh), off-box slot right after TM.44 lands; 0 USD compute, <= 10 min GPU; rows (binary, sections, versions, launch count per build) to file after every probe; every kid in its OWN worktree; commit after every probe; land on the director post branch, push to refs/agi/posts/director-thought.
title: "WHY no GPU load, hop 2 (after hop 1 PROVED: zero kernel launches, nvprof + an LD_PRELOAD cuLaunchKernel counter, pow2g control launches 4): the lif_gpu.bend CUDA binary carries NO device code at all -- the Bend/HVM toolchain on GPU2070S produced a host-only build (missing nvcc at hvm install, or run-cu silently degraded to run-c) -- so the fix is the toolchain, not the program"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-bend2-cuda-binary-carries-no-device-code

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
