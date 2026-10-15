# One-bit / ternary model quantisation, and whether it applies to a diffusion LLM

Reader: a00-989a0516 (iteration TM.22, one-bit hunt). Date of research: 2026-09-16.
All figures tagged MEASURED (read from source) or ESTIMATE (my arithmetic on assumptions).

## Sources read
1. **The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits** (Ma et al., Microsoft) — arXiv 2402.17764, fetched 2026-09-16 via arxiv.org API.
2. **BitNet b1.58 2B4T Technical Report** — arXiv 2504.12285; model card huggingface.co/microsoft/BitNet-b1.58-2B-4T, fetched 2026-09-16.
3. **1-bit AI Infra: Fast and Lossless BitNet b1.58 Inference on CPUs** — arXiv 2410.16144 (bitnet.cpp tech report); **Bitnet.cpp: Efficient Edge Inference for Ternary LLMs** — arXiv 2502.11880; microsoft/BitNet README (raw.githubusercontent.com), fetched 2026-09-16.
4. **BitNet a4.8: 4-bit Activations for 1-bit LLMs** (Microsoft) — arXiv 2411.04965, 2026-09-16.
5. **OneBit: Towards Extremely Low-bit Large Language Models** — arXiv 2402.11295, 2026-09-16.
6. **PB-LLM: Partially Binarized Large Language Models** — arXiv 2310.00034, 2026-09-16.
7. **BiLLM: Pushing the Limit of Post-Training Quantization for LLMs** — arXiv 2402.04291, 2026-09-16.
8. **ParetoQ: Improving Scaling Laws in Extremely Low-bit LLM Quantization** (Meta) — arXiv 2502.02631, 2026-09-16.
9. **PTQTP: Post-Training Quantization to Trit-Planes for LLMs** — arXiv 2509.16989, 2026-09-16.
10. **Mercury: Ultra-Fast Language Models Based on Diffusion** (Google DeepMind) — arXiv 2506.17298; inceptionlabs.ai/blog/introducing-mercury, 2026-09-16.
11. **LLaDA: Large Language Diffusion Models** (GSAI) — arXiv 2502.09992 + github.com/ML-GSAI/LLaDA + huggingface.co/GSAI-ML/LLaDA-8B-Instruct, 2026-09-16.
12. **DiffusionGemma Technical Report** (Google DeepMind) — arXiv 2608.00146; deepmind.google/models/gemma/diffusiongemma, 2026-09-16.
13. **MDM-Prime-v2: Binary Encoding and Index Shuffling Enable Scaling of Diffusion Language Models** — arXiv 2603.16077, 2026-09-16.

Plus negative-result arXiv searches (2026-09-16): all:"ternary" AND all:"masked diffusion"; all:"1-bit" AND all:"diffusion" AND cat:cs; all:"BitNet" AND all:"diffusion" → **zero results**.

## Mechanisms
- **BitNet b1.58** (S1): every weight ternary in {-1,0,1} ("trit"); activations stay fp8/bf16. Quantisation is done in **training** (straight-through-estimator QAT, activation around quantised weights — the weights are ternary *by architecture*, not by post-hoc rounding). Requires training from scratch on huge token budgets; defines a new scaling law.
- **bitnet.cpp** (S3): inference system; two kernels — **TL** (Ternary Lookup Table, packs 5 ternary weights per byte) and **I2_S** (Int2 with a Scale — decomposes each weight into a 1-bit sign plane + a tiny per-weight scale to stay lossless). Splits Gemm into binary and scale Gemms so the bulk runs in integer/low-bit cheap paths.
- **BitNet a4.8** (S4): 1-bit weights (same as b1.58) but pushes activations to 4-bit by hybrid quantisation + sparsification of outlier channels (the sparsified intermediate states stay 8-bit); only 55% of parameters fire; supports 3-bit KV cache.
- **OneBit** (S5): 1-bit weights via a binary + scaling-factor representation, matrix-decomposition-based init for fast QAT convergence. Works as both PTQ and QAT; keeps ≥81% of the fp model.
- **PB-LLM** (S6): finds naive full binarisation collapses an LLM; fixes it by keeping a small salient-weight submatrix in higher bits (partially-binarised). GPTQ-guided PTQ plus QAT recovery.
- **BiLLM** (S7): 1-bit **post-training** quantisation; structurally and saliency-selects the "important" weights, binary-residual-approximates them, and optimally splits the bell-shaped non-salient remainder into groups.
- **ParetoQ** (S8): one unified framework comparing 1 / 1.58 / 2 / 3 / 4 bit. Key teaching: **a transition between 2 and 3 bits** — at ≥3 bits fine-tuning stays near the pretrained distribution; at ≤2 bits representations change completely (so ultra-low-bit is a different learning regime, better trained natively than tuned from fp).
- **PTQTP** (S9): decomposes weights into **two ternary trit-planes** {-1,0,1}^2 times continuous scales → multiplication-free additive inference, pure PTQ, no architecture change.
- **Mercury** (S10): a commercial-scale diffusion **LLM** (Transformer, predicts many tokens per step in parallel). Not a quantisation paper — it is the reference dLLM. Weights are NOT released for general use (DeepMind API-first "commercial-scale"); no open-weight HF release found.
- **LLaDA-8B** (S11): open-source (Apache-2.0) discrete masked-diffusion LM trained from scratch, LLaMA3-8B-comparable. **This is the open dLLM to run a QAT experiment on.**
- **DiffusionGemma** (S12): open-weight (Apache-2.0) discrete-diffusion LM, obtained by *fine-tuning* the Gemma-4 MoE rather than from scratch — evidence diffusion LMs can be adapted from an autoregressive checkpoint (relevant to a QAT-from-checkpoint path).
- **MDM-Prime-v2** (S13): closest thing to "binary diffusion LM" — but the *binary encoding is of the subtokens/tokenizer*, not of the weights. No weight-level binary/ternary dLLM.

