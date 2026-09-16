# Kid A — box + server + model 1 (local-town)

Parent: `hypothesis:gpu-local-town-openai-endpoint` · Kid A slice = "box + server + model 1".
All commands below are **verbatim**, run as
`ssh -F <keeper-dir>/ssh/config local-town '<cmd>'` from core-town.
Every command is idempotent; the long ones use `nohup` + poll; each ssh invocation < 10 min.

Host: **local-town** · gpu-8g SUPER 8192 MiB · driver 595.84 · `/data` 339G (317G free) ·
16 vCPU · 15 GB RAM · docker with `nvidia` runtime · systemd 255 --user.

---

## 0. Read-only box probe (2026-09-16)

```
hostname; nvidia-smi --query-gpu=name,memory.total,memory.used,driver_version --format=csv; df -h /data | tail -1; docker images --format "{{.Repository}}:{{.Tag}} {{.ID}}"; ls /data/ml 2>/dev/null; nproc; free -g | head -2
```
out: `local-town`, memory.used **1 MiB**, `/data 339G 5.2G 317G`, only `nvidia/cuda:12.6.3-base-ubuntu24.04`,
`/data/ml/.venv`, 16 cpus, Mem 15 total / 14 available.

## 1. Container runtime probe

```
which nvidia-container-runtime nvidia-container-toolkit curl aria2c; docker info 2>/dev/null | grep -i runtime; ls -d /data/ml/.venv 2>/dev/null; cat /etc/docker/daemon.json 2>/dev/null; systemctl is-active docker
```
out: `/usr/bin/nvidia-container-runtime`, `/usr/bin/nvidia-container-toolkit`, `/usr/bin/curl`;
docker runtime `nvidia` registered; docker active.

## 2. Pull image + download the GGUF (idempotent; nohup + poll)

```
mkdir -p /data/ml/models /data/ml/logs && cd /data/ml && (nohup docker pull ghcr.io/ggml-org/llama.cpp:server-cuda > /data/ml/logs/pull.log 2>&1 &) && (nohup curl -L --retry 3 -o /data/ml/models/Qwen3.5-9B-Q4_K_M.gguf https://huggingface.co/unsloth/Qwen3.5-9B-GGUF/resolve/main/Qwen3.5-9B-Q4_K_M.gguf > /data/ml/logs/curl.log 2>&1 &) && sleep 3 && echo STARTED && ls -la /data/ml/models /data/ml/logs
```

Poll (idempotent, safe to re-run):

```
du -h /data/ml/models/Qwen3.5-9B-Q4_K_M.gguf; tail -c 400 /data/ml/logs/pull.log; echo ---; docker images | head; ps aux | grep -E "curl|docker pull" | grep -v grep | wc -l
```

```
du -h /data/ml/models/Qwen3.5-9B-Q4_K_M.gguf; echo ---PULL---; tail -3 /data/ml/logs/pull.log; echo ---IMAGES---; docker images --format "{{.Repository}}:{{.Tag}} {{.ID}} {{.Size}}"
```

```
stat -c "%s %n" /data/ml/models/Qwen3.5-9B-Q4_K_M.gguf; ps aux | grep -c "[c]url -L"
```

**Image:** `ghcr.io/ggml-org/llama.cpp:server-cuda`
repo digest `sha256:d4bdfe78ad26a1ef3ccc834fc4e4a106d882e0f2163dd9a06e067c580c742101`
(image id `d4bdfe78ad26`, 6.99 GB). `llama-server` version **build 10991, commit 930e2fa59**.

**Model:** `/data/ml/models/Qwen3.5-9B-Q4_K_M.gguf`
exactly **5,680,522,464 B** (matches the HF API blob size),
sha256 **`03b74727a860a56338e042c4420bb3f04b2fec5734175f4cb9fa853daf52b7e8`**.
0 bytes to core-town — the file was written only to `/data` on local-town.

```
sha256sum /data/ml/models/Qwen3.5-9B-Q4_K_M.gguf; docker inspect --format "{{index .RepoDigests 0}}" ghcr.io/ggml-org/llama.cpp:server-cuda
```

## 3. Capability probe (router mode present in this image)

