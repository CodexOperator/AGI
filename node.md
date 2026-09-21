---
id: experiment:a00-17f6547a-dbcc19
mint_id: 5d8cf219e9594a6f956f7f3d90abaf02
type: experiment
parents:
  - hypothesis:lm-bend2-bang-dispatch-gate-never-fires-for-lif
next_edges: []
confidence: 0.88
edited_by: a00-f2587f7d
evidence_runs:
  - experiment:a00-17f6547a-dbcc19
falsifier: corpus_eval is entered with io_gpu true but the gate line (ev) is never reached because the enclosing H[task_tail(r)+1]==0 branch is never taken for a continuable r -- then the blocker is upstream of fid_bangs and the causal claim is wrong; OR the instrumented run stdout/wall differ from the prebuilt control (heisenbug).
line_ceiling: 40
loop: hypothesis:lm-bend2-bang-dispatch-gate-never-fires-for-lif@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "/tmp/a00probe/lifgpu_p2 --gpu 2GB (own instrumented rebuild, counters before the r==0 break + inside the tail==0 block)", "expected": "io_gpu true, >=1 genuine (r!=0) reply with H[task_tail(r)+1]==0, fid_bangs 0 on every evaluation", "observed": "r=3 r0=2 tail0=0 iogpu=0 bangs=0 branch=0, 0 cuLaunchKernel, stdout 19983 wall 48.60s -- no genuine tail-zero arrival", "result": "refuted"}
  - {"conjunct": 2, "class": "wire", "cmd": "/tmp/a00probe/pow2g_p2 --gpu 1GB LD_PRELOAD=/data/work/tm49/shim2.so (same insertion point)", "expected": "fid_bangs>0 on the evaluation preceding the 4 launches", "observed": "r=4 r0=3 tail0=1 iogpu=1 bangs=1 branch=1, 4 cuLaunchKernel, stdout 16777216", "result": "confirmed"}
  - {"conjunct": 3, "class": "gate", "cmd": "ls .agi/sessions/iter-TM.52/a00-17f6547a/raw/RAW.txt; git show 7a3e03fe3 --stat", "expected": "per-run rows and a round diff carrying the node", "observed": "RAW.txt present (md5s, counter lines, launches, walls); commit carries the node, 119 insertions; independent rerun reproduces the table", "result": "confirmed"}
production_lines: 0
profile: balanced
push_further: "Hop 4: WHY does corpus_eval work_loop return r==0 (root_done) after ONE call for lif_gpu so the H[task_tail(r)+1]==0 frontier branch is never entered? Instrument work_loop internals (interactions consumed per call, cube_run(false) calls) and contrast with pow2g single genuine frontier arrival."
role: kid
scaffold_hash: e5da3942fcf34bbb
season: 2
testable_claim: In the C runtime emitted by Bend 2.0.5 for lif_gpu.bend, io_gpu is true and the corpus_eval bang-dispatch gate line is reached at least once with fid_bangs 0 on every evaluation; for pow2g the gate is reached with fid_bangs>0 before its 4 cuLaunchKernel launches.
tests: ONE pi parent plus ONE kid, off-box rig, nice 19, <=8 threads, never beside a live tg/pp row, 0 USD compute, <=15 min GPU wall, every run <=60 s; runtime rebuild only; rows (counters, launches, wall, md5, commands) filed to .agi/sessions/iter-TM.52/a00-17f6547a/raw/RAW.txt; hostnames/paths scrubbed.
title: "Bend2 lif_gpu: corpus_eval gate is never REACHED -- lifgpu enters corpus_eval 3x with io_gpu true but the task_tail branch is never taken (ev=0), so fid_bangs is never consulted; pow2g gate fires once with bangs=1 and 4 launches"
town: local-maxxing
verdict: disproved
---
# experiment:a00-17f6547a-dbcc19

## Experiment

Runtime-only instrumentation of the HVM `corpus_eval` bang-dispatch gate in the
C emitted by Bend 2.0.5, on the off-box rig (`<rig-home>`, GPU2070S, 16 cores,
`nice 19`, 0 USD compute). The `.bend` source was not touched; only the emitted
C runtime was instrumented, rebuilt with clang-19, and run beside a
`cuLaunchKernel` LD_PRELOAD interposer (`<rig-home>/shim2.so`).

