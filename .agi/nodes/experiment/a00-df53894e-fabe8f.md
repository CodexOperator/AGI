---
id: experiment:a00-df53894e-fabe8f
mint_id: 1938f61310ac4c4ea8cfce8e51252f23
type: experiment
parents:
  - hypothesis:lm-served-9b-cold-first-request-prefills-token-linearly
next_edges: []
confidence: 0.9
edited_by: a00-df53894e
evidence_runs:
  - experiment:a00-df53894e-fabe8f
line_ceiling: 40
loop: hypothesis:lm-served-9b-cold-first-request-prefills-token-linearly@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 76
profile: balanced
rebrief_request: "cold_first_round.py is 76 production lines vs the 40-line ceiling (1.9x, under the 2x stop): the overage is the five-stage T1-T4+TF driver with a fresh container, a spare port and a health-wait per trial, plus the T2/T3 slice table -- 17 trials in one GPU round. Requested ceiling 80; the round is landed, no test was dropped and nothing was padded."
role: kid
scaffold_hash: 2e07cef0b7292788
season: 2
title: "The cold first request is NOT token-linear: it is a fixed ~45 s CUDA JIT-ComputeCache cost (281/2061/7638 tokens -> 44.9/47.8/49.7 s; a 13-token first request also 44.7 s) that a warm /root/.nv/ComputeCache removes to 137 ms (329x) -- the warm bar and the tiny-warm-up bar both hold at 1490-1524 tok/s, and the router pays it 0 times in 8 loads today"
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-df53894e-fabe8f

## Experiment

**Question.** On the served `Qwen3.5-9B-Q4_K_M` (RTX 2070 SUPER, 8 GB) under llama-server with the
router's recorded args, is the FIRST request after a load a token-linear cold prefill at >= 15 ms per
prompt token, is a warm server >= 1,000 tok/s, and does a <= 16-token warm-up make the next ~2k request
warm? (Hypothesis bars B1/B2/B3; falsifier = B1 fails.)

**T0 guard + restore (`t0_guard.txt`, `restore_proof.txt`).** 2026-09-23T17:19:52Z: 6/30 agents live, no
pi-local round; `GET :8080/slots?model=Qwen3.5-9B-Q4_K_M` -> `n_ctx 49664, is_processing false`;
`MemAvailable` 10,943,992 kB >= 2 GB; only GPU compute app was the router (6,736 MiB).
`docker stop llama-server` freed the card to **1 MiB**. Restored 17:52:47Z: `docker start
llama-server`, real `POST /v1/chat/completions` from `Qwen3.5-9B-Q4_K_M` (`completion_tokens=16`),
`GET /slots` -> `n_ctx 49664, is_processing false`, build `b10991-930e2fa59`, GPU 6,726 MiB.
**The router was up before this report was written.**

**Inputs.** Served GGUF `/data/ml/scratch/osc02/Qwen3.5-9B-Q4_K_M.gguf` sha256
`03b74727a860a56338e042c4420bb3f04b2fec5734175f4cb9fa853daf52b7e8` (re-hashed this round);
`wiki.test.raw` sha256 `173c87a53759e0201f33e0ccf978e510c2042d7f2cb78229d9a50d79b9e7dd08`. Nothing was
written to any model file. Image `ghcr.io/ggml-org/llama.cpp:full-cuda` (build 11058),
`--entrypoint /app/llama-server`, fresh `docker run --rm` per trial, a distinct spare port each
(18081-18094), the router's `model_args_9b` verbatim minus `--port` and the in-container model path --
**no `-fa`/`-ctk`/`-ctv` added**. One driver, `.agi/context/local-maxxing/serve/cold_first_round.py`
(new, 76 lines), stages `t1 t2 t3 t4 tf`; every path via `paths.get_local`; outputs under
`datasets/serving-sweep/2026-09-23-cold/` (`cold.json`, `logs/`, `t4.log`, `router_log_full.txt`).

**T1 -- cold vs warm, 3 trials (fresh server -> A ~2k -> B ~2k, different slices).**

