# llama-cpp-kv — llama.cpp quantised KV, slot save/restore, prefix caching — reading digest
READ-ONLY. MEASURED = quoted from page/source read; ESTIMATE = inferred, arithmetic shown.
Local tree read (read-only): /home/ubuntu/src/llama.cpp
- VERSION (MEASURED): build b10951, commit 093a2f86c3e37c54fa3e1f9efb17b304f3433abd,
  dated 2026-09-14 05:24:05 +0200. Backends built: ggml-cpu (no CUDA in this build).

## PAGE 1 — server README (fetched 2026-09-18)
URL: https://raw.githubusercontent.com/ggml-org/llama.cpp/master/tools/server/README.md
- `-ctk, --cache-type-k TYPE` / `-ctv, --cache-type-v TYPE` (MEASURED, quoted):
  "allowed values: f32, f16, bf16, q8_0, q4_0, q4_1, iq4_nl, q5_0, q5_1 (default: f16)".
  Env: LLAMA_ARG_CACHE_TYPE_K / LLAMA_ARG_CACHE_TYPE_V.
- `--cache-prompt, --no-cache-prompt` (MEASURED): "whether to enable prompt caching (default:
  enabled)". This is the prefix cache: common prefix not re-processed.
- `--cache-reuse N` (MEASURED, quoted): "min chunk size to attempt reusing from the cache via KV
  shifting, requires prompt caching to be enabled (default: 0)".
- `--cache-idle-slots` (MEASURED): "save idle slots to the prompt cache on new task ... (default:
  enabled, requires cache-ram)".
- `--slot-save-path PATH` (MEASURED): "path to save slot kv cache (default: disabled)".
- `--np, --parallel N`: parallel slots; `--kv-unified` (MEASURED, server.cpp L152-155): when
  n_parallel is auto, "using n_parallel = 4 and kv_unified = true".
- SLOT SAVE API (MEASURED, README §): `POST /slots/{id_slot}?action=save|restore|erase`. Save
  response example: `"n_saved": 1745, "n_written": 14309796, "save_ms": 49.865`; restore
  `"restore_ms": 42.937`. File goes under `--slot-save-path`. NOTE: 14309796/1745 ≈ 8200 B/token
  for that (unstated) model — ESTIMATE that it is a mid-size model at f16; the file carries the
  slot's KV in its current cache type, so a quantised cache saves proportionally fewer bytes.

## PAGE 2 — local source (read 2026-09-18, read-only)
- QUANTISED V REQUIRES FLASH ATTENTION (MEASURED, src/llama-context.cpp):
  L3704-3710: `if (ggml_is_quantized(params.type_v) && params.flash_attn_type !=
  LLAMA_FLASH_ATTN_TYPE_ENABLED) { ... "quantized V cache requires flash_attn to be enabled" }`.
  L465 also throws "quantized V cache was requested, but this requires Flash Attention".
- QUANTISED K PATH (MEASURED): L3715 `if (params.flash_attn_type != DISABLED &&
  ggml_is_quantized(params.type_k))` selects the quantised-K FA path.
- CPU FA EXISTS (MEASURED, ggml/src/ggml-cpu/ggml-cpu.c): L2027
  `ggml_compute_forward_flash_attn_ext(...)` — FA is implemented on the CPU backend, so quantised
  KV is not GPU-only in principle. PERFORMANCE on ARM4C is untested here (ESTIMATE: FA on CPU is
  memory-bandwidth bound; quantised KV cuts bytes read, which should help).
- BLOCK SIZES (MEASURED, ggml/src/ggml-common.h + ggml.c): QK4_0=32, block_q4_0 = half scale +
  16 bytes nibbles = 18 B / 32 elems = 0.5625 B/elem. QK8_0=32, block_q8_0 = half scale + 32 int8
  = 34 B / 32 elems = 1.0625 B/elem. q5_0 = (2+4+16)/32 = 0.6875 B/elem.
- COMPRESSION vs f16 (MEASURED-derived): q8_0 = 2/1.0625 = 1.88x; q4_0 = 2/0.5625 = 3.56x.
  So llama.cpp q4_0 KV is ~3.6x smaller than f16, NOT 4x and far from TurboQuant's claimed 6x.

## BYTE TABLE — llama.cpp cache types (ESTIMATE — arithmetic shown)
Formula: bytes = layers × kv_heads × head_dim × seq_len × 2 (K+V) × B_per_elem.
- 9B-class (36 layers, 8 kv_heads, head_dim 128; per token/layer 2×8×128 = 2048 elems):
  4k tokens → 36 × 2048 × 4096 = 301,989,888 elems.
    f16: ×2.0 = 603,979,776 B = 576 MiB.
    q8_0: ×1.0625 = 320,864,256 B = 306 MiB.  q4_0: ×0.5625 = 169,869,312 B = 162 MiB.
  32k tokens (×8): f16 = 4608 MiB (4.5 GiB); q8_0 = 2448 MiB (2.39 GiB);
    q4_0 = 1296 MiB (1.27 GiB).
- 27B-class (64 layers, 8 kv_heads, head_dim 128):
  4k tokens → 64 × 2048 × 4096 = 536,870,912 elems.
    f16: ×2.0 = 1,073,741,824 B = 1024 MiB (1.0 GiB).
    q8_0: ×1.0625 = 570,425,344 B = 544 MiB.  q4_0: ×0.5625 = 301,989,888 B = 288 MiB.
  32k tokens (×8): f16 = 8192 MiB (8.0 GiB); q8_0 = 4352 MiB (4.25 GiB);
    q4_0 = 2304 MiB (2.25 GiB).
- ARM4C FIT (ESTIMATE): 27B/32k f16 KV = 8.0 GiB > 7 GiB free → impossible. q4_0 → 2.25 GiB,
  leaving room for a q4_K weights file (~15-16 GiB for 27B) — which does NOT fit 23 GB total
  alongside. Realistic ARM4C target is 9B/32k: q4_0 KV 1.27 GiB + ~5-6 GiB q4 weights ≈ 7 GiB.
- PRACTICAL NOTE (MEASURED recommendation pattern, not from a doc page): q8_0 for K is the common
  safe default, q4_0 for V is where quality loss shows; V quant is what forces Flash Attention on.
