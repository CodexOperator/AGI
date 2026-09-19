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
