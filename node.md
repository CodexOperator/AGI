---
id: experiment:a00-8d86b8db-4d4efb
mint_id: e36cd14a048745f9a985d1ca88f00b0c
type: experiment
parents:
  - hypothesis:lm-pow2g-first-reply-is-a-saturated-bang
next_edges: []
confidence: 0.9
edited_by: a00-dd8458a6
evidence_runs:
  - experiment:a00-8d86b8db-4d4efb
line_ceiling: 40
loop: hypothesis:lm-pow2g-first-reply-is-a-saturated-bang@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "bend pow2g.bend -o pow2g.c; apply instr67 anchors (task_node writer + corpus_eval work_loop); clang -std=c11 -O3 -lpthread -lm; run ./pow2g_i", "expected": "pow2g first reply saturated: FID_POW2 arity 1, H[tl+1] low=0", "observed": "FIRST n=1 io_gpu=0 term_aux=1 FID_POW2 fid_arity=1 tl=51417605; H[tl+1] low=0 hi=0 -> saturated", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "re-run TM.67 instrumented lifgpu_i67 host binary and read its FIRST rows", "expected": "lif first reply owes 2: fid_arity 2, H[tl+1] low=2", "observed": "FIRST n=1 term_aux=11 FID_BATCH_J24 fid_arity=2 tl=51417606; H[tl+1] low=2 -> owes 2", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "decode lif first-reply fid 11 against FID_ARITY_T and the named net.fin wrapper hop", "expected": "if the owed 2 sits on net.fin (arity 1) the wrapper is the cause; else the conjunct fails", "observed": "owed 2 sits on FID_BATCH_J24 arity 2, the batch pair-join, NOT net.fin arity 1 -> FALSIFIER B fires", "result": "fail"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: f0b92ae2b93ddfb8
season: 2
title: pow2g first reply is a saturated powder bang task but lif owed 2 is the batch join, not the net.fin wrapper — hypothesis disproved
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-8d86b8db-4d4efb

## Experiment

Built BOTH programs with the same Bend toolchain (bend 2.0.5, `bend <src> -o <src>_c.c`)
into a DEVICE=0 HOST build (`clang -std=c11 -O2 <src>_c.c -lpthread -lm`; no
`-DBEND_CUDA`, no `-DBEND_METAL`), then instrumented each emitted C with one script
`instr70.py` that asserts each of its three anchors occurs exactly once and stops if
not (as directed): (1) the `task_node` writer `e.mem[loc + ar + 1] = ((u64)idx << 32) | rem;`
prints every task creation, (2) the `corpus_eval` `work_loop(...)` call prints the first
reply `r` + `task_tail(r)` + `H[tl+1]`, (3) the `WL_CASE(FID_ENTER)` segment (`u32 war =
fid_arity(f);`) prints the dispatched fid and the owed word at entry. Rows in
`rows70.txt`; script in `instr70.py`; emitted+instrumented C in `pow2g_c.c`, `lifgpu_c.c`.

## What happened

pow2g (`pow2g_i70`, stdout 16777216, rc=0):
- first reply `r`: `term_aux=1 = FID_POW2` (bang), `fid_arity=1`, `tl+1=51417605`,
  `H[tl+1] low=0` -> owes 0, SATURATED. Its task was created `TNODE n=3 ... fid=1 rem=0`.
- first non-main `FID_ENTER`: `term_aux=1 = FID_POW2`, `H[tl+1] low=0` -> saturated too.

lif_gpu (`lifgpu_i70`, stdout 19983, rc=0, 52.8 s host):
- first reply `r`: `term_aux=11 = FID_BATCH_J24` (join), `fid_arity=2`, `tl+1=51417606`,
  `H[tl+1] low=2` -> owes 2. Created `TNODE n=3 ... fid=11 rem=2`.
- first non-main `FID_ENTER`: `term_aux=8 = FID_BATCH`, `H[tl+1] low=0` -> LIF'S FIRST
  ENTERED TASK IS ALSO SATURATED.

`FID_BATCH_J24` is written by `WL_CASE(FID_BATCH)` (lifgpu_c.c L1928) as the two-way join
of `batch(p,s) batch(p, s+...)` — a batch fork/join frame. `net!`/`net.fin`
(`FID_NET`=6 / `FID_NET_K21`=7) is reached only from that same case's leaf branch (`d_0==0`).

Def hops main -> bang fid (line numbers from the copies in this session dir):
- pow2g.bend: main L11-12 applies `pow2!(24n)` directly (bang def L3); hops = 1.
- lif_gpu.bend: main L85-86 -> `batch` (L78) -> `net!` (L80/L75) -> `net.fin` (L76/L71);
  hops = 2 to the bang fid, 3 to net.fin. The wrapper hop exists, but no frame is owed by it.

## Verdict against the falsifiers

- FALSIFIER A (pow2g also enters with owed args): does NOT fire. pow2g's first reply AND
  first entered task are saturated (`H[tl+1] low=0`). Note pow2g does have a rem=2 two-way
  join (`FID_POW2_J4`) — it just is not the first reply; it appears as the 2nd reply.
- FALSIFIER B (lif's owed count not tied to the `net.fin` wrapper hop): FIRES. The owed 2
  sit on `FID_BATCH_J24`, the `batch` fork/join frame — a different frame from `net.fin`
  (and from the top-level call). lif's own first entered task (`FID_BATCH`) is saturated,
  so the wrapper is exonerated as the cause.

Independent reproduction of the TM.67 suspicion, same locs and same fid (11). The
hypothesis's causal half is falsified, so the hypothesis is DISPROVED: the difference
between pow2g and lif is not the number of def hops to the bang def; both programs
create a two-way join frame with owed 2, and the question is which task `work_loop`
returns first (pow2g returns the saturated bang redex first, lif returns the join first).

## Evidence

- Rows: `.agi/sessions/iter-TM.70/a00-8d86b8db/work/rows70.txt`
- Instrumentation: `.agi/sessions/iter-TM.70/a00-8d86b8db/work/instr70.py`
  (anchor-asserted; fails closed if any anchor count != 1)
- Emitted/instrumented C + binaries: `pow2g_c.c`/`pow2g_i70`, `lifgpu_c.c`/`lifgpu_i70`
- Sources: `pow2g.bend`, `lif_gpu.bend` (copies in the same dir)
- Toolchain: bend 2.0.5 at `/home/ubuntu/.bend/bin/bend`; clang 18.1.3; DEVICE=0 host.
Raw output, screenshots, logs.

## Agent Notes
Device0 host build of pow2g and lif_gpu, anchor-asserted instrumentation of task_node + corpus_eval + FID_ENTER. pow2g first reply FID_POW2 H[tl+1]low=0 saturated; lif first reply FID_BATCH_J24 low=2. FALSIFIER B fires: the owed 2 is the batch fork/join frame, not net.fin; lif first entered task FID_BATCH is itself saturated. Hypothesis disproved. Rows in rows70.txt.

Parent review accepted the kid as disproved after the kid own rows and three parent-run probes agreed: pow2g first reply FID_POW2 saturated (owed 0); lif first reply FID_BATCH_J24 owed 2; the owed 2 sit on the batch pair-join frame, NOT the net.fin wrapper (FALSIFIER B fires). Deliverables rows70.txt, instr70.py, pow2g_c.c, lifgpu_c.c, both binaries and both .bend sources are all present in the session work dir.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT THE INSTRUCTION SAID: "One negative probe per claim conjunct, run by YOU, recorded as `probes:`"; and "edit a kid's node in place, and write why the node now says what it says into that node's THOUGHT block".

WHAT THE MACHINE ACTUALLY DOES (built and ran, not read): emitted pow2g's C with bend 2.0.5 (`bend pow2g.bend -o pow2g.c`), applied the same instrumentation as the TM.67 kid (the generic `task_node` writer anchor `e.mem[loc + ar + 1] = ((u64)idx << 32) | rem;` and the `corpus_eval` `work_loop(e, io_stk, t, !BANGS and ...)` call), built host-only with `clang -std=c11 -O3 -lpthread -lm`, and ran it. Result: `FIRST n=1 term_aux=1` (= FID_POW2, arity 1), `H[tl+1] low=0` -- the first reply is the saturated bang def. Re-ran the TM.67 instrumented lif_gpu host binary: `FIRST term_aux=11` (= FID_BATCH_J24, arity 2), `H[tl+1] low=2`. Artifacts under `.agi/sessions/iter-TM.70/a00-dd8458a6/`.

THE NEAR MISS: a reader could accept the kid's `disproved` on the strength of its own rows alone; the step that actually settles conjunct 3 is the arithmetic decode of fid 11 against `FID_ARITY_T` -- the 2 owed args sit on a `FID_BATCH_J24` frame of arity 2 (the batch pair-join), while the named `net.fin` frame has arity 1, so the wrapper is exonerated. The kid performed that decode and so did I; the un-decoded row is the plausible reading that satisfies the words and loses the mechanism.

DEVIATION FROM A STANDING RULE: the parent review section says read the kid's DIFF via `git diff merge-base..<kid-branch>`, while the same brief says "Do not run git at all". I read the changed bytes directly (the node file and its named session artifacts) rather than running any git command. Both are read-only; the direct read is the one that cannot touch the shared tree's index, and the node file IS the changed authored artifact this round.
<!-- THOUGHT:END -->
