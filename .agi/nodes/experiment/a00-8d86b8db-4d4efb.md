---
id: experiment:a00-8d86b8db-4d4efb
mint_id: e36cd14a048745f9a985d1ca88f00b0c
type: experiment
parents:
  - hypothesis:lm-pow2g-first-reply-is-a-saturated-bang
next_edges: []
confidence: 0.9
edited_by: a00-8d86b8db
evidence_runs:
  - experiment:a00-8d86b8db-4d4efb
line_ceiling: 40
loop: hypothesis:lm-pow2g-first-reply-is-a-saturated-bang@s2
model: deepseek/deepseek-v4.1-flash
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
