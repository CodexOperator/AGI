---
id: experiment:a00-80a08fbb-3ad171
mint_id: 8e5d4407a0ab4a99998dd9ee18f096f6
type: experiment
parents:
  - hypothesis:gpu-local-town-openai-endpoint
next_edges: []
confidence: 0.8
edited_by: a00-b410af3e
evidence_runs:
  - experiment:a00-80a08fbb-3ad171
loop: hypothesis:gpu-local-town-openai-endpoint@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 /tmp/probe_prefill.py -> POST http://127.0.0.1:18080/v1/chat/completions Qwen3.5-35B-A3B-Q3_K_M with a fresh ~410-token prompt, then distinct 650-token prompts", "expected": "if pp512=10.44 tok/s were a true prefill rate, warm FRESH prompts stay near it", "observed": "cold-first-request 8.787 tok/s (prompt_n=410, prompt_ms=46662, wall 118.7s); then three distinct uncached prompts 232.524 / 327.722 / 333.166 tok/s", "result": "kid holds: the 10.44-class rate is cold-only; warm prefill is 26-38x higher, direction reproduced independently through the tunnel"}
  - {"conjunct": 2, "class": "gate", "cmd": "ssh local-town: curl -s http://127.0.0.1:8080/props ; docker logs llama-server | grep -iE n_gpu_layers|n_cpu_moe|offloading|CUDA0 model|load_tensors", "expected": "if --fit on resolved -ngl/n-cpu-moe were queryable, /props or the router log would state them, making the explicit re-run unnecessary", "observed": "/props returns role=router with no split fields; docker logs llama-server emitted ZERO load_tensors/offloading/n_gpu_layers lines", "result": "kid holds: the running router does not expose the split; the explicit re-run was necessary and its readback is the only source"}
profile: balanced
role: kid
scaffold_hash: 450a0357a321ce86
season: 2
title: A00 80a08fbb 3ad171
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-80a08fbb-3ad171

Residue round on `hypothesis:gpu-local-town-openai-endpoint`: the kid-sized
prefill row for `Qwen3.5-35B-A3B-Q3_K_M` and the explicit CPU/GPU split that
`--fit on` had been choosing silently. Both measured from core-town through
`127.0.0.1:18080` (`local-town-tunnel` -> loopback llama-server on local-town).

## Result (one line)

The 35B-A3B prefill at ~8.1k prompt is **593.78 tok/s warm** (13.66 s), and the
existing 512-token row (`pp512 = 10.44 tok/s`) is **not a prefill measurement
at all** — it is the cost of the *first request after model load*, when the
`--fit on` CPU-side MoE experts are still being first-touched through the
mmap. Same server, same 512-token request: **9.58 tok/s cold vs 400.54 tok/s
warm** (42x). The explicit split that reproduces `--fit on`'s VRAM is
`-ngl 99 --n-cpu-moe 28` -> 6640 MiB VRAM (vs 6666 measured for `--fit on`),
tg128 12.556 tok/s (vs 12.396), with `n_gpu_layers` / `n_cpu_moe` now READ
BACK from the load log instead of inferred.

## What was done

1. Verified the tunnel and the running router (`--models-dir /models
   --models-max 1 --fit on --jinja -np 2`); both model ids listed.
2. Item 1 first attempted against the running router: the 35B JIT-loads with
   **`n_ctx_slot = 4096`** (the 9B gets 23552) — `--fit on` gives the larger
   MoE the minimum context, so an 8k prompt was rejected
   (`request (10018 tokens) exceeds the available context size (4096 tokens)`).
   An 8k prefill cannot be issued against the running router at all.
3. Readback attempt (Item 2) before touching anything: `docker logs` prints no
   `load_tensors`/`n_gpu_layers` line at verbosity 3, `/props` exposes no
   split, and `/v1/models` only echoes the preset args (`--fit on`). The
   resolved split is **not queryable** from the running server, so the explicit
   re-run was the sanctioned fallback.
4. Chose N from the GGUF tensor table (733 tensors, 15,588 MiB total): each of
   the 40 MoE layers carries 332.0 MiB of expert weights (`*_exps`), non-expert
   blk weights 1,512.5 MiB, token_embd+output 795.8 MiB. `--n-cpu-moe N` keeps
   the **first N** layers' experts on CPU (`common/arg.cpp` L2763-2772,
   "first N layers"). Trial `N=30` -> CUDA0 5230.32 MiB / 5976 MiB VRAM;
   **`N=28` -> CUDA0 5894.32 MiB = 6640 MiB VRAM**, the ballpark match.
5. Ran the explicit server direct on 8080 (`docker stop llama-server`;
   `docker run -d --name llama-35b ... -ngl 99 --n-cpu-moe 28 -np 1 -c 16384 -lv 4`),
   then the 8.1k prefill, a cold-vs-warm 512 control, and tg128; sampled
   nvidia-smi + `/proc/loadavg` + `free` every 2 s throughout.