```
docker run --rm --gpus all ghcr.io/ggml-org/llama.cpp:server-cuda --version 2>&1 | head -5; echo "---HELP---"; docker run --rm --gpus all ghcr.io/ggml-org/llama.cpp:server-cuda --help 2>&1 | grep -E "models-dir|models-max|fit|jinja|n-cpu-moe|alias" | head -20
```
out includes `--models-dir PATH` (router server), `--models-max N`, `--fit`, `--jinja`,
`-ncmoe, --n-cpu-moe`, `-a, --alias`. → the `--models-dir` route is available; **no fallback needed**.

Binary layout: `/app/llama-server` and `/app/llama` (multi-tool launcher). There is **no**
`/app/llama-bench`; `llama help all` exposes `bench`:

```
docker run --rm --entrypoint /app/llama --gpus all ghcr.io/ggml-org/llama.cpp:server-cuda --help 2>&1 | head -40
docker run --rm --entrypoint /app/llama --gpus all ghcr.io/ggml-org/llama.cpp:server-cuda help all 2>&1 | head -60
```
(`/app/llama-bench` → `stat /app/llama-bench: no such file or directory`; use `llama bench`.)

## 4. run.sh (idempotent; writes server container)

```
mkdir -p /data/ml/llama-server && cat > /data/ml/llama-server/run.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
IMAGE=ghcr.io/ggml-org/llama.cpp:server-cuda
NAME=llama-server
docker rm -f "$NAME" 2>/dev/null || true
docker run -d --name "$NAME" --restart unless-stopped --gpus all --network host \
  -v /data/ml/models:/models \
  "$IMAGE" \
  --host 127.0.0.1 --port 8080 \
  --models-dir /models --models-max 1 \
  --fit on --jinja -np 2 \
  > /data/ml/logs/server_run.log 2>&1
cat /data/ml/logs/server_run.log
EOF
chmod +x /data/ml/llama-server/run.sh && bash /data/ml/llama-server/run.sh
```

## 5. Server up: /v1/models + /v1/chat/completions

```
docker ps --format "{{.Names}} {{.Status}}"; echo ---LOG---; docker logs llama-server 2>&1 | tail -20; echo ---MODELS---; curl -s --max-time 10 http://127.0.0.1:8080/v1/models
```
out: container up; `starting server in router mode. models will be automatically loaded on-demand`;
`listening on http://127.0.0.1:8080`; `/v1/models` → `{"data":[{"id":"Qwen3.5-9B-Q4_K_M", ... "status":{"value":"unloaded"} ...}]}`.
Router child args recorded by the server: `--alias Qwen3.5-9B-Q4_K_M --fit on --model /models/Qwen3.5-9B-Q4_K_M.gguf --parallel 2`.

Completion #1 (loads the model; 16 tokens; thinking on by default):

```
curl -s --max-time 240 http://127.0.0.1:8080/v1/chat/completions -H "Content-Type: application/json" -d '{"model":"Qwen3.5-9B-Q4_K_M","messages":[{"role":"user","content":"Reply with exactly the word: pong"}],"max_tokens":16,"temperature":0}' -o /data/ml/logs/chat1.json -w "HTTP %{http_code} time %{time_total}s\n"; echo ---RESP---; cat /data/ml/logs/chat1.json; echo; echo ---GPU---; nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu,power.draw --format=csv,noheader; echo ---LOAD---; cat /proc/loadavg
```
out: `HTTP 200`, `finish_reason":"length"` (16-token cap, reasoning_content stream),
prompt 0.41 tok/s (includes 40 s model load), predicted **58.47 tok/s**.
GPU: **memory.used 6674 MiB / 8192 MiB, 148 W**; loadavg `0.83 1.09 0.66`.

Completion #2 (thinking disabled → clean stop):

```
curl -s --max-time 150 http://127.0.0.1:8080/v1/chat/completions -H "Content-Type: application/json" -d '{"model":"Qwen3.5-9B-Q4_K_M","messages":[{"role":"user","content":"Reply with exactly the word: pong"}],"max_tokens":64,"temperature":0,"chat_template_kwargs":{"enable_thinking":false}}' -o /data/ml/logs/chat2.json -w "HTTP %{http_code} time %{time_total}s\n"; echo ---RESP---; cat /data/ml/logs/chat2.json; echo; echo ---GPU---; nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu,power.draw --format=csv,noheader; cat /proc/loadavg
```
out: `HTTP 200`, **`finish_reason":"stop"`**, `content":"pong"`, 57.08 tok/s.
GPU: memory.used **6674 MiB**, loadavg `0.70 1.06 0.66`.

