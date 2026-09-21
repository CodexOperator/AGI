# README-ranked-table — Looped / recurrent-depth small LMs with RELEASED weights, CPU-first
READER: research-reader (read-only). TROVE. Read 2026-09-18 UTC. All model facts MEASURED from the
HF API / model config / README today; paper facts MEASURED from arXiv abs/html today.
RANKING TARGET: a released looped/recurrent-depth LM a kid-tier eval can run on the 4-core aarch64
box (23 GB RAM, ~7 GB free, no GPU) today, with a loop dial that proves looping > not-looping at
the SAME unique parameters.
ANONYMIZATION: boxes and accelerators by generic class only (this box = "the 4-core aarch64 box";
training rigs = "an academic AMD-accelerator cluster", "a datacenter-class accelerator"). HF model
ids are model repositories and are given as required.

## RANKED TABLE (released weights only)
| # | Model | arXiv | Unique params | Eff. depth (loops) | Weights: HF id / bytes / licence | CPU path today | Quality, looped vs un-looped (same unique params) | Training recipe cost |
|---|---|---|---|---|---|---|---|---|
| 1 | **Ouro-1.4B** (ByteDance) | 2510.25741 | 1.43 B (MEASURED, safetensors) | 96 = 24 layers x 4 loops (MEASURED config + GGUF README) | `ByteDance/Ouro-1.4B` BF16 2.87 GB, Apache-2.0; GGUF `BrandeisPatrick/Ouro-1.4B-GGUF` F16 2.87 / Q8_0 1.53 / Q4_K_M 0.896 GB (MEASURED) | transformers (custom code, <4.56); GGUF only via PATCHED llama.cpp (`ouro` arch NOT upstream today) | GSM8K 3-shot strict, 200-problem subset: **26.0% @1 loop -> 80.5% @4 loops** (F16); paper Table 10 step1->4 MMLU 41.21->67.45 (MEASURED) | 7.7 T tokens (6T pre + 1.4T CT anneal + 20B longctx + 300B mid); hardware/hours NOT stated (gap) |
| 2 | **Ouro-2.6B** (ByteDance) | 2510.25741 | 2.67 B (MEASURED) | 192 = 48 layers x 4 loops | `ByteDance/Ouro-2.6B` BF16 5.34 GB, Apache-2.0; GGUF F16 5.34 / Q8_0 2.84 / Q4_K_M 1.65 GB (MEASURED) | same as #1 (patched llama.cpp) | 4 loops beats 3-12B dense on most benches; 1.4B ablation is the same-param proof | same 7.7 T-token recipe |
| 3 | **Huginn-0125** (Geiping et al.) | 2502.05171 | 3.91 B stored (F32, MEASURED safetensors); ~3.5 B nominal | 132 = 2 prelude + 4x32 recurrent + 2 coda (MEASURED config) | `tomg-group-umd/huginn-0125` F32 15.63 GB, Apache-2.0; NO GGUF for this model (the "Huginn-13B" GGUFs are an unrelated Llama) | transformers `trust_remote_code` only; no llama.cpp arch (open feature request) | 180B-token early ckpt, r=32 vs r=1: HellaSwag 48.80 vs 29.19; GSM8K-CoT 9.02/10.24 vs 0.00/0.15; fixed-depth baseline HellaSwag 37.34 (MEASURED Table 4) | 800B tokens main + 180B baseline; academic AMD-accelerator cluster; FLOPs ~ a 32B dense pretrain (MEASURED) |
| 4 | **MoR 360M** (Bae et al.) | 2507.10524 | ~1/3 of 360M base (MEASURED README) | N_r=2..3 recursions | NOT on HF; checkpoints (Vanilla/Recursive/MoR 360M) on an external drive link; repo Apache-2.0 (MEASURED) | Llama-based code; would need conversion + router/KV-sharing graph; no GGUF | equal-FLOPs 16.5e18: MoR 43.1% avg few-shot vs vanilla 42.3% with ~50% fewer params; **1.7B MoR loses to vanilla** (MEASURED) | FineWeb-Edu, 10-20B tokens in experiments; 135M-1.7B base |
| 5 | **Universal Transformer / ALBERT** | 1807.03819 / 1909.11942 | ALBERT-base-v2 11.84 M, large 17.88 M, xxlarge 223.2 M (MEASURED safetensors) | ALBERT = 12 shared layers, fixed depth (NO test-time loop dial) | `albert/albert-*-v2` Apache-2.0 (MEASURED) | transformers, CPU-native; no loop dial | UT: +0.9 BLEU over Transformer on WMT14 En-De (MEASURED abstract); ALBERT: SOTA GLUE/RACE/SQuAD with fewer params than BERT-large (exact GLUE gap) | BERT-scale pretraining |
| 6 | **Looped Transformers (theory)** | 2301.13196 / 2311.12424 | small, scratch | constant layers, looped | none released | n/a | Yang: looped matches standard with **<10% params** on data-fitting (MEASURED abstract) | n/a |
| 7 | **RLT (temporal recurrence)** | alphaXiv 2609.recurrent-looped-transformer | not stated | unbounded TEMPORAL depth (grows with tokens), fixed decoder depth | NONE; no results reported | n/a | none — analytical report only (MEASURED) | not stated |
| 8 | **Loop, Think, & Generalize / T2MLR / Recurrent Transformer** | 2604.07822 / 2607.15178 / 2604.21215 | small, scratch / retrofit | depth recurrence | Loop-Think-Generalize checkpoints on external drive (Apache-2.0); T2MLR code `princeton-pli/T2MLR` | research code | recurrent-depth > vanilla on compositional generalization + depth extrapolation (MEASURED abstracts) | small-scale |