| trial | A prompt_n | A prompt_ms | A ms/token | B prompt_n | B prompt_ms | B tok/s |
|---|---|---|---|---|---|---|
| t1r0 | 2061 | 47,831.8 | **23.21** | 2132 | 1,402.1 | **1,520.6** |
| t1r1 | 2061 | 45,929.5 | **22.29** | 2132 | 1,399.0 | **1,523.9** |
| t1r2 | 2061 | 47,617.1 | **23.10** | 2132 | 1,430.6 | **1,490.3** |

B2 holds: the second request is 1,490-1,524 tok/s (0.66 ms/token), 3/3. Superficially B1 holds too
(22.3-23.2 ms/token at 2061 tokens).

**T2 -- tiny warm-up (fresh server -> W <= 16 tokens -> A ~2k).**

| trial | W prompt_n | W prompt_ms | W ms/token | A prompt_n | A prompt_ms | A tok/s |
|---|---|---|---|---|---|---|
| t2r0 | **13** | 44,677.8 | **3,436.8** | 2061 | 1,377.0 | **1,496.7** |
| t2r1 | **13** | 44,885.3 | **3,452.7** | 2061 | 1,357.0 | **1,518.8** |
| t2r2 | **13** | 46,110.3 | **3,546.9** | 2061 | 1,373.8 | **1,500.3** |

B3 holds (3/3). But **B1 is destroyed here**: a 13-token first request cost 44.7-46.1 s. 45 s divided by
13 tokens is not a per-token price.

**T3 -- cold first request vs size, one fresh server per size.**

| size | prompt_n | prompt_ms | ms/token |
|---|---|---|---|
| ~256 | **281** | 44,948.4 | 159.96 |
| ~2k | **2061** | 47,762.5 | 23.17 |
| ~8k | **7638** | 49,674.8 | 6.50 |

Total cold time is **44.9 / 47.8 / 49.7 s for 281 / 2061 / 7638 tokens**: a FIXED cost of ~45 s, flat
to within 10 pct across a 27x span of prompt length. ms/token is not a rate, it is 45 s divided by
whatever arrived first. Fitting a fixed F plus the measured warm rate (0.66 ms/token) gives
F = 44.8, 46.4, 44.6, 44.7 s -- one constant.

