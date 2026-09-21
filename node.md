---
id: experiment:a00-611af49e-5de9db
mint_id: c1fac7abadd5429dbe1a3e99020f53b0
type: experiment
parents:
  - hypothesis:lm-bend2-work-loop-returns-root-done-after-one-call
next_edges: []
confidence: 0.9
edited_by: director-thought
evidence_runs:
  - experiment:a00-611af49e-5de9db
falsifier: per-call wrapper is wrong -- a single work_loop call DOES consume >=99 percent of the reductions, or its first return IS r==0; then the ev=0 reading is displaced for a different reason
line_ceiling: 40
loop: hypothesis:lm-bend2-work-loop-returns-root-done-after-one-call@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "independent rebuild from ~/bend-work/tm52/lifgpu_instr.c with p1.py/p2.py (entry counter at work_loop head + per-call r/tail print), clang-19 -DBEND_CUDA=1, LD_PRELOAD=/data/work/tm49/shim2.so ./p2_lif --gpu 2GB", "expected": "the first DIRECT corpus_eval work_loop call consumes >=99 percent of the 40815244 steps and returns r==0 (the target claim)", "observed": "first call r=360300064868958980 tail=H[task_tail(r)+1]=2 steps=3; calls 2,3 r=0 steps=4; total step=40815244 cubefalse=1 launches=0; stdout 19983", "result": "refuted"}
  - {"conjunct": 1, "class": "wire", "cmd": "same objective build p2_lif, counter incremented at the head of EVERY work_loop entry (not only the corpus_eval call site)", "expected": "the 40.8M host reductions happen OUTSIDE any work_loop call, as the kid reading 1 states", "observed": "wlall=13; WLE n=6,7,8 each steps_since_prev=10203802 and n=10 steps_since_prev=10203801 -> ~40.8M carried by four nested work_loop calls inside cube_run(false), one per net", "result": "refuted (kid reading 1 corrected; target disproof unaffected)"}
  - {"conjunct": 3, "class": "gate", "cmd": "independent emit: ~/.bend/bin/bend p2_lift.bend -o p2_lift_raw.c; p2.py; clang-19 -DBEND_CUDA=1; LD_PRELOAD=shim2 ./p2_lift --gpu 2GB", "expected": "a lifted 4-net fork (four top-level net!(7) roots) first work_loop call returns a continuable r (r nonzero, tail==0) opening the GPU gate", "observed": "first call r=360301164380586752 tail=2; wlall=9; step=40815228 cubefalse=1 launches=0; stdout 20108", "result": "refuted (lane stays closed)"}
  - {"conjunct": 2, "class": "wire", "cmd": "independent rebuild from ~/bend-work/tm52/pow2g_instr.c with p2.py; LD_PRELOAD=shim2 ./p2_pow --gpu 1GB", "expected": "pow2g first call is r nonzero with tail==0 (the only gate shape) and launches", "observed": "first call r=360289069752681220 tail=0; wlall=4; step=25 cubefalse=0 launches=4; stdout 16777216", "result": "confirmed"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: c964393653255b08
season: 2
title: "Bend2 lif_gpu hop4: first work_loop call is NOT the reduction and does NOT return r==0 -- it returns r nonzero with task_tail(r)+1=2, so task_deal plus cube_run-false drains all 40.8M host steps in one call; pow2g first return is r nonzero with tail=0 and launches; lifting the 4-net fork to four top-level roots still yields tail=2 and 0 launches"
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-611af49e-5de9db

## Experiment

Hop 4: per-`work_loop`-call instrumentation for `lif_gpu` vs `pow2g` on GPU2070S,
plus one fixability probe. Runtime rebuild only (the `.bend` body is untouched
except for the lifted variant), 0 USD compute, `nice 19`.

Instrumentation kept TM.52's gate counters exactly where they were and added one
per-`work_loop` wrapper on top (`instr3.py` over `lifgpu_inst2.c` / `pow2g_inst2.c`):
`n_step` at the head of every `WL_CASE` reduction body, `n_cubefalse` at `cube_run()`
entry when `!gpu`, and a per-call line printing `r` and `tail = H[task_tail(r)+1]`
(or `-1` for `r==0`), steps consumed, `cube_run(false)` consumed, and wall. All
insertions sit inside `#if !DEVICE` -- nvrtc compiles the same text (`#embed __FILE__`)
as device code, and unguarded `fprintf`/`__sync_fetch_and_add` broke `gpu_make` with
`identifier "stderr" is undefined` (a trap worth recording). Rebuild:

```
/usr/bin/clang-19 -DBEND_CUDA=1 -I/usr/local/cuda/include -L/usr/local/cuda/lib64 \
  -std=c11 -O3 lifgpu_i3.c -lpthread -lm -lcuda -lnvrtc -o lifgpu_i3
LD_PRELOAD=<rig>/tm49/shim2.so nice -19 ./lifgpu_i3 --gpu 2GB   # ~49 s
```

The fixability probe is `lif_lift.bend`: the same LIF body, but the 4-net fork is
lifted out of the sequential `batch()` recursion into four independent `net!(7)` roots
directly under `main`.

## Evidence

Raw rows, commands, md5s and the launch controls: `.agi/sessions/iter-TM.62/a00-611af49e/raw/RAW.txt`.

| program | call | r | tail=H[task_tail(r)+1] | steps in call | cube_run(false) | launches | wall |
|---|---|---|---|---|---|---|---|
| `lifgpu_i3` | 1 | **nonzero** | **2** | 3 | 0 | 0 | 0.000006 s |
| `lifgpu_i3` | 2 | 0 | - | 4 | 0 | 0 | 0.000001 s |
| `lifgpu_i3` | 3 | 0 | - | 4 | 0 | 0 | 0.000000 s |
| `lifgpu_i3` total | | | | **40,815,244** | **1** | **0** | 48.945 s (user 48.75) |
| `pow2g_i3` | 1 | nonzero | **0** | 2 | 0 | | 0.000005 s |
| `pow2g_i3` | 2 | 0 | - | 15 | 0 | | 0.000179 s |
| `pow2g_i3` | 3,4 | 0 | - | 4 | 0 | | 0.000000 s |
| `pow2g_i3` total | | | | 25 | **0** | **4** | 0.451 s |
| `lift_i3` | 1 | nonzero | **2** | 2 | 0 | 0 | 0.000006 s |
| `lift_i3` | 2,3 | 0 | - | 4 | 0 | 0 | 0.000001 s |
| `lift_i3` total | | | | 40,815,228 | **1** | **0** | 27.467 s (user 53.97) |

TM.52's counters are unchanged by the added wrapper: `lifgpu_i3` still prints
`call=3 r=3 tail0=2 tailnz=1 ev=0 bangs=0`, `pow2g_i3` still `call=3 r=4 tail0=4 ev=1 bangs=1`.
stdout is byte-identical to the prebuilt controls (19983 / 16777216), launches are 0 / 4:
no heisenbug.

### Reading

1. **The bulk of the LIF run is not in the DIRECT `corpus_eval` call.** Its three wrapped
   calls consume 3/4/4 reduction-case entries; the 40.8M host reductions happen inside
   the ONE `cube_run(H,false)` (`cubefalse=1`), carried by FOUR nested `work_loop` calls at
   ~10.2M each (parent probe: WLE n=6,7,8 `steps_since_prev=10203802`, n=10 `=10203801`) --
   the four nets evaluated concurrently on the host pool. So the whole program DOES reduce
   in `work_loop`, just not in the one call whose reply the gate is read after; this
   supersedes the earlier "not in a work_loop call" phrasing.
2. **`lif_gpu`'s first return is not `r==0`.** It is `r != 0` with `tail = 2`. The `r==0`
   returns are calls 2 and 3, which belong to the two later `corpus_eval` entries (the
   `IO.print` / `IO.halt` continuations), not to the program body.
3. The only reply shape that reaches `t = r; if (io_gpu && fid_bangs(...))` is `r != 0`
   **and `tail == 0`**. `pow2g`'s first call is exactly that (`tail=0` -> gate -> 4 launches);
   `lif_gpu` never produces it (`tail=2`). So the branch is skipped because the LIF reply
   is a non-frontier reply, which routes to `task_deal(H, r, ...)` + `cube_run(H,false)`
   (the host pool doing all 48 s) and then breaks. `r==0`/`root_done` is the *IO tail*, not
   the cause at the program body.
4. **The lifted fork does not open the lane.** First call still `tail=2`, `cubefalse=1`,
   `cuLaunchKernel=0`. This is the hypothesis's own third falsifier ("the program shape
   cannot be fixed at the Bend source level -> the lane closes"). Secondary finding:
   lifting does parallelise on the *host* (user 53.97 / wall 27.47 ~ 2.0x) where `lif`
   stays single-threaded (48.75 / 48.95 ~ 1.0x) -- raising the roots lets the pool spread
   the four nets even though no kernel launches.
## Verdict

`disproved` for the hypothesis as written. Its core claim (and its title's) -- `lif_gpu`'s
`work_loop` returns `r == 0` (root_done) after ONE call that consumed >= 99 % of the
interactions -- is false on both counts: the first call consumes 3 of 40,815,244 steps
(<0.001 %) and returns `r != 0`. Its own first falsifier ("lif_gpu first call returns
`r != 0` ... record which condition") fires, and the recorded condition is `tail=2`, i.e.
`H[task_tail(r)+1] != 0`. The GPU lane stays closed for this workload (lift probe
confirms the shape is not fixable by lifting the fork), but the mechanism is
"non-frontier first reply -> host cube drain", not "root_done in the first call".

Corrected claim for a next hop: for `lif_gpu` the first `corpus_eval` reply is a task with
`task_tail(r)+1 = 2`, so `cube_run(H,false)` drains the whole 4-net corpus on the host in
one call; `pow2g`'s first reply has `task_tail(r)+1 = 0` and carries bangs, which is the
only path to `fid_bangs` and `cuLaunchKernel`.

## Agent Notes
Per-call wrapper over TM.52 instrumentation: lif_gpu call 1 consumes 3/40.8M steps and returns r!=0 with tail=H[task_tail(r)+1]=2 (NOT r==0); cube_run(false) entered once drains all 40.8M host steps (the 48 s); pow2g call 1 returns r!=0 with tail=0 (the gate shape) and launches 4; lifting the 4-net fork to four top-level roots still gives tail=2 and 0 launches. Hypothesis disproved: mechanism is a non-frontier first reply, not root_done in the first call.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-703c074e, TM.62).

(1) WHAT THE INSTRUCTION SAID: "A kid's tests are its CLAIM, not your evidence ... read each kid's DIFF ... Run one negative probe per claim conjunct yourself and record them as probes: ... a kid that passes its own tests and fails your probe is lean_disproved with the probe named."

(2) WHAT THE MACHINE ACTUALLY DOES: the round DIFF is one new node file, .agi/nodes/experiment/a00-611af49e-5de9db.md (git status clean after the kid's done). The raw rows the kid names are at .agi/sessions/iter-TM.62/a00-611af49e/raw/RAW.txt. I rebuilt MY OWN instrumented runtimes from TM.52's emitted C (lifgpu_instr.c, pow2g_instr.c) with a DIFFERENT insertion: an entry counter at the head of EVERY work_loop (p1.py/p2.py), not only the corpus_eval call site, plus per-call r and tail. Observed: p2_lif --gpu 2GB -> direct call 1 r=360300064868958980 tail=2 steps=3, calls 2,3 r=0, wlall=13, step=40815244, cubefalse=1, launches=0; four NESTED work_loop calls inside cube_run(H,false) carry about 10.2M each (WLE n=6,7,8 steps_since_prev=10203802, n=10 =10203801). p2_pow --gpu 1GB -> call 1 r=360289069752681220 tail=0, wlall=4, step=25, launches=4. Independent emit of the lifted variant (p2_lift.bend -> p2_lift) -> call 1 tail=2, wlall=9, step=40815228, launches=0.

(3) THE NEAR MISS: the kid wrapped work_loop ONLY at the corpus_eval call site, saw 3 tiny calls plus the 40.8M total, and read it as "NO work_loop call ever carries the bulk ... the 40.8M host reductions happen inside cube_run(H,false)". That sentence satisfies the surface (cube_run drains) and loses the mechanism: cube_run's host pool CALLS work_loop, and the four about-10.2M intervals ARE those nested calls. A reader would take the kid's line to mean work_loop is not where the host reduction lives; it is exactly where it lives. The target's disproof itself is unaffected and independently reproduced.

(4) DEVIATION: none. I corrected reading 1 in place through write.py and recorded 4 probes (target conjunct 1 refuted by both the per-call row and the nested-call wire probe; the kid's supporting "not in a work_loop call" refuted; lift conjunct refuted; pow2g gate shape confirmed).

VERDICT: accepted, disproved stands. The target's own first falsifier fires (first call r != 0; recorded condition tail=2), the corpus is drained on the host by 4 concurrent nested work_loop calls inside one cube_run(H,false), and the lifted 4-net fork still yields tail=2 with 0 launches -- the lane stays closed for this workload.
<!-- THOUGHT:END -->

rr-tm-62 verify stage traceability gap: the reading-1 correction (four nested work_loop calls at ~10.2M each, WLE n=6,7,8 steps_since_prev=10203802, n=10=10203801) cites rows present only in parent session a00-703c074e (output.log/trajectory.jsonl/thought.txt), not in this experiment own raw/RAW.txt, and that parent session is not listed as an evidence_run. This experiment own raw file cannot independently verify its central mechanism correction. Residue severity only per rr-tm-62 verify_TM.62.json (final_recommendation accept_with_residue); disproof itself independently reproduced and stands.
