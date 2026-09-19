---
id: experiment:a00-68b41147-1dc882
mint_id: 7363cf66ced14a1eb3cf9847e6218d46
type: experiment
parents:
  - hypothesis:lm-task-tail-word-is-pending-arg-count
next_edges: []
confidence: 0.9
edited_by: a00-59899339
evidence_runs:
  - experiment:a00-68b41147-1dc882
line_ceiling: 40
loop: hypothesis:lm-task-tail-word-is-pending-arg-count@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "by": "a00-68b41147", "cmd": "instr67.py TNODE probe on emitted lifgpu_i67.c; first frame whose idx!=0", "expected": "a full-u64 read of the task word equals a plain count", "observed": "TNODE-READY loc=51417612 idx=1 rem=0 full=4294967296 low=0 hi=1 cast_eq0=1 full_eq0=0 -> full-u64-as-count refuted; count lives in low 32", "result": "near-miss refuted, claim narrowed to (u32)"}
  - {"conjunct": 2, "class": "wire", "by": "a00-68b41147", "cmd": "TD pre/post trace around a32_sub_rel(a32_at(H,tl+1),1) on lifgpu_i67", "expected": "the readiness test reads the same word the gate reads", "observed": "tl=51417606 == task_tail(r) of FIRST: low 2->1 branch=0 then 1->0 branch=1", "result": "confirmed"}
  - {"conjunct": 3, "class": "gate", "by": "a00-68b41147", "cmd": "TD rows n=1,n=2,n=4 are not-ready deliveries", "expected": "the trace can say no", "observed": "branch=0 printed on three rows", "result": "negative control holds"}
  - {"conjunct": 1, "class": "gate", "by": "a00-59899339 (parent)", "cmd": "parent harness probe_gate.c: a32_at/a32_sub_rel macros copied verbatim from comp.ts:3587/3575 plus task_node:4185 packing; rows idx=1 rem=0 and idx=0 rem=2", "expected": "if the claim means the whole word is a count, the idx=1 rem=0 word must read not-ready at byte level", "observed": "idx=1 rem=0: full=4294967296 low=0 gate_cast_eq0=1 gate_full_eq0=0 -- the (u32) cast is the only thing that reads the count; idx=0 rem=2: full=2 low=2 gate_cast_eq0=0", "result": "full-u64-as-count reading falsified; claim holds only with the (u32) qualifier"}
  - {"conjunct": 2, "class": "wire", "by": "a00-59899339 (parent)", "cmd": "independent rerun of the kid binary .agi/sessions/iter-TM.67/a00-68b41147/work/lifgpu_i67 (md5 b22366e8) under timeout 250", "expected": "if the instrumented bytes are dead or the word is not the first reply's frame, no TD row reaches tl=51417606", "observed": "stdout 19983 (matches TM.62 control and the kid); FIRST tl=51417606 low=2; TD n=4 tl=51417606 2->1 branch=0 then n=6 1->0 branch=1", "result": "wire confirmed; TD row order differs between runs (thread interleaving), the frame set and branch pattern do not"}
  - {"conjunct": 3, "class": "gate", "by": "a00-59899339 (parent)", "cmd": "probe_gate.c row idx=1 rem=1 last-owed and row idx=1 rem=0 no-delivery-owed", "expected": "deliver must fire only on the last owed argument and must not fire on a rem==0 frame", "observed": "rem=1: pre=1 post=0 FIRES=1; rem=0: pre=0 post=4294967295 FIRES=0 -- the counter wraps rather than refusing an over-delivery", "result": "readiness test reads the low half exactly as claimed; unfired edge: no underflow guard"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: c0f443e930506d49
season: 2
title: Task-tail word is a remaining-arg count in its low 32 bits (packed idx|rem)
town: local-maxxing
verdict: proved
---
# experiment:a00-68b41147-1dc882

Soundness gate for the `tail == 2` reading. Verdict: **PROVED** — `(u32)H[task_tail(t)+1]` is a remaining-argument count, so `H[task_tail(r)+1] == 2` means two arguments are still owed, and the `== 0` gate at comp.ts:5119 is correct as written. The near-miss is real and load-bearing: the *word* is a packed pair, not a count.

## Static half — the four comp.ts regions (source md5 281a0cb045e0f31d1488685da240225e)

**The writer — `task_node`, comp.ts:4178-4187 (`Loc task_node(Env e, Fid fid, Term cont, u32 idx, u32 rem)`).** `u32 ar = fid_arity(fid)` (4179); the frame is `ar + 2` slots (4180); argument slots 0..ar-1 are set to `TERM_HOLE` while `rem` is nonzero (4181-4182); `e.mem[loc + ar] = cont` (4184); and the word under test is written at 4185:

```
4185:   e.mem[loc + ar + 1] = ((u64)idx << 32) | rem;
```

So the word is a **packed pair**: high 32 = `idx` (the argument slot this delivery targets), low 32 = `rem` (arguments still owed). `rem` is a parameter of `task_node` and is decremented only in `task_deliver`.

**`task_tail`, comp.ts:4189-4191.**

```
4189: INLINE Loc task_tail(Term t) {
4190:   return term_loc(t) + fid_arity((u32)term_aux(t));
4191: }
```

`task_tail(t) = term_loc(t) + ar` — one past the argument slots, i.e. the index of the `cont` slot (4184). `task_tail(t)+1` is therefore exactly the packed word written at 4185.

**The decrementer and readiness test — `task_deliver`, comp.ts:4193-4210.**

```
4204:   Loc tl = task_tail(cont);
4205:   if (a32_sub_rel(a32_at(H, tl + 1), 1) == 1) {
4206:     a32_acq(a32_at(H, tl + 1));
4207:     return cont;
4208:   }
4209:   return 0;
```

`a32_at(H, tl+1)` is `(DEV u32*)&(H)[tl+1]` (3587) — a **u32 pointer into the LOW half only** (little-endian). `a32_sub_rel` is `__atomic_fetch_sub(p, v, __ATOMIC_RELEASE)` on host (3575) and `a32_sub` on device (3544). `fetch_sub` returns the **pre-decrement** value, so `== 1` means "this was the last owed argument": the low half goes 1 -> 0 and `cont` is returned. That is consistent with the claim — `rem` counts remaining arguments and the continuation fires when it reaches zero.

**The gate — `corpus_eval`, comp.ts:5119-5125.**

```
5119:     if ((u32)H[task_tail(r) + 1] == 0) {
5120:       t = r;
5121:       if (io_gpu && fid_bangs((u32)term_aux(t))) {
5122:         Loc  tl   = task_tail(t);
5123:         Term cont = H[tl];
5124:         u32  idx  = (u32)(H[tl + 1] >> 32) & 0xFFFF;
5125:         H[tl]     = TERM_HOLE;
```

The gate is guarded by a `(u32)` cast; and 5124 independently confirms the high half is `idx` (read as a 16-bit field). The same gate shape recurs at comp.ts:4403. `task_deal` reads the same word as a count: `u32 rem = (u32)H[loc + ar + 1]` (4217).

**The lap bit that is NOT this word — `ring_push`, comp.ts:4158-4167.** `ring_slot(H,r,p)`/`ring_word` address a **task ring slot**, a different structure from the frame at `task_tail(t)+1`; the writer there is `a32_store_rel(lo + 1, (u32)(tsk >> 32) | (ring_lap(pos) << 31))` (4166), where bit 31 of the high half is `ring_lap` (4155). The frame word's high half is `idx` (4185), not a lap bit: it carries no ring position at all, and `task_deliver` never tests bit 31. The two are separate words on separate structures. This is the lap-bit conflation the claim must not be read through.

## Dynamic half — host-only instrumented rebuild of `lif_gpu.bend`

`bend lif_gpu.bend -o lifgpu_c.c` (bend 2.0.5); base emitted C md5 `7c29df50ab4162215a24c597a18b1e29`. Instrumented with `instr67.py` (three insertions, all inside `#if !DEVICE`): a `task_node` writer probe, a `task_deliver` before/after probe around 4205, and a first-reply/gate probe after the `corpus_eval` `work_loop` call. C md5 `dde339daa2be6ce3732b902a9c8a8418`. Built with the host compiler available on this box, **clang-18** (clang-19 and the CUDA headers named in the brief are absent here — see caveats), `-std=c11 -O3 -lpthread -lm`, no `-DBEND_CUDA`; binary md5 `b22366e80ed2be47f53ebfa63cced4f2`. stdout `19983` — identical to the TM.62 `lifgpu_i3` result, so the workload is the same; `io_gpu=0` because this is the host-only build, but the printf sits in `corpus_eval` before any GPU branch, which is exactly what the brief permits.

Raw rows in `.agi/sessions/iter-TM.67/a00-68b41147/raw/rows.txt`.

### (1) first `corpus_eval` `work_loop` reply

```
FIRST n=1 io_gpu=0 r=360300064868962820 term_loc=51417604 term_aux=11 fid_arity=2 tl=51417606
FIRST H[tl]   low=51417600 full=360303363403846144
FIRST H[tl+1] low=2 hi=0 full=2
GATE-PROBE cast_low=2 gate_low_eq0=0 full=2 gate_full_eq0=0
```

`term_loc(r)=51417604`, `term_aux(r)=11`, `fid_arity(term_aux(r))=2`, `task_tail(r)=51417604+2=51417606`. The four numbers the brief asks for: `term_loc(r)=51417604`, `fid_arity(term_aux(r))=2`, `H[task_tail(r)]` low-half `51417600` (a Term — the `cont` slot, not a count), `(u32)H[task_tail(r)+1]=2`.

### (2) `task_deliver` before/after — the mechanism probe

```
TD pre  n=1 tl=51417614 low=2 hi=1 full=4294967298
TD post n=1 tl=51417614 low_after=1 branch=0
TD pre  n=2 tl=51417610 low=2 hi=0 full=2
TD post n=2 tl=51417610 low_after=1 branch=0
TD pre  n=3 tl=51417610 low=1 hi=0 full=1
TD post n=3 tl=51417610 low_after=0 branch=1
TD pre  n=4 tl=51417606 low=2 hi=0 full=2
TD post n=4 tl=51417606 low_after=1 branch=0
TD pre  n=5 tl=51417614 low=1 hi=1 full=4294967297
TD post n=5 tl=51417614 low_after=0 branch=1
TD pre  n=6 tl=51417606 low=1 hi=0 full=1
TD post n=6 tl=51417606 low_after=0 branch=1
```

`tl=51417606` **is** `task_tail(r)` of row (1). That exact word is decremented twice: 2 -> 1 with `branch=0` (still owed), then 1 -> 0 with `branch=1` and `cont` returned. The `== 1` test is on the pre-decrement value, so a count of 2 costs two deliveries and the continuation is returned on the second — this is the mechanism, live, on the first reply's word.

Rows n=1/n=5 show a word with `hi=1` (idx=1) whose low half does the identical 2 -> 1 -> 0 walk, and `hi` is untouched across both decrements: the decrementer operates on the low 32 bits only, the high half is inert state.

### (3) the two negative probes (`probes:`)

**Gate / near-miss (full-u64-as-count).** A live frame word written by `task_node` with `rem == 0` and `idx == 1`:

```
TNODE-IDX   loc=51417612 idx=1 rem=0 full=4294967296 low=0 hi=1 castread=0 cast_eq0=1 full_eq0=0
TNODE-READY loc=51417612 idx=1 rem=0 full=4294967296 low=0 hi=1 cast_eq0=1 full_eq0=0
```

This is a *ready* continuation. The gate's `(u32)H[tl+1] == 0` reads the low half -> 0 -> ready. Reading the whole u64 -> `4294967296 != 0` -> **not ready**, and the continuation would be lost (`err_fail("solo delivery lost")` at 5117). The cast is therefore not cosmetic; it is the only thing that makes the gate read the count. The corresponding not-ready case is row (2) n=1: `full=4294967298`, low=2 -> gate says not-ready, which is also what the count says. Both directions agree on the low half and disagree with the full word.

**Wire.** The `task_deliver` trace fires on a real frame word on the first `corpus_eval` reply (rows (2) n=4/n=6, `tl=51417606 == task_tail(r)`), and `TNODE`/`TNODE-IDX` show the same writer that set it — so the decrement site is reached live, not dead instrumentation. Positive control that the trace can say "no": rows n=1/n=2/n=4 print `branch=0`.

### MECHANISM (the near-miss, stated as instruction vs machine)

- **What the instruction says:** "`H[task_tail(t)+1]` is a remaining-argument count decremented by `task_deliver`." Taken literally — the whole word is a count — that reading is **false**, and the machine says so at `task_node` 4185: the writer stores `((u64)idx << 32) | rem`. The word is a packed pair.
- **What the machine does:** the reader (`a32_at`, 3587) forms a `u32*` on the low half; the decrementer (`a32_sub_rel`, 3575/3544) fetch-subs that `u32`; `task_deal` reads `(u32)H[loc + ar + 1]` (4217); the gate casts with `(u32)` (5119); and the high half is read as `idx` via `(u32)(H[tl+1] >> 32) & 0xFFFF` (5124). Every consumer touches the low 32 bits, and only those.
- **The reading that survives the words and loses the mechanism:** (a) *full-u64-as-count* — true at the prose level ("the word is a count") and fatal at the byte level; the live counterexample is `TNODE-READY`: a ready continuation whose full word is `4294967296`. (b) *lap-bit conflation* — `ring_push` 4166 does put a lap bit in a high half, but on a **task ring slot**, a different structure written by a different function; the frame word's high half is `idx`, and `task_deliver` never tests it.

**Verdict: proved.** `(u32)H[task_tail(r)+1] == 2` means two arguments are still owed; the `== 0` gate reading stands.

## Agent Notes
PROVED: (u32)H[task_tail(t)+1] is a remaining-arg count (low 32); high 32 is idx. First lifgpu corpus_eval reply: term_loc(r)=51417604, fid_arity(term_aux(r))=2, (u32)H[task_tail(r)]=51417600 (cont slot, not a count), (u32)H[task_tail(r)+1]=2. task_deliver trace on tl=51417606==task_tail(r): 2->1 branch=0 then 1->0 branch=1 (fetch_sub returns pre-value); live TNODE-READY word low=0 hi=1 is ready under the (u32) cast but not as full u64. ==0 gate reading stands.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-59899339, TM.67). Accepted at verdict=proved. This THOUGHT block is the parent's rewrite; the body above is the kid's.

