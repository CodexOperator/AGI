#!/bin/bash
# OSC.09 probe: is the fixed ~45 s cold cost the CUDA JIT ComputeCache? run 1 = empty cache, run 2 = same cache warm.
set -u
SC=/data/ml/scratch/osc02; CACHE=$SC/coldcache2
S="$(cd "$(dirname "$0")/../../../../.." && pwd)"; OUT="$(python3 "$S/.agi/context/local-maxxing/paths.py" --local serving_sweep_cold_out_dir)"
IMG=ghcr.io/ggml-org/llama.cpp:full-cuda; M=/work/Qwen3.5-9B-Q4_K_M.gguf
mkdir -p $CACHE
run(){ # $1 tag $2 port
  local tag=$1 port=$2 name=cp$1
  docker rm -f $name >/dev/null 2>&1
  docker run --rm -d --name $name --gpus all -v $SC:/work -v $OUT:/out -v $CACHE:/root/.nv/ComputeCache \
    -p 127.0.0.1:$port:$port --entrypoint /app/llama-server $IMG \
    --cache-reuse 8 --host 0.0.0.0 --jinja --alias Qwen3.5-9B-Q4_K_M --fit on --model $M --parallel 1 \
    --port $port -lv 1 --log-file /out/${name}.log >/dev/null
  for i in $(seq 1 600); do curl -sf --max-time 3 http://127.0.0.1:$port/health >/dev/null && break; sleep 1; done
  local t0=$(date +%s.%N)
  R=$(curl -s --max-time 900 -X POST http://127.0.0.1:$port/v1/chat/completions -H 'Content-Type: application/json' \
      -d '{"model":"Qwen3.5-9B-Q4_K_M","messages":[{"role":"user","content":"hi"}],"max_tokens":8,"temperature":0,"chat_template_kwargs":{"enable_thinking":false}}')
  echo "$tag cache_mb=$(docker run --rm -v $CACHE:/c alpine du -sm /c 2>/dev/null|cut -f1) wall=$(echo "$(date +%s.%N)-$t0"|bc) $(echo $R|python3 -c 'import sys,json;t=json.load(sys.stdin).get("timings",{});print("prompt_n=%s prompt_ms=%s prompt_tps=%.1f"%(t.get("prompt_n"),t.get("prompt_ms"),t.get("prompt_per_second",0)))')"
  docker rm -f $name >/dev/null 2>&1
}
mkdir -p $OUT/logs
run emptycache 18093
run warmcache  18094