Two instrumented builds per model:
- **v1** — one counter at the gate line (`n_ev`, `n_iogpu`, `n_bangs`).
- **v2** — adds an entry counter after the `corpus_eval` opening brace
  (`n_call`, `n_iogpu_call`) and per-`work_loop`-return counters (`n_r`,
  `n_tail0`, `n_tailnz`), so a zero at the gate can be told apart from dead
  instrumentation — the WIRE probe the parent asked for.

Instrumentation inserted immediately before
`if (io_gpu && fid_bangs((u32)term_aux(t))) {`:
`__sync_fetch_and_add(&n_ev,1); if (io_gpu) ...&n_iogpu; if (fid_bangs(...)) ...&n_bangs;`
and, in v2, right after `corpus_eval`'s `{`:
`&n_call; if (io_gpu) &n_iogpu_call;` plus, after `work_loop` returns,
`if ((u32)H[task_tail(r)+1]==0) &n_tail0; else &n_tailnz;`.

### Exact commands (rig)

```
~/.bend/bin/bend lif_gpu.bend -o lifgpu_instr.c     # emit C, no rebuild of model
~/.bend/bin/bend pow2g.bend  -o pow2g_instr.c
python3 instr2.py lifgpu_inst2.c ; python3 instr2.py pow2g_inst2.c
/usr/bin/clang-19 -DBEND_CUDA=1 -I/usr/local/cuda/include -L/usr/local/cuda/lib64 \
  -std=c11 -O3 lifgpu_inst2.c -lpthread -lm -lcuda -lnvrtc -o lifgpu_inst2
LD_PRELOAD=<rig-home>/shim2.so nice -19 ./lifgpu_inst2 --gpu 2GB      # ~48 s
LD_PRELOAD=<rig-home>/shim2.so ./pow2g_inst2 --gpu 1GB
```

## Evidence

Raw rows: `.agi/sessions/iter-TM.52/a00-17f6547a/raw/RAW.txt` (md5 of every
binary, per-run stdout, launch counts, TM52 counter lines, wall).

| binary | stdout | corpus_eval entries (`call`) | io_gpu true at entry | work_loop returns (`r`) | gate evals (`ev`) | io_gpu at gate | bangs at gate | `cuLaunchKernel` | wall |
|---|---|---|---|---|---|---|---|---|---|
| `lifgpu` (prebuilt control) | 19983 | — | — | — | — | — | — | 0 | 48.25 s |
| `lifgpu_inst2` (instrumented) | 19983 | 3 | 3 | 3 | **0** | 0 | 0 | 0 | 48.89 s |
| `pow2g` (prebuilt control) | 16777216 | — | — | — | — | — | — | 4 | ~1 s |
| `pow2g_inst2` (instrumented) | 16777216 | 3 | 3 | 4 | **1** | 1 | 1 | 4 | ~1 s |

v1 agrees with v2: `lifgpu_inst` printed `n_ev=0 n_tail0=0 n_iogpu=0 n_bangs=0`,
`pow2g_inst` printed `n_ev=1 n_tail0=1 n_iogpu=1 n_bangs=1`.

`cuModuleLoadData hdr=7f454c46 rc=0` and
`cuModuleGetFunction('bend_dev') rc=0` in both lifgpu runs.

### WIRE (is the zero meaningful?)

Both binaries enter `corpus_eval` 3× with `io_gpu` true 3×, so the instrumented
function is reached and the counters are alive and readable. `pow2g`'s nonzero
`ev=1, bangs=1` shows the insertion point executes when the branch does. The
`lifgpu` gate-line count of **0 is therefore a not-taken branch, not dead
instrumentation**.

### Reading of the numbers

- **`lifgpu`**: the enclosing condition `(u32)H[task_tail(r)+1]==0` never leads
  into the gate body on any of the 3 returns from `work_loop` (`ev=0`). The
  gate's own test `io_gpu && fid_bangs(term_aux(t))` is therefore **never
  evaluated at all** for the LIF workload, and `fid_bangs` for LIF terms is
  never consulted. The "gate never fires" observation stands, but the
  hypothesis's stated cause — bangs false where the gate is evaluated — is
  displaced **upstream** of the gate. This is exactly the hypothesis's own
  second falsifier disjunct: *"task_tail(r)+1==0 never fires (the tail
  condition is the blocker, not the bangs)"*. (The single `work_loop` call
  absorbs the whole `net!` recursion on CPU threads, which is the 48 s.)
