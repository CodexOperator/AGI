# latent-reasoning-recurrence-2026 — test-time latent reasoning by recurrence (2026) — reading digest
READ-ONLY. MEASURED = quoted from a page/abstract read today; ESTIMATE = inferred, arithmetic shown.

## A. Loop, Think, & Generalize: Implicit Reasoning in Recurrent-Depth Transformers
- arXiv: **2604.07822** (MEASURED); submitted 2026-04-09.
- MECHANISM (2 lines, MEASURED): studies recurrent-depth transformers (iterative computation over the
  same layers) for IMPLICIT multi-hop reasoning inside a single forward pass. Two challenges:
  systematic generalization (composing never-seen pairs) and depth extrapolation (train on <=5-hop,
  test on 10-hop).
- FINDING (MEASURED abstract): vanilla transformers struggle with both; recurrent-depth transformers
  generalize. Systematic generalization "emerges through a three-stage grokking process"
  (memorization -> in-distribution -> systematic); recursion extrapolation "can be unlocked by
  scaling inference-time recurrence, with more iterations enabling deeper reasoning". A named
  limitation: **overthinking** — excessive recurrence degrades predictions at very deep compositions.
- RELEASED: code + select checkpoints, **Apache-2.0**, github.com/OSU-NLP-Group/Loop-Think-Generalize
  (99 stars, pushed 2026-09-03); checkpoints on an external drive, NOT HF (MEASURED).
- CPU: small from-scratch models; runnable in principle but no HF/GGUF (ESTIMATE). No quality-vs-dense
  number extracted beyond the qualitative generalization claim (gap).

## B. T^2MLR: Transformer with Temporal Middle-Layer Recurrence
- arXiv: **2607.15178** (MEASURED); submitted 2026-07-16.
- MECHANISM (2 lines, MEASURED): fuses a cached MIDDLE-layer representation from the previous token
  directly into an earlier layer of the current token position, so abstract intermediate computation
  persists across decoding steps with little inference overhead. This is TEMPORAL recurrence applied
  to a localized middle block (not the whole stack).
- FINDING (MEASURED abstract): beats data- and parameter-matched Transformer baselines on NL
  pretraining and multi-hop reasoning finetuning; recurrence on as little as **20% of the network**
  often outperforms full-layer recurrence; **does not require pretraining from scratch** — it can be
  retrofitted into an existing model.
- RELEASED: code at github.com/princeton-pli/T2MLR (10 stars, MEASURED); weights not found (gap).
- TOWN RELEVANCE (ESTIMATE): the "retrofit a small recurrent path into an existing small model"
  recipe is the cheapest possible CPU experiment — if a Qwen3-0.6B-class model can be retrofitted,
  the loop-vs-no-loop test needs no new pretraining.

## C. The Recurrent Transformer: Greater Effective Depth and Efficient Decoding
- arXiv: **2604.21215** (MEASURED); submitted 2026-04-23. Authors include Oncescu, Morwani, Jelassi,
  Meterez, Kwun, Kakade (from RLT's reference list).
- MECHANISM (2 lines, MEASURED): each layer attends to key-value pairs computed OFF ITS OWN
  activations, yielding LAYERWISE RECURRENT MEMORY while preserving standard autoregressive decoding
  cost. Emulates both a conventional Transformer and token-to-token recurrent updates; an exact
  tiling algorithm reduces HBM traffic from Theta(N^2) to Theta(N log N).
- FINDING (MEASURED abstract): on 150M and 300M C4 pretraining, Recurrent Transformers improve
  cross-entropy over a PARAMETER-MATCHED Transformer baseline and achieve it with FEWER layers —
  i.e. a same-params loop-vs-no-loop win at small scale. No released weights found (gap).
- CPU: 150M/300M scale is box-friendly in principle; no HF/GGUF found (ESTIMATE).

## CROSS-CUTTING (ESTIMATE unless marked)
- 2026 is when depth recurrence moved from a 3.5B proof-of-concept (Huginn) to small-scale,
  parameter-matched, from-scratch and RETROFIT studies (A, C). The retrofit path (B) is the town's
  cheapest route to a same-params loop-vs-no-loop test on CPU without pretraining.
- None of A/B/C has an HF GGUF today; the only CPU-loadable released looped LM in this whole slice is
  Ouro (GGUF, patched llama.cpp).
- Watch "overthinking" (A): a loop dial must be tuned, not maxed — consistent with Ouro's Table 10
  (performance peaks at the trained depth 4, degrades at 5-8).
