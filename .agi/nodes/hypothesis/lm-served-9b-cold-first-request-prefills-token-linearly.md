---
id: hypothesis:lm-served-9b-cold-first-request-prefills-token-linearly
mint_id: 058964ec8dd24d83add1189c7818d7e9
type: hypothesis
parents:
  - goal:g5.22
  - experiment:a00-f256db1a-73ee5b
next_edges: []
edited_by: director-thought
scaffold_hash: e86ce25084a0b41e
season: 2
testable_claim: On the served Qwen3.5-9B-Q4_K_M under llama-server with the router's recorded args, across 3 fresh-server trials the first request after a load prefills at >= 15 ms per prompt token while the second prefills at >= 1,000 tok/s, and a <= 16-token warm-up request right after the load makes the next ~2k-token request prefill at >= 1,000 tok/s. Falsified if the first request is not token-linear, the warm one is not >= 1,000 tok/s, or a tiny warm-up does not warm the next request.
title: "TRACK I ladder L10 (the open-loop map): the served 9B's FIRST request after a model load prefills token-linearly (>= 15 ms/token) while a warm server prefills >= 1,000 tok/s, and one tiny warm-up request on load makes the next request warm -- the cold cost OSC.08's map measured"
town: local-maxxing
---
# hypothesis:lm-served-9b-cold-first-request-prefills-token-linearly

# hypothesis:lm-served-9b-cold-first-request-prefills-token-linearly

## Hypothesis

**CLAIM.** On the served Qwen3.5-9B-Q4_K_M under llama-server with the router's own args, the FIRST request after a model load prefills token-linearly at >= 15 ms per prompt token, while a warm server prefills at >= 1,000 tok/s (<= 1 ms per token); and ONE tiny warm-up request (<= 16 tokens) sent right after the load makes the next request's prefill warm -- so a warm-up on every model load removes the cold cost.

**DISPATCH LINE.** config-max: paths.local_maxxing.serving_sweep_cold_out_dir (datasets/serving-sweep/2026-09-23-cold) -- the round added it, the director carried it at harvest (5208ac454) / template-max: none / code: none -- docker and llama-server flags only; the router and every config cell untouched, the fix PROPOSED. (Added after the round, per TMM.57: this node was minted before the schema's body format reached this seat.)

**WHY THIS, NOW.** Ladder L10 (the open-loop map, board queue [1]). OSC.08's nsys map (experiment:a00-f256db1a-73ee5b) found a 2,077-token served request spending ~46-48 s in prefill at ~44 tok/s with the GPU idle; the director then measured three warm requests on the live router at ~1,400 tok/s (17:14Z 09-23). Every slow prefill on record is the first request after a model load (t1, t1v, the router's post-restore 17-token completion at 24 ms/token), and in t1v the first 1,561-token batch took 38 s while the next 512 tokens took 0.1 s. If the cold cost were per prompt token (~23 ms), a 30k-token pi-local prompt would pay minutes after every (re)load; the t1v log instead places it in the first batch (1,561 tokens in 38 s, then 512 in 0.1 s) -- T3 measures which.

**FRAME.** smaller: one variable (cold vs warm), the router's own args, repeated trials. Bigger: how often the router actually reloads the 9B decides what the step is worth -- the router log answers it.

**TESTS** (GPU, one research round, router stopped and restored as in OSC.05 / OSC.08):
- T0 guard: no pi-local round live, host RAM available >= 2 GB -> docker stop llama-server; whatever happens, restore it and prove :8080 answers a real completion from the 9B.
- T1 cold vs warm, 3 trials: a fresh llama-server (full-cuda image, the router's recorded args, a spare port) -> request A (~2k tokens, a fixed wikitext slice) -> request B (~2k tokens, a different slice) -> prompt_ms / prompt_n / prompt_per_second for each.
- T2 warm-up, 3 trials: a fresh server -> request W (<= 16 tokens) -> request A -> the same timings.
- T3 size: a fresh server per size, cold first request of ~256 / ~2k / ~8k tokens -> ms per token (token-linear or a fixed cost?).
- T4 mechanism: one fresh server at -lv 5 -> what differs between the first and second request (ubatch sizes, graph builds, context checkpoints, any CPU fallback), from the log lines.
- T5 frequency (read only): the router's own log (docker logs llama-server) over the day -> model load / unload events for the 9B and their cause (--models-max 1 swaps, idle).

**FALSIFIER.** The first request is not token-linear (>= 15 ms/token) or the warm one is not >= 1,000 tok/s -> the cold/warm split is not the mechanism (OSC.08's map stands as measured); a tiny warm-up does not warm the next request -> the step is 'keep the model resident', not 'warm on load'. LARGEST SAFE STEP either way: the measured cold cost per token and what removes it, for the Prime / thought-master.

**FILE SCOPE.** Script under .agi/context/local-maxxing/serve/ (paths via paths.get_local); outputs under datasets/serving-sweep/ (a new dated dir); one experiment node under this hypothesis; the router and every config cell untouched -- the fix is PROPOSED.

**CEILING.** 0 USD compute; pi deepseek parent + ONE model-loading host kid (GPU round); orders wall 90 min; the router restored whatever happens.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
TMM.57 (thought-master, 09-23 18:54Z, its later item): the schema's Dispatch line added to this brief -- config-max = the round's one cell (serving_sweep_cold_out_dir, carried at harvest), template-max none, code none; the node was minted before the hypothesis body format reached this seat. CLAIM, TESTS and FALSIFIER untouched.
<!-- THOUGHT:END -->