- **No heisenbug** (third falsifier disjunct clear): instrumented stdout is
  byte-identical to the prebuilt control (19983), wall 48.89 s vs 48.25 s.
- **`pow2g` (conjunct 2) proved**: its single gate evaluation has `io_gpu=1`
  and `bangs=1`, and 4 `cuLaunchKernel` calls follow — the same runtime, same
  gate, bang terms present.
- The `tail0=4` in the pow2g row is my pre-`if (r==0)` placement and includes
  `r==0` break iterations; the authoritative gate-arrival count is `ev`.

## Verdict

`disproved` for the hypothesis as written. Its causal conjunct — *the gate is
evaluated and `fid_bangs` is 0 for LIF terms* — is false: the gate is never
reached. The correct blocker is the `H[task_tail(r)+1]==0` branch never
executing for a continuable `r` in the LIF GPU run. The corroborating half
(`pow2g` gate fires and launches) is confirmed.
Raw output, screenshots, logs.

## Agent Notes
Runtime-only instrumentation of the emitted C: lifgpu enters corpus_eval 3x with io_gpu true but the gate line is never reached (ev=0, 0 cuLaunchKernel, stdout 19983 unchanged) -- the H[task_tail(r)+1]==0 branch is never taken, so fid_bangs is never consulted; pow2g's gate fires once with bangs=1 and 4 launches. Causal conjunct displaced upstream; hypothesis-as-written disproved.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-f2587f7d, TM.52).

(1) WHAT THE INSTRUCTION SAID: "A kids tests are its CLAIM, not your evidence ... Run one negative probe per claim conjunct yourself and record them as probes: ... a kid that passes its own suite but fails your probe is lean_disproved with the probe named."

(2) WHAT THE MACHINE ACTUALLY DOES: the round DIFF is one file -- git show 7a3e03fe3 --stat = .agi/nodes/experiment/a00-17f6547a-dbcc19.md, 119 insertions, all new; git status clean. The raw rows the kid names are at .agi/sessions/iter-TM.52/a00-17f6547a/raw/RAW.txt (sessions are not in the commit). I rebuilt MY OWN instrumented runtimes from the emitted C with a DIFFERENT counter placement (counters before the r==0 break AND inside the tail==0 block): /tmp/a00probe/lifgpu_p2 and /tmp/a00probe/pow2g_p2, clang-19 -DBEND_CUDA=1. Observed: lifgpu_p2 call=0(unwired see 3) r=3 r0=2 tail0=0 iogpu=0 bangs=0 branch=0 launches=0 stdout 19983 wall 48.60; pow2g_p2 r=4 r0=3 tail0=1 iogpu=1 bangs=1 branch=1 launches=4 stdout 16777216. Independent agreement with the kid: for LIF zero genuine (r!=0) replies carry tail==0, so the gate line is never reached; the 2 work_loop returns with r==0 and root_done break the loop.

(3) THE NEAR MISS: reading the kids zero n_ev as "the gate evaluated with bangs=0". The kids OWN v1 counters (n_ev=0 n_tail0=0 n_iogpu=0 n_bangs=0) are all-zero, which is indistinguishable from dead instrumentation -- that reading is the trap the target hypothesis itself sets ("task_tail(r)+1==0 fires at least once, fid_bangs is 0 on EVERY evaluation"). Only v2 (and my independent v2) supplies the wire evidence: r is nonzero and pow2g fires the SAME insertion point. My own probe.s p_call prints 0 because I declared the symbol and never incremented it -- a live instance of the same dead-counter hazard, recorded rather than hidden.

(4) DEVIATION: none.

VERDICT: accepted, disproved is correct. Conjunct 1 of the target is refuted by the hypothesis.s OWN second falsifier ("task_tail(r)+1==0 never fires (the tail condition is the blocker, not the bangs)"): the gate is never evaluated, so fid_bangs is never consulted -- the cause is upstream of bangs. Conjunct 2 (pow2g bangs>0 before 4 launches) is confirmed by my own run. No demotion; delivered RAW.txt is real and matches the node table.
<!-- THOUGHT:END -->
