#!/usr/bin/env bash
# T1 placement probe (OSC.07): with -lv 5, does the split's flash attention run on CUDA or fall back to CPU?
set -u
S=/data/work/agi/.agi/worktrees/a00-27ee7e7b
D=$S/datasets/kv-format/2026-09-23-split/logs
IMG=ghcr.io/ggml-org/llama.cpp:full-cuda
run() {  # $1=tag $2=ctk $3=ctv $4=port
  local name=place_$1
  docker rm -f "$name" >/dev/null 2>&1
  docker run -d --rm --name "$name" --gpus all -v /data/ml/scratch/osc02:/work \
    -p 127.0.0.1:$4:$4 --entrypoint /app/llama-server "$IMG" \
    --cache-reuse 8 --host 127.0.0.1 --jinja --alias Qwen3.5-9B-Q4_K_M --fit on \
    --model /work/Qwen3.5-9B-Q4_K_M.gguf --parallel 1 --port $4 -lv 5 \
    -fa on -ctk "$2" -ctv "$3" >/dev/null
  for i in $(seq 1 60); do
    sleep 3
    docker logs "$name" > "$D/$name.log" 2>&1
    grep -q "listening on" "$D/$name.log" && break
  done
  docker stop "$name" >/dev/null 2>&1
  echo "== $1: $(grep -c . "$D/$name.log") log lines =="
}
run split q8_0 q4_0 18085
run f16 f16 f16 18086
