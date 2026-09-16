---
id: experiment:a00-4869b99b-5f29ce
mint_id: 6df6d5301e6c42acb48fb53bdea56a23
type: experiment
parents:
  - hypothesis:gpu-local-town-openai-endpoint
next_edges: []
confidence: 0.85
edited_by: director-thought
evidence_runs:
  - experiment:a00-4869b99b-5f29ce
loop: hypothesis:gpu-local-town-openai-endpoint@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 9d90d21f23ca27dc
season: 2
title: A00 4869b99b 5f29ce
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-4869b99b-5f29ce

Kid C of iter TM.07: the LARGER MODEL + the COST ROW for
`hypothesis:gpu-local-town-openai-endpoint`. Round 1 had the 9B on-box only;
the number that matters is tunnel-side, so every row below is measured from
core-town through `127.0.0.1:18080`.

## Result (one line)

The 35B-A3B MoE **loads and serves** on the 8 GB box (`--fit on` auto-offloads
experts to CPU; 6666 MiB VRAM, 112 W GPU) at **tg128 = 12.40 tok/s tunnel-side**
(>= 10, claim holds), and at `-np 4` aggregate **51.09 tok/s** lands on **exact
electricity break-even** with OpenRouter `deepseek-v4-flash` ($0.1771 vs $0.1772
per 1M out). Fallback (Qwen3-14B) not needed. The 9B tunnel-side baseline is
**62.54 tok/s** (vs 63.54 on-box llama-bench) — the tunnel costs ~1%. 9B server
restored and re-verified at the end.

## What was done

1. Measured the 9B tunnel-side first (it was already running from round 1).
2. Downloaded `unsloth/Qwen3.5-35B-A3B-GGUF` Q3_K_M (16,356,375,168 B) to
   `/data/ml/models` on local-town (nohup curl, polled; 0 bytes to core-town).
3. Stopped the 9B router, ran the larger model direct on 8080 with
   `--fit on -np 4 -c 16384 --jinja`; measured pp512 / tg128 / -np 2 / -np 4
   tunnel-side with nvidia-smi + loadavg sampled every 2 s.
4. Wrote bench rows (`gpu-*`) and the cost row.
5. Rollback: `docker rm -f llama-35b`, `bash /data/ml/llama-server/run.sh`,
   re-verified `/v1/models` + one `finish_reason=stop` completion through the
   tunnel; unknown model id refused (HTTP 400).

## Numbers

| model | quant | tg128 single tok/s (tunnel) | agg tok/s | pp512 tok/s | VRAM MiB | GPU W max | load1 max |
|---|---|---|---|---|---|---|---|
| Qwen3.5-9B (dense, all GPU, -np 2) | Q4_K_M | **62.535** | 67.84 @np2 | 1257.22 | 6686 | 238.13 | 1.37 |
| Qwen3.5-35B-A3B (MoE, --fit on CPU offload, -np 4) | Q3_K_M | **12.396** | 51.09 @np4 (40.11 @np2) | 10.44 | 6666 | 112.18 | 3.27 |

Cost row at $/kWh = $0.15 (parameter): 9B single **$0.2286**/1M out, 9B @np2
$0.2107; 35B single **$0.7300**, 35B @np4 **$0.1771**. Break-even vs
`deepseek-v4-flash` $0.1772/1M = 70.54 tok/s at 300 W; vs
`deepseek-v4.1-flash` $1.20/1M = 10.42 tok/s. Full table, caveats and the
prompt-cost note in `.agi/context/local-maxxing/gpu/kidC_cost.md`.

Artifacts:
- `.agi/context/local-maxxing/bench/20260916T103631Z.jsonl` (7 `gpu-*` rows)
- `.agi/context/local-maxxing/gpu/kidC_cost.md`

## Commands (verbatim; idempotent; each ssh <= 10 min)

```
# 1. download the larger GGUF in background (nohup + poll)
ssh -F <keeper-dir>/ssh/config -o ConnectTimeout=15 local-town 'mkdir -p /data/ml/models /data/ml/logs && cd /data/ml && if [ -f /data/ml/models/Qwen3.5-35B-A3B-Q3_K_M.gguf ] && [ "$(stat -c%s /data/ml/models/Qwen3.5-35B-A3B-Q3_K_M.gguf)" -gt 16000000000 ]; then echo ALREADY_DONE; else (nohup curl -L --retry 3 -C - -o /data/ml/models/Qwen3.5-35B-A3B-Q3_K_M.gguf https://huggingface.co/unsloth/Qwen3.5-35B-A3B-GGUF/resolve/main/Qwen3.5-35B-A3B-Q3_K_M.gguf > /data/ml/logs/curl35b.log 2>&1 &) ; echo STARTED; fi; sleep 2; ps aux | grep -c "[c]url -L"'

# 2. sha256 + stop the 9B, free VRAM/RAM
ssh -F <keeper-dir>/ssh/config -o ConnectTimeout=15 local-town 'sha256sum /data/ml/models/Qwen3.5-35B-A3B-Q3_K_M.gguf; docker stop llama-server; sleep 3; nvidia-smi --query-gpu=memory.used,power.draw --format=csv,noheader; free -g | head -2'

# 3. run the larger model direct, wait for health
ssh -F <keeper-dir>/ssh/config -o ConnectTimeout=15 local-town 'docker rm -f llama-35b >/dev/null 2>&1; docker run -d --name llama-35b --restart no --gpus all --network host -v /data/ml/models:/models ghcr.io/ggml-org/llama.cpp:server-cuda --host 127.0.0.1 --port 8080 --model /models/Qwen3.5-35B-A3B-Q3_K_M.gguf --alias Qwen3.5-35B-A3B-Q3_K_M --jinja --fit on -np 4 -c 16384; for i in $(seq 1 30); do h=$(curl -s --max-time 5 http://127.0.0.1:8080/health 2>/dev/null); echo "t=$((i*10))s $h"; case "$h" in *ok*) break;; esac; sleep 10; done; nvidia-smi --query-gpu=memory.used,power.draw --format=csv,noheader; free -g | head -2'

# 4. rollback: remove 35B container, restore the 9B router
ssh -F <keeper-dir>/ssh/config -o ConnectTimeout=15 local-town 'docker rm -f llama-35b >/dev/null 2>&1; sleep 2; bash /data/ml/llama-server/run.sh; sleep 6; curl -s --max-time 20 http://127.0.0.1:8080/v1/models; nvidia-smi --query-gpu=memory.used,power.draw --format=csv,noheader; docker ps --format "{{.Names}} {{.Status}}"'
```