## Numbers
- Ternary 1.58-bit **matches fp16/bfloat16 perplexity and end-task** at equal size and training tokens (S1, MEASURED).
- BitNet-b1.58-2B-4T: 2.4B parameters, trained on 4T tokens, on par with open full-precision peers of similar size (S2, MEASURED); model is MIT-licensed, safetensors, ~0.4–0.5 GB on disk (ESTIMATE: 2.4e9 × 1.58 bit ≈ 475 MB raw).
- bitnet.cpp speedups: **1.37–5.07× on ARM CPUs, 2.37–6.17× on x86 CPUs**; energy −55.4–70% (ARM), −71.9–82.2% (x86) (S3, MEASURED from microsoft/BitNet README 2026-09-16). A **100B** BitNet b1.58 runs on a **single CPU at 5–7 tokens/s**, "comparable to human reading" (S3, MEASURED). Newer 2026 kernels add 1.15–2.1× more (README news, MEASURED).
- BitNet a4.8: 55% of parameters active, 3-bit KV cache, faster than b1.58 with 4-bit (INT4/FP4) kernels (S4, MEASURED).
- OneBit: ≥81% of non-quantised LLaMA performance with 1-bit weights (S5, MEASURED).
- BiLLM: 8.41 ppl on LLaMA2-70B at 1 bit (S7, MEASURED).
- ParetoQ: **ternary 600M model beats the previous SoTA ternary 3B model**, with 1/5 the parameters (S8, MEASURED); token-level: ultra-low-bit is a native-training regime.
- Ternary **training cost** figures: the S1 recipe needs scaled-up retraining (b1.58 2B used 4T tokens, S2); ParetoQ's efficiency comes from training small (600M) ternary models outright (S8). There is no closed-form "ternary FT cost" — it is proportionate to training a small model from scratch (ESTIMATE).

## Code availability
- **bitnet.cpp** — MIT; github.com/microsoft/BitNet; builds on x86 (AVX2) and ARM (NEON); no pip needed (make/cmake). **MIT-licensed weights** for BitNet-b1.58-2B-4T on HF. → CPU-toy feasible: **yes**, it is the intended use.
- **unilm/bitnet** — b1.58 training code (QAT) in the training-tips PDF (S1), non-pip, needs a GPU to train.
- **OneBit / BiLLM** — research repos on GitHub (BooThink/OneBit, xvyao/BiLLM); Python, CPU-compatible for the PTQ conversion of a small model (numpy feasible for a <1B probe).
- **PB-LLM / ParetoQ / PTQTP** — research code on GitHub (ParetoQ is release-ready, PyTorch); the PTQ candidates (BiLLM, PB-LLM, PTQTP) are the ones that convert an *existing* checkpoint and are numpy/PyTorch-CPU feasible in minutes on a tiny model.
- **LLaDA-8B** — Apache-2.0, weights + code on HF/GitHub; inference runs on a ~24 GB GPU; Apache-2.0 → free to QAT.

