# Trove: qwen38-50b — resolving "qwen3.8 50b" (MODEL CARD slice)

READ-ONLY public web + HF API. All numbers MEASURED (from a page/API read) unless tagged ESTIMATE.
Dates are page/API read dates: 2026-09-18. No keys, no clones, no installs.

## HEADLINE
**There is NO official Qwen3.8-50B.** MEASURED via HF API enumerations:
- `https://huggingface.co/api/models?author=Qwen&limit=300&sort=lastModified&direction=-1` (2026-09-18): only 3.8 models = `Qwen/Qwen3.8-Flash-Next-FP8` (2026-08-31), `Qwen/Qwen3.8-Flash-Next` (2026-08-27), `Qwen/Qwen3.8-27B` (2026-08-14), `Qwen/Qwen3.8-27B-FP8` (2026-08-14), `Qwen/Qwen3.8-2.4T-A95B` (2026-08-12), `Qwen/Qwen3.8-2.4T-A95B-FP8` (2026-08-12).
- `search=Qwen3.8-50B` → 0 results. `search=Qwen3.8-32B`/`-72B` → 0 official (only community `StargazerLabs/Qwen3.8-32B-Jumbo`*).
- Nearest real 50B-class in the lineage: **none**. Qwen3.5 family = 0.8B/2B/4B/9B/27B/35B-A3B/122B-A10B/397B-A17B; Qwen3.6 = 27B/35B-A3B; Qwen3.7 = none; Qwen3.8 = 27B/Flash-Next/2.4T-A95B.
- Community-only 45B: `win10/Qwen3.8-45B-A30B` (MoE, `Qwen3_5MoeForConditionalGeneration`, hidden 5120) — MEASURED config, no README ("Entry not found"). Not official; treat as a merge/finetune.

## The 3.8 line that DOES exist (official, MEASURED)
| Repo id | Released | Kind | Notes |
|---|---|---|---|
| `Qwen/Qwen3.8-27B` | 2026-08-14 | dense, hybrid-attn | 7,456,257 downloads |
| `Qwen/Qwen3.8-27B-FP8` | 2026-08-14 | FP8 | 7,603,458 downloads |
| `Qwen/Qwen3.8-Flash-Next` | 2026-08-27 | `Qwen4ExpForConditionalGeneration`, `qwen4_exp` | hidden 2560 |
| `Qwen/Qwen3.8-Flash-Next-FP8` | 2026-08-31 | FP8 | |
| `Qwen/Qwen3.8-2.4T-A95B` | 2026-08-12 | MoE `Qwen3_5MoeForCausalLM` | 2.4T total / 95B active |
| `Qwen/Qwen3.8-2.4T-A95B-FP8` | 2026-08-12 | FP8 | |

## Qwen3.8-27B — the base of Ternary-Bonsai-2-27B (MEASURED config.json, 2026-09-18)
`https://huggingface.co/Qwen/Qwen3.8-27B/raw/main/config.json`:
- `architectures: ["Qwen3_5ForConditionalGeneration"]`, `model_type: qwen3_5`, `language_model_only: false` (multimodal)
- `hidden_size: 5120`, `intermediate_size: 17408`, `head_dim: 256`, `attn_output_gate: true`
- `full_attention_interval: 4` → layer_types = 3x `linear_attention` : 1x `full_attention` (≈75% linear / 25% full)
- `dtype: bfloat16`, `bos/eos_token_id: 248044`
- PrismML card (`https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/raw/main/README.md`, 2026-09-18) states: base `Qwen/Qwen3.8-27B`; 27.36B total = 24.35B backbone (64 blocks) + 2.54B emb/LM-head + 0.46B vision; **262K context**; licence **Apache 2.0**.

## Ternary-Bonsai-2-27B (MEASURED, prism-ml card)
- PTQ1_0 dense trits: **5.95 GB**, 1.75 bits/w; PQ2_0 2-bit slots: **7.21 GB**, 2.13 bits/w; true ~1.72 bits/w.
- 98.2% of FP16 intelligence retained (84.78 avg over 14 thinking-mode benchmarks); ~47 tok/s on Apple M5 Max.
- 24 GB VRAM: both fit trivially (5.95/7.21 GB + KV). 8 GB: both fit weights; 8k KV on 262K-context hybrid-attn model needs checking (linear-attn layers have small state).

## 2026-09-18 page 4-6: sizes, quants, KV math
### Qwen3.8-27B bf16 (MEASURED, tree API)
- `https://huggingface.co/api/models/Qwen/Qwen3.8-27B/tree/main` TOTAL = **55.586 GB** (18 shards + 0.93 GB vision sidecars). Matches PrismML "~54 GB FP16".
- config (MEASURED): 64 layers, `full_attention_interval:4` → **16 full-attn + 48 linear-attn**; `num_attention_heads:24`, `num_key_value_heads:4`, `head_dim:256`; linear heads 48v/16k, dim 128; ctx 262,144 (extensible 1M via YaRN); vocab 248,320 (padded); Apache-2.0.

### Qwen3.8-27B-FP8 (MEASURED tree API)
- TOTAL = **30.890 GB**, 81 files (per-layer `layers-N.safetensors`, ~0.384 GB each).

