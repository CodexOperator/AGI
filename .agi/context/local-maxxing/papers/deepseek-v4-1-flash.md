# read:deepseek-v4-1-flash — compute-cost digest for the local-maxxing town

Owner thread: compute-cost tricks that can be supercharged by a bit-wise byte-neuron SNN
(bit FLIP = impulse), coupled oscillators as flip-timing (digital Kuramoto), and a recurrent
looped transformer with cross-token gated state feedback.

**Reader:** town research reader (`goal:g14`), READ-ONLY except this file.
**Date read:** 2026-09-14.

---

## 0. Provenance — exactly what was read

| Item | Value |
|---|---|
| Primary index page | `https://www.alphaxiv.org/abs/2609.deepseek-v4-1-flash` — HTTP 200, 256 KB HTML, fetched 2026-09-14 |
| Full document (PDF) | `https://www.alphaxiv.org/abs/2609.deepseek-v4-1-flash.pdf` — HTTP 200, `application/pdf`, **1,809,802 bytes**, fetched 2026-09-14 |
| Identical mirror | `https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/resolve/main/DeepSeek_V41_Tech_Report.pdf` — HTTP 200, `application/pdf`, **1,809,802 bytes**, byte-size identical; author-listed checkpoint repo |
| Title | *DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression* |
| Author | DeepSeek-AI (`research@deepseek.com`); `author: []` in page metadata |
| Publisher / id | arXiv, id `2609.deepseek-v4-1-flash` |
| Date published (page metadata) | Thu Sep 10 2026 17:20:23 GMT+0000 (UTC) |
| Engagement at fetch | 30,960 views, 277 likes |
| Extraction | `pdftotext -layout` → 2,881 lines; all quotes below from that text |