Final re-verify after restart:

```
docker start llama-server >/dev/null; sleep 5; curl -s --max-time 20 http://127.0.0.1:8080/v1/models | head -c 300; echo; curl -s --max-time 240 http://127.0.0.1:8080/v1/chat/completions -H "Content-Type: application/json" -d '{"model":"Qwen3.5-9B-Q4_K_M","messages":[{"role":"user","content":"Reply with exactly: pong"}],"max_tokens":32,"temperature":0,"chat_template_kwargs":{"enable_thinking":false}}' -o /data/ml/logs/chat_final.json -w "HTTP %{http_code} time %{time_total}s\n"; python3 -c "import json;d=json.load(open(\"/data/ml/logs/chat_final.json\"));print(\"finish_reason:\",d[\"choices\"][0][\"finish_reason\"]);print(\"content:\",d[\"choices\"][0][\"message\"][\"content\"])"; echo ---GPU---; nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu,power.draw --format=csv,noheader; cat /proc/loadavg
```
out: `HTTP 200` in 3.5 s (warm cache), `finish_reason: stop`, `content: pong`,
GPU **6674 MiB**, loadavg `0.43 0.83 0.73`.

### Note on "all layers in VRAM" evidence
This build's `llama-server` at default verbosity does **not** print the historic
`offloaded N/N layers to GPU` / model-buffer lines (greps for `tensor|buffer|device|layer|
offloaded|CUDA0` return nothing), and there is no `/app/llama-bench` binary — `llama bench`
is the tool. Full offload is therefore evidenced by the bench rows below
(`backends: CUDA`, `n_gpu_layers: 99`, GPU util **100 %**, `gpu_mem_used_max_mib 5568`)
plus `nvidia-smi memory.used 6674 MiB` with the server resident — **not** by a log line.

## 6. llama-bench x5 with per-row GPU telemetry (idempotent)

The server must be stopped first: it holds ~6.6 GB of the 8 GB and `llama bench -ngl 99`
gets OOM/killed ("failed to load model") while it runs. Stop, bench, restart.

```
docker stop llama-server; sleep 3; nvidia-smi --query-gpu=memory.used --format=csv,noheader; (nohup bash /data/ml/bin/gpu_bench.sh > /data/ml/logs/gpu_bench.log 2>&1 &); sleep 2; echo RERUN_LAUNCHED
```

`gpu_bench.sh` (written on the box; 5 iterations, each samples `nvidia-smi` every 500 ms
for max memory / power / util, captures loadavg before+after, runs `llama bench -p 512 -n 128 -ngl 99 -o json`):