## CPU tok/s ESTIMATE for the 4-core aarch64 box
MEASURED today on this box: memcpy 256 MB x6 = **23.8 GB/s combined read+write**; a crc32 read scan
gave 2.4 GB/s but is compute-bound, so not used. For decode the weights stream from RAM once per loop
(4-core L2/L3 far smaller than the model), so effective bytes-touched/token = weight_bytes x loops.
ESTIMATE `tok/s = BW / (weight_bytes x loops)`, two bandwidth bounds 12 GB/s (conservative, memcpy
read-half) and 24 GB/s (optimistic, memcpy combined). All ESTIMATE except BW.

| model / file | bytes | loops | tok/s @12 GB/s | tok/s @24 GB/s |
|---|---|---|---|---|
| Ouro-1.4B Q4_K_M | 0.896 GB | 1 | 13.4 | 26.8 |
| Ouro-1.4B Q4_K_M | 0.896 GB | 4 | 3.3 | 6.7 |
| Ouro-1.4B Q8_0 | 1.53 GB | 4 | 2.0 | 3.9 |
| Ouro-2.6B Q4_K_M | 1.65 GB | 4 | 1.8 | 3.6 |
| Huginn-0125 bf16 (converted) | 7.8 GB | 8 | 0.19 | 0.38 |
| Huginn-0125 bf16 (converted) | 7.8 GB | 32 | 0.048 | 0.096 |

Cross-check (MEASURED, from the GGUF README, on a consumer ARM laptop SoC): Ouro-1.4B Q8_0 ~36 tok/s
@1 loop and ~9.5 tok/s @4 loops — consistent with the ESTIMATE at a higher bandwidth envelope.

## TOP-3 FALSIFIABLE HYPOTHESES (town 20-prompt kid checklist)
- **H1 (Ouro-1.4B).** On the 20-prompt kid checklist, Ouro-1.4B Q8_0 at `--override-kv ouro.num_loops=4`
  beats BOTH (a) the same file at 1 loop and (b) a same-unique-param dense non-looped model
  (Qwen3-1.7B-class, Q4) on exact-answer accuracy. **Falsified if** loops=4 <= loops=1 (looping adds
  nothing) or loops=4 <= the dense baseline (depth is not the source of the gain). Decisive, cheap,
  short outputs only (<=64 new tokens) so 2-4 tok/s is tolerable.
- **H2 (Ouro-2.6B).** The 1.4B loop-scaling curve reproduces at 2.6B: GSM8K/checklist accuracy rises
  monotonically 1->2->4 loops and the 2.6B@4-loops beats 1.4B@4-loops at equal wall-clock. **Falsified
  if** 2.6B shows no monotone gain, or its @4-loop accuracy ties 1.4B (scale, not loops, is the lever).
- **H3 (Huginn-0125, archival control).** At a compute budget the box can afford (r=4..8), Huginn's
  recurrence gain is visible but sub-kid-tier: r=8 beats r=1 on the checklist but absolute accuracy
  stays below Ouro-1.4B@4 loops. **Falsified if** Huginn r=8 already beats Ouro-1.4B@4 loops (then the
  3.5B latent-depth line is CPU-viable and outranks Ouro).

## CAVEATS / GAPS (never invent)
- Only **Ouro** has a released looped LM with a working CPU path (and it needs a patched llama.cpp
  until the `ouro` arch merges upstream; MEASURED: no `ouro` in llama.cpp master today).
- **MoR** and **Loop-Think-Generalize** weights are on external drive links, not HF; no GGUF.
- **Huginn** GGUF does not exist for the real model; F32 15.63 GB must be converted/downcast.
- **RLT** reports no empirical numbers at all — do not cite it as evidence.
- "qwen3.8 50b": still no such released id (prior trove `2026-09-18-round0/qwen38-50b.md`); unrelated
  to this slice.
- Looping multiplies CPU memory traffic by the loop count — the town's bytes-touched-per-token ledger
  should record `weight_bytes x loops`, not `weight_bytes`.