### Qwen3.8-27B quant files (MEASURED, HF tree APIs 2026-09-18)
`unsloth/Qwen3.8-27B-GGUF`: UD-IQ1_S **6.192**, UD-IQ1_M 6.729, UD-IQ2_XXS **7.266**, UD-IQ2_S 8.372, UD-Q2_K_XL 9.829, UD-IQ3_XXS 10.935, UD-IQ3_S 12.041, UD-Q3_K_XL 13.146, UD-IQ4_XS 14.253, UD-Q4_K_S 15.358, Q4_0 16.056, UD-Q4_K_M 16.464, Q4_1 17.541, UD-Q4_K_XL 17.559, UD-Q5_K_S 18.666, UD-Q5_K_M 19.772, UD-Q5_K_XL **20.877**, UD-Q6_K 21.984, Q8_0 29.047, UD-Q8_K_XL 31.458. mmproj-Q8_0-style 0.928-0.931 GB extra.
`bartowski/Qwen3.8-27B-GGUF`: IQ2_XXS **8.881**, IQ2_XS 9.089, IQ2_S 9.684, IQ2_M 10.522, Q2_K 10.822, IQ3_XXS 12.320, IQ3_XS 12.800, Q3_K_S 12.740, Q3_K_M 13.404, IQ3_M 14.861, IQ4_XS 15.476, Q4_K_S 16.364, Q4_K_M 17.442, IQ4_NL 17.442, Q5_K_M 20.924, Q6_K 23.861, Q8_0 29.116. bf16 GGUF 54.658 GB.
`cyankiwi/Qwen3.8-27B-AWQ-INT4`: 5 shards = **21.018 GB** (MEASURED sum 2.543+4.968+4.997+4.976+3.534).
`turboderp/Qwen3.8-27B-exl3`: repo holds only cal_trace files (0.009 GB) — **actual EXL3 3.x-bpw weights not in this repo** (MEASURED: no safetensors shards listed).

### PrismML ternary (MEASURED, `prism-ml/Ternary-Bonsai-2-27B-gguf`)
- PTQ1_0 = **5.947 GB** (1.75 bits/w); PQ2_0 = **7.206 GB** (2.13 bits/w); F16 ref = 53.808 GB; mmproj Q8_0 = 0.629 GB.
- 24 GB VRAM: PTQ1_0/PQ2_0 trivial. 8 GB: PTQ1_0 fits; PQ2_0 = 7.206 GB weights alone → **does not** fit 8 GB with any KV.

### KV cache at 8k context, fp16 (ESTIMATE, arithmetic shown)
Qwen3.8-27B: `2 (K,V) x 4 kv_heads x 256 head_dim x 2 B = 4096 B/layer/token`; x **16 full-attn layers** = 65,536 B/token = 64 KiB/token.
- 8,192 tokens → 8,192 x 65,536 = **0.537 GB** (536,870,912 B). Linear-attn layers use constant-size recurrent state, not a growing KV (ESTIMATE: +tens of MB).
- 24 GB VRAM budget (0.54 GB KV): fits bf16-Q4_K_M(17.4)→Q5_K_XL(20.9)+KV≈21.4; Q6_K_M(23.1)+KV≈23.6 = **tight/risky**; FP8(30.9) and bf16(55.6) **no**. Bonsai PTQ1_0 5.95, PQ2_0 7.21 both trivial.
- 8 GB budget (0.54 GB KV): fits Bonsai PTQ1_0 (5.95+0.54=6.5), UD-IQ1_S (6.19+0.54=6.7); UD-IQ2_XXS (7.27+0.54=7.8) tight; Bonsai PQ2_0 7.21+0.54=7.75 tight/risky; IQ2_S (8.37) no.

### Other official members (MEASURED config/card)
- `Qwen/Qwen3.8-Flash-Next` (2026-08-27): `qwen4_exp`/`Qwen4ExpForConditionalGeneration`, 48 layers, hidden 2560, 24 heads / 2 kv, head_dim 256, ctx 262,144, vocab 248,320 — a small/efficient (non-50B) experimental arch.
- `Qwen/Qwen3.8-2.4T-A95B` (2026-08-12): MoE, 213 shards, **4892.4 GB (~4.89 TB)** total (MEASURED) — flagship, not 50B.
- `Qwen/Qwen3.5-35B-A3B` (Apache-2.0, card MEASURED): 40 layers, 256 experts / 8 active, hidden 2048, 262,144 ctx. This is the real "35B-A3B"; the `empero-ai/Qwen3.8-35B-A3B-Distill` repos are distills, not official.

## CONCLUSION (MEASURED)
"qwen3.8 50b" does **not** resolve to any official model. Existing sizes: **27B dense** (the Bonsai base), **Flash-Next** (small), **2.4T-A95B** (4.89 TB MoE). Nearest 50B-class: community `win10/Qwen3.8-45B-A30B` (unofficial) and official `Qwen3.5-35B-A3B` / `Qwen3.5-122B-A10B`. Recommend treating "50B" as a misremembering of **35B-A3B** or **27B**, and pinning the line on `Qwen/Qwen3.8-27B` (already the Ternary-Bonsai base).
