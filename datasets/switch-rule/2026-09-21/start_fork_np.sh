#!/bin/bash
# $1 = np (slots), $2 = ctx total. arm B = no LoRA.
NP=${1:-1}; CTX=${2:-8192}
docker rm -f fork-bonsai 2>/dev/null || true
docker run -d --name fork-bonsai --gpus all --network host \
  -v /data/ml/models:/models \
  -v /data/work/trove/20260920/OrcaBonsai-27B-Uncensored/gguf:/lora \
  -v /data/ml/llama-prism-fork/fork/llama-prism-b10685-7dffb15:/fork \
  -e LD_LIBRARY_PATH=/fork \
  --entrypoint /fork/llama-server \
  ghcr.io/ggml-org/llama.cpp:server-cuda \
  -m /models/bonsai/Ternary-Bonsai-2-27B-PTQ1_0.gguf \
  -c $CTX -ngl 99 -fa on -np $NP -ctk q4_0 -ctv q4_0 --jinja \
  --temp 1.0 --top-p 0.95 --top-k 20 --host 127.0.0.1 --port 8899
echo "started fork-bonsai np=$NP ctx=$CTX"
