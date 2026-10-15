# README-ranked-table — Efficient decode training: freeze trunk, train decode-side module
READER: research-reader (read-only). TROVE APPEND-ONLY. Read 2026-09-18 UTC. All URLs checked 2026-09-18.
RANKING TARGET: train a tiny decode-side module (draft head / oscillator readout / C2C fuser)
against a FROZEN small Qwen trunk on an 8 GB GPU, CPU/ordinary-RAM-first.

| # | Paper (year) | arXiv | Trunk | Decode-side module | Freeze recipe | Headline number | Code / licence |
|---|---|---|---|---|---|---|---|
| 1 | Medusa (2024) | 2401.10774 | LLaMA/Vicuna-class | N draft heads + tree attention | Medusa-1: frozen backbone, heads only | 2.2-3.6x inference speedup, lossless | FasterDecoding/Medusa, Apache-2.0 |
| 2 | EAGLE-3 (2025) | 2503.01840 | Qwen2.5-7/14/32B available | 1-layer drafter, multi-layer feature fusion | frozen target, train drafter | up to 6.5x; 1.38x throughput @B64 | SafeAILab/EAGLE + SpecForge, Apache-2.0 |
| 3 | DSpark (2026) | 2607.05147 | DeepSeek-V4 (generic) | parallel backbone + Markov head + confidence head | frozen target, shares frozen embed/lm_head | +60-85% per-user gen speed (prod) | NVIDIA Megatron-Bridge/NeMo |
| 4 | DeepSeek-V3.2-Exp (2025) | github deepseek-ai (no arXiv id found) | DeepSeek-V3 MoE | lightning indexer (token selector) | freeze ALL, train indexer 1000 steps / 2.1B tok / LR 1e-3, then unfreeze | alignment warm-up; ~6% of steps trunk-frozen | DeepSeek-V3.2-Exp repo, MIT |
| 5 | LiT (2021/2022) | 2111.07991 | ViT-g/14 (vision) | text readout tower | LOCKED image trunk, train text tower | 85.2% zero-shot IN, 82.5% ObjectNet | big_vision, Apache-2.0 |
| 6 | FreezeOut (2017) | 1706.04983 | CIFAR CNNs | n/a (schedule) | progressively freeze early layers out of backward | up to 20% wall-clock, 0-3% acc | ajbrock/FreezeOut, MIT |
| 7 | DEQ (2019) | 1909.01377 | transformer (scratch) | n/a (implicit depth) | literal fixed-point equilibrium via root-finding | up to 88% memory reduction | locuslab/deq, MIT |
| 8 | FailFast (2025/26) | 2512.20573 | diverse AR models | off-the-shelf dLLM drafter | NO fine-tuning at all | up to 4.9x, 1.7x over EAGLE-3 | open-source (repo unverified) |

## FITS (ranked for the 8 GB / CPU town)
1. **Medusa-1** — smallest, simplest decode-side module; trunk-frozen is the headline recipe.
   Draft heads are tiny; trainable on a single 8 GB GPU with a Q4 Qwen trunk.
2. **EAGLE-3** — best-evidenced for Qwen; open training harness (SpecForge) + published Qwen
   draft heads. Multi-layer feature fusion needs trunk hidden states (CPU-feasible).
3. **DSpark** — modern, closest to the owner's "draft head + sequential readout + fuser" trio
   (parallel backbone + Markov head + confidence head), all on a frozen trunk.
4. **DeepSeek-V3.2-Exp warm-up** — the exact freeze-then-align-then-unfreeze choreography,
   with a concrete budget (1000 steps / 2.1B tokens / LR 1e-3) to copy for a readout.
5. **LiT** — conceptual ancestor (frozen heavy trunk, trained light readout); vision, not LLM.
6. **FreezeOut** — the progressive-freeze schedule; use for the unfreeze phase, not the module.
7. **DEQ** — only if "equilibrium" means a literal fixed point; otherwise a different sense.
8. **FailFast** — the zero-training upper bound; if an off-the-shelf drafter suffices, skip training.

## CAVEATS
- "Equilibrium/plateau" in the owner's brief = loss plateau, NOT DEQ's fixed point. Do not conflate.
- All "speedup" numbers are INFERENCE speedups unless labelled training; only FreezeOut (20%
  wall-clock) and DEQ (88% memory) are training-side numbers.
- No paper found that trains a "coupled-oscillator readout" or "SNN C2C fuser" against a frozen
  LLM trunk — that intersection appears OPEN (ESTIMATE, from this 8-paper scan).
- "qwen3.8 50b": no such released Qwen3 model found; nearest = Qwen3-8B / Qwen3-30B-A3B. UNRESOLVED.