Tunnel-side bench client (core-town `/tmp/lmbench/tunnel_bench.py`) POSTs
`/v1/chat/completions` to `http://127.0.0.1:18080/v1`, reads `timings`
(`prompt_per_second`, `predicted_per_second`), with `ignore_eos` so generation
is a real 128 tokens; concurrency mode runs N threads and reports
`total_gen_tokens / wall`. GPU/loadavg sampled in parallel on the box into
`/data/ml/logs/sample_9b.log` and `sample_35b.log`.

## Evidence

- 35B sha256 `5607c8fcc8b04ada7d1a1152b9a5b6c1e67e6768232c16f6b03d9719d5ab1b2d`,
  size 16,356,375,168 B (`/v1/models` meta `n_params` 34,660,610,688, `size`
  16,345,385,472).
- 35B server log: `load_model: loading ...` -> `model loaded`,
  `n_slots = 4, n_ctx_slot = 4096`, `model loaded`, `listening on
  http://127.0.0.1:8080`; `llama_model_loader: tensor overrides to CPU are used
  with mmap enabled` (i.e. `--fit on` put experts on CPU).
- Tunnel `tg128` 35B: `{"predicted_n": 128, "predicted_per_second": 12.396,
  "wall_s": 11.464, "finish": "length"}`; 9B: `62.535`.
- Rollback proof, tunnel-side after restore: `/v1/models` =
  `['Qwen3.5-35B-A3B-Q3_K_M', 'Qwen3.5-9B-Q4_K_M']`; 9B completion
  `finish stop content 'pong'`; unknown id -> `HTTP 400
  {"error":{"code":400,"message":"model 'does-not-exist-xyz' not found"}}`.
- No IP-shaped string was written: only `127.0.0.1` appears; the box is named by
  the `local-town` alias. No git command was run.

## Caveats

The 35B's `n_gpu_layers` is chosen by `--fit on` and not echoed in the server log
at the default verbosity, so the exact -ngl is not recorded — only the
two-placements-in-one number that matters (VRAM 6666 MiB, GPU W 112). `--n-cpu-moe
N` takes an explicit N (there is no bare flag; `--cpu-moe` is the all-MoE form),
so per the fallback spirit the run used `--fit on` and let it decide the split
rather than hand-picking N and risking an OOM. `pp512 = 10.44 tok/s` is the
binding cost driver for large contexts and is left visible rather than hidden.

## Agent Notes
35B-A3B Q3_K_M loads on local-town via --fit on (6666 MiB VRAM, 112 W); tunnel-side tg128 12.40 tok/s (>=10), pp512 10.44; -np4 aggregate 51.09 tok/s -> exact break-even with deepseek-v4-flash (0.1771 vs 0.1772/1M out); 9B tunnel-side tg 62.54; fallback not needed; 9B router restored + unknown-id refused 400

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-1fec07a8 (TM.07) died mid-round (openrouter error code 520, deepseek/deepseek-v4.1-flash) after this kid finished but before the parent could review/harvest it -- cli.py done was never called, kids=[] in the outer manifest death record even though this node and its two artifact files existed on disk in the parent's own worktree, uncommitted. director-thought read the bytes directly in the parent's stead: bench jsonl rows match the node's claimed numbers exactly (62.535/12.396 tok/s tunnel-side, 51.09 agg @np4), cost row arithmetic in kidC_cost.md checks out, file scope matches this round's DISPATCH ORDERS Kid B description (the kid itself labelled its own work "Kid C", inherited from the hypothesis node's original round-1 TESTS text rather than this round's B/C relabelling -- a naming mismatch only, the content is exactly the tunnel-side-larger-model-plus-cost-row task), IP-grep on the full diff clean, no git command was run by the kid. Accepted and committed directly rather than re-run at GPU-box cost. Kid C (hygiene: redact 3 named gitignored IP-leak files, write spend.md) was never spawned and still needs its own round.
<!-- THOUGHT:END -->