```
mkdir -p /data/ml/bench /data/ml/bin && cat > /data/ml/bin/gpu_bench.sh <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
IMAGE=ghcr.io/ggml-org/llama.cpp:server-cuda
MODEL=/models/Qwen3.5-9B-Q4_K_M.gguf
OUT=/data/ml/bench/kidA_bench_raw.jsonl
mkdir -p /data/ml/bench /data/ml/logs
: > "$OUT"
for i in 1 2 3 4 5; do
  SMILOG=/data/ml/logs/smi_$i.csv
  nvidia-smi --query-gpu=memory.used,power.draw,utilization.gpu --format=csv,noheader,nounits -lms 500 > "$SMILOG" 2>/dev/null &
  SMIPID=$!
  LOAD_BEFORE=$(cat /proc/loadavg)
  docker run --rm --entrypoint /app/llama --gpus all -v /data/ml/models:/models "$IMAGE" \
     bench -m "$MODEL" -p 512 -n 128 -ngl 99 -o json > /data/ml/logs/bench_$i.json 2> /data/ml/logs/bench_$i.err
  RC=$?
  kill $SMIPID 2>/dev/null; wait $SMIPID 2>/dev/null
  MAXMEM=$(awk -F, 'BEGIN{m=0}{gsub(/ /,"");if($1+0>m)m=$1+0}END{print m}' "$SMILOG")
  MAXPWR=$(awk -F, 'BEGIN{m=0}{gsub(/ /,"");if($2+0>m)m=$2+0}END{print m}' "$SMILOG")
  MAXUTIL=$(awk -F, 'BEGIN{m=0}{gsub(/ /,"");if($3+0>m)m=$3+0}END{print m}' "$SMILOG")
  LOAD_AFTER=$(cat /proc/loadavg)
  N=$(wc -l < "$SMILOG")
  python3 - "$i" "$RC" "$MAXMEM" "$MAXPWR" "$MAXUTIL" "$LOAD_BEFORE" "$LOAD_AFTER" "$N" /data/ml/logs/bench_$i.json "$OUT" <<'PY'
import sys,json
i,rc,mem,pwr,util,lb,la,n,benchf,out = sys.argv[1:]
rec={"iter":int(i),"rc":int(rc),"smi_samples":int(n),
     "gpu_mem_used_max_mib":int(mem),"gpu_power_draw_max_w":float(pwr),
     "gpu_util_max_pct":int(util),
     "loadavg_before":lb.strip(),"loadavg_after":la.strip(),
     "bench":json.load(open(benchf))}
open(out,"a").write(json.dumps(rec)+"\n")
PY
done
echo BENCH_DONE
EOF
chmod +x /data/ml/bin/gpu_bench.sh && (nohup bash /data/ml/bin/gpu_bench.sh > /data/ml/logs/gpu_bench.log 2>&1 &) && sleep 2 && echo LAUNCHED
```

Poll + fetch:

```
tail -3 /data/ml/logs/gpu_bench.log; wc -l /data/ml/bench/kidA_bench_raw.jsonl; echo ---; head -c 300 /data/ml/logs/bench_1.json
cat /data/ml/bench/kidA_bench_raw.jsonl
```

### Bench summary (5 iterations × 5 samples each = 25 samples per direction)

| iter | pp512 avg tok/s | tg128 avg tok/s | mem MiB | power W | util % | loadavg after |
|---|---|---|---|---|---|---|
| 1 | 1505.08 | 62.98 | 5568 | 239.92 | 100 | 0.91 0.91 0.66 |
| 2 | 1558.29 | 63.51 | 5568 | 236.85 | 100 | 1.04 0.95 0.69 |
| 3 | 1563.77 | 63.60 | 5568 | 234.59 | 100 | 1.01 0.96 0.72 |
| 4 | 1564.47 | 63.62 | 5568 | 236.30 | 100 | 1.00 0.97 0.75 |
| 5 | 1563.58 | 63.54 | 5568 | 235.53 | 100 | 0.92 0.97 0.77 |

`backends: CUDA`, `n_gpu_layers: 99`, `gpu_info: NVIDIA GeForce gpu-8g SUPER` in every row.
**pp512 ≈ 1560 tok/s (claim ≥ 500 ✓); tg128 ≈ 63.5 tok/s (claim ≥ 30 ✓);
gpu_mem_used_max_mib 5568 ≥ 5 GB ✓.**

## 7. Rollback proof (idempotent; server restored afterwards for Kid B)

```
docker rm -f llama-server >/dev/null 2>&1; sleep 2; echo "---PORT AFTER RM---"; curl -s --max-time 5 http://127.0.0.1:8080/v1/models -o /dev/null -w "curl_exit=%{exitcode} http=%{http_code}\n" 2>&1 || echo "curl refused rc=$?"; docker ps --format "{{.Names}}" | wc -l; echo "---RESTORE---"; bash /data/ml/llama-server/run.sh; sleep 5; curl -s --max-time 20 http://127.0.0.1:8080/v1/models -o /dev/null -w "restored http=%{http_code}\n"
```
out: after `rm -f` → `curl_exit=7 http=000` (connection refused), `0` containers;
after `run.sh` → new container, `restored http=200`.
**Rollback = `docker rm -f llama-server` closes the port; `run.sh` is idempotent and re-creates it.**
Final state left on the box: `llama-server` **running** (for the Kid B tunnel slice).