**Mechanism (T4 + two probes).** `-lv 5` first request (`logs/t4.log`):
`slot operator(): task 0 | new prompt ... task.n_tokens = 2061` at `0.50.397`,
then 38.9 s of in-graph silence, then
`slot print_timing: id 0 | task 0 | prompt processing, n_tokens = 1545, progress = 0.75, t = 38.91 s / 39.70 tokens per second`
(`1.29.310`) and the remaining 516 tokens in **0.10 s** (`1.29.409`), then the second request's
`cached n_tokens = 1616` after 1.006 s (`1.38.425`) = 1,607 tok/s. Note also
`load_model: cache_reuse is not supported by this context, it will be disabled` -- the router's
`--cache-reuse 8` is a no-op on this hybrid/SSM model, so the warm speed is not prefix caching.
Two probes pinned the fixed cost to the **CUDA JIT compute cache**: (a) a fresh container running the
ROUTER'S OWN container command (`--models-dir /models --models-max 1 --fit on --jinja -np 1
--cache-reuse 8`, image `server-cuda`) still paid **44,718 ms on a 13-token first request** then
1,853 ms/2,061 tokens = 1,112 tok/s (`router_mode_probe.json`); (b) the same image with
`-v $CACHE:/root/.nv/ComputeCache` -- **empty cache: 44,992 ms; the same 77 MB cache mounted in a
fresh container: 136.8 ms** (329x), `logs/jitcache_probe.txt`. The router container carries a
populated `/root/.nv/ComputeCache` (123 MB, `docker cp llama-server:/root/.nv`). That is why the
router's own first post-restore request in this round took **424.1 ms for prompt_n=13**
(`restore_proof.txt`) and why OSC.08's recorded `412.6 ms / 17 tokens` was real while a fresh
container measured ~45 s for the same shape: the fixed cost is per-container-cache, not per-load and
not per-token.

**T5 -- frequency (read only, `router_log_full.txt`, 5,541 lines).** The router loaded
`Qwen3.5-9B-Q4_K_M` **8 times** today (`load_model` pids 41165, 51919, 47155, 40675, 50311, 53451,
41079 + 1) and unloaded it each time (`unload_all: stopping model instance`, `--models-max 1` swaps,
incl. one 35B load); every reload's first request was **0.24-1.80 s** (370.6, 704.8, 686.5, 1800.5,
412.6 ms ...), never ~45 s. So no cold first request reached a pi-local round today: the container's
JIT cache is warm, and a model reload inside a live container does not re-pay it. A cold first
request reaches pi-local only when the **container** is recreated (new image, force-recreate, new box).

## Verdict, bar by bar (falsifier: B1 fails -> disproved)

- **B1 token-linear >= 15 ms/token: REFUTED.** 45 s is fixed: 281 tokens 44.9 s, 2061 tokens 47.8 s,
  7638 tokens 49.7 s, 13 tokens 44.7 s. The T1 numbers that looked linear were 45 s spread over 2061
  tokens.
- **B2 warm >= 1,000 tok/s: CONFIRMED** (1,490-1,524, 3/3; 1,460 / 1,112 on the two router-fidelity runs).
- **B3 tiny warm-up warms the next request: CONFIRMED** (W prompt_n=13 -> 1,497-1,519 tok/s, 3/3).

The cold/warm split is real and the remedy works, but the mechanism named in the claim is wrong, so
the claim as written is disproved.

## LARGEST SAFE STEP (PROPOSED -- not landed; router and config cells untouched)

1. **Persist the CUDA JIT cache into the server container**: mount a volume at
   `/root/.nv/ComputeCache` (or set `CUDA_CACHE_PATH` to a mounted dir). Measured: cold first request
   44,992 ms -> **136.8 ms (329x)** with the same 77 MB cache. This removes the cost instead of moving
   it, and it is the only step that also helps the `-lv>/dev/null`-cold first request.
2. **If (1) is not wanted, warm at load**: one <= 16-token request right after each model load. It
   works (B3) but it does not remove the 45 s, it books it at load time -- and T5 shows the router
   already does not pay it per load, so its value today is ~0 except on container recreation.
3. Do **not** build anything on the "23 ms/token" figure from OSC.08 or the restored-router log line:
   it is a fixed cost divided by a prompt length, and any step sized from it will be sized wrong.

## Defects / limits named (not fixed this round)

- T1/T2 ran before `--log-file` was wired, so their server logs are absent; `docker logs` on a
  `docker rm -f`'d container returned only line 1 (llama-server's log file is buffered), and the t3/tf
  `--log-file` outputs are 0 bytes for the same reason. Only `t4.log` survived.
- Verdict is scored against the hypothesis text; the OSC.08 measurement it builds on stands corrected,
  not retracted.
- The two probes live in the session scratch
  (`.agi/sessions/iter-OSC.09/a00-df53894e/probe/{router_mode_probe.sh,jitcache_probe.sh}`) and use
  literal box paths (`/data/ml/scratch/osc02/coldcache*`); the shipped driver uses only `paths.get_local`.

## Agent Notes
Cold first request is a FIXED ~45 s CUDA JIT ComputeCache cost, not token-linear: 281/2061/7638 tokens -> 44.9/47.8/49.7 s and a 13-token first request 44.7 s (17 fresh-container trials). Warm bar holds (1490-1524 tok/s) and the tiny warm-up holds (prompt_n=13 -> next 2061-token request 1497-1519 tok/s), so the remedy works but the named mechanism is wrong. Mechanism pinned by two probes: the router's OWN container command still pays 44.7 s on 13 tokens; an empty cache 44992 ms vs the same 77 MB /root/.nv/ComputeCache mounted warm in a fresh container 136.8 ms (329x). Router's 8 loads of the 9B today never paid it (JIT cache lives in the container layer) -- so the LARGEST SAFE STEP is PROPOSED: persist CUDA_CACHE_PATH/ComputeCache for the server container (removes the cost), else warm at load (books it, does not remove it). Router stopped then restored and proven: n_ctx 49664, real completion, build b10991-930e2fa59.
