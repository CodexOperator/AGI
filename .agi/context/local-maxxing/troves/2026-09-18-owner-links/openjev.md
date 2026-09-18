# Slice OPENJEV — TheoLeeCJ/openjev
Read-only digest, 2026-09-18Z. No key, no install, no clone. MEASURED = quoted from a page read here; ESTIMATE = my arithmetic. Reader: local-maxxing town (A1 CPU / local-town gpu-8gS 8GB / Camber XS 24GB).

## 0. WHAT IT IS (MEASURED)
- GitHub API `github.com/TheoLeeCJ/openjev` (read 2026-09-18): description **"Can we run something like Jev on a 3090 at home?"**; MIT licence; Python; created **2026-09-16T03:51:21Z**; 878 stars / 59 forks; homepage `openjev.com`; default branch **master**; 0 releases. Young — 2 days old at read.
- README (raw `master/README.md`): **"Jev is TypeSafe's closed service for runtime-defined semantic decisions. This project reproduces that interface pattern with open models; it does not reproduce Jev's undisclosed model or training."**
- So: **NOT a Jev API clone, NOT an open System-One model.** It is an open *baseline for the decision interface*: runtime criteria + typed options → probabilities via one forward pass. Weights are off-the-shelf Qwen, not trained.
- NAME COLLISION (MEASURED, web search): ≥4 unrelated "openjev" repos. `AlexWortega/openjev` (HF) = crossencoder that plays Doom/games; `ekzhang/openjev-sglang` = Jev-compatible HTTP API on Qwen3.6-35B-A3B/SGLang (54 stars, created 2026-09-17); `vinnylarouge/jevlike`; `zhihz/openjev`. Only TheoLeeCJ/openjev is the browser/3090 decision baseline.

## 1. ARCHITECTURE (MEASURED, README + docs/METHOD.md)
- **Direct mode:** one native forward pass of frozen Qwen3.5-4B; softmax over the logits of the fixed uppercase answer tokens A–P (2–16 options). **No token is decoded** — "no answer sentence, JSON repair, or decoding loop."
- **Reranker mode:** Qwen3-Reranker-4B native yes/no; `logit(yes) − logit(no)` per option, softmax across options (that last normalisation is the authors', not upstream's contract).
- **Shared-state paths:** serial prefix reuse and parallel suffixes after one state prefill (`--mode shared`).
- Prompt: system = "Choose exactly one listed option. Respond with only its uppercase letter."; user = JSON `{evidence, criterion, options:[{letter,description}]}`.
- Browser demo (`webgpu-demo/`): WebLLM 0.2.85 + Vue 3.5.21, MLC q4f16_1, Qwen3-0.6B (~352 MB) / Qwen3.5-0.8B (~447 MB); reads ≤5 top logprobs per call, groups of 4 + shared `A` anchor for 6–20 options.
- `openjev.com` (read 2026-09-18) extends it: MiniCPM5 2B default on desktop, Qwen3.5 4B "high-memory desktop"; states "1.56 GB model", "browser only / no backend", inputs never leave the page.

## 2. WEIGHTS / LICENCE (MEASURED)
- **Code: MIT** (`LICENSE`, "Copyright (c) 2026 TheoLeeCJ"). **Weights are NOT redistributed** — README: "Model weights and third-party records without a redistribution grant are excluded". Upstream model licences apply.
- `manifests/models.json`: direct = `Qwen/Qwen3.5-4B` rev `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`, bfloat16; reranker = `Qwen/Qwen3-Reranker-4B` rev `22e683669bc0f0bd69640a1354a6d0aebcfeede5`, bfloat16.
- Deps (`pyproject.toml`): torch 2.10.0, transformers 5.17.0, accelerate 1.12.0, numpy 2.2.6; Python ≥3.10; script `openjev-score`.

## 3. TRAINING / SERVING (MEASURED)
- **Training: none.** Models are frozen, pinned revisions; docs/RESULTS.md "Not reproduced: ... RLCD training, because neither the training data nor a sufficient algorithmic specification is public."
- **Serving:** single-process CLI `openjev-score --mode {direct,serial,shared,reranker}`; create-only JSONL out. `src/openjev_phase1/core.py` hard-gates: **"if not torch.cuda.is_available() or torch.cuda.device_count() != 1: raise ValueError"** — exactly one CUDA GPU required; BF16 `device_map={"": "cuda:0"}`.

## 4. BENCHMARKS vs TypeSafe Jev (MEASURED, results/phase1-summary.json dated 2026-09-16)
| Workload | Direct Qwen3.5-4B | Reranker | Published Jev |
|---|---:|---:|---:|
| Authored 144, family balanced acc | **0.813** | 0.625 | — |
| WANLI 256, balanced acc | **0.637** | 0.522 | — |
| TypeSafe public 102, equal-case modal agreement | **0.845** | 0.560 | **0.883** |
| TypeSafe 102, TV distance | 0.177 | 0.444 | **0.127** |
| Every judgment grid 36, accuracy | **0.806** | 0.694 | — |
| Every action firewall 10 | 0.700 | 0.700 | — |
- Gap to Jev = **3.8 pp** modal agreement on 102 selected rows; authors explicitly: "does not establish near-Jev capability … small and selected, Jev was not run by us."
- Speed (one RTX 3090, BF16, README): 21 criteria median **1.023 s** direct vs **5.332 s** generative JSON array (111 tokens) = **5.21×**; 777-decision fixture: fresh 2.33 dec/s → parallel suffixes **20.03 dec/s** (38.8 s), 6/777 argmax drift vs fresh.
- Perturbations (36): option reversal flips 10 argmaxes (direct) vs 2 (reranker); both made 1 confident non-`insufficient` choice >0.8 on missing-evidence.

