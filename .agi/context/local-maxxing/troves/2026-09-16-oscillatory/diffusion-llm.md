# Diffusion-LLM trove — reader hunt 2026-09-16 (a00-288aec4d)

Read-only hunt: 11 bash curl fetches (arXiv abs + search, HuggingFace API, GitHub/HF READMEs). Every claim tagged MEASURED (read from source) or ESTIMATE (my arithmetic/assumption). Fetch date for all URLs: **2026-09-16**.

## Sources read
1. LLaDA README + arXiv — MEASURED — https://raw.githubusercontent.com/ML-GSAI/LLaDA/main/README.md ; https://arxiv.org/abs/2502.09992
2. iLLaDA — MEASURED — https://arxiv.org/abs/2606.25331 (+ README news 2026-06-24)
3. LLaDA 1.5 — MEASURED — LLaDA README news 2025-05-25
4. LLaDA-V — MEASURED — LLaDA README news 2025-05-23
5. LLaDA-MoE-7B-A1B — MEASURED — LLaDA README news 2025-09-11
6. Mercury / Mercury Coder — MEASURED — https://arxiv.org/abs/2506.17298
7. SEDD — MEASURED — HF tag arxiv:2310.16834 on https://huggingface.co/louaaron/sedd-small (7,381 dl)
8. Fast_dLLM v2 — MEASURED — https://huggingface.co/Efficient-Large-Model/Fast_dLLM_v2_7B (apache-2.0, 13,696 dl) + _1.5B
9. Dream-7B quantisation — MEASURED — HF search: mradermacher/Dream-7B-slerp-GGUF (209 dl) + i1-GGUF (552 dl)
10. Block Diffusion (R3: Review, Remask, Refine) — MEASURED — arXiv search hit "Process-Guided Block Diffusion for Text Generation" https://arxiv.org/search/?query=block+diffusion

## Mechanisms
- **Masked/remasking diffusion (LLaDA, iLLaDA, 1.5, MoE).** MLM-style: mask most tokens, denoise over T steps by unmasking the highest-confidence tokens each step; confidence = the model's logit rank at that step. LLaDA's own FAQ (item 3, README): *"optimal performance when sampling steps == response length; fewer steps hurts quality"*. iLLaDA adds a `mask_id=5` single-control reusing LLaDA inference — the unmask schedule is an explicit, addressable time axis.
- **Mercury (Inception Labs).** Parallel multi-token prediction framed as diffusion; Transformer params, trained to predict multiple tokens per step. Decoder-only-style dLLM aimed at serving throughput.
- **SEDD.** Discrete-state (absorbing) diffusion LLM; teaches scaling + instruction-tuning of diffusion LMs; weights small (sedd-small) are on HF.
- **Fast-dLLM.** Discrete diffusion LLM with attention-cache (dKV) reuse/dedup across denoising steps; v2 1.5B & 7B open under apache-2.0.
- **Block Diffusion (BD3 / R3).** Diffusion at the granularity of contiguous blocks rather than single tokens; process-guided scheduling — "which span to touch next" is itself a decision, i.e. no strict left-to-right layer/position hierarchy.
- **Dream 7B.** Hybrid discrete-continuous diffusion LLM; community GGUF/i1-GGUF exist → a real quantisation path already exists off-repo.

## Numbers
- LLaDA-8B-Base: open, **MIT** license (iLLaDA: Apache-2.0); 22,499 HF downloads — MEASURED (HF API 2026-09-16).
- LLaDA-MoE-7B-A1B: ~1B active params at inference, "surpasses LLaDA 1.5 (8B dense), comparable to Qwen2.5-3B-Instruct" — MEASURED (README).
- LLaDA optimal sampling steps ≈ response length (so a 100-token answer ≈ 100 unmask passes) — MEASURED (README FAQ). **This is the key cost lever for gating on our iron.**
- Mercury Coder Mini / Small: **1,109 / 737 tok/s** on NVIDIA H100 — MEASURED (arXiv 2506.17298).
- SEDD small weights on HF: 7,381 dl — MEASURED.
- Fast_dLLM_v2_7B: 13,696 dl, apache-2.0 — MEASURED.
- Dream-7B GGUF exists (i1: 552 dl) — MEASURED (HF search).

## Code availability
- LLaDA/B/iLLaDA/1.5/MoE: open weights + MIT/Apache; runs on `transformers==4.38.2`, `trust_remote_code=True` — MEASURED (README).
- Mercury: **API only, weights NOT open** — MEASURED (arXiv 2506.17298: "We also release a public API").
- SEDD: open weights; reference impl is pytorch, CPU-toy feasible at sedd-small size (ESTIMATE: a numpy character-level toy is ~minutes).
- Fast-dLLM v2: open weights apache-2.0; dKV-cache code accompanies the HF release.
- Dream-7B: GGUF (community) = llama.cpp-portable quantisation path exists, ESTIMATE.