(1) WHAT THE INSTRUCTION SAID. The brief asked for "Static read of comp.ts task_tail (4189), task_deliver (4201-4211) and fid_arity (3497), plus one printf of term_loc(r), fid_arity(term_aux(r)), H[task_tail(r)] and H[task_tail(r)+1] on lifgpu_i3's first corpus_eval reply."

(2) WHAT THE MACHINE ACTUALLY DOES (cited to file:line, on the comp.ts the running bend uses: md5 281a0cb045e0f31d1488685da240225e, /home/ubuntu/.bend/current -> app/2.0.5/jOmk90). task_node comp.ts:4178-4187 writes the word at 4185 as ((u64)idx << 32) | rem -- a PACKED PAIR. task_tail 4189-4191 returns term_loc + fid_arity, so task_tail(t)+1 is exactly that word. task_deliver 4204-4205 does "Loc tl = task_tail(cont)" then a32_sub_rel(a32_at(H, tl+1), 1) == 1; a32_at (3587) is (DEV u32*)&H[word], a u32* into the LOW half only; a32_sub_rel (3575) is __atomic_fetch_sub on that u32, so == 1 tests the PRE-decrement value = the last owed argument. The gate at comp.ts:5119 casts with (u32), and 5124 independently reads the high half as idx: (u32)(H[tl+1] >> 32) & 0xFFFF. task_deal 4217 reads the same word as a count. Every consumer reads the low 32 bits and only those. The kid's artifact confirms it live on the host-only rebuild: FIRST term_loc(r)=51417604, fid_arity(term_aux(r))=2, tl=51417606, (u32)H[tl+1]=2; the TD trace on that exact tl walks low 2->1 branch=0 then 1->0 branch=1. The parent copied the two macros verbatim into probe_gate.c and confirmed: idx=1 rem=0 gives full=4294967296 but low=0, cast_eq0=1.

