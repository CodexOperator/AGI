# CACTUS NEEDLE — reading digest (2026-09-17)

Source slice: https://cactuscompute.com/needle + docs + GitHub. All numbers
MEASURED = quoted from page/file; ESTIMATE = my inference. Read-only; no install.

## 1. WHAT IT IS — a MODEL + a Python package + per-platform engines, not a runner
MEASURED (cactuscompute.com/needle, 2026-09-17): "Today we release Needle 3: a
foundation model for mobile, wearables, robots, smart home, automotive and
microcontrollers. The whole model is a single 8-29 MB binary built on our
Simple Attention Network".
- MEASURED (github README): "Needle 3 is a Laddered Simple Attention Network …
  Monarch Hadamard MLP in place of the FFN, GQA attention with causal conv taps,
  engram n-gram memory read by gather, multi-lane hyper-connections."
- 29-121M params (ladder 2L..20L), CQ2 quant, trained on "360B tokens of
  proprietary structured dataset" (site).
- Tasks: tool calls (exact-match), structured extraction (field micro-F1),
  text embedding. NOT a general chat/reasoning model — the site says it "trades
  general chat capacity" for tool calls/extraction.
- Delivery: `pip install cactus-needle` (runtime, no JAX) + engine binary
  auto-downloaded from HF; `needle build --platform <folder>`.
- Two generations: Needle 2 tag 0x05E12A83, Needle 3 tag 0x05E12A84.

## 2. HARDWARE (MEASURED — blog/needle-supported-devices, dated 2026-09-18)
13 platform folders, each engine <1 MB, same needle3.cact weights:
macos-arm64, linux-x86_64, **linux-arm64**, linux-armv7, linux-riscv64,
linux-mipsel, windows-x86_64, windows-arm64, android-arm64/armv7/riscv64,
ios-arm64, watchos-arm64, tvos-arm64, wasm, wasm-component (WASI P2).
- Native folders ship `needle` CLI + `libneedle.a` + `needle.h`; `--serve` HTTP.
- "pip install cactus-needle covers macOS on Apple Silicon, Linux x86-64 and
  ARM64 (glibc and musl)".
=> ARM64 CPU target exists and is first-class. THIS box (ARM4C aarch64) is
   `linux-arm64`. Second headless box is `linux-x86_64`.

## 3. QUANTISATION — Cactus Quants (CQ), rotation + codebook, 1-4 bit
MEASURED (blog/cact-format, 2026-09-18): ".cact … Cactus-Quantised blobs at
2.125 bits per weight"; "2.125 bits at CQ2, 4.125 at CQ4"; groups of 128;
Walsh-Hadamard rotation then Lloyd-Max codebook; CQ-W2A8 (W 2-bit, act 8-bit).
- MEASURED (docs/cactus_quants): at 3-bit CQ "sweeps all 8 text metrics on
  Gemma 4, with margins of up to +32 points"; at 2-bit "CQ is the only method
  retaining usable accuracy" vs GPTQ/AWQ/HQQ. Note: BFCL Parallel-Multi 2-bit
  = 1.33 for CQ too — 2-bit breaks tool calling in the general model.
- Needle3.cact: 29 MB, 581 tensors, 115 CQ2 = 84.7% bytes, 7 CQ4 = 11.4%,
  456 FP16 = 3.6%, tokenizer RAW 111 KB. Engram tables = 2/3 of weight bytes.
- Not BitNet/bitnet.cpp: CQ is rotation+codebook PTQ over any HF model, not a
  1.58-bit trained-from-scratch scheme.

## 4. MEASURED TOK/S (vendor-claimed; device not this box)
- MEASURED (blog/needle-supported-devices): "On a Raspberry Pi 5 decode runs
  from roughly 400 tokens/s at the top of the ladder to 4,000 at the bottom,
  and prefill from 1,000 to 10,000." (RPi5 = 4-core Cortex-A76, ARM CPU.)
- MEASURED (huggingface.co/Cactus-Compute/needle, Needle v1 26M): "In
  production, Needle runs on Cactus at 6000 toks/sec prefill and 1200 decode"
  (device unspecified).
