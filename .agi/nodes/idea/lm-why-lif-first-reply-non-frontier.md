---
id: idea:lm-why-lif-first-reply-non-frontier
mint_id: 887eec2b3fac4e57ba0b509e6deb6969
type: idea
parents:
  - hypothesis:lm-bend2-work-loop-returns-root-done-after-one-call
next_edges: []
edited_by: why-stage
scaffold_hash: 8e725babe444c13e
season: 2
thought_session: iter-TM.60
title: Why does lif_gpu's first corpus_eval reply carry task_tail(r)+1=2 instead of the tail=0 frontier that opens the GPU gate -- is it inherent to the 4-net sequential batch recursion, or an artifact of how the corpus is constructed?
town: local-maxxing
---
# idea:lm-why-lif-first-reply-non-frontier

## Idea

scale: small (extension of the TM.62 lif/bend2 lane).

### The measured failure (what happened, not what was hoped)
TM.62 disproved `hypothesis:lm-bend2-work-loop-returns-root-done-after-one-call`.
Per `experiment:a00-611af49e-5de9db` (verdict: disproved) and its independent
reproduction in parent session a00-703c074e:

- `lif_gpu` (`lifgpu_i3`, 4-net sequential `batch()` recursion): first DIRECT
  `corpus_eval` `work_loop` call returns `r != 0` with `task_tail(r)+1 = 2`,
  consuming 3 of 40,815,244 steps. The 40.8M host reductions are carried by
  FOUR nested `work_loop` calls inside ONE `cube_run(H,false)` (~10.2M each;
  WLE n=6,7,8 `steps_since_prev=10203802`, n=10 `=10203801`), 48.9 s wall,
  `launches=0`.
- `pow2g` (`pow2g_i3`): first call returns `r != 0` with `task_tail(r)+1 = 0` --
  the ONLY reply shape that reaches `if (io_gpu && fid_bangs(...))` -- 25 steps,
  `launches=4`.
- Lifted 4-net fork (`lif_lift.bend`, four top-level `net!(7)` roots under
  `main`): first call STILL `tail=2`, `cubefalse=1`, `launches=0`. The host
  parallelises (user 53.97 / wall 27.47 ~ 2.0x) but no kernel launches.

So the question is not whether the lane closes (it does), but WHY the LIF
program's first reply is a non-frontier task (`tail=2`) rather than a frontier
(`tail=0`) -- what in the program shape or the corpus construction makes the
first reply carry a non-empty tail.

### Candidate causes (each falsifiable)
1. INHERENT to the 4-net sequential batch recursion: the outer `batch()`
   recursion is a chain, so the first reducible task always has a pending
   continuation -> `tail != 0`. FALSIFIED BY: any LIF variant whose first reply
   is `tail=0` (e.g. a 1-net or 2-net reduction) -- if a 1-net variant gives
   `tail=0`, the tail is a function of arity, not of "sequential recursion" in
   general.
2. ARTIFACT of corpus construction: the net encoding/order or the LIF
   weight/neuron layout creates pending work. FALSIFIED BY: rebuilding with a
   reordered/restructured corpus that STILL yields `tail=2`. (The round already
   tried lifting the fork and still got `tail=2` -- evidence against the
   fork-lift axis, not against corpus layout.)
3. `task_tail` mis-read: `task_tail(r)` counts something other than frontier
   depth for LIF's task encoding, so `tail=2` does not mean "non-frontier".
   FALSIFIED BY: reading the runtime's `task_tail` definition and showing that
   `tail=2` IS the non-frontier shape.

### Evidence
`experiment:a00-611af49e-5de9db` (disproved); parent session a00-703c074e
(independent rebuild); raw rows `.agi/sessions/iter-TM.62/a00-611af49e/raw/RAW.txt`;
gate `comp.ts:5111-5135`, `fid_bangs(x) = FID_FLAG_T[x] & 1` (`comp.ts:3499`),
documented in sibling `experiment:a00-fb08ab32-529654` (~L180-196).
Traceability residue: the "four nested calls" correction cites rows not present
in the round's own RAW.txt (they live in parent session a00-703c074e).