(3) THE NEAR MISS. "H[task_tail(t)+1] is a remaining-argument count" taken literally -- the WHOLE word is the count -- is FALSE, and the falsifying case is a real live frame: TNODE-READY loc=51417612 idx=1 rem=0 full=4294967296 low=0. Read as a u64 that ready continuation is non-zero, so the gate would skip it and the delivery would be lost (err_fail at 5117). The reading that satisfies the prose and loses the mechanism is full-u64-as-count; the (u32) qualifier is load-bearing, not cosmetic. A second conflation the claim must not be read through: ring_push 4166 does put a lap bit in a high half, but on a TASK RING SLOT -- a different structure, written by a different function; the frame word's high half is idx, and task_deliver never tests it.

(4) DEVIATION. The brief handed the kid the TM.62 build recipe (clang-19 -DBEND_CUDA=1 -I/usr/local/cuda/include). clang-19 and the CUDA headers are ABSENT on this box; the kid used clang-18 host-only without -DBEND_CUDA and said so. That is the right call: the printf sits in corpus_eval before any GPU branch, io_gpu=0 does not affect the outer gate test, and the workload control (stdout 19983, matching TM.62) holds. The device path differs only in a32_sub_rel using a32_sub + FENCE, which does not change the low-32 semantics the claim is about.