- MEASURED (cactus README benchmark, Gemma-4-E2B-CQ4, Apple-only table):
  Mac M5 Max 2964tps prefill / 154tps decode; iPhone 15 Pro 517/26. No ARM
  Linux row. => tok/s on A1 is ESTIMATE only, must be measured locally.

## 5. LICENCE (two different licences — check the artifact)
- MEASURED (needle repo pyproject.toml): `license = { text = "Apache-2.0" }`;
  MEASURED (needle repo LICENSE): Apache License 2.0. Needle = Apache-2.0.
- MEASURED (HF Cactus-Compute/needle v1 page): "License: MIT".
- MEASURED (cactus engine repo LICENSE, 2025): source-available, NOT open
  source — free only for individuals/edu/nonprofit and orgs with <$2M funding
  AND <$2M revenue; otherwise commercial licence required.
- => Needle weights/code Apache-2.0, but the **Cactus runtime engine it loads
  is under the restrictive licence**. Check which binary `needle build` pulls.

## 6. vs llama.cpp / bitnet.cpp FOR A 4-CORE ARM BOX
- ESTIMATE: Needle is not a llama.cpp substitute. llama.cpp runs general GGUF
  LLMs (chat/reasoning); Needle is a 29 MB task model with grammar-constrained
  decode for tool-calls/extraction/embedding. They solve different problems.
- bitnet.cpp targets trained 1.58-bit BitNet models; CQ is PTQ applied to any
  HF model (cactus convert <HF-Name>). Needle's advantage is size + the ladder,
  not a general throughput win.
- For the town question (kid-tier / verifier on A1, no GPU): Needle fits
  memory (29 MB weights, low RAM) and is ARM-native, but only for the tasks it
  was trained on. A verifier/typed-act router is plausibly in reach IF fine-tuned
  (`needle finetune` + `needle build --layers 8`). General node-writing prose is
  NOT what it does.

## 7. LADDER (the town-relevant bit)
MEASURED (blog/intelligence-ladders, 2026-09-17): every depth 2..20 is a
deployable model from ONE checkpoint; 2L=25M, 4L=29M, 8L=52M, 16L=98M, 20L=121M.
- "from 4 layers up the tuned subnetwork passes DeepSeek V4 Flash" on DroidCall
  (fine-tuned). Fine-tuning lifts every depth 18-36 points.
- Slicing is free: `needle build --lora adapter --layers N`.
- KV cache is per block, so shallower depth = proportionally smaller cache.
=> A 4L or 8L fine-tune is the cheap unit for a local kid/verifier model.

## 8. GAPS / NOT YET VERIFIED
- No A1/ARM-Linux measured tok/s found on public pages (ESTIMATE ~ hundreds
  decode, based on RPi5 Cortex-A76 being same core class as arm-cloud).
- `cactus run` runtime bundle generation "unavailable while the graph builder
  is being rewritten" (docs/cactus_quants) — conversion path may be rough now.
- Needle3 HF repo (Cactus-Compute/needle3) not fetched (time); weights+engines
  said to live there.

## 9. HYPOTHESIS SEEDS (smallest experiment on THIS box, no GPU)
- H1 $0 / ~15 min: `pip install cactus-needle` in a throwaway venv (runtime
  only, no [train]), `needle build --platform linux-arm64 --layers 4`, run 20
  tool-call + 20 extraction prompts, record `decode_tps`, `prefill_tps`,
  `peak_ram_mb`. Falsifies "Needle runs at usable tok/s on A1". MEASUREMENT ONLY.
- H2 $0 / ~30 min: same but fine-tune 4L on ~200 synthetic tool-call rows
  (`needle finetune`, needs [train]) and re-measure accuracy — tests the ladder
  claim that 4L tuned >= frontier on a narrow task. CPU JAX, slow; if >30 min,
  push to local-town (gpu-8gS 8 GB) which the repo supports via [train,gpu].
- H3 $0 / ~10 min: run the same prompts through the WASM build under Node to
  confirm a portable $0 verifier path independent of the C engine licence.