## 5. CPU / 8 GB GPU — THE TOWN QUESTION (MEASURED + ESTIMATE)
- **Phase-1 CLI on this A1 box: NO.** No CUDA GPU → `core.py` raises before load. No CPU path in the repo.
- **local-town gpu-8g: 4B BF16 will not fit.** MEASURED peak CUDA on the 3090: fresh batch1 **8.89 GB**, serial 8.99 GB, parallel **11.61 GB** — already >8 GB at the cheapest mode. Reranker peaks 8.19–9.19 GB. ESTIMATE: 4-bit GGUF would fit (~2.5 GB) but is not provided.
- **What DOES fit the small hardware:** the browser WebGPU models — Qwen3-0.6B q4f16 ~352 MB, Qwen3.5-0.8B q4f16 ~447 MB, MiniCPM5 2B 1.56 GB (openjev.com). WebGPU needs a GPU adapter; local-town has one, the A1 headless box has none.
- **ESTIMATE (A1 CPU, unmeasured):** Qwen3-0.6B/0.8B as GGUF q4 runs on a 4-core A1 via llama.cpp; the *direct-letter-logit* readout is reproducible there because the pattern needs only logit access, not the repo's CUDA loader. ~10–40 tok/s prompt-eval class. No page read measured this.

## 6. COST vs TypeSafe (MEASURED $0.042/Mtok input, from typesafe/pricing-terms.md)
- TypeSafe: $42/Btok input, **output free** → a decision costs (state+question tokens)×$0.042/Mtok. ESTIMATE: 500-tok act ≈ **$0.000021**; 2,000-tok act ≈ **$0.000084**; **$0.021–$0.084 per 1,000 typed acts**.
- openjev local: **$0 marginal** (electricity only) once a model is resident. Savings are real but tiny in absolute terms unless act volume is very large; the win is latency + data residency + no per-call key, not headline dollars.
- The repo's own comparison does NOT claim cost parity with Jev — RESULTS.md: "They do not yet reproduce the full economic claim around Jev."

## 7. FIT TO GRAPH TYPED ACTS (verdict class, accept/demote, next-call suggestion)
- Structurally **yes**: those are exactly "runtime criteria + typed options → probabilities". A verdict taxonomy is a `choice`; accept/demote is binary; next-call suggestion is a `choice` over candidate calls.
- Caveats (MEASURED): probabilities are **uncalibrated** ("conditional option score; uncalibrated as decision confidence"); option-order sensitivity (10 flips); the only measured quality is at **4B**, which does not fit either local GPU. At 0.6–0.8B quality is unmeasured by this repo.

## 8. HYPOTHESIS SEEDS (smallest experiments; $0 unless stated)
- **H1 — direct-letter logit readout on the A1 CPU (highest value).** llama.cpp + `Qwen3-0.6B` GGUF q4 (`-ngl 0`), reproduce openjev's *direct* pattern: one prompt per typed act, read logprobs of `A`–`P`, softmax over declared options; score 36 graph typed acts with a hand label. Measure wall-ms/act and argmax agreement. **Cost $0 (electricity), ~40 min.** Needs a package install → seed only in a READ-ONLY stage. Falsifier: <60% agreement or >2 s/act.
- **H2 — 0.8B WebGPU readout on local-town.** Serve `webgpu-demo/` locally (`python3 -m http.server`), load Qwen3.5-0.8B q4f16, time direct vs generation on 21 criteria. **Cost $0, ~20 min, ssh only.** Tests whether 8 GB iGPU-class hardware gives usable latency.
- **H3 — 4-bit 4B on local-town.** Quantise Qwen3.5-4B to q4 GGUF and measure whether direct-logit readout fits 8 GB and holds quality vs the published BF16 numbers. **Cost $0, ~50 min.** ESTIMATE ~2.5 GB weights; risk = transformers `Qwen3_5ForCausalLM` support for 4-bit.
- **H4 — calibration probe.** Run openjev direct on graph acts at 4B on Camber XS (24 GB) and measure ECE against human verdicts. **Cost ≈ 0.15 GPU-h of 3/month (XS), ~15 min** — counts as spend; only if H1/H2 fail.

## 9. BOUNDARIES (do not over-claim)
- No live Jev endpoint run by openjev; TypeSafe comparison is 102 selected rows of a claimed 711.
- "Reproduces the interface pattern", explicitly **not** Jev's architecture, RLCD training, calibration, or economics.
- All openjev speed numbers are one RTX 3090; nothing here measures A1 CPU or 8 GB GPUs.