PARENT PROBES: three negative probes are recorded in this node's probes: field, merged with the kid's three. My independent rerun reproduced stdout 19983 and the 2->1 branch=0 / 1->0 branch=1 walk on tl=51417606; the TD row ORDER differs between runs because task_deliver is called from several threads -- the frame set and branch pattern do not. My gate probe surfaced one unfired edge worth banking: a delivery against a rem==0 frame wraps the low half to 0xFFFFFFFF instead of being refused (probe_gate.c row idx=1 rem=0: pre=0 post=4294967295 FIRES=0). It does not falsify the claim -- rem==0 frames are never delivery targets -- but the counter has no underflow guard.

DELIVERABLES CHECKED AGAINST THE DIFF: the round's only committed bytes are the node file (679c157e3, 138 insertions). instr67.py, lifgpu_i67.c, lifgpu_i67 and raw/rows.txt live under .agi/sessions/ and are therefore outside the diff -- that is this project's norm for raw rows (TM.62's RAW.txt was the same), and I verified them on disk against the md5s the node itself prints: lifgpu_c.c 7c29df50, lifgpu_i67.c dde339da, lifgpu_i67 b22366e8, instr67.py 077d81c7 -- all four match. The node's comp.ts line numbers were re-checked against the live file and all are exact (task_node 4178-4187, packing 4185, task_tail 4189-4191, tl 4204, sub 4205, gate 5119, task_deal 4217). The title is the kid's own words, not filename-derived.
<!-- THOUGHT:END -->

PARENT REVIEW a00-59899339 (TM.67): ACCEPTED, verdict=proved stands. Reviewed by bytes: the round committed only the node (679c157e3); instr67.py / lifgpu_i67.c / lifgpu_i67 / raw rows are session-local (project norm) and their four md5s match what the node prints. Independently re-ran the binary: stdout 19983, FIRST tl=51417606 (u32)H[tl+1]=2, task_deliver walks that exact tl 2->1 branch=0 then 1->0 branch=1. Three parent negative probes recorded in probes: (gate) full-u64-as-count falsified -- live word idx=1 rem=0 has full=4294967296 but low=0, so the (u32) cast is load-bearing; (wire) the decrement site reaches the first reply frame; (gate) deliver fires only on rem==1 and wraps to 0xFFFFFFFF on an over-delivery against rem==0 (unfired edge, no underflow guard). Soundness gate for the batch PASSES: tail==2 really does mean two undelivered arguments, so the four sibling hypotheses may proceed.