No arXiv-blessed `arxiv.org/abs/...` page resolved (HTTP 404) — the doc was read from the two
PDF mirrors above, which agreed in byte size. **Nothing below is invented; every number is
quoted from this document.** Numbers are tagged **[MEASURED]** (quoted from the document, with
section/figure/table) or **[ESTIMATE]** (this reader's arithmetic/inference, shown).

> Caveat on "MEASURED": the tag means *the document reports it*, not that the town reproduced
> it. All efficiency claims in this report are **vendor self-reports under "our internal
> evaluation framework"**; the paper publishes no third-party reproduction and, for the cost
> numbers, no raw hardware counters. Treat every efficiency figure as a *claim under the
> paper's own conditions*, not as independent ground truth.

**Hardware/scale gap [GAP]:** the paper **never names a GPU, accelerator count, cluster size,
or wall-clock cost**. It discusses HBM, SSD, host DRAM, RDMA, sub-NUMA partitioning, and
"millions of concurrent sandbox instances" (`§5.1.3`) but gives no device model, no node count of
the training cluster, and no per-token dollar figure. Every hardware assumption below that is
not a parameter count is tagged **[GAP]**.

---

## 1. TL;DR for a CPU/edge local-maxxing town

The paper is a **KV-cache-and-prefill cost paper**, wrapped around a 552B-parameter multimodal
MoE. Its five load-bearing tricks are, in order of how much they transfer to a ≤4 B CPU model:

1. **Reasoning-effort control** (`§5.1.4`, Table 2, Fig. 9) — zero architecture change, pure
   token-budget knob. **Transfers fully. Highest value per unit of effort.**
2. **SWA Bounded Replay** (`§2.2`, `§3.2.2`) — a pure inference-system trick that bounds prefix
   recomputation to the window instead of `L × nwin`. **Transfers fully at small scale.**
3. **Speculative decoding with a tiny drafter** (DSpark, `§2.4.3`) — 3-block drafter; **transfers
   to CPU if the break-even is respected** (see falsifier F3).
4. **Cross-layer KV / index reuse** (CSA2, `§2.3.1`) and **hierarchical sparse indexer**
   (`§2.3.2`) — transfers in *mechanism* but its prize (a 1M-token KV budget) does **not** exist
   for a ≤4 B model serving ≤8 K contexts; see §4.
5. **FP4 KV cache / CED half-encoder prefill / Single-Pass mHC** — mostly **does not transfer
   unmodified**: FP4 needs QAT + a dequant path CPU lacks; CED needs from-scratch training; mHC's
   win is a fused GPU kernel.

The **single biggest transferable insight** is not a compression ratio — it is the *coupling
discipline*: this model reduces cost along **three multiplicative axes at once** (entry size ×
sequence compression × layer reuse, `§2.3`) while keeping each axis individually simple. A CPU
town should copy the *decomposition*, not any one number.

The **owner's oscillator/SNN/looped bridge is not supported or refuted by this document.** The
552B model here is a conventional Transformer + MoE with **no spiking, oscillatory, or looped
component anywhere.** The paper therefore provides zero evidence that such a layer "supercharges"
its tricks — and zero evidence it cannot. It is an untested hypothesis. §5 assesses each trick
against it, with a falsifier apiece.

---

## 2. Technique inventory (mechanism → measured saving → scale it assumes)

Legend: **[M]** = MEASURED, quoted with locator. **[E]** = ESTIMATE / this reader's arithmetic.

| # | Technique | Mechanism (one line) | Reported saving [M] | Locator | Scale/hardware it assumes |
|---|---|---|---|---|---|
| T1 | Causal Encoder–Decoder (CED) | Bottom 20/40 layers = encoder; decoder global KV projected from encoder hidden state `H_{L/2}` via per-layer `W^KV, W^Z` | Prefill complexity `O(NL) → O(NL/2 + nwin·L/2) ≈ O(NL/2)`; *"nearly halves prefill computation"*; 8B active/token prefill vs 16B decode | `§2.2`, abstract, `§2.1` | 40-layer model; assumes long `N ≫ nwin`; training from scratch (no retrofit) |
| T2 | CSA2 cross-layer KV + index reuse | Layers statically in Full / Reindex / Reuse; Reuse layers borrow most-recent main KV + indexer K + Top-K indices | Layers execute with **15 kernels prefill / 11 decode** in Reuse mode | `§3.2`, `§1` | 40-layer stack, 6-layer reuse groups; needs training-aware shared params |
| T3 | Hierarchical Sparse Indexer | First Full-mode decoder layer builds a candidate pool (2048 blocks × 8 = 16 384 positions); deeper indexers score only that pool | Per-query cost of deeper indexers goes **linear → constant** in context length; first-layer full scan retained | `§2.3.2`, `§4.2.1` | 1M-token contexts; decoder-only; trained into the model |
| T4 | FP4 main KV cache (MXFP4 / NVFP4-like, E2M1 + 1×E4M3 scale per 16 ch) | QAT during post-training; dequant before attention; **FP4 chosen for storage, not matmul** | Main KV *"nearly halves the storage footprint"* vs FP8, HBM and SSD; overall global KV **890 B/token ≈ 1/4 of V4-Flash**, ≈ **437× smaller than V1** | `§2.4.4`, abstract, `§6`, Fig. 1(b) | QAT pipeline; dequant path; SWA KV stays FP8 (accuracy-sensitive) |
| T5 | SWA Bounded Replay | Reconstruct SWA KV by replaying only the last `nwin` tokens (truncated SWA), not `L × nwin`; decoder replay bounds forward pass to `nwin`; simulated during post-training | Persistent KV footprint → **≈1/8 of V4-Flash** (= ½ from dropping SWA persistence × ¼ from global-KV compression); *"negligible performance degradation"* | `§2.2`, `§3.2.1`, `§3.2.2`, abstract | `nwin = 128`; approximate (not exact) state; needs train-aware simulation |
| T6 | Single-Pass mHC + Mega-mHC kernel | Shift input-mixing coefficients by one block so residual update, input mixing, coefficient prediction fuse into one pass | Activation traffic `(4n+4)d → (2n+2)d` — *"halving the activation memory traffic"* | `§2.4.1` | GPU kernel fusion (DeepGEMM `Mega-mHC`); `n` residual streams (`mHC` expansion factor = 4, `§4.2.1`) |
| T7 | Engram conditional memory | N-gram hash lookup tables (orders {2,3,4}, 8 heads, ~16M entries/head, dim 2048/order), FP8, prefetched from host by RDMA | 196B params added **without** per-token compute; *"decouple memorization from computation"*; embedding tables stay GPU-resident during RL to avoid host OOM | `§2.4.2`, `§2.1`, `§3.1.3` | 196B-param tables [GAP: no lookup latency/cost number published] |
| T8 | DSpark speculative decoding | 3-block drafter (window 128), one pass produces 5 draft positions in parallel; Markov head + confidence head; scheduler picks verification length | *"improve decoding efficiency"* — **[GAP: no acceptance-rate, no tok/s, no speedup number is published]** | `§2.4.3` | Drafter trained post-hoc, backbone frozen; GPU engine throughput curves |
| T9 | Reasoning-effort control (scalar `b`∈1–100) | Length-penalty coefficient `k(b)=k0·exp(−(b−bmin)/τ)` shapes RL reward; effort prepended to system prompt | Effort 25→100: avg Pass@1 on 8 reasoning benchmarks **67.1%→76.3%**, DeepSWE v1.1 **66.0%→74.2%**, Terminal-Bench 2.1 **82.4%→90.6%**, at **≈2.5× more output tokens**; 60–80 recovers most accuracy at <½ token budget; 100 adds 1.6–1.8× length for marginal gain | `§5.1.4`, `§5.3.2`, Table 2, Fig. 9 | RL post-training with length reward; API tiers max/high/low = b 100/75/50 |
| T10 | Head-wise Muon + Sinkhorn-balanced updates | Per-head preconditioner for Q/K; Sinkhorn row/column balancing replaces Newton–Schulz for embeddings/head (momentum buffer only) | *"requires only a momentum buffer"* for Engram/embed/head — avoids Adam's two moments and optimizer-state blowup | `§2.5`, Alg. 1 | Custom optimizer; γ=0.18 LR correction |
| T11 | EPD disaggregation + kernel fusion | Vision-encode / prefill / decode scale independently and overlap; fused FlashMLA/DeepGEMM kernels | Reuse-mode layers: 15/11 kernels (see T2) | `§3.2` | Multi-node serving pool |
| T12 | Async RL w/ stateful rollout resume | Token-level interruption; persist KV cache + expert routing at token granularity; concatenated routing-replay; sample-level dispatch | *"eliminating the cost of re-prefilling"* on checkpoint switch; no number published | `§5.2.1`, `§5.2.3` | Cluster-scale RL; [GAP: no % throughput] |
| T13 | DSec sandbox density | Sub-NUMA partition + per-worker-VM binding; `SCHED_IDLE` + core scheduling for latency-sensitive class | Density **~1,000 → >2,500 live containers per physical node** before measurable degradation | `§5.1.3` | Datacenter CPUs; [GAP: device model absent] |
| T14 | Multimodal balanced image sharding | Shard images across CP ranks, load each once | Loading hidden behind compute iff `ρ < (B_IO/B_GPU)·C` — *per-token, N cancels* | `§3.1.1` | Vision-heavy training; I/O-bound only for small models |

Reference model geometry (all **[M]**, `§4.2.1`): 40 layers, `d=5120`, 20 encoder + 20 decoder;
CSA2 `m=2` encoder / `m=1` decoder; indexer 32 heads × 128 dim, top-k 512; `nwin=128`; MoE
1 shared + 384 routed experts, 6 active, inner dim 2304; mHC expansion 4, 20 Sinkhorn iters.
Full counts **[M]**: 552B backbone + 196B Engram params; 8B active prefill / 16B active decode.
Training **[M]**: 45T tokens, batch 100.6M tokens, sparse attention from scratch at 64K, extended
to 1M at 34T tokens (`§4.2.2`).

---

## 3. The savings, quantitatively

### 3.1 KV cache — the headline

- Global KV (always in HBM) **[M]**: **890 bytes/token**, *"roughly 1/4"* of DeepSeek-V4-Flash
  (`§6`, abstract). ⇒ V4-Flash ≈ 3,560 B/token **[E]**.
- vs first generation **[M]**: **≈4×** smaller than V4-Flash and **≈437×** smaller than V1
  (Fig. 1(b) caption).
- Persistent KV (SSD/host) **[M]**: **≈1/8** of V4-Flash (`§3.2.1`), decomposed multiplicatively
  as *"no longer stores SWA KV, which almost halves its size"* × *"global KV … compressed to 1/4"*
  (`§3.2.1`). ½ × ¼ = ⅛ **[E]** confirms.
- FP4 alone **[M]**: *"nearly halves the storage footprint"* of the FP8 main KV cache, HBM and SSD
  (`§2.4.4`).

### 3.2 Compute

- Decode FLOPs **[M]**: extending context **256× (4K→1M) raises decode FLOPs by only ¼**
  (Fig. 2 caption, `§1`). Compute weights: BF16/FP8/FP4 = 1 / 0.5 / 0.25.
- Prefill **[M]**: CED *"nearly halves prefill computation"*; explicit complexity
  `O(NL) → O(NL/2 + nwin·L/2)` (`§2.2`).
- Indexer **[M]**: deeper-indexer per-query cost *"linear in context length → constant"* for a
  fixed candidate-pool size (`§2.3.2`).
- Kernel count **[M]**: 15 prefill / 11 decode kernels for Reuse-mode layers (`§3.2`).
- Activation traffic **[M]**: `(4n+4)d → (2n+2)d`, *"halving … activation memory traffic"* (`§2.4.1`).

### 3.3 Capability at a smaller active budget

- Base model **[M]** (`§4.3.2`, `§1`): V4.1-Flash-Base matches V4-Pro-Base on world
  knowledge/reasoning/coding with **1/3 the total params and 1/4 the activated params**
  (Table 1: 552B/8–16B vs 1.6T/49B), +5–10% on held-out evals.
- Post-trained **[M]** (`Table 3`): Codeforces 3471, DeepSWE v1.1 74.2%, Terminal-Bench 2.1
  90.6%, GPQA-D 90.9%. Highest or near-highest in most rows; a stated gap remains on
  science-oriented agentic tasks (Terminal-Bench 4.0: 31.2 vs Opus-5 51.8).

---

## 4. What transfers to a ≤4 B model on CPU — and what does not

Frame: the town's boxes are **4-core ARM arm64-N1, no i8mm, 23 GB**; **8 GB Intel**;
**M3 Air 16 GB**; one **gpu-8g** soon; **Camber GPU 3 h/month**. Everything must
fit CPU + ordinary RAM. So the question is not "is this a good trick at 552B" but "does it still
pay at ≤4B and ≤a few thousand context tokens, where **decode is memory-bandwidth-bound on
CPU** and **prefill over short prompts is nearly free**".

### 4.1 Transfers cleanly

- **T9 reasoning-effort / token-budget control.** No architecture, no kernel, no training-lab
  required to *use* it: a length reward during any small-model fine-tune, or even a prompt-level
  budget at inference. The transferable lesson is the **front-loaded curve** (`60–80` recovers
  most accuracy at <½ the tokens; `100` costs 1.6–1.8× length for marginal gain, `§5.3.2`). On a
  CPU town paying per generated token in wall-clock, that knee is exactly the operating point.
- **T5 SWA Bounded Replay.** Pure systems trick. Works on any SWA model, any device: recompute
  the last `nwin` tokens instead of `L×nwin`, accept approximate state, simulate during
  fine-tune. On a CPU town doing multi-turn agents with prefix caching, this is the difference
  between "re-prefill the whole prefix" and "re-prefill 128 tokens". **Caveat:** the paper measures
  quality loss as *"negligible"* only for **its** model/`nwin=128`; at small `nwin`/small model the
  approximation error is unmeasured — the town must re-measure it (seed H2).
- **T8 speculative decoding (tiny drafter).** A 3-block drafter is cheap enough to run alongside a
  ≤4B CPU target. The concept (small draft, confidence-gated verification length) transfers; the
  *numbers* do not, because none are published.

### 4.2 Transfers in mechanism, but the prize may not exist at small scale

- **T2 CSA2 cross-layer KV reuse.** Mechanically trivial to copy: share main KV + indexer K across
  layers, reuse Top-K selections. On CPU, **KV bytes are read every decode step**, so fewer
  distinct KV arrays = fewer memory reads = real speedup. But the prize here is a *1M-token*
  footprint; at **≤8 K context and ≤4 B params, a dense KV cache is already ~tens of MB** and the
  reuse saves bandwidth, not capacity. Reuse can still pay via bandwidth — but it must be
  *measured*, not assumed. Also: Reuse mode risks quality because layers lose their own selection;
  the paper compensates with Reindex mode and training-time sharing (§3.1.2).
- **T3 Hierarchical Sparse Indexer.** Constant-cost deeper indexing matters only when the context
  is long enough that a full indexer scan dominates. For ≤4 K–8 K contexts the indexer is already
  cheap; **sparse attention typically costs more (gather/scatter, branch) than dense** on a CPU
  with no gather acceleration. Transfers only if the town pushes contexts past ~32 K.
- **T6 Single-Pass mHC.** The *idea* (one fused pass, `(2n+2)d` instead of `(4n+4)d`) is a
  memory-traffic reduction — and CPU decode is memory-traffic-bound, so the idea is attractive.
  But the paper's win is a **GPU fused kernel (Mega-mHC/DeepGEMM)**; on CPU the town would need
  its own fused SIMD/NEON residual-mixing loop, and mHC adds `n` residual streams, which
  *raises* RAM. Net sign is unmeasured on CPU.

### 4.3 Does not transfer unmodified

- **T4 FP4 KV cache.** The storage win (½ of FP8) is real and device-independent; the *speed* win
  is not: the paper explicitly lets FP4 be dequantized before attention, and CPUs lack FP4 matmul.
  To get the RAM win the town must (a) train QAT or accept post-hoc quantization error, and
  (b) pay a dequant cost per attention. On **arm64-N1 without i8mm**, even INT8 dots are weak;
  FP4 KV is a *capacity* trick on CPU, likely a *net slowdown* for speed unless KV reads dominate.
- **T1 CED.** Concept transfers (project decoder KV from encoder hidden state, halve prefill
  layers) but **only if you train your own small model** — CED is baked into pre-training; you
  cannot retrofit a downloaded Transformer. For short CPU prompts, prefill is not the dominant
  cost anyway (decode is), so CED's ~2× prefill saving buys little on a chat/agent workload.
- **T7 Engram.** Conceptually *very* anti-CPU-friendly in a good way (hash lookups, fp8 tables,
  host prefetch) and it decouples memory from compute — attractive for a small model. But the
  numbers here are at 196B params and the paper publishes **no lookup-latency or bandwidth cost**
  [GAP]. The town would build its own tiny n-gram table and measure whether lookups beat the
  compute they replace. Promising, unproven.
- **T10 Sinkhorn / head-wise Muon.** Training-only. The one transferable idea is **Sinkhorn
  replaces Adam's 2-moment optimizer state with 1 momentum buffer** (`§2.5`) — meaningful for the
  town's RAM when fine-tuning, and CPU-friendly (no GPU kernel needed). Head-wise Muon is a
  quality trick, not a cost trick.
- **T11–T14 (EPD, async RL, DSec, image sharding).** Multi-node infrastructure. No transfer to a
  single CPU box. Included only because the brief asked for *every* compute-saving technique.

---

## 5. The owner's bridge — frank assessment, one paragraph per technique

Standing framing: the claim under test is *"the oscillator/SNN/looped layer can supercharge each
compute-saving trick in these papers."* **This document cannot test it** — there is no spiking,
oscillatory, or looped component in V4.1-Flash. So each paragraph below is a **hypothesis with a
falsifier**, not a verdict. The honest prior is: the bridge is *orthogonal-or-hostile* to the
paper's dominant cost centre (KV **bytes**), and *plausibly aligned* with its secondary centre
(**how many tokens/loops you spend**). A bit-flip neuron and FP4 KV are both "few bits", but they
sit at different places in the stack — the paper never asks whether the *neuron* should be a bit,
only whether the *cache* can be.

- **T1 CED (half-encoder prefill).** No obvious bridge benefit — CED is a depth-sharing trick in a
  conventional stack; a looped layer already *is* depth-sharing by construction, so CED mostly
  *duplicates* what looping gives cheaply. If anything, looped state feedback could make the
  encoder→decoder KV projection redundant: the loop carries the context instead of a projected KV.
  *Falsifier:* train a 6-layer looped model and an equivalent CED model at equal params/FLOPs; if
  the looped model's prefill quality or throughput does **not** beat CED, the "redundant" claim is
  wrong. Also falsified if the loop fails to preserve long-range recall that CED's explicit KV does.

- **T2 CSA2 cross-layer KV reuse.** **Best-fit bridge.** A looped transformer with cross-token
  gated state feedback *is* layer reuse taken to its limit (unbounded reuse, gated). The natural
  claim: the loop replaces CSA2's Reuse mode, and gating decides what the shared state forgets.
  *Falsifier:* if a looped layer with a single shared state cannot match a model that keeps
  per-layer Reindex selections (CSA2's escape hatch for quality), then reuse-by-looping is not a
  superset of reuse-by-layering — it is a cheaper, weaker operation, and the paper's Reindex mode
  is evidence *against* pure looped reuse.

- **T3 Hierarchical Sparse Indexer.** Bridge is plausible: an indexer whose scores come from
  oscillator phase-alignment (a digital-Kuramoto "resonance" score over KV) could be computed with
  popcount/integer ops instead of dense float dots — a genuine CPU win. The hierarchical pool idea
  (coarse filter → fine rescore) maps naturally onto two oscillator timescales. *Falsifier:* if the
  phase-based coarse filter's Top-K **recall** on the positions a dense indexer selects falls
  below the level at which end-task quality holds, the oscillator indexer is a worse filter at the
  same FLOPs — measure recall@K against a dense indexer and require parity before claiming a win.

- **T4 FP4 KV cache.** Orthogonal at best, antagonistic at worst. A bit-neuron (1-bit) is *more*
  aggressive than FP4, so "bit-flip neurons" could subsume FP4 KV — but the paper's own caution is
  the warning: **SWA KV stays FP8 because it is "sensitive to quantization"** (`§2.4.4`), and
  main KV is FP4 only after QAT and RoPE. *Falsifier:* drop KV to 1 bit (or to bit-flip state) at
  equal scale and measure task quality; if degradation is not negligible while FP4's is, the
  SNN bridge does **not** supercharge this trick — it over-runs it.

- **T5 SWA Bounded Replay.** Bridge is weak-to-neutral: bounded replay is a *recompute* strategy;
  a looped/recurrent layer could instead *carry* the SWA state across turns (replay becomes
  implicit). If it works, it beats bounded replay (no recompute at all). *Falsifier:* measure
  multi-turn quality with carried looped state vs bounded replay; if carried state drifts or
  cannot be checkpointed cheaply (the paper's own async-RL trick persists KV by token, `§5.2.3`),
  the loop is not cheaper than replay — deterministic recompute wins.

- **T6 Single-Pass mHC.** Friendly bridge on paper: mHC is literally *multiple residual streams
  with token-wise mixing coefficients* — an oscillatory/coupled-gating layer is a natural way to
  generate those coefficients (phase offsets as mixing weights). The CPU-relevant prize is the
  `(2n+2)d` traffic bound. *Falsifier:* if generating `A,B,C` from oscillator phases adds more
  reads/compute than it removes (e.g., `n` streams cost more RAM than the fused pass saves), the
  bridge is net-negative on CPU — measure bytes-moved-per-token, not FLOPs.

- **T7 Engram.** Bridge is genuinely interesting and *independent of spiking*: Engram shows the
  value of a cheap lookup that replaces compute. A byte-neuron/oscillator memory could be the
  lookup substrate (associative recall by phase). *Falsifier:* if hash-lookup Engram already
  saturates the memorization the model needs at small scale, adding an associative oscillator
  memory buys nothing; and if the oscillator memory's recall is not stable under context growth,
  it fails where hash tables do not.

- **T8 DSpark speculative decoding.** Strong bridge: a drafter is exactly where a cheap
  oscillator/SNN could live — small, fast, and allowed to be wrong. *Falsifier:* speculative
  decode is a break-even machine — with draft length 5 and a CPU target, you need **acceptance
  rate × target-cost-per-token > drafter-cost + overhead**. If an oscillator drafter's acceptance
  rate at ≤4B is below the break-even the town measures for a 3-block Transformer drafter, the
  bridge does not supercharge spec decode, it taxes it.

- **T9 Reasoning-effort control.** **Strongest bridge of all, and it is a mathematical fit, not a
  biological metaphor.** "Effort `b`" is a scalar that buys more tokens for more accuracy; a looped
  layer has a *free* scalar of the same kind — **loop count**. The paper's front-loaded curve
  (`§5.3.2`) is the target: the town wants loops, not tokens, to be the cheap axis, because loop
  iterations reuse resident weights (no KV growth, no new tokens to generate). *Falsifier:* sweep
  loop count and plot accuracy-vs-FLOPs; if it is **not monotone** (more loops not reliably more
  accuracy) or if loop iterations cost more wall-clock per unit accuracy than simply emitting more
  tokens, then "loops = reasoning effort" is false for this hardware and the knob does not exist.

- **T10 Sinkhorn update.** No bridge needed; a looped/oscillatory *training* rule could in principle
  drop the momentum buffer too, but the paper gives no reason to expect an oscillator optimizer to
  beat Sinkhorn's row/column balancing. *Falsifier:* equal-parameter fine-tune with an
  oscillator-based update vs Sinkhorn momentum; if peak memory is not lower at equal quality, no win.

- **T11–T14.** No bridge. These are cluster/system tricks; SNN/oscillator has no purchase on
  datacenter scheduling or sandbox density.

**Bridge verdict (frank):** the claim "the oscillator/SNN/looped layer supercharges *each* trick"
is **unsupported by this document and, where testable, half-true at best.** The bridge plausibly
supercharges **T9 (loop count as effort)**, **T2 (state reuse)**, **T8 (cheap drafter)**, and **T3
(phase-based coarse indexer)**; it is **neutral or hostile** to **T4 (KV bits — already near the
SNN's own 1-bit floor)** and **T1 (CED — looping duplicates it)**. The paper's dominant cost centre
is *cache bytes*, which the neuron's bit-width does not touch. Any town claim that the bridge
"saves compute" must be sited at a *named technique* and a *named falsifier* from the list above —
otherwise it is the metaphor doing the arguing.

---

## 6. Hypothesis seeds runnable on the town's CPUs

Each seed: **runnable now**, **CPU-only**, ≤4B params, with a hard pass/fail and a falsifier.

### H1 — Loop-count-as-effort vs token-count-as-effort (test of T9 + owner's strongest bridge)
- **Do:** train one tiny looped Transformer (≈50–150M params, cross-token gated state feedback) on
  a small reasoning task (e.g. arith word problems / GSM8K-subset); sweep loop count `r=1..8`.
  In parallel, sweep *token* budget on a same-size vanilla model. Plot accuracy vs FLOPs.
- **Pass:** looped accuracy-vs-FLOPs dominates token-budget accuracy-vs-FLOPs at some operating
  point, and is monotone in `r`.
- **Falsifier:** monotonicity fails, or token-budget wins — then "loops = reasoning effort" is false
  on CPU.
- **Cost:** single-box fine-tune, hours; inference comparison in minutes.

### H2 — SWA Bounded Replay at small scale (test of T5)
- **Do:** take a ≤1B sliding-window model (or train a tiny one), implement prefix caching +
  bounded replay (`nwin` sweep: 32/64/128/256), measure (a) quality on multi-turn dialogues,
  (b) prefill tokens recomputed and wall-clock, on the 4-core ARM box.
- **Pass:** quality loss within noise, prefill recompute drops by ~`L/2 ×` at equal `nwin`.
- **Falsifier:** quality loss is not negligible at small `nwin` — the paper's *"negligible"* does
  not carry to small models.
- **Cost:** days of engineering; benchmark minutes.

### H3 — CPU decode is KV-bandwidth-bound (measurement that decides T2/T4 relevance)
- **Do:** at ≤1B params, 4K/8K context, measure decode tok/s vs KV precision (FP16 / FP8 / INT4 /
  1-bit) on the ARM (no i8mm) and the M3. Separately measure **bytes read from KV per token**.
- **Pass:** a clear tok/s gain from fewer KV bytes ⇒ KV bandwidth is the CPU bottleneck ⇒ T2/T4-class
  tricks are worth porting.
- **Falsifier:** no gain (dequant/compute dominates) ⇒ the paper's KV-bytes prize is *not* the CPU
  prize; pursue T9/T5 instead.
- **Cost:** a day; this is the gating measurement for the whole roadmap.

### H4 — Speculative decoding break-even on CPU (test of T8 + oscillator-drafter bridge)
- **Do:** ≤1B target + a 3-block Transformer drafter first (baseline), then an oscillator/bit-flip
  drafter, on the 4-core ARM and M3. Measure acceptance rate, drafter cost fraction, end tok/s.
- **Pass:** end-to-end speedup >1 on at least one box with the Transformer drafter; then test
  whether the oscillator drafter reaches the same acceptance rate at lower cost.
- **Falsifier:** the measured break-even (acceptance × target-cost) is not met in either case ⇒
  the bridge taxes spec decode rather than supercharging it.
- **Cost:** days; benchmark minutes.

### H5 — Phase-based coarse indexer: recall-at-equal-FLOPs (test of T3 + oscillator bridge)
- **Do:** build a dense top-k indexer over synthetic long sequences; replace its coarse stage with a
  sign/phase (popcount) score. Compare **recall@K** and FLOPs against the dense indexer.
- **Pass:** recall@K within ~2 points of dense at materially lower FLOPs / no gather on CPU.
- **Falsifier:** recall@K collapses ⇒ the oscillator filter is a worse filter at equal FLOPs, and
  T3's hierarchical trick does not transfer to the bridge.
- **Cost:** a day of numpy/C; no training needed for the recall proxy.

*(Optional H6, if the above pay off: hash-table Engram memory (T7) at ≤1B — measure whether n-gram
lookups beat the compute they replace on CPU. No paper number exists to target; start from the
mechanism, not the 196B scale.)*

---

## 7. Gap register — what this document does NOT tell you (do not assume it)

| Gap | Consequence for the town |
|---|---|
| **No device model / accelerator count / cluster size anywhere** | Every efficiency figure is relative (×-fold, bytes/token, kernel count); **no absolute tok/s, no $/token**. Do not quote 890 B/token as a wall-clock claim. |
| **No DSpark acceptance rate, speedup, or tok/s** (`§2.4.3`) | Spec decode cannot be budgeted from this paper; town must measure (H4). |
| **No Engram lookup latency / bandwidth cost** (`§2.4.2`) | The "cheap memory" claim is qualitative; measure before porting (H6). |
| **No absolute FLOPs; Fig. 2 is relative, precision-weighted** | "Only ¼ growth over 256× context" is a ratio, not a budget. |
| **No baseline KV bytes-per-token stated as a raw number** | V4-Flash ≈ 3,560 B/token is **my arithmetic [E]**, not a quoted figure. |
| **No raw quality-vs-compression ablation table for SWA Bounded Replay** | "Negligible degradation" is asserted; the town must reproduce at its scale (H2). |
| **No quantized-vs-dense CPU relevance** | Whether KV bytes are the CPU bottleneck is *unmeasured by the paper* — H3 exists to decide it. |
| **No spiking / oscillator / looped baseline of any kind** | The owner's bridge is untested by construction. Frank reading: this paper is **evidence-neutral** on the bridge. |
| **Post-training claims are self-reported under "our internal evaluation framework"** | Vendor numbers; treat as claims. |

---

## 8. Bottom line for the town

- **Adopt first, zero-risk:** T9 (effort/token-budget knee), T5 (SWA bounded replay), and the
  T10 Sinkhorn-momentum idea (fine-tune RAM). All are CPU-clean and need no new hardware.
- **Measure before adopting:** T2 KV reuse, T4 quantized KV, T8 spec decode — their relevance is
  *decided by whether CPU decode is KV-bandwidth-bound* (H3). Do H3 first; it is one day and it
  gates everything.
- **Do not port:** CED (needs from-scratch training; short-prompt prefill is not the CPU cost),
  and the cluster tricks (T11–T14).
- **On the owner's bridge:** this paper neither proves nor disproves it. Its best case is **loop
  count as a reasoning-effort knob (H1)** and **state reuse standing in for cross-layer KV
  (H2/T2)**; its worst case is **KV-bit compression, where FP4 already sits near the SNN's own
  1-bit floor**. Every claim must name a technique and a falsifier, or it is metaphor.

---

*End of digest. Single permitted write for `read:deepseek-v4-1-flash`.*