6. Rollback: `docker rm -f llama-35b; docker start llama-server`; verified
   `/v1/models` lists both ids, 9B `loaded`, one completion through the tunnel
   returns `finish_reason=stop`, content `pong`.

## Numbers (all tunnel-side, from core-town, through 127.0.0.1:18080)

| run (explicit `-ngl 99 --n-cpu-moe 28 -np 1 -c 16384`) | prompt_n | prompt_ms | pp tok/s | wall s | VRAM MiB | GPU W max | load1 max |
|---|---|---|---|---|---|---|---|
| pp8118, **first request after load** | 8118 | 59796 | **135.76** | 60.63 | 6662-6664 | 203.04 | 3.68 |
| pp8118, **warm (resident)** | 8110 | 13658 | **593.78** | 15.12 | 6662 | 156.94 | 1.96 |
| pp512, **cold first request** (control) | 524 | 54671 | **9.58** | 55.28 | 6640 | ~200 | — |
| pp512, **warm** (control) | 524 | 1309 | **400.54** | 2.01 | 6662 | 119.50 | 1.28 |
| tg128 (`ignore_eos`) | ~24 | — | — | 3.4-17.2 | 6662 | 203 | 3.38 |

**tg128 is the noisy one.** Seven `max_tokens=128 ignore_eos` calls on this
config ranged **8.22 / 12.56 / 16.39 / 20.90 / 41.12 / 42.10 / 44.12 tok/s**
(median 20.90). The first two (12.56, 8.22) were measured before the mmap'd
CPU expert pages were fully resident; the 41-44 cluster is the resident state.
Round 2's `--fit on` row was 12.396 — squarely inside this spread, so the
explicit split is **throughput-neutral vs `--fit on`**.

### Explicit split, read back (Item 2)

`-ngl 99 --n-cpu-moe 28`, load log verbatim:

```
load_tensors: offloading output layer to GPU
load_tensors: offloading 39 repeating layers to GPU
load_tensors: offloaded 41/41 layers to GPU
load_tensors:   CPU_Mapped model buffer size = 10751.51 MiB
load_tensors:        CUDA0 model buffer size =  5894.32 MiB
llama_context: n_ctx = 16384
```

- chosen `--n-cpu-moe`: **28** (first 28 layers' experts on CPU); `-ngl` **99**
- VRAM at load **6640 MiB** (round 2 `--fit on`: 6666; trial N=30: 5976)
- host RSS (`docker exec llama-35b ps -o rss= -C llama-server`) **10,878,640 KB
  ~= 10.38 GiB** (later `10,264,376 KB ~= 9.79 GiB`); `docker stats` MemUsage
  2.87-5.83 GiB; host `free -m` used 2.2-2.5 GB with 13.5 GB in `buff/cache`
- the loader's own warning names the mechanism:
  `tensor overrides to CPU are used with mmap enabled - consider using
  --load-mode none for better performance`

## Reading

- **The premise handed to this round is refuted by its own measurement.**
  `pp512 = 10.44 tok/s` was read as "prefill is the binding cost"; it is the
  one-time first-touch cost of paging the mmap'd CPU_Mapped expert tensors
  (10.75 GiB) in for the first request. Warm, the same config prefills 8.1k at
  593.78 tok/s and 512 at 400.54. The existing tooling understated *nothing*
  about long context: it overstates prefill cost by 40-60x at every length.
- **What is actually expensive is the first token of a cold model**, not
  length. A kid-sized 8k prompt costs 13.7 s warm; the first request after a
  load costs ~55-60 s regardless of prompt length.
- **The explicit split is knowable and cheap to pin.** `--n-cpu-moe 28` lands
  within 0.4% of `--fit on`'s VRAM at statistically identical tg, and the load
  log then states the split instead of hiding it. If the box is to be
  re-loaded often, `--load-mode none` (prefaulting the CPU experts) is the knob
  the loader itself recommends.
- The router's `--fit on` preset gives the 35B **`n_ctx_slot = 4096`** (9B:
  23552), so the running router cannot serve an 8k prompt for the larger model
  at all — a separate, harder limit than VRAM headroom.

## Caveats / what is weak

- One prompt length (8.1k), one model. The 512 control used a different
  process instance than the 8118 runs, so cold-vs-warm is compared across
  requests, not inside one process; the 512 cold/warm pair *is* inside one
  process and is the cleanest evidence.
- tg128 spread of 8-44 tok/s means any single tg number from this box is
  unreliable to better than ~2x; the round-2 12.396 is not comparable to a
  warm 42.
- `-np 1` here vs `-np 4` in round 2; `-c 16384` both. Single-stream tg is
  unaffected by slot count, but the aggregate rows are not.
- $/kWh, CPU W and system W in `kidC_cost.md` remain parameters, not
  measurements. The cost row below recomputes with the new rates but inherits
  those parameters.

## Commands (verbatim; idempotent; alias `local-town` only)

