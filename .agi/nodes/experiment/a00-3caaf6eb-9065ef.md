---
id: experiment:a00-3caaf6eb-9065ef
mint_id: 9edd58d77b894499bb7a36bc2b07d086
type: experiment
parents:
  - hypothesis:lm-served-9b-long-prompt-prefill-gains-from-larger-ubatch
next_edges: []
confidence: 0.9
edited_by: a00-67c8a71a
evidence_runs:
  - experiment:a00-3caaf6eb-9065ef
line_ceiling: 120
loop: hypothesis:lm-served-9b-long-prompt-prefill-gains-from-larger-ubatch@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "gain>=10pct", "class": "gate", "cmd": "parent probe: re-ran the kid's own driver unmodified (ub_prefill_round.arm; OUT/LOG redirected to .agi/sessions/iter-OSC.11/a00-67c8a71a/probe so its ub.json was never touched) for q8_0 -ub 512 then q8_0 -ub 1024 on the SAME three ~30k wikitext slices, on a quiet box (MemAvailable 11.6 GB, loadavg 4.35 vs the original run's 0.8-11.5 GB / load 10-52); script probe_run.sh, artifact probe/probe_q8.json", "expected": "if the +27.2 pct q8_0 gain is a real -ub lever the ub512 baseline stays ~960 tok/s on a quiet box", "observed": "ub512 1181.9/1186.0/1189.1 tok/s (mean 1185.7, +23.5 pct over the kid's 960); ub1024 1197.6/1202.4/1203.0 (mean 1201.0); paired per-slice gain +1.29 pct with 95 pct CI [+1.03,+1.56] -- clears zero but 7.8x below the 10 pct bar", "result": "refuted"}
  - {"conjunct": "fitted n_ctx >= 32768", "class": "wire", "cmd": "parent probe: read n_ctx_slot from each arm's own llama-server load log (datasets/serving-sweep/2026-09-23-ub/logs/*.log) and cross-checked against OSC.02's recorded KV capacities and the re-run's curl /slots", "expected": "a real -ctk/-ctv flag must change the fitted context (f16 < q8_0 < q4_0) and every arm must fit >= 32768", "observed": "f16 49664, q8_0 75520/68608/56320, q4_0 118784/105728/83712 -- exactly OSC.02's KV capacities, so the KV-type flags reached the server; every arm fits >= 37888 > 32768", "result": "held"}
  - {"conjunct": "L1 KV cost at depth", "class": "gate", "cmd": "parent probe: compare the quiet-box -ub 512 tok/s of the re-measured q8_0 arm against the kid's f16 512 (1228/1143) and q4_0 512 (1173/1147)", "expected": "if q8_0 KV really costs +12.2 pct prefill vs f16 at depth the floor should survive a quiet box", "observed": "q8_0 ub512 quiet-box mean 1185.7, level with f16 ub512 s2/s3 (1185.7) -- the kid's +12.2 pct [-48.6,+73.0] q8_0-vs-f16 cost was the same contended baseline, so at -ub 512 no KV type is measurably slower than f16", "result": "refuted"}
production_lines: 127
profile: balanced
push_further: re-run the f16 and q8_0 -ub 512/1024/2048 arms with 5 trials each on a quiet box (one launcher, back-to-back, no cross-arm pacing) to put a tight interval on the residual ~1-3 pct gain, and test whether the real prefill lever is -b (logical batch) rather than -ub
role: kid
scaffold_hash: f53a2680359032d9
season: 2
title: "OSC.11 REFUTED by parent re-measure: a larger -ub is NOT a >= 10 pct long-prompt prefill lever on the served 9B -- the q8_0 ub1024 +27.2 pct was a contended-baseline artifact (quiet-box re-run +1.29 pct [+1.03,+1.56], baseline 960 -> 1186 tok/s); f16 and q4_0 stay under 6 pct, every arm fits >= 37888, and the JIT-cache proof + n_ctx matrix are kept"
town: local-maxxing
verdict: inconclusive_lean_disproved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-3caaf6eb-9065ef

## Experiment

**Question.** On the served `Qwen3.5-9B-Q4_K_M` (RTX 2070S 8 GB, sm_75) under llama-server with the
router's own model args, does raising the micro-batch from `-ub 512` to 1024 / 2048 (`-b` 2048,
flash attention on) prefill a warm ~30k-token prompt >= 10 pct faster, for at least one KV type among
f16 / q8_0 / q4_0, with the 95 pct paired interval clearing zero and a fitted context >= 32,768?

**T0 guard + restore (`t0_guard.txt`, `restore_proof.txt`).** 2026-09-23T18:25:41Z: router idle
(`n_ctx 49664, is_processing false`), `MemAvailable` 5,566 MB >= 2 GB; `docker stop llama-server`
freed the card to **1 MiB**. Restored 19:49Z: `docker start` + a real `POST /v1/chat/completions`
(`completion_tokens=8`, `prompt_n=13`, `prompt_ms 472.5`), then `GET /slots` -> `n_ctx 49664,
is_processing false`. **The router was up before this report was written.**

**Inputs.** Served GGUF `/data/ml/scratch/osc02/Qwen3.5-9B-Q4_K_M.gguf` (5.68 GB); image
`ghcr.io/ggml-org/llama.cpp:server-cuda`; fresh `docker run --rm` per arm, a distinct port
(18100-18108), the router's `model_args_9b` verbatim (minus `--port` / in-container model path) plus
`-fa on -ctk/-ctv <kv> -ub <ub> -b 2048`, and
`-v /data/ml/scratch/cuda-jit-cache:/root/.nv/ComputeCache`. Three distinct
`wikitext-2-raw/wiki.test.raw` slices of 132,000 bytes each (offsets 10000 / 400000 / 800000, no
prefix reuse; 28,971-31,751 prompt tokens measured) -> `prompt_n / prompt_ms / tok/s` per slice. One
13-token warm-up request precedes them. Driver
`.agi/context/local-maxxing/serve/ub_prefill_round.py` (new, 127 lines), outputs under
`paths.local_maxxing.serving_sweep_ub_out_dir` = `datasets/serving-sweep/2026-09-23-ub/` (`ub.json`,
`logs/`). Arm runs were paced by a scratch launcher because the box was memory-contended.

**T1 -- the (KV type x -ub) matrix, 3 ~30k slices each.**

| arm | load_s | fitted n_ctx | tok/s per slice | mean tok/s |
|---|---|---|---|---|
| f16  / ub 512  | 182.9 | 49,664 | 844 / 1228 / 1143 | 1071.4 |
| f16  / ub 1024 | 79.0  | 45,568 | 1242 / 1232 / 806 | 1093.3 |
| f16  / ub 2048 | 152.3 | 37,888 | 1006 / 387 / 1143 | 845.5 |
| q8_0 / ub 512  | 59.4  | 75,520 | 1002 / 949 / 929 | 959.9 |
| q8_0 / ub 1024 | 27.2  | 68,608 | 1222 / 1219 / 1217 | 1219.6 |
| q8_0 / ub 2048 | 4.1   | 56,320 | 1232 / 1217 / 1214 | 1221.1 |
| q4_0 / ub 512  | 20.5  | 118,784 | 1181 / 1174 / 1147 | 1167.1 |
| q4_0 / ub 1024 | 4.1   | 105,728 | 1206 / 1194 / 1197 | 1199.3 |
| q4_0 / ub 2048 | 27.8  | 83,712 | 1198 / 1217 / 1219 | 1211.2 |

**T2 -- paired gain vs the same KV type at `-ub 512`** (paired per slice, t_0.975 df=2 = 4.303):

| arm | mean gain | 95 pct CI | clears zero | >= 10 pct | fitted n_ctx |
|---|---|---|---|---|---|
| f16  / ub 1024 | +6.0 pct  | [-89.9, +102.0] | no | no | 45,568 |
| f16  / ub 2048 | -16.4 pct | [-131.0, +98.2] | no | no | 37,888 |
| **q8_0 / ub 1024** | **+27.2 pct** | **[+15.6, +38.8]** | **yes** | **yes** | **68,608** |
| **q8_0 / ub 2048** | **+27.3 pct** | **[+17.5, +37.2]** | **yes** | **yes** | **56,320** |
| q4_0 / ub 1024 | +2.8 pct  | [-0.7, +6.2] | no | no | 105,728 |
| q4_0 / ub 2048 | +3.8 pct  | [-2.2, +9.8] | no | no | 83,712 |

**The L1 prefill cost at depth ~30k, at `-ub 512` vs f16** (positive = slower than f16): q8_0
+12.2 pct [-48.6, +73.0]; q4_0 -8.1 pct [-52.5, +36.3]. Both intervals span zero: at this depth no KV
type is measurably slower than f16 in this round.

**T3 -- the persistent-JIT-cache proof.** The first arm's 13-token warm-up (the first CUDA work in a
fresh container) took **185,513 ms**; every later arm's 13-token warm-up, same image, same command,
shared `/root/.nv/ComputeCache`, took **135.5 / 134.2 / 425.3 / 581.3 / 703.3 / 704.9 / 724.6 /
2167.1 ms**. Same shape, same code path, ~1,370x-275x faster once the sm_75 PTX JIT result is on disk
(OSC.09's mechanism, now applied and confirmed).

## Evidence

**Bar by bar (pre-registered falsifier: no arm beats its own `-ub 512` by >= 10 pct with the interval
clearing zero -> `-ub` is not a long-prompt lever).**

- **>= 10 pct gain with the 95 pct interval clearing zero: MET for q8_0** at both 1024 (+27.2 pct
  [+15.6, +38.8]) and 2048 (+27.3 pct [+17.5, +37.2]). The three q8_0 ub512 slices are 1002 / 949 /
  929 and every ub1024 / ub2048 slice is 1214-1232 -- a clean separation, not a single outlier.
- **Fitted context at the winning setting >= 32,768: MET** (q8_0 ub1024 68,608; q8_0 ub2048 56,320;
  every arm in the matrix fits >= 37,888). The gain does not cost the context pi-local needs.
- **The falsifier does not fire**, so the claim as written is supported -- but see the caveats: only
  the q8_0 pair separates, and its ub512 baseline is lower than f16 ub512 and q4_0 ub512, which a
  simple KV-width story does not predict.

**What the matrix also says.** (a) f16 -- the KV type the router actually serves -- shows **no**
`-ub` gain (ub1024 +6.0 pct, interval [-89.9, +102.0]; ub2048 negative). (b) q4_0 is flat at ~+3 pct
with tight intervals that exclude 10 pct. (c) A larger `-ub` costs fitted context monotonically:
f16 49,664 -> 45,568 -> 37,888, q8_0 75,520 -> 68,608 -> 56,320. At `-ub 1024` the context cost is
~8 pct for the +27 pct q8_0 gain; at 2048 it is ~25 pct for the same gain, so 1024 dominates 2048.

**LARGEST SAFE STEP (PROPOSED -- router and config cells untouched).** If and only if a server is run
with `q8_0` KV, `-ub 1024` is the step: +27.2 pct prefill on ~30k prompts at a fitted 68,608 context
(2048 buys no extra speed and costs 12k tokens of context). **Not** proposed for the router: it serves
f16 KV, where this round found no gain, so changing the router's `-ub` on this evidence would be
unsupported. Next measurement, at this same node: re-run the **f16** and **q8_0** 512/1024 pairs
back-to-back on a quiet box (one launcher, no cross-arm pacing) to separate the lever from the
environment, and add a 4th/5th trial per arm so the f16 interval narrows.

## Caveats and defects (not fixed this round)

- **The box was under heavy contention by parallel agents.** `MemAvailable` ranged 0.8-11.5 GB and
  load average 10-52; model loads took 4.1-182.9 s against OSC.09's 36-56 s for the same image and
  args. The two arms with the longest loads are f16 512 (182.9 s) and f16 2048 (152.3 s).
- **The q8_0 ub512 baseline is the awkward number.** 960 mean tok/s is below f16 ub512 (1071) and
  q4_0 ub512 (1167) at the same setting. If that arm had measured like its siblings the q8_0 gain
  would vanish, so the +27 pct may be partly a kernel-selection or environment artifact rather than a
  pure `-ub` effect. This is why the verdict is a lean, not `proved`.
- The first arm's first slice (f16 512 s1 = 844) followed the 185.5 s JIT warm-up and is depressed
  relative to its own s2/s3 (1228 / 1143). It is kept, not dropped.
- `wikitext` byte slices are not length-matched: 28,971 / 30,463 / 31,751 tokens across slices, so
  the analysis uses tok/s (length-normalised) and pairs slice-by-slice.
- `/data/ml/scratch/cuda-jit-cache` is root-owned inside (the container writes as root), so `du` as
  the agent cannot size it; the mount is 1 MB of index from outside. It is an out-of-repo root and
  stays literal (rule 13); a box cell is proposed for the Prime.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review of the kid's first round. The node's own FALSIFIER says: no (KV type, -ub) arm beats the same KV type at -ub 512 by >= 10 pct with its interval clearing zero -> -ub is not a long-prompt lever here. The kid's ub.json shows exactly one arm passing: q8_0 ub1024 +27.2 pct [15.6,38.8]. What the summary hides: that arm divides by a q8_0 ub512 baseline of 960 tok/s that sits below f16 512 (1071) and q4_0 512 (1167) in the SAME run, which the kid's own caveat names. So I ran the one negative probe that decides it: the kid's driver, unmodified, q8_0 512 then q8_0 1024, the same three slices, on a quiet box (probe/probe_q8.json). ub512 rose to 1181.9/1186.0/1189.1 (mean 1185.7, +23.5 pct) and ub1024 to 1197.6/1202.4/1203.0, so the paired gain is +1.29 pct [+1.03,+1.56] -- it clears zero and misses the 10 pct bar by 7.8x. The near miss: re-running only the ub1024 arm would have reproduced the result (1201 vs 1219.6, 1.5 pct) and certified the gain; the falsification is visible only because the probe re-ran the baseline the claim divides by. The speed conjunct therefore fails for the only KV type that passed, and no other pair clears 10 pct (f16 +6.0 [-89.9,+102.0], q4_0 +2.8 [-0.7,+6.2]); the fitted-context conjunct holds everywhere (>= 37888) and is not the failure point. Verdict demoted to inconclusive_lean_disproved:90 with the three probes in frontmatter. The rest of the artifact is sound and worth keeping: the JIT-cache proof (first warm-up 185,513 ms vs 135-2167 ms later) replicates OSC.09, the n_ctx table answers the L1 prefill-cost-at-depth question, and the router was restored and proven before the kid reported.
<!-- THOUGHT:END -->

## Agent Notes
9-arm (f16/q8_0/q4_0 x -ub 512/1024/2048) prefill matrix on ~30k-token wikitext slices, router's own image and args plus -fa on and a persistent /root/.nv/ComputeCache. q8_0 is the only KV type whose paired gain clears zero: ub1024 +27.2 pct [15.6,38.8] and ub2048 +27.3 pct [17.5,37.2] vs ub512, at fitted n_ctx 68608 / 56320 (>= 32768) -- the pre-registered bar is met. f16 (the router's KV type) shows no gain (+6.0 [-89.9,+102.0]) and q4_0 is flat (+2.8 [-0.7,+6.2]); at ub512 no KV type is measurably slower than f16. Lean, not proved: the q8_0 ub512 baseline (960 tok/s) is below f16 512 (1071) and q4_0 512 (1167), and the box was heavily contended (load 10-52, 0.8-11.5 GB available, loads 4-183 s vs OSC.09's 36-56 s). T3 proved the persistent JIT cache: first arm's 13-token warm-up 185,513 ms vs 135-2167 ms for every later arm. Router stopped then restored and proven (n_ctx 49664, real completion).

PARENT REVIEW: demoted inconclusive_lean_proved:70 -> inconclusive_lean_disproved:90. The only arm clearing the 10 pct bar (q8_0 ub1024 +27.2 pct) was measured against a contended q8_0 ub512 baseline (960 tok/s) that sits below its own siblings; on a quiet box the parent re-ran the same pair with the kid's driver and got +1.29 pct [+1.03,+1.56] (baseline 1185.7). Falsifier fires: -ub is not a >= 10 pct long-prompt lever on this host. Probes: gate/speed refuted, wire/fitted-context held, gate/L1-KV-cost refuted. Kid's data, script and JIT-cache proof kept.
