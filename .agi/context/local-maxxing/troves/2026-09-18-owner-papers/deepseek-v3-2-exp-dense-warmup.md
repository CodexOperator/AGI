# deepseek-v3-2-exp-dense-warmup — DeepSeek-V3.2-Exp two-stage continued pretraining
READER: research-reader (read-only). TROVE APPEND-ONLY. Read 2026-09-18 UTC.

## PAGE 1 — DeepSeek-V3.2-Exp tech report (PDF mirror aarnphm.xyz/thoughts/papers/DeepSeek_V3_2.pdf)
- TITLE (MEASURED): DeepSeek-V3.2-Exp tech report (the paper that introduced DeepSeek Sparse
  Attention, DSA, + the "lightning indexer"). YEAR: 2025. Official PDF is
  github.com/deepseek-ai/DeepSeek-V3.2-Exp (paper/). arXiv id NOT found in this read
  (arXiv API for ti:"DeepSeek-V3.2-Exp" returned only a third-party ESS paper, 2512.10576).
- MECHANISM (MEASURED, verbatim from PDF p.2):
  * "Dense Warm-up Stage. We first use a short warm-up stage to initialize the lightning indexer.
    In this stage, we keep dense attention and freeze all model parameters except for the
    lightning indexer."
  * Target distribution = main attention scores summed across heads, L1-normalized along seq.
  * Loss: L_I = sum_t D_KL( p_t,: || Softmax(I_t,:) ) — indexer distilled to match main attention.
  * "For warm-up, we use a learning rate of 10^-3. We train the indexer for only 1000 steps,
    with each step consisting of 16 sequences of 128K tokens, resulting in a total of 2.1B tokens."
  * Stage 2 "Sparse Training Stage": "Following indexer warm-up, we introduce the fine-grained
    token selection mechanism and optimize ALL model parameters to adapt the model to the
    sparse pattern of DSA."
- HEADLINE NUMBERS (MEASURED): warm-up = 1000 steps; 16 seqs x 128K tokens/step = 2.1B tokens;
  LR 1e-3; then 15,000 sparse steps (paper) with ALL params. Indexer-only stage is ~6% of the
  total step count (1000 / 16000) => ESTIMATE: trunk-frozen stage is a small prefix.
- COMPUTE SAVED: not stated as a % (it is a quality-alignment warm-up, not a cost-saving claim).
  The saving is structural: only the tiny indexer gets gradients for 1000 steps.
- CODE/LICENCE (MEASURED): github.com/deepseek-ai/DeepSeek-V3.2-Exp — MIT (DeepSeek repos).
- QWEN-CLASS TRUNK? No — DeepSeek-V3 MoE trunk. But the RECIPE is the owner's exact shape:
  freeze the whole trunk, train one small decode-side module to equilibrium, then unfreeze.
- FIT: THE most exact match to "freeze trunk, train the small module alone" in a frontier
  production model. Module = lightning indexer (token selector), not a draft head, but the
  freeze/align/unfreeze choreography transfers directly.

## PAGE 2 — DeepSeek-V4 / V4.1-Flash (context, alphaxiv + arxiv.org/html/2606.19348)
- MEASURED: V4 (arXiv:2606.19348) retains "two-stage training recipe": Dense warm-up (1000 steps,
  indexer only, KL) then Sparse training (15000 steps, all params). Same recipe as V3.2-Exp.
- MEASURED: V4.1-Flash (alphaxiv 2609.deepseek-v4-1-flash) does sparse attention from scratch at
  64K "without any dense attention warmup stages" — i.e. the freeze-warmup was DROPPED once the
  trunk was trained natively sparse. Useful counterpoint: warm-up is a migration aid, not a law.
