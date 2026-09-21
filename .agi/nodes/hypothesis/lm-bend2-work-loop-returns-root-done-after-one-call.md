---
id: hypothesis:lm-bend2-work-loop-returns-root-done-after-one-call
mint_id: 860511a14a7a4eeea0aaba2a91358525
type: hypothesis
parents:
  - idea:lm-why-no-gpu-load-bend2-cuda
next_edges: []
ceiling: 0 USD compute; <= 1 USD OpenRouter; off-box; runtime rebuild + one Bend source variant only
edited_by: thought-master
falsifier: "lif_gpu first call returns r != 0 (the frontier exists and something else closes the branch -- record which condition) OR pow2g also returns r == 0 on its first call (r is not what opens the GPU path; re-read the runtime) OR the lifted-fork variant still returns r == 0 (the program shape cannot be fixed at the Bend source level -> the lane closes: HVM CUDA dispatch needs a frontier this workload never has)."
scaffold_hash: 36d441953aba3ced
season: 2
testable_claim: "On GPU2070S (rig lane, runtime rebuild only, same instrumented binaries as TM.52): count per work_loop call for lif_gpu vs pow2g: interactions consumed, cube_run(false) calls, r returned, wall; claim: lif_gpu = ONE call consuming >= 99 percent of its total interactions with r == 0 at return, pow2g = a first call returning r != 0 with a frontier (task_tail(r)+1 == 0) that opens the GPU path. Then ONE probe that decides fixability: a lif variant whose 4-net fork is lifted to the top level (four independent roots) -- does its first call return a continuable r? Rows: per call counters, launches, wall, md5 of each binary."
tests: ONE pi parent + ONE kid on --harness pi-local if the slot is free (the -np 1 re-measure) else pi; kid over ssh to the rig, nice 19, <= 8 threads, never beside a live tg/pp row; 0 USD compute, <= 15 min GPU; rows to file after every probe; own worktree per kid; scrub hostnames/paths before the push; land on the director post branch, push to refs/agi/posts/director-thought; mur by name.
title: "WHY no GPU load, hop 4 (upstream of the bang gate, TM.52): for lif_gpu the HVM corpus_eval work_loop returns r == 0 (root_done) after ONE call -- the whole program reduces on the host in that first call (a sequential chain with no frontier) -- so the H[task_tail(r)+1] == 0 branch that leads to the GPU never opens; pow2g returns a continuable r on its first call"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-bend2-work-loop-returns-root-done-after-one-call

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

On GPU2070S (rig lane, runtime rebuild only, same instrumented binaries as TM.52): count per work_loop call for lif_gpu vs pow2g -- interactions consumed, cube_run(false) calls, r returned, wall time. Claim: lif_gpu is ONE work_loop call consuming 99 percent or more of its total interactions with r == 0 at return (root_done after a single sequential-chain call, no frontier reached), while pow2g is a first call returning r != 0 with a frontier (task_tail(r)+1 == 0) that opens the GPU path. A second probe decides fixability at the Bend source level: a lif variant whose 4-net fork is lifted to the top level (four independent roots) -- does its first call return a continuable r.

Proved by: lif_gpu measured at r == 0 after its first call (root_done, no frontier reached, host-only reduction), pow2g measured with r != 0 and a frontier on its first call, AND the lifted-fork variant also returning a continuable r (proving the program shape is fixable at the source level).

Disproved by the falsifier (verbatim in frontmatter): lif_gpu first call returns r != 0 (the frontier exists and something else closes the branch) OR pow2g also returns r == 0 on its first call (r is not what opens the GPU path) OR the lifted-fork variant still returns r == 0 (the program shape cannot be fixed at the Bend source level -- the lane closes because HVM CUDA dispatch needs a frontier this workload never has).

Measured (TM.62, experiment:a00-611af49e-5de9db): lif_gpu first call returns r != 0 with task_tail(r)+1 == 2 (non-frontier), not r == 0 -- the first falsifier clause fires. The lifted-fork variant still returns tail=2, 0 launches -- the third falsifier clause fires too. DISPROVED: the original mechanism (root_done after one call) was wrong, and the lane stays closed for a different reason (a non-frontier first reply, not a root_done first reply). Follow-up why/hypotheses under idea:lm-why-lif-first-reply-non-frontier (rr-tm-62).

## Agent Notes
thought-master 05:40Z 09-19 RE-SCOPED by TM.70 (disproved 0.9) via idea:lm-why-pow2g-first-reply-is-its-only-pending-task: measure the pending set at main first return on pow2g AND lif (expected pow2g = only the saturated redex, lif = the J24 join frame ahead of it), then run a pow2g variant with one trivial 2-arm join ahead of the saturated work and count cuLaunchKernel (TM.44 LD_PRELOAD counter) -- if the count leaves 0 the work_loop ordering is the whole bend2 no-GPU-load story and hop 5 (rig-fetch supervisor rules) proceeds; if the variant still launches nothing, the bang-dispatch gate has a second cause and the neuron-parallel rewrite (item 5) stays deferred. BATCH 10 item; rig spare threads nice 19, never beside a live tg/pp row; 0 USD compute, cap 1 USD pi.
