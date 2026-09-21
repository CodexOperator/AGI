# bonsai — cmds run (2026-09-18, kid a00-c0675ae5, TM.30)

Fork prebuilt releases (PrismML-Eng/llama.cpp, tag `prism-b10685-7dffb15`) — **a build is not required**.
Raw rows: `bonsai/probe.jsonl`; bench rows: `bench/20260918T050800Z.jsonl`.

## A1 (core-town, aarch64, 4x Neoverse-N1, Ubuntu 24.04) — CPU ternary
```
mkdir -p /tmp/bonsai-a1 && cd /tmp/bonsai-a1
curl -fsSL -o fork-arm64.tar.gz https://github.com/PrismML-Eng/llama.cpp/releases/download/prism-b10685-7dffb15/llama-prism-b10685-7dffb15-bin-ubuntu-arm64.tar.gz
curl -fsSL -o Ternary-Bonsai-8B-PQ2_0.gguf https://huggingface.co/prism-ml/Ternary-Bonsai-8B-gguf/resolve/main/Ternary-Bonsai-8B-PQ2_0.gguf
tar xzf fork-arm64.tar.gz -C fork && F=fork/llama-prism-b10685-7dffb15
$F/llama-bench -m Ternary-Bonsai-8B-PQ2_0.gguf -p 128 -n 64 -t 4 -r 2 -o jsonl   # pp128 4.706 tg64 2.754 t/s
$F/llama-completion -m Ternary-Bonsai-8B-PQ2_0.gguf -p "Say hello in exactly three words." -n 24 -t 4 -c 256 --temp 0
```
sha256 model `1376f942…` == HF lfs oid; tarball `238f34e5…`; backend `libggml-cpu-armv8.2_2.so`; output coherent.

## local-town (x86_64, local-town GPU sm_75, driver 595.84) — fork CUDA runs
```
# /data/ml/llama-prism-fork/prism-cuda-12.4.tar.gz (sha256 29326793…); tar xzf -C fork
docker run --rm --gpus all --entrypoint /bin/sh -v <forkdir>:/fork ghcr.io/ggml-org/llama.cpp:server-cuda \
  -c 'LD_LIBRARY_PATH=/fork /fork/llama-bench --list-devices'
grep -aoE "sm_75" /fork/libggml-cuda.so | wc -l    # 145; lib carries pq2_0 + ptq1_0 kernels
```
Host lacks `libcudart.so.12`; runs inside the existing `server-cuda` image. GPU had 1004 MiB free.

## Not done (next kid)
27B PTQ1_0 (5,946,648,928 B, sha256 `53107f53…`) **not downloaded** — local-town stayed on the
athena fetch (0.48 MB/s); A1 cannot hold it (4.2 GB free < 5.95 GB). No GPU tg/pp, no 27B number, no proxy row.

---

# TM.30 kid a00-da8359fa — GPU ternary proof + 27B header/fetch (2026-09-18)

Reached by `ssh -F ~/work/.sanctuary/ssh/config local-town '<cmd>'` from core-town
(<ip> -> local-town <ip>). Fork dir on belam:
`/data/ml/llama-prism-fork/fork/llama-prism-b10685-7dffb15` (CUDA, sm_75).

## 1. 27B PTQ1_0 GGUF header only (16 MiB range, NOT the 5.95 GB file), on core-town
```
curl -sL -r 0-16777215 -o /tmp/bonsai27b_hdr.bin \
  "https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/resolve/main/Ternary-Bonsai-2-27B-PTQ1_0.gguf"
python3 gguf_meta.py bonsai27b_hdr_first16MiB.bin  # scratch parser -> qwen35, 64 blocks, full_attention_interval 4
```
Budget table: `vram_budget.md`. **16 of 64 layers carry KV**; 65,536 B/token f16 ->
weights 5671 + KV 512 = 6183 MiB at `-c 8192` on a 7786 MiB card.

## 2. Ternary PQ2_0 runs FULLY on the GPU (1.7B — the real sm_75 kernel proof)
```
# fetch 463,290,464 B from HF onto belam (sha256 de68ba48... == HF lfs oid)
# then, inside the existing server-cuda image:
FORK=/data/ml/llama-prism-fork/fork/llama-prism-b10685-7dffb15
docker run --rm --gpus all --entrypoint /bin/sh -v $FORK:/fork -v /data/ml/models/bonsai:/models \
  ghcr.io/ggml-org/llama.cpp:server-cuda -c \
 'LD_LIBRARY_PATH=/fork /fork/llama-bench -m /models/Ternary-Bonsai-1.7B-PQ2_0.gguf \
    -ngl 99 -t 16 -p 512 -n 128 -r 3 -o jsonl'
```
out: **pp512 6892.82 t/s, tg128 317.94 t/s** (CUDA, ngl=99, 16 threads); VRAM
6680 -> 7646 MiB peak (the 9B server stayed resident, no offload). Row:
`bench/20260918T061455Z.jsonl`. Warm-up via `llama-completion` first.
NOTE `llama-bench` has no `-tb` flag (`-tb` is llama-server only) — `-tb 16` is
rejected as "invalid parameter"; `-t 16` is the llama-bench spelling.

## 3. 27B PTQ1_0 resumable fetch (started, still running — ~9-10h ETA)
```
cd /data/ml/models/bonsai && nohup python3 bonsai27b_fetch.py supervise > fetch27b_super.log 2>&1 &
python3 bonsai27b_fetch.py status
```
12 segments, no rate cap, sha256 53107f53... pinned. `cat Ternary-Bonsai-2-27B-PTQ1_0.gguf.seg* > final`
then sha256sum. **Measured egress cap: ~0.2 MB/s aggregate on belam no matter the
connection count** (8 uncapped parallel ranges = 0.200 MB/s; 12 xi12k = 0.067;
12 uncapped = 0.177). The 5.95 GB is ~9h of wall clock, shared with the
athena/gemma `fetch_parallel.py supervise` already on the box.