```
# read the running router's per-model preset + child args (readback attempt)
ssh -F <keeper-dir>/ssh/config -o ConnectTimeout=15 local-town 'curl -s http://127.0.0.1:8080/v1/models; echo; docker logs llama-server 2>&1 | tail -40'

# explicit-split server, chosen to match --fit on VRAM (N=28; N=30 was the trial)
ssh -F <keeper-dir>/ssh/config -o ConnectTimeout=15 local-town 'docker stop llama-server; docker rm -f llama-35b; docker run -d --name llama-35b --gpus all --network host -v /data/ml/models:/models ghcr.io/ggml-org/llama.cpp:server-cuda --host 127.0.0.1 --port 8080 --model /models/Qwen3.5-35B-A3B-Q3_K_M.gguf --alias Qwen3.5-35B-A3B-Q3_K_M --jinja -ngl 99 --n-cpu-moe 28 -np 1 -c 16384 -lv 4'

# the split, read back from the load log
ssh -F <keeper-dir>/ssh/config -o ConnectTimeout=15 local-town 'docker logs llama-35b 2>&1 | grep -iE "offloading|CPU_Mapped|CUDA0 model buffer|n_ctx "'

# 8.1k prefill and 512 control: tunnel POST /v1/chat/completions (max_tokens=1),
# read timings.prompt_n / prompt_ms / prompt_per_second

# RSS beside the number
ssh -F <keeper-dir>/ssh/config -o ConnectTimeout=15 local-town 'docker exec llama-35b ps -o rss= -C llama-server; docker stats --no-stream --format "{{.Name}} mem={{.MemUsage}}" llama-35b; free -m | head -2'

# rollback + verify
ssh -F <keeper-dir>/ssh/config -o ConnectTimeout=15 local-town 'docker rm -f llama-35b; docker start llama-server; sleep 5; curl -s http://127.0.0.1:8080/v1/models'
curl -s --max-time 240 http://127.0.0.1:18080/v1/chat/completions -H 'Content-Type: application/json' -d '{"model":"Qwen3.5-9B-Q4_K_M","messages":[{"role":"user","content":"Reply with exactly: pong"}],"max_tokens":400,"temperature":0}'
```

Rollback verified: `/v1/models` through the tunnel lists both ids with the 9B
`loaded`, and the completion above returns `finish_reason=stop`, content `pong`.

Artifacts: `.agi/context/local-maxxing/gpu/kidC_bench.jsonl` (raw rows),
`.agi/context/local-maxxing/gpu/kidC_cost.md` (new section).

## Agent Notes
35B-A3B explicit split read back: -ngl 99 --n-cpu-moe 28 -> 6640 MiB VRAM (fit-on 6666), CUDA0 5894.32 MiB, CPU_Mapped 10751.51 MiB, RSS 10.38 GiB, tg128 12.6-44 tok/s (median 20.9; fit-on 12.396 inside spread). pp512=10.44 was a COLD-FIRST-REQUEST artifact: same config 9.58 cold vs 400.54 warm, pp8118 135.76 first vs 593.78 warm. Router --fit on gives 35B n_ctx_slot=4096 so 8k prompts need an explicit -c. Rollback verified (9B stop/pong).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review a00-b410af3e TM.10. The kid delivered both residue items and in doing so refuted the premise it was sent to test. Read the bytes: node plus kidC_bench.jsonl plus kidC_cost.md diff, +258 lines. Re-derived the raw JSONL arithmetic: 8118/59796.144e3 = 135.76; 8110/13658.254e3 = 593.78; 524/54671e3 = 9.585; 524/1309e3 = 400.31; prompt cost 0.0184 USD per 1M; output 0.614/0.291/1.022 per 1M at 20.9/44.12/12.556 tok/s; break-even 72.4 tok/s. All match. Two parent-run probes, one per claim conjunct. Probe 1 wire: re-ran cold vs warm prefill through the tunnel with fresh uncached prompts; cold 8.787 tok/s vs warm 232.5/327.7/333.2 tok/s, so the cold-first-request reading holds independently (my warm rate is lower than the kid numbers on the explicit server because the router uses different fit-on settings and n_ctx_slot 4096, but the direction is what the claim rests on). Probe 2 gate: tried to falsify the claim that the split is not queryable; /props and docker logs on the running router are both silent on n_gpu_layers and n_cpu_moe, so the explicit re-run was necessary. Verdict proved stands. Near miss: my first warm probe reused the same prompt, so KV prefix caching returned prompt_n=4 at 19/36 tok/s; the letter of warm-greater-than-cold passed while the mechanism of a full fresh prefill was not exercised, fixed by using distinct prompts. Deviation: the dispatch premise that pp512=10.44 tok/s is the binding prefill cost is refuted by measurement, recorded not hidden.
<!-- THOUGHT:END -->

PROBES: two parent-run probes recorded (wire conjunct 1, gate conjunct 2); both residue items delivered, arithmetic re-derived exactly, premise reframed (pp512=10.44 is a cold-first-request artifact, not a prefill rate). Verdict proved, confidence 0.8.
