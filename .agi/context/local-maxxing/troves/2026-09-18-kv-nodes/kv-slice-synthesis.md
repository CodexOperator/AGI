# kv-slice-synthesis — KV-cache compression landscape + byte table — SYNTHESIS
READ-ONLY. MEASURED = quoted from a page/source read; ESTIMATE = inferred, arithmetic shown.
Pages read this session (7): arXiv 2504.19874v1 + Google blog; arXiv 2402.02750v2 + KIVI repo;
arXiv 2401.18079v6 + KVQuant repo; llama.cpp server README + local src (b10951, 093a2f86c3);
arXiv 2412.19442 (survey). Per-page digests: turboquant-2504-19874.md, kivi-2402-02750.md,
kvquant-2401-18079.md, llama-cpp-kv.md.

## WHAT THE OWNER LIKELY MEANS (MEASURED)
- "TurboQuant (Google, 2025)" = arXiv:2504.19874v1, Zandieh/Daliri/Hadian/Mirrokni, 28 Apr 2025,
  Google Research + DeepMind + NYU. It is a general online vector-quantisation method; KV-cache is
  one application. Google blog (2025) frames it for KV: "at least 6x" memory, "3 bits", ICLR 2026.
- "KV turbo / KVTurbo / TurboKV" = third-party implementations of TurboQuant, not a distinct paper.
  PyPI `turbokv` v0.1.0 self-describes as "First open-source implementation of TurboQuant"; claims
  4-7x. Others: 0xSero/turboquant (Triton+vLLM, 3-bit K/2-bit V), OnlyTerp/turboquant,
  llmsresearch/kvcompress. NONE from Google; NO CPU path; licences unverified (read per-repo before
  any use).

## COMPARISON (all numbers MEASURED from the cited page unless marked ESTIMATE)
| Method | bits/KV elem | quality loss | speed | code+licence | CPU? |
|---|---|---|---|---|---|
| TurboQuant (2504.19874) | 3.5 neutral; 2.5 marginal | "absolute quality neutrality with 3.5 bits"; marginal at 2.5 | not a serving system; no kernel in paper | no upstream code; 3rd-party GPU/Triton; licence unverified | no |
| KIVI (2402.02750) | 2-bit asym (K per-channel, V per-token) + 32-tok fp16 residual | "almost the same quality"; 2.6x peak-mem incl weights | 2.35-3.47x throughput; 4x batch | github jy-yuan/KIVI, MIT, stars 433, pushed 2025-11 | no (CUDA) |
| KVQuant (2401.18079) | nuq4/3/2 ≈ 3.7/4.8/6.9x savings | <0.02 / <0.1 / <0.5 PPL on Wikitext-2 | up to ~1.7x vs fp16 matvec | github SqueezeAILab/KVQuant; NO licence file; pushed 2024-08 | no (CUDA) |
| llama.cpp q8_0 | 1.0625 B/elem = 1.88x | low (safe default for K) | CPU-native, FA available | llama.cpp MIT | YES |
| llama.cpp q4_0 | 0.5625 B/elem = 3.56x | more loss, esp. V | CPU-native; V-quant forces FA | llama.cpp MIT | YES |
| llama.cpp q5_0 | 0.6875 B/elem = 2.91x | middle | CPU-native | llama.cpp MIT | YES |

## BYTE TABLE (ESTIMATE — arithmetic shown; formula bytes = L×kvH×D×seq×2×(K+V)×B/elem)
9B-class = 36 layers, 8 kv_heads, head_dim 128 (Qwen3-8B-like). 27B-class = 64 layers, 8 kv_heads,
head_dim 128 (Qwen3-32B-like). "Ideal" = no metadata; llama.cpp q4_0/q8_0 include block overhead.
| cache | 9B @4k | 9B @32k | 27B @4k | 27B @32k |
|---|---|---|---|---|
| f16 (llama default) | 576 MiB | 4.5 GiB | 1.0 GiB | 8.0 GiB |
| llama q8_0 (1.0625 B/e) | 306 MiB | 2.39 GiB | 544 MiB | 4.25 GiB |
| llama q4_0 (0.5625 B/e) | 162 MiB | 1.27 GiB | 288 MiB | 2.25 GiB |
| KIVI 2-bit (ideal ÷8 + residual) | ~76 MB | ~606 MB | ~135 MB | ~1.08 GB |
| KVQuant nuq2 (÷6.9) | ~83 MiB | ~667 MiB | ~148 MiB | ~1.16 GiB |
| TurboQuant 3.5-bit (÷~4.57) | ~126 MiB | ~1008 MiB | ~224 MiB | ~1.75 GiB |
| TurboQuant 2.5-bit (÷6.4) | ~90 MiB | ~720 MiB | ~160 MiB | ~1.25 GiB |
(All ESTIMATE; ±20% on real head/layer counts. KIVI/KVQuant/TurboQuant rows are research numbers,
not achievable on ARM4C without a CPU implementation that does not currently exist.)

## HARDWARE VERDICT (ESTIMATE)
- ARM4C (4-core, 23 GB RAM, ~7 GB free, no GPU): only llama.cpp q4_0/q8_0 is runnable today.
  27B/32k f16 = 8.0 GiB KV alone → impossible. 27B/32k q4_0 = 2.25 GiB KV, but 27B q4 weights
  ~15-16 GiB → total > 23 GB, no fit. Realistic: 9B/32k q4_0 = 1.27 GiB KV + ~5-6 GiB q4 weights.
- V-quantisation needs Flash Attention; this build (ggml-cpu only) has CPU FA, so it is possible,
  but CPU-FA throughput on ARM4C is untested here (ESTIMATE: bandwidth-bound).
- GPU2070S / 8 GB GPU: a 9B/32k q4_0 KV (1.27 GiB) + q4 weights (~5-6 GiB) fits 8 GB only barely;
  27B never fits.

## MECHANISMS ALREADY IN llama.cpp (MEASURED, b10951)
- `-ctk/-ctv` quantise KV: f32/f16/bf16/q8_0/q4_0/q4_1/iq4_nl/q5_0/q5_1 (default f16).
- `--slot-save-path` + `POST /slots/{id}?action=save|restore|erase` persists a slot's KV to disk;
  saves in the cache's current type, so a quantised cache writes fewer bytes.
- `--cache-prompt` (default on) = prefix cache across requests/slots; `--cache-reuse N` shifts KV
  to reuse a matched chunk; `--cache-idle-slots` (default on, needs `--cache-ram`) parks idle slots.
- `--np/--parallel` slots + `--kv-unified` (auto → np=4, unified=true).
- CAVEAT (MEASURED, README): prompt caching can be non-deterministic — "logits are not guaranteed
  to be bit-for-bit identical for different batch sizes".

## GAPS / NEXT (ESTIMATE)
- No CPU implementation of KIVI/KVQuant/TurboQuant found → opportunity: implement per-channel-K
  2-bit + per-token-V dequant in ggml-cpu, or port KIVI's idea to llama.cpp's q4_0 path.
- q4_0 KV in llama.cpp = 3.56x, well short of the 6x research claims → the headroom is real but
  needs new code, not a flag.