## Fit on our iron
- local-town **gpu-8g**: 8B dense dLLMs (LLaDA-8B bf16 ≈ 16 GB, ESTIMATE; 4-bit ≈ 4–5 GB) do NOT run unquantised. **Fit: Fast_dLLM_v2_1.5B** (apache-2.0, ~1.5B; 4-bit ≈ 1–1.5 GB, ESTIMATE) — comfortably under 8 GB with the 15 GB system RAM for tokenizer/CPU pre-pass. LLaDA-MoE-7B-A1B (1B active) is the dense-alternative but 7B total weights need quant (ESTIMATE).
- A1 4-core CPU 23 GB: sedd-small and a numpy discrete-diffusion toy run in minutes (ESTIMATE); no server-grade dLLM CPU inference.
- Camber XS 24 GB / 3 GPU-hr·mo: LLaDA-8B (bf16) fits in 24 GB and is THE highest-quality open dLLM per-shot — but the 3 GPU-hr budget rules out heavy remask loops (ESTIMATE: 100-step unmask on 8B is ~tens of min/sample).

## How it maps to the owner sketch
- **"each oscillator's frequency = both energy and predicted value"** ← unmask-confidence: per-position, per-step logit confidence IS a scalar "how sure" that is both the decision signal and, if you watch it across steps, an energy-esque trajectory.
- **"LLM KV caches read as on/off bit triggers"** ← Fast-dLLM's dKV-Cache: it explicitly reuses/subscribes attention cache across denoising steps — the exact read-site the sketch wants.
- **"no strict layer hierarchy"** ← Block Diffusion / R3: block+schedule structure replaces positional left-to-right order.
- **"timeful steady state that shifts as meaning evolves"** ← a remask schedule is a genuine time axis: the set of masked positions + their confidences is the oscillator network's readable state, evolving per step.
- **"energy = alignment; misaligned frequencies cost energy to align"** ← in dLLM terms, low-confidence/contested positions (where two unmask candidates fight) are the "misaligned" sites that an oscillator gate would defer or force-subscribe.

## What to try first at $0
**The ONE open dLLM to run: `Fast_dLLM_v2_1.5B`** (apache-2.0; ~1.5B, quant ≈1–1.5 GB — fits gpu-8g). Runner-up dense: LLaDA-8B on Camber XS (24 GB) only when GPU-hours allow.

**The ONE $0 hybrid experiment (oscillators read per-step confidences to schedule unmasking):**
1. Run FastDLLM-1.5B (or LLaDA-8B) on one short prompt; at each denoising step record per-position unmask-confidence/entropy (a 2-line hook on the HF/dKV forward pass).
2. Feed those per-step confidence series to a tiny numpy oscillator net: one oscillator per position, phase/frequency = its confidence trajectory; a single rhythm-neuron subnetwork acts as the metronome.
3. GATE the unmask schedule: positions whose oscillator is phase-locked to the metronome proceed to unmask this step; misaligned (entropy-spiking) positions are deferred.
4. Metric: quality (perplexity/grammar) vs unmask-steps at matched budget, vs LLaDA's equal-steps baseline. Cost = model download + CPU/numpy + your GPU-hours only if you push to 8B.

**Smallest numpy oscillatory toy (from the parent chain question):** N=32 oscillators, each reads a synthetic "KV-confidence" time series; alignment = phase-lock onto a 2-neuron rhythm subnetwork; energy = mean phase-error; subscription = the read-site set (10–200). Integrate with plain numpy, <5 min CPU. This maps to the "3 closest mechanisms": (a) masked remask schedule = time axis; (b) unknown-mask-gating = alignment energy; (c) dKV cache subscribe = read sites.

## Direct end-answers
- **Mercury weights open?** **NO** — API only (citation: https://arxiv.org/abs/2506.17298, fetched 2026-09-16).
- **One open dLLM for our iron?** Fast_dLLM_v2_1.5B — apache-2.0, fits 8 GB (ESTIMATE).
- **Ternary dLLM?** **No open ternary-weight dLLM surfaced in this hunt** (surveyed LLaDA/iLLaDA/MoE, Mercury, SEDD, Fast-dLLM, Dream GGUF — none ternary; nearest quantisation is community GGUF of Dream-7B). Flagged honest-hole: absence-of-evidence demote risk; dedicated ternary-dLLM hunt recommended rather than asserted.
- **One-bit CPU tok/s:** this is the sibling one-bit (bitnet.cpp) leg — no measured figure taken here; see that digest. Label ESTIMATE-only here.