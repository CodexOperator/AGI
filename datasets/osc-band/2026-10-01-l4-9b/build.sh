#!/usr/bin/env bash
# L4 run 5 build (hypothesis:lm-l4-direct-head-windows-hold-on-the-served-9b): upstream llama.cpp at the pinned sha,
# CPU only, built twice -- unpatched (base) and with head-window.patch (patched) -- inside a memory-capped container.
# Trees live OUTSIDE the repo under $SCRATCH; only this script and the patch are committed.
# usage: bash build.sh [SCRATCH=/data/tmp/l4-9b]
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SHA="$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['llama_cpp_sha'])" "$HERE/params.json")"
SCRATCH="${1:-/data/tmp/l4-9b}"
IMG=l4-9b-build:alpine
CAP=(--memory 7g --cpus 6)
mkdir -p "$SCRATCH"
if ! docker image inspect "$IMG" >/dev/null 2>&1; then   # tools image: a capped container + commit
  docker rm -f l4-9b-tools >/dev/null 2>&1 || true
  docker run "${CAP[@]}" --name l4-9b-tools alpine:latest apk add --no-cache build-base cmake linux-headers git
  docker commit l4-9b-tools "$IMG" && docker rm l4-9b-tools
fi
[ -d "$SCRATCH/llama.cpp" ] || git clone -q https://github.com/ggml-org/llama.cpp.git "$SCRATCH/llama.cpp"
git -C "$SCRATCH/llama.cpp" fetch -q --depth 50 origin "$SHA" 2>/dev/null || true
for t in base patched; do
  src="$SCRATCH/llama.cpp-$t"
  [ -d "$src" ] || git -C "$SCRATCH/llama.cpp" worktree add -q --detach "$src" "$SHA"
  git -C "$src" checkout -q --detach "$SHA" && git -C "$src" checkout -q -- .
  [ "$t" = patched ] && git -C "$src" apply "$HERE/head-window.patch"
  docker run --rm "${CAP[@]}" -u "$(id -u):$(id -g)" -v "$src:$src" -w "$src" "$IMG" sh -c \
    "cmake -B build -DGGML_NATIVE=ON -DGGML_CUDA=OFF -DLLAMA_CURL=OFF -DBUILD_SHARED_LIBS=OFF \
       -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_SERVER=OFF -DCMAKE_BUILD_TYPE=Release >/dev/null &&
     cmake --build build -j 4 --target llama-perplexity llama-tokenize >/dev/null && ls -la build/bin"
done
echo "built $SHA: $SCRATCH/llama.cpp-{base,patched}/build/bin"
