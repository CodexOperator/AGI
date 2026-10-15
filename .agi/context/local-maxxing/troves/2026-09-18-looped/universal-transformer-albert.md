# universal-transformer-albert — UT (1807.03819) + ALBERT (1909.11942) — reading digest
READ-ONLY. MEASURED = quoted from a page/config read today; ESTIMATE = inferred, arithmetic shown.

## A. Universal Transformer (UT) — arXiv 1807.03819
URL: https://arxiv.org/abs/1807.03819
- TITLE (MEASURED): "Universal Transformers". AUTHORS (MEASURED): Mostafa Dehghani, Stephan Gouws,
  Oriol Vinyals, Jakob Uszkoreit, Lukasz Kaiser. DATE (MEASURED): submitted 2018-07-10.
- MECHANISM (2 lines, MEASURED): a parallel-in-time self-attentive RECURRENT sequence model — the
  SAME transformer block is applied for a variable number of steps t, with a per-position (and
  optionally per-step) transition function; a depth-wise recurrent inductive bias. "cast as a
  generalization of ... Transformer ... RNN".
- UNIQUE PARAMS vs EFFECTIVE DEPTH: weights shared across steps, so unique params ~ one block; the
  effective depth is the (possibly adaptive) number of steps. Exact counts are experiment-dependent.
- RELEASED WEIGHTS (MEASURED): no widely-used pretrained checkpoint found; the model is defined by the
  paper and reference code. Do NOT claim released weights. (GAP)
- CPU RUNNABILITY: reference code is TensorFlow-era (ESTIMATE); not a plug-in HF model today.
- QUALITY vs NON-LOOPED (MEASURED abstract): "UTs achieve a 0.9 BLEU improvement over Transformers on
  the WMT14 En-De dataset"; also new SOTA on LAMBADA; abstract claims better generalization on
  copy/string and logical-inference tasks where vanilla Transformers fail to extrapolate.
- TRAINING RECIPE COST: not extracted (gap).
- WHY IT MATTERS HERE: the direct ancestor of Huginn/Ouro/MoR depth recurrence. It established that
  weight-tied iterative depth generalizes where fixed depth does not.

## B. ALBERT — arXiv 1909.11942
URL: https://arxiv.org/abs/1909.11942
- TITLE (MEASURED): "ALBERT: A Lite BERT for Self-supervised Learning of Language Representations".
  AUTHORS (MEASURED): Zhenzhong Lan, Mingda Chen, Sebastian Goodman, Kevin Gimpel, Piyush Sharma,
  Radu Soricut. DATE (MEASURED): submitted 2019-09-26.
- MECHANISM (2 lines, MEASURED): two parameter-reduction techniques — factorized embedding
  parameterization and CROSS-LAYER PARAMETER SHARING (all layers share one block); plus an
  inter-sentence coherence loss (SOP). This is parameter SHARING, NOT test-time recurrence: the
  number of layers is FIXED; the same weights are reused at each of the L fixed layers.
- UNIQUE PARAMS vs EFFECTIVE DEPTH (MEASURED from HF safetensors): `albert-base-v2` 11,842,272;
  `albert-large-v2` 17,875,424; `albert-xxlarge-v2` 223,180,256. ALBERT-base uses 12 layers but only
  ~12M unique params because every layer shares one block => effective depth 12, unique params of
  one block. (Contrast a looped model where depth is a runtime dial; ALBERT's is fixed.)
- RELEASED WEIGHTS (MEASURED from HF API today): `albert/albert-base-v2`, `albert/albert-large-v2`,
  `albert/albert-xxlarge-v2` — all **apache-2.0** (MEASURED). Plus community fine-tunes.
- CPU RUNNABILITY: transformers, CPU-native, no custom code; runs on the box today (ESTIMATE, small).
- QUALITY vs NON-LOOPED (MEASURED abstract): "our best model establishes new state-of-the-art results
  on the GLUE, RACE, and SQuAD benchmarks while having fewer parameters compared to BERT-large".
  Exact GLUE score not extracted here (gap); the comparison is against BERT-large (110M), NOT a
  same-unique-params non-looped model — so it is a parameter-efficiency claim, not a loop-vs-no-loop
  proof. Do not use ALBERT as evidence that looping beats not-looping.
- TRAINING RECIPE COST: BERT-scale pretraining (MEASURED context); no per-model cost extracted (gap).

## VERDICT FOR THE TOWN
- These are the historical anchors, not runnable looped LMs for the kid eval. ALBERT is a cheap,
  licence-clean CPU control (fixed-depth, shared weights); UT has no released weights. Cite them for
  provenance only — the falsifiable loop-vs-no-loop evidence lives in Huginn and Ouro.