## Fit on our iron
- **A1 — 4-core CPU, 23 GB RAM. Full fp16 7–8B ≈ 16 GB (too big); ternary 7–8B ≈ 7e9 × 0.1975 B ≈ 1.6–1.9 GB** (ESTIMATE: 1.58 bit/weight × 8e9 ≈ 1.58 GB) → **fits the A1 CPU AND the 8 GB GPU with room**. Measured tok/s reference: bitnet.cpp never published a arm64 4-core number in what I read; closest measurables — 100B/one-CPU = 5–7 tok/s (S3) and ARM speedups up to 5.07× over fp16. **ESTIMATE for a 2B ternary on a 4-core arm64: ~15–35 tok/s** (interpolating 100B→5–7 tok/s down 50× in parameters but up-arm by the memory-boundness; treat as estimate, the run on A1 is the measurement).
- **local-town — gpu-8g, 8 GB**: BitNet-b1.58-2B-4T (≈0.5 GB) and even ternary 7–8B (≈1.6 GB) fit; official GPU kernel supports it (S3/S4 MEASURED that GPU kernels exist).
- **Camber XS — 24 GB, 3 GPU-hours/MONTH**: LLaDA-8B fp16 fits (~18 GB). But **ternary/1-bit QAT of an 8B dLLM exceeds 3 GPU-hr** (ESTIMATE: a LoRA-QAT of the attention+FFN linear layers of 8B, even a few steps, lands ~4–10 GPU-hr). Realistic within budget: **QAT a ~0.4–1B slice/sub-block, or distil-then-quantise a small masked-diffusion MLP**, ~1–3 GPU-hr per small pass (ESTIMATE).

## How it maps to the owner sketch
The owner wants the internal metronome (RHYTHM-neuron oscillation) to WORK, with the subscription-set = weight idea. Ternary/1-bit research maps mostly as **the substrate**, not the oscillator:
- **Subscription-set-as-weight → BitNet b1.58 ternary {-1,0,1}** (S1): a ternary weight IS a signed on/off subscription. The {-1,0,1} trit is literally "subscribe positively / subscribe negatively / do not subscribe", plus one non-zero band per source — the owner's "one weight per source clamped between two non-zero positive/negative bands" is the b1.58 ternary tensor in near-identical words.
- **Selective subscription / 10–200 read sites → OneBit / PB-LLM / BiLLM salient-weight retention** (S5/S6/S7): their "salient weights", which must not be collapsed to 1 bit, are exactly "which read-sites matter" — a sparsity/importance mask inside the quantisation.
- **Frequency quantisation should EMERGE → ParetoQ's ≤2-bit-vs-≥3-bit regime transition** (S8): tastes the same — a categorical (quantised) behaviour that emerges from the learning dynamics without an explicit clock.
- **Cheap propagation of aligned frequencies → bitnet.cpp TL/I2_S integer add-dominance** (S3, and PTQTP S9's multiplication-free additive inference): when weights are ternary, heavy ops become cheap signed adds — aligned/misaligned "cost" is exactly the energy story (alignment propagates at add-cost, misalignment costs multiply).
- **Ternary dLLM does not exist** (negative searches, S13) → the oscillator-on-a-dLLM slot is **greenfield**: no one has put ternary weights under a diffusion LM, so the owner's architecture would be the first.

## What to try first at $0
1. **Run bitnet.cpp BitNet-b1.58-2B-4T on the A1** (MIT, no pip — cmake build; weights ~0.5 GB). Measure actual tok/s on the 4-core arm64; my ESTIMATE is 15–35 tok/s, but the ARM-neon kernel decides it. This validates the ternary substrate end-to-end at zero cost.
2. **Numpy-probe a ternary matmul** (minutes): quantise a small LLaDA-linear block's weights to {-1,0,1} + scale (scikit-free, a few lines) and watch the error and the add-vs-multiply cost — the "subscription set = weight" intuition, cheap and safe.
3. **If a real ternary dLLM is wanted:** no open ternary dLLM exists → the cheapest honest path is **PTQ-to-termary of a small masked-diffusion slice** (BiLLM/PTQTP convert an existing checkpoint) or **LoRA-QAT of sub-1B dLLM block on Camber XS**, budgeted inside the 3 GPU-hr (ESTIMATE 1–3 hr small pass). QAT of full LLaDA-8B to ternary is out of the monthly budget (ESTIMATE 4–10 GPU-hr).