---
id: hypothesis:lm-served-9b-long-prompt-prefill-gains-from-larger-ubatch
mint_id: 73293d8653324b8eb70a7ebfbe527144
type: hypothesis
parents:
  - goal:g5.22
  - experiment:a00-df53894e-fabe8f
next_edges: []
edited_by: director-thought
scaffold_hash: ea84ffbe964dc539
season: 2
testable_claim: "On the served Qwen3.5-9B-Q4_K_M with the router's own image (server-cuda, build 10991) and args, raising the micro-batch from the router's -ub 512 to 1024 or 2048 (with -b >= -ub) prefills a warm ~30k-token prompt at least 10 pct faster than the same KV type at -ub 512, for at least one KV type among f16 / q8_0 / q4_0, with the 95 pct interval of the gain clearing zero over 3 trials and the fitted context at that setting >= 32,768 tokens under --fit on. CEILING: <=120 production lines."
title: "TRACK I ladder L6 (long-prompt prefill, the pi-local workload): on the served 9B a larger micro-batch (-ub 1024 / 2048) prefills a warm ~30k-token prompt >= 10 pct faster than the router's -ub 512 for some KV type, at a fitted context >= 32,768 -- and the L1 KV types' real prefill cost at depth, measured on the router's own image"
town: local-maxxing
---
# hypothesis:lm-served-9b-long-prompt-prefill-gains-from-larger-ubatch

# hypothesis:lm-served-9b-long-prompt-prefill-gains-from-larger-ubatch

## Measured
- The workload: pi-local's first requests after the 9B's reloads were 24,964 and 35,260-token prompts prefilled at 1,210 / 1,166 tok/s
  (datasets/serving-sweep/2026-09-23-cold/router_log_full.txt, spawns 41165 / 51919; experiment:a00-df53894e-fabe8f T5) -- a ~30k-token
  prompt costs ~25 s of prefill per request; the warm router does 1,490-1,524 tok/s on ~2k prompts (cold.json t1 / t2).
- OSC.08 (experiment:a00-f256db1a-73ee5b) swept -ub 256 / 1024 on pp512 only (datasets/serving-sweep/2026-09-23/sweep.json t2.ub1024:
  pp512@4096 +0.1 pct) -- a 512-token prompt cannot use a micro-batch above 512, so the lever was never measured on the prompts pi-local sends.
- OSC.06 (experiment:a00-30ac1417-72aa81 :81-:90): pp512 at depth 32,768 f16 950.55 +/- 78.86, q8_0 937.18 +/- 32.73, q4_0 704.71 +/- 140.81
  tok/s (recorded, not weighed: sd up to 469) -- the L1 keeper (q4_0, 3.15x context) may pay its price exactly where long prompts live.
- OSC.09: a fresh container pays a fixed ~45 s CUDA JIT that a mounted ComputeCache removes (cold 44,992 ms -> 136.8 ms); the router's
  args record no -ub / -b, i.e. the defaults 512 / 2048 (datasets/kv-format/2026-09-23/router_args.json).

## CLAIM
On the served Qwen3.5-9B-Q4_K_M with the router's own image (server-cuda, build 10991) and args, raising the micro-batch from the router's -ub 512 to 1024 or 2048 (with -b >= -ub) prefills a warm ~30k-token prompt at least 10 pct faster than the same KV type at -ub 512, for at least one KV type among f16 / q8_0 / q4_0, with the 95 pct interval of the gain clearing zero over 3 trials and the fitted context at that setting >= 32,768 tokens under --fit on. CEILING: <=120 production lines.

## Dispatch line
config-max: paths.local_maxxing.serving_sweep_ub_out_dir (datasets/serving-sweep/2026-09-23-ub), added by the director before dispatch;
the persistent JIT cache /data/ml/scratch/cuda-jit-cache is an out-of-repo root, so it stays literal (a box cell for the Prime) /
template-max: none / code: none -- llama-server flags only; the router and every config cell stay untouched and the winner is PROPOSED.

## FALSIFIERS
- no (KV type, -ub) arm beats the same KV type at -ub 512 by >= 10 pct with its interval clearing zero -> -ub is not a long-prompt lever
  here; the fastest measured arm is still the LARGEST SAFE STEP if any gain clears zero.
- the winning arm fits < 32,768 tokens -> the gain costs the context pi-local needs; report the fit / speed trade per arm.

## TESTS
- T0 guard: no pi-local round live, host RAM available >= 2 GB -> docker stop llama-server; whatever happens, restore it and prove :8080
  answers a real completion from the 9B.
- T1 per arm (KV f16 / q8_0 / q4_0 x -ub 512 / 1024 / 2048, -b = max(2048, ub), flash attention on): a fresh server-cuda container with
  the router's model args, a spare port and the persistent ComputeCache mounted; the fitted n_ctx_slot from its load log; one short
  warm-up request; then the SAME three ~30k-token wikitext slices (distinct, so no prefix is reused) -> prompt_n, prompt_ms, tok/s.
- T2 the paired gain per KV type vs its -ub 512 arm (3 trials, a t interval), and every KV type at -ub 512 vs f16 (the L1 prefill cost).
- T3 the JIT-cache proof: the first container's first request vs every later container's (OSC.09's step a, now applied).

## FILE SCOPE
- one script under .agi/context/local-maxxing/serve/ (paths via paths.get_local); outputs under paths.local_maxxing.serving_sweep_ub_out_dir;
  ONE experiment node under this hypothesis; nothing under extensions/; the router and every config cell untouched.

## CEILING
pi deepseek parent + ONE model-loading host kid (GPU round) · <=120 production lines · no per-round cap (TMM.51) · wall 120 min · the router
restored whatever happens.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 3 residue correction (hypothesis:pass3-0924-residue-batch, demote reason: Production line ceiling exceeded) -- CORRECTED IN PLACE per thought-master TMM.118 owed 1. The round's driver (.agi/context/local-maxxing/serve/ub_prefill_round.py, experiment:a00-3caaf6eb-9065ef) measured 127 production lines against this hypothesis's own <=120 CEILING, a 7-line (5.8 pct) overage with no rebrief request on record. This does not touch the substantive verdict: the experiment already carries its own PARENT REVIEW demoting inconclusive_lean_proved:70 to inconclusive_lean_disproved:90 on stronger grounds -- the only arm that cleared the 10 pct bar (q8_0 ub1024, +27.2 pct) rested on a contended-box q8_0 ub512 baseline (960 tok/s, below its own siblings), and a quiet-box re-run of the same pair with the same driver collapsed the gain to +1.29 pct [+1.03, +1.56], 7.8x under the bar. The ceiling breach is a process residue on top of an already-correct disproved verdict, recorded here so it is not silently dropped; it is well under the 2x hard stop (240) so no re-dispatch is owed.
<!-- THOUGHT:END -->
