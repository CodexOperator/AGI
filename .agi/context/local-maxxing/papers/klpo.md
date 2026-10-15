# read:klpo — digest of KLPO (KL-Regularized Policy Optimization)

**Reader:** local-maxxing town (goal:g14; moral:local-maxxing = knowledge and wisdom per token).
**Status of this digest:** read-only research; one output file (this one).
**Owner link:** 2026-09-21.

## 0. What was actually read (documents + dates)

| What | Identifier / URL | Read on |
|---|---|---|
| Repo README | `https://github.com/yifanzhang-pro/KLPO` (clone of `main`, depth 1) | 2026-09-21 |
| Paper PDF | `KLPO.pdf` in that repo, 56 pages, "September 18, 2026 · Revised: September 20, 2026" | 2026-09-21 |
| Algorithm reference | `docs/algorithms.md` | 2026-09-21 |
| Training guide | `docs/training.md` | 2026-09-21 |
| Website maintenance notes | `docs/website.md` | 2026-09-21 |
| Loss implementation | `klpo/loss.py` (358 lines), `klpo/_validation.py`, `klpo/budget.py`, `klpo/molt.py` | 2026-09-21 |
| CPU example | `examples/train_toy.py` (146 lines) | 2026-09-21 |
| Tests | `tests/*.py` (7 files, ~820 lines) | 2026-09-21 |
| Licence / notice | `LICENSE` (Apache-2.0), `NOTICE` | 2026-09-21 |

The PDF text was extracted with `pypdf` loaded from a wheel downloaded into `/tmp` (no system install; `pip install` was blocked by PEP 668 and was not forced). **No `torch` is installed on this box**, so the repo's own CPU tests were **read, not executed**. Every "MEASURED" tag below therefore quotes the *document or source code*, not a run I performed. Where I did arithmetic, it is tagged ESTIMATE.

The paper's own metadata: "Technical report: September 18, 2026 · Revised: September 20, 2026" (README L15). Authors "Yifan Zhang et al." Citation `@techreport{zhang2026klpo,...}`.

## 1. Executive summary (the honest one)

KLPO is a **theory-and-implementation report**, not an empirical paper. It has **no benchmark, no training curve, no ablation table, and no measured throughput/memory/cost number**. It says so itself:

> "This release provides the theory, loss implementation, CPU verification, and native training integration. **GPU training and paper-scale benchmark reproduction have not been validated.**" — MEASURED, `README.md` L97.

> "The local validation is CPU-based; CUDA/vLLM training and multi-GPU performance have not been run on this machine." — MEASURED, `docs/training.md` L118–119.

> "This does not validate a CUDA, Ray, FSDP, vLLM, or multi-node training run. No paper-scale result is claimed." — MEASURED, `docs/training.md` L250–251.

> "The website reports theoretical properties and implementation checks; do not present these as measured training or benchmark results." — MEASURED, `docs/website.md` L45.

So: **there is no MEASURED compute saving anywhere in this release.** What KLPO offers is a set of *structural* savings (whole models and whole passes it does not need) plus an **O(·) cost statement for the record formats**. Every quantitative saving below is either a direct quote of an asymptotic claim (MEASURED as a claim) or my own arithmetic (ESTIMATE). The "four KL estimators" and "eight combinations" are real and implemented and CPU-tested; the *speedups* are not measured.

The one genuinely useful fact for the town: **the loss is pure PyTorch and CPU-testable by design.** `klpo/molt.py` docstring: *"It does not import Molt, Ray, transformers, or CUDA, so its gradients can be checked on CPU."* — MEASURED. So the *objective* is CPU-runnable; the *model* is the cost, and the paper is silent on small-scale training cost.

## 2. The exact loss (default: token regression + MC-KL)

Notation (paper §3): `p = π_θ` current trainer, `q = π_sampler` the actual historical collection sampler, `R` the terminal reward, `a_u` the sampled action at prefix `s_u`, and

```
ℓ_u   = log p(a_u) − log q(a_u)                      (trainer-to-sampler log-ratio)
z_u   = log p(a_u) − mean_j log p(v_j),  v_j ~ q, M draws   (sampler-centred score)
h_u   = R − β · ℓ_u                                  (per-token return coefficient)
loss  = − mean_responses Σ_tokens  stopgrad(h_u) · z_u
```

Quoted verbatim from `README.md` "The default update" and `docs/algorithms.md`:

> `loss_token_mc = -mean_responses(sum_tokens(stopgrad(R-beta*ell) * (log(p_action) - mean_j(log(p(v_j))))))`

MEASURED. Sum over generated policy tokens, **mean over complete responses, without length normalization**. `stopgrad` means the coefficient `h_u` is detached; the gradient flows through **both** current log-probability expressions (the sampled action's `log p(a_u)` and the auxiliary mean `mean_j log p(v_j)`). Paper Step 9 / Eq. (3.26)–(3.27) gives the same thing; `klpo/loss.py::klpo_token_loss` implements it.

Two routes × four estimators = eight legal combinations (MEASURED, `docs/algorithms.md` table):

| Route | Feedback | MC-KL | TopK-KL | Binary KL | Full KL |
|---|---|---|---|---|---|
| **Token (default)** | per-token `R − βℓ_u` | `klpo_token_loss` (default) | `klpo_token_loss(kl_estimator="topk")` | `...("binary")` | `...("full")` |
| Sequence | one trajectory residual `D = R − β Σ(ℓ+k)` | `klpo_sequence_mc_loss` (M≥2) | `klpo_sequence_topk_loss` | `klpo_sequence_loss` | `klpo_sequence_full_loss` |

### 2.1 The four KL estimators (all MEASURED, `docs/algorithms.md`)

1. **MC-KL (default).** `k_MC = mean_j( log q(v_j) − log p(v_j) )`, `v_j ~ q` IID **with replacement**, independent of the rollout. Unbiased estimate of full local KL for any `M ≥ 1`; individual estimates may be negative and must **not** be clamped. Token route allows `M ≥ 1`; sequence route requires `M ≥ 2` for leave-one-out residuals. Duplicate token IDs are valid and required.
2. **TopK-KL.** Keep the sampler's `K` highest-probability tokens, aggregate the rest into one tail bucket: `k_K = Σ_head q_v log(q_v/p_v) + q_tail log(q_tail/p_tail)`. Default `K=128`. Head IDs and probabilities are stored from the *sampler*, never renormalised or reselected from the trainer; the sampled action need not be in the head. Tail floor `1e-6`.
3. **Binary KL.** Sampled action vs its complement only: `k_bin = q log(q/p) + (1−q) log((1−q)/(1−p))`. Needs only sampled-action logps. Explicitly *not* an exact critic-free population gradient.
4. **Full KL.** The exact sum over the whole vocabulary.

Sequence-regression MC-KL uses the leave-one-out construction `D_j = R − βΣ(ℓ + log q(v_j) − log p(v_j))`, `D_{−j} = mean_{l≠j} D_l`, and weights column `j`'s corrected score by `D_{−j}` — this removes the covariance bias you would get by reusing an MC estimate inside both residual and derivative.

## 3. What it drops, versus GRPO / PPO / DPO

**Caveat first, and it matters:** the paper **never names GRPO, PPO, or DPO** (`grep -c GRPO` = 0 across `KLPO.txt`, `README.md`, `docs/*.md`; "PPO" appears zero times; DPO only as a one-line citation for the Q⋆ relationship). So the comparison below is **not the paper's claim** — it is the structural comparison implied by the algorithm, tagged ESTIMATE / external RLHF knowledge. What the paper *does* compare itself to, by name, is **SKLPO, SPPO, GPO, BPO, FlashREINFORCE, AWR, REBEL** (Appendix J, §6, §H.2).

| Component | PPO | GRPO | DPO | KLPO (structural, ESTIMATE unless quoted) |
|---|---|---|---|---|
| Learned value/critic network | **yes** (same order as policy) | no | no | **no** — MEASURED: "No critic or auxiliary normalizer" (Fig. 3 caption) |
| Same-prompt response group (G rollouts) | not required | **required** (G per prompt) | no | **no** — MEASURED: "One complete response per prompt is sufficient" (README) |
| Frozen reference-policy forward pass | usually for KL | usually for KL | **yes** (ref model) | **no** — the *historical sampler logps are recorded at collection*; the sampler **is** the KL reference (§2 "The collection policy … is also the fixed KL reference") |
| Multiplicative importance ratio | **yes** | ratio in objective | no | **no** — MEASURED: "no multiplicative importance weights" (§H.1 Eq. H.2; KLPO contribution is `d·g`, IS is `ρ·d·g`) |
| Ratio clipping / trust region | **yes** | **yes** | no | **no** — MEASURED: "there is no policy-ratio clipping, binary probability clamp, trust gate, or dynamic outcome filter" (`docs/training.md` L121) |
| Reward/prompt normalizer model | no | group-mean baseline | no | **no** — MEASURED: dispenses with both value *and* normalizer (vs SKLPO's `c*`) |
| Batch/group reward centering | advantage norm | **group centering** | no | **no** (terminal return enters raw) |

The closest published relative the paper itself positions against is **FlashREINFORCE** (Hu et al., 2026), "critic-free single-rollout asynchronous training with token IS, batch reward centering, sequence admission, and within-trajectory averaging" (MEASURED, §6). KLPO's §H.2 Eq. (H.4) shows the delta: FlashREINFORCE puts `ρ = p/q` **multiplicatively** in front of each token score; KLPO puts its logarithm inside the regression residual and adds an additive sampler-centred correction.

## 4. Data shape (what a row is)

MEASURED, `docs/algorithms.md` "Shared contracts" + `klpo/_validation.py`:

- `log_probs`, `behavior_log_probs`, `action_mask`: `[B, T]`; `rewards`: `[B]`.
- **Each row must be a COMPLETE trajectory.** Action mask excludes prompt, padding, tool-output, external-observation tokens. Every row must contain at least one policy token (`lengths == 0` raises).
- `rewards` is a **single terminal scalar per row** (the verifier reward). No per-token reward, no critic, no baseline.
- Reward is **detached**; sampler logps are **detached and fixed**; the current-policy logps retain the autograd graph.
- MC-KL additionally needs `mc_log_probs`, `behavior_mc_log_probs`: `[B, T, M]` — the current trainer's logp *gathered at the stored sampler draw IDs*, and the stored sampler logps at those same IDs. M is **not** capped by vocabulary size; repeated IDs allowed.
- TopK/full need `[B, T, K]` (or `[B, T, V]`) conditionals aligned to **stored sampler head IDs**.
- Loss returns a **local response mean of a token sum**; for DDP/accumulation multiply by `B_local · dp_size / B_global` and do **not** re-average (`klpo/molt.py` does exactly this: `scaled_loss = loss * (log_probs.shape[0] * dp_size / count)`).
- Float32-or-higher log-softmax before gathering sampled tokens; Binary KL rejects an active logp of exactly 0.

For our town: a "verdict-labelled trajectory" is exactly `(prompt tokens, response tokens, one terminal reward from the verdict, behaviour logps)` — shape-compatible with the loss. The only non-trivial obligation is **capturing the behaviour log-probs at collection time**, which for a locally served open model is a real but ordinary engineering step.

## 5. Off-policy replay / asynchrony

MEASURED, paper §4 and `docs/algorithms.md`:

- Workers sample from `π_sampler(θ_{t−k})`; the learner trains `π_θt`; `k` is a per-response lag, not a fixed limit. A batch can mix several sampler versions.
- **Reuse preserves the stored sampler probabilities** and recomputes the trainer scores, the residual/coefficient, and the chosen correction at every update.
- "Keep the recorded sampler probabilities and version fixed during reuse." (§3.7 / algorithms.md)
- **Fresh-draw rule:** "Fresh auxiliary draws from the historical sampler preserve conditional unbiasedness after adaptive updates; fixed-record reuse is an empirical surrogate." (abstract). So after the trainer has adapted, reusing a fixed MC bank is a surrogate, not an unbiased gradient. `docs/training.md` L99–100: "Auxiliary MC records are used once, before any update can depend on them."
- **Current launcher restriction (MEASURED):** `force_sync_mode`, queue depth one, drained rollout batch; one actor GPU + seven rollout GPUs; one response per prompt and one optimizer update per complete batch. Native KLPO rejects partial rollouts, MTP speculative decoding, routing replay, context-compacted segments.
- Cost of the records, MEASURED as asymptotic claims (`docs/training.md` L93–97): **TopK-KL transfers O(T·K); Full transfers O(T·V)**; MC "materializes full sampler logprobs internally before reducing them to O(T·M) records on the engine host. It saves transport/replay storage, but is not yet a fused O(M) GPU sampler." Long-context Full/MC collection can be costly.

That last sentence is the single most important honesty point in the whole repo: **the default MC path does not save the forward-pass logit computation**, only the *stored/transported* record size.

## 6. Compute-saving techniques (mechanism, saving, hardware, CPU transfer, bridge, falsifier)

Because there are no measured benchmarks, "MEASURED saving" below means *a quoted asymptotic claim or a quoted absence of a component*, and every numeric speedup is my ESTIMATE with the arithmetic shown.

### T1. Critic-free — no value network
- **Mechanism.** Terminal return `R` replaces the sampler advantage `A`. The per-token coefficient `h_u = R − βℓ_u`; the sampler-conditioned mean is supplied by score centering, not by a critic. Paper Theorem 3.3: `∇L_tok = ∇L_TR = −E Σ (R−βℓ)·g̃`.
- **MEASURED saving (structural, quoted).** "No critic or auxiliary normalizer" (Fig. 3); "without a critic or reward group" (abstract). No performance number.
- **ESTIMATE.** A PPO critic is typically policy-sized; removing it removes one full forward+backward and its Adam moments. On a 1.7B model that is on the order of **half the training memory and a large fraction of per-step compute** (params 6.8 GB fp32 + grads 6.8 GB + moments 13.6 GB for a 1.7B critic ≈ 27 GB at fp32; a same-size policy carries the same again). This is the **largest single saving in the whole method** and it is architectural, not measured.
- **Hardware assumed.** None in the paper; launchers target 1 actor GPU + 7 rollout GPUs, 8-GPU Ray, FSDP2, vLLM, models DeepSeek-R1-Distill-Qwen-1.5B and Qwen2.5-Math-1.5B (MEASURED, `docs/training.md`).
- **CPU/tiny transfer.** Full. Dropping the critic is model-agnostic and *helps* small boxes the most, because a same-size critic is the difference between fitting and not fitting on 8–23 GB.
- **Oscillator/SNN/looped bridge (frank).** The saving is substrate-independent, so it transfers to an oscillator or byte-neuron model for free — and that is the whole honest answer. It does **not** get "supercharged": the oscillator idea buys nothing extra here because there was no critic to approximate. A byte-neuron SNN would also have to be *trained* without a critic, which KLPO allows, but the SNN's own gradient machinery (surrogate spike gradients, eligibility traces) is a separate problem KLPO does not touch.
- **Falsifier.** Train KLPO and PPO at equal tokens on the same small model; if PPO's critic-free variant (e.g. GRPO-style group baseline) matches KLPO's reward while KLPO's single-rollout variance is higher, the critic-free saving costs more in sample efficiency than it saves in FLOPs — measurable on CPU at 0.6B.

### T2. Single rollout per prompt — no same-prompt group
- **Mechanism.** "One complete response per prompt is sufficient" because the conditional score mean is supplied by independent **token** draws, not by sibling responses (Step 9). SKLPO's group-centering gives zero loss for a singleton; KLPO does not centre against a group.
- **MEASURED saving.** README "One complete response per prompt is sufficient"; §5 "No same-prompt response group." Asymptotic only.
- **ESTIMATE.** vs GRPO's usual `G=8` completions per prompt, this is up to an **8× reduction in generation tokens** (generation, not training FLOPs). If `G` is 4–16, the range is 4–16×.
- **Hardware assumed.** Same 8-GPU launcher; the claim is about *collection*, and the paper explicitly notes single-rollout collection still needs the local conditional information.
- **CPU/tiny transfer.** Full and valuable: generation on CPU is the slowest part, so 1 rollout instead of 8 is the difference between an hour and eight.
- **Oscillator/SNN/looped bridge.** Plausible and interesting: a spiking/oscillator model that produces one deterministic trajectory per prompt loses nothing here, whereas group-based methods need `G` stochastic rollouts and thus `G` spike-train samples. The looped-transformer angle is that a *looped* model already re-uses state across passes, so one "rollout" can be many internal iterations — but that is not a KLPO saving, it is a modelling choice.
- **Falsifier.** Measure reward-per-generated-token of KLPO (M=1 token route) against a group method at matched optimizer steps; if KLPO needs ≥G× more optimizer steps to reach the same reward, the single-rollout saving is cancelled by slower learning.

### T3. No reference-policy forward pass — the sampler is the reference
- **Mechanism.** `q = π_sampler` is the KL reference **and** the behaviour policy, and its logps were recorded at collection. The KL term `k_θ` is estimated from sampler records, so no frozen reference model is loaded or run.
- **MEASURED saving.** "The collection policy … is also the fixed KL reference. … no separate reference snapshot is needed." (§2). "no reference-policy pass" (`docs/algorithms.md`).
- **ESTIMATE.** DPO/PPO-KL typically run a frozen reference forward per scored token. Removing it removes ~**one forward pass of a second model** per token, i.e. ~1/3 of a naive three-pass (policy fwd + ref fwd + policy bwd) step, plus the reference model's weight memory.
- **Hardware assumed.** Same 8-GPU setup; needs a sampler that logs probabilities.
- **CPU/tiny transfer.** Full — and again biggest on small boxes, where a second copy of a 0.6B model is real RAM.
- **Oscillator/SNN/looped bridge.** Full transfer of the *structural* saving. The oscillator framing actually rhymes: the "reference" is the *recorded history* of the system's own phase trajectory, not a separate frozen copy. A digital-Kuramoto model could in principle store the collection-time oscillator phase/readout as `q`, and the trainer's current readout as `p` — exactly the two distributions the loss needs. Nothing about the loss forbids this.
- **Falsifier.** If recording sampler logps costs more (in storage or in a second forward at collection) than running a reference model would, the saving is negative. Measure the collection-time overhead per token on CPU.

### T4. No prompt/version normalizer predictor
- **Mechanism.** SKLPO fits `c*(x) = β log E_Y e^{R/β}` per prompt-and-version; KLPO profiles the **local** intercept instead (`c_θ(s) = β k_θ(s)`, Lemma 3.2) and profiles it away. So no auxiliary normalizer network, no per-prompt version bookkeeping across historical samplers.
- **MEASURED saving.** "KLPO removes prompt-normalizer estimation and same-prompt grouping from asynchronous replay" (conclusion). "an auxiliary prompt normalizer is not necessarily a critic; KLPO dispenses with both" (§5).
- **ESTIMATE.** Saves one auxiliary predictor (a head or small model) and its training loop; and saves the replay-time bookkeeping that Appendix A.6 / §4.1 show is required for SKLPO when several sampler versions share a batch.
- **Hardware assumed.** Same launcher; the predictor is small, so this is a *systems complexity* saving more than a FLOP saving.
- **CPU/tiny transfer.** Full, and disproportionately valuable on tiny hardware where an extra predictor + its optimizer state can double the resident model count.
- **Oscillator/SNN/looped bridge.** Mild. A looped/recurrent model's hidden state is *already* a per-prompt summary; one could imagine reading `c*` off it, but that is a learned normalizer by another name and KLPO's point is to avoid it. Frankly, this technique and the oscillator idea are orthogonal.
- **Falsifier.** Compare KLPO vs an SKLPO-style learned-normalizer variant at equal parameter budget; if the normalizer is cheap and speeds convergence enough to win on reward-per-FLOP, the saving is nominal.

### T5. Async off-policy replay without a collection barrier
- **Mechanism.** Workers return completed trajectories with their sampler version; the learner scores them without waiting for a second response. Recompute only trainer-side quantities. (§4.3, Fig. 3.)
- **MEASURED saving.** "trains concurrently from this queue without a collection barrier" (§4.3). No throughput number.
- **ESTIMATE.** Eliminating the barrier raises rollout-GPU utilisation; the paper's own launcher nevertheless runs *synchronous* (`force_sync_mode`, queue depth 1), so the advertised asynchrony is **not exercised in the provided code** (MEASURED, `docs/training.md`).
- **Hardware assumed.** 7 rollout GPUs + 1 actor GPU, Ray, vLLM.
- **CPU/tiny transfer.** Partial. On a CPU box there is no separate rollout GPU to keep busy, but the *algorithmic* property — that a stale trajectory is still usable because there is no IS ratio to blow up — is exactly what a town of asynchronous CPU kids needs.
- **Oscillator/SNN/looped bridge.** Good fit conceptually: a looped/recurrent agent naturally produces trajectories over time, and KLPO's version-conditioned update tolerates the staleness. A digital-Kuramoto clock could even use its own phase as the "sampler version" tag. But the honest caveat stands: this is a *compatibility* argument, not a measured speedup.
- **Falsifier.** Run the town's async loop with and without the barrier on the same CPU box; if wall-clock per reward is not better, the barrier was not the bottleneck.

### T6. MC-KL with M ≥ 1 token draws instead of extra response rollouts
- **Mechanism.** `k_MC = mean_j (log q(v_j) − log p(v_j))`, `M` auxiliary **token** draws at visited prefixes, no continuations, no extra rollouts. Token route works at `M=1`.
- **MEASURED saving.** "The extra token draws need no response continuations" (§3.9); "MC tokens are sampled independently of the rollout action and continuation; they are extra token draws, not extra response rollouts" (algorithms.md). Asymptotic: MC records `O(T·M)` vs the group's `G` full sequences of length `T`.
- **ESTIMATE.** vs a group method, generation drops from `G·T` response tokens to `T` response tokens + `T·M` cheap single-token logp evaluations. `M=128` sounds large but each is **one gather**, not a rollout. At `M=1` the token route is the cheapest possible score correction.
- **Hardware assumed.** Same; the Molt capture "materializes full sampler logprobs internally" before reducing, so **not yet fused**.
- **CPU/tiny transfer.** Good *if* you can evaluate `log p(v_j)` cheaply. On CPU you still need one forward pass through the model per prefix to get logits; the `M` gathers are then trivial. So MC-KL's CPU win is in *storage and transport*, exactly as the doc says, not in the forward.
- **Oscillator/SNN/looped bridge.** This is the technique most naturally "supercharged" by a stochastic oscillator readout: sampling `M` extra tokens from the sampler is *literally* sampling `M` phase readouts from the collection-time oscillator bank, and the log-ratio is a phase-log-ratio. A byte-neuron SNN whose readout is a categorical over bit-patterns can implement it. **But**: the estimator's unbiasedness proof needs `v_j ~ q` to be an exact IID categorical draw, so the spike readout must be a true sampler, and "may be negative" variance carries over.
- **Falsifier.** On a tiny enumerated-support model, check that the MC gradient equals the full-KL gradient in expectation for the *oscillator readout* exactly as `tests/test_mc.py` does for a softmax. If the readout is not a normalised categorical, the identity fails.

### T7. TopK-KL — O(T·K) records instead of O(T·V)
- **Mechanism.** Store the sampler's top-`K` head + one aggregated tail; gather trainer logps at those same IDs. Default `K=128`.
- **MEASURED saving (asymptotic claim).** "TopK-KL transfers O(TK) conditional records. Full transfers O(TV)." (`docs/training.md` L93).
- **ESTIMATE.** For `V≈150k` and `K=128`, the record size is ~**1,000× smaller** (150000/128 ≈ 1172). Storage/transport only.
- **Hardware assumed.** Same; long-context Full is called out as costly.
- **CPU/tiny transfer.** Excellent. On an 8 GB box, the `[B,T,V]` full-conditional tensor is the memory bomb: `8·512·150000·4 B ≈ 2.46 GB` for one float32 batch (ESTIMATE). `[B,T,128]` is ~2 MB. This is the single most transferable *memory* trick for the town.
- **Oscillator/SNN/looped bridge.** Weak. If the readout is a byte-neuron bit-pattern space, the "vocabulary" is small (256), so `K` and `V` nearly coincide and TopK-KL's ratio saving evaporates. Frankly: this trick is for large-tokenizer transformers, not for byte-level substrates.
- **Falsifier.** Measure record bytes and peak RAM for Full vs TopK on the town's largest `V`; if `K ≈ V` (byte-level), the trick does nothing.

### T8. Binary KL — only sampled-action records, O(T)
- **Mechanism.** `k_bin` needs only `q_action`, `p_action` and their complements; no head, no tail, no full vocabulary.
- **MEASURED saving.** "Binary KL needs only rollout-action records" (§3.9); "No head or full-vocabulary records are needed" (`docs/training.md`).
- **ESTIMATE.** `O(T)` records — the cheapest record format, ~`V/K` smaller than TopK and ~`V` smaller than Full. Cost: it is an **approximation** and "does not inherit the exact full-KL population identity in general" (MEASURED).
- **Hardware assumed.** Same.
- **CPU/tiny transfer.** Best of all for RAM: a CPU box can afford to store binary records for a whole dataset. Accuracy cost is real and unmeasured.
- **Oscillator/SNN/looped bridge.** Strong for byte-neurons: the "sampled action vs its complement" partition is exactly a single-bit decision, and a bit-flip impulse readout gives `q_action` for free. This is arguably the estimator that fits a bit-wise substrate best.
- **Falsifier.** Train token-Binary vs token-MC at equal budget on the town's data; if Binary's reward-per-FLOP is worse than MC's, the O(T) saving is paid back in sample efficiency.

### T9. Step 10 predicted-KL optimizer scaling (optional)
- **Mechanism.** Compute a **Jacobian-vector product** `J_logits · D` on fixed probe histories and a quadratic KL estimate `q(D)`; scale the full AdamW displacement by `α = min(α_max, sqrt(δ/q(D)))`. Replaces a realised-KL / trust-region evaluation with one JVP.
- **MEASURED saving.** None quoted. **Disabled by default** in the Molt launcher (MEASURED, `docs/training.md` L224).
- **ESTIMATE.** A JVP is ~one forward pass; cheaper than evaluating realised KL over full vocab or over rollouts. But it is optional and unwired.
- **Hardware assumed.** Same; "not wired into the distributed Molt optimizer".
- **CPU/tiny transfer.** Plausible and cheap on CPU (`torch.func.jvp`), and a small trust region is *useful* on tiny hardware where a bad step is expensive. But it is extra machinery for a method that otherwise prides itself on having no trust gate.
- **Oscillator/SNN/looped bridge.** Weak-to-moderate: a JVP through an oscillator network is not obviously cheap (event-driven SNNs do not have a dense Jacobian in the usual sense). The digital-Kuramoto framing could treat the step-size as a coupling-strength scale, but that is a re-description, not a saving.
- **Falsifier.** Measure realised-KL violations with and without the budget on a tiny model; if the quadratic prediction is a poor proxy (the doc warns it "is not a hard bound"), the JVP is spent for nothing.

### T10. No ratio clipping, no trust gate, no admission mask
- **Mechanism.** Removing the IS multiplier means there is no outlying ratio to clip; the residual is additive. `docs/training.md`: "there is no policy-ratio clipping, binary probability clamp, trust gate, or dynamic outcome filter in the KLPO objective."
- **MEASURED saving.** That sentence (quoted). No number.
- **ESTIMATE.** Removes PPO's clip machinery and the second (old-policy) scoring pass; small compute, large code-path simplification.
- **Hardware assumed.** Same.
- **CPU/tiny transfer.** Full and *safe*: fewer moving parts means fewer ways a small-box run silently breaks. But the doc also warns that removing IS "fixes neither" sampler-record error nor coverage loss (§4.2) — the robustness is conditional on honest records.
- **Oscillator/SNN/looped bridge.** Neutral.
- **Falsifier.** Compare KLPO against a clipped variant on stale trajectories; if KLPO destabilises where clipping would not, the saving is bought with robustness.

## 7. Can the loss alone run on CPU / an 8 GB box for a 0.6B–1.7B model?

Short answer: **the loss, yes; the training step, only at the small end.**

- **Loss code:** pure `torch>=2.2`, no Molt/Ray/transformers/CUDA import in `klpo/loss.py` (MEASURED, `klpo/molt.py` docstring and `pyproject.toml`). CPU-runnable by construction; the toy example runs "on CPU without a model or dataset download" (README) and `torch.set_num_threads(1)` in `examples/train_toy.py` (MEASURED).
- **Dependencies (MEASURED):** `torch>=2.2`; optional `pytest>=8`; optional native backend = the `labs-molt` fork branch `feat/klpo-all-kl`, **pinned to revision `e24e22faaf0d3cf3ad56dec47215117d95914be2`**; launcher scaffolding adapted from **FlashREINFORCE** (Apache-2.0). Licence: **Apache-2.0** (code); the labs-molt backend retains its own NVIDIA/OpenRLHF notices.
- **Memory, ESTIMATE (arithmetic, no doc claim).** AdamW full fine-tuning needs roughly `4× params` in fp32 (weights + grads + 2 moments) plus activations and the logit tensor:
  - 0.6B: weights 2.4 GB → AdamW state ~9.6 GB + activations → **does not fit 8 GB**, fits 23 GB ARM with care.
  - 1.7B: weights 6.8 GB → AdamW ~27 GB → **fits neither** at fp32; needs 8-bit optimizer/LoRA and even then is marginal on 23 GB.
  - **Forward-only scoring** (no grads, no optimizer) fits easily: 1.7B fp16 ≈ 3.4 GB, int8 ≈ 1.7 GB → fits 8 GB.
  - **Full-vocabulary logits** are the hidden bomb: `[B,T,V]` at `B=8, T=512, V=150k` ≈ **2.46 GB fp32** for one batch (ESTIMATE). TopK/MC avoid materialising it in *storage*, but the doc says the current capture still materialises it internally.
- **So the realistic town recipe:** use KLPO as a **loss/estimator** over locally-captured behaviour logps from a small (≤0.6B) CPU-served model, with **forward-only scoring** on the 8 GB box and Adam updates only on the 23 GB ARM box, or with a frozen base + tiny trained head. `M=1` token route, Binary or TopK records, are the RAM-cheapest configurations.
- **Verdict-labelled trajectories:** fully compatible. `(tokens, terminal reward, behaviour logps, mask)` is the exact contract; our `datasets/trajectories` + `kid-sft` need a capture step that logs `log q(a_u)` at collection. This is the **only** new obligation.

## 8. Validation: what is VALIDATED vs only implemented

| Thing | Status |
|---|---|
| Eight route × estimator combinations | **Implemented + CPU-tested** (MEASURED: tests cover "all eight route/estimator combinations") |
| Independent MC gradient expectation == full KL | **Validated on CPU** by finite enumeration (`tests/test_mc.py`, `product(range(2), repeat=steps*m)`, asserts `atol=1e-12`) |
| Leave-one-out U-statistic, naive plug-in bias | **Validated on CPU** (test asserts naive grad differs by `>1e-4`) |
| M=1 token updates, duplicates, negative MC estimates | **Validated on CPU** |
| TopK tail corrections, masked/extreme probabilities | **Validated on CPU** |
| Population equivalence on an enumerated variable-length tree | **Validated on CPU** (`tests/test_population.py`) |
| Microbatch / DP gradient normalisation | **Validated on CPU** |
| Native Molt backend contract | **Optional test only**, needs `MOLT_SOURCE_PATH`; read-only `scripts/check_molt.py` |
| **GPU training** | **NOT validated** (MEASURED, README L97) |
| **Paper-scale benchmark reproduction** | **NOT validated** (MEASURED) |
| **CUDA / Ray / FSDP / vLLM / multi-node run** | **NOT validated** (MEASURED, `docs/training.md` L250) |
| **Any measured reward / throughput / memory number** | **Does not exist in this release** |
| Hyperparameters `β=0.1`, AdamW lr=1e-6, wd=.1, grad-norm 1, cosine, warmup .03 | "starting values, not tuned benchmark settings" (MEASURED) |

## 9. Honest assessment of the owner's oscillator / byte-neuron-SNN / looped bridge

**The hypothesis, stated so it can fail.** *"The oscillator/SNN/looped layer can supercharge each compute-saving trick in this paper."*

**Frank answer: the paper's savings are substrate-independent, so the bridge cannot supercharge them; at most it can multiply them by making the one remaining cost — the forward pass — cheaper, and that is a property of the substrate, not of KLPO.**

Every saving in §6 is a statement about *what the algorithm does not need to compute*: no critic network (T1), no group rollouts (T2), no reference model (T3), no normalizer predictor (T4), no barrier (T5), smaller records (T6–T8), no trust gate (T10). None of those depend on whether the policy is a transformer, a spiking network, or a Kuramoto bank. So KLPO transfers to the owner's substrate **cleanly and for free** — but it transfers *nothing extra*. The one place the substrate could genuinely help is T2/T6: if a byte-neuron SNN's forward is event-driven and sparse, then the `T` forward passes KLPO still needs become cheap, and the "one rollout, M token draws" pattern is a natural fit for a stochastic spike readout.

**Where the bridge is real.** (i) The loss needs only two normalised distributions `p` and `q` and their log-ratios; it never assumes a softmax over text tokens. A spike-pattern readout that *is* a normalised categorical satisfies the contract, and `tests/test_mc.py`'s enumeration test is exactly the harness to prove it on a spiking model. (ii) The MC-KL estimator is a Monte-Carlo phase average; a digital-Kuramoto bank whose readout is sampled `M` times at collection gives `q(v_j)` directly, and the log-ratio `log q(v_j) − log p(v_j)` is a *phase-timing* difference between recorded and current oscillator state. (iii) A looped transformer maps naturally onto the **sequence** route, where the residual `D = R − βΣ(ℓ+k)` is already a path sum — loop iterations are extra terms in that sum.

**Where the bridge is not real, and must not be claimed.** (i) The default MC capture "materializes full sampler logprobs internally" — if the spike readout also needs a dense logsumexp over `V` patterns to get `log p(v)`, the substrate saving evaporates and TopK/Binary become the only viable estimators. (ii) KLPO's unbiasedness proofs assume `v_j ~ q` is an **exact IID categorical**; a deterministic oscillator bank that only *looks* stochastic will silently break the estimator (and the paper warns MC estimates can be negative and must not be clamped — a broken readout will produce exactly that). (iii) The paper gives **no** leverage against the dominant cost, which is the model forward; only a genuinely cheaper forward pass helps, and that is the substrate's burden to prove.

**Falsifier for the whole bridge.** Implement the KLPO token+MC loss on a tiny oscillator/spiking readout with an enumerated support; run the repo's own population-equivalence test (`tests/test_mc.py` pattern) and require the MC gradient to equal the full-KL gradient in expectation to `1e-12`. If the spiking readout is a normalised categorical, it passes — proving the bridge is *sound* but adding no speed. If it fails, the readout is not a sampler and the bridge is *false*. Either way, the paper's compute savings are unchanged; only the per-forward cost moves. That is the honest boundary.

## 10. Hypothesis seeds runnable on the town's CPUs (3–5)

All five are CPU-only, need no paid API, and use only the repo's own loss plus our trajectory store.

1. **MC-gradient equivalence holds on our capture path.**
   *Claim:* on a tiny enumerated-support policy over our verdict-labelled trajectories, `klpo_token_loss(kl_estimator="mc", M=1)` and `klpo_sequence_mc_loss(M=2)` match the full-KL gradient in expectation to `1e-12`, as the repo's own tests assert.
   *Falsifier:* measured gradient mismatch beyond float64 tolerance, or a NaN from our real capture.
   *CPU experiment:* port `tests/test_mc.py`'s enumeration to a 4-token categorical built from one of our trajectories; run on the 23 GB ARM box. *est_cost:* minutes.
2. **Behaviour log-prob capture is faithful for a CPU-served 0.6B model.**
   *Claim:* the `log q(a_u)` logged at collection by a locally served 0.6B model equals a re-scored forward pass at the same weights to float32 tolerance, so the KLPO residual is not systematically wrong.
   *Falsifier:* mismatch large enough to flip the sign of `h = R − βℓ` on a majority of tokens.
   *CPU experiment:* serve a 0.6B model (llama.cpp or transformers CPU), log logps for 200 short responses, re-score, compare. *est_cost:* hours.
3. **The 8 GB box can score but not train.**
   *Claim:* forward-only KLPO scoring of a 0.6B model fits in 8 GB; a full AdamW update does not, and the breakpoint is the optimizer state (~4× params).
   *Falsifier:* an AdamW step completes inside 8 GB (claim false), or forward-only scoring OOMs (recipe wrong).
   *CPU experiment:* instrument peak RSS for forward-only vs `loss.backward(); optimizer.step()` on 0.6B, fp32 and int8. *est_cost:* hours.
4. **The estimators agree at matched policy, so divergence is a plumbing bug.**
   *Claim:* at `π_θ = π_sampler` on real captured trajectories, all four estimators report conditional KL ≈ 0 and gradient ≈ 0 (within MC noise for MC-KL), giving a cheap canary for a broken capture.
   *Falsifier:* a non-MC estimator reports non-negligible KL at an exact match, or the four disagree beyond noise on matched weights.
   *CPU experiment:* evaluate `klpo_token_loss` in all four modes with `log_probs == behavior_log_probs` on 500 stored trajectories. *est_cost:* minutes.
5. **The byte-neuron/oscillator readout carries KLPO but does not cheapen the forward.**
   *Claim:* a normalised spike-pattern readout passes the MC population-equivalence test, and its forward cost per token is *not* lower than a dense small-transformer forward at matched parameter count, so the "supercharge" is not from KLPO.
   *Falsifier:* the readout fails equivalence (bridge false), or it *does* cut forward cost at equal reward (bridge genuinely helps).
   *CPU experiment:* tiny spiking readout + the enumeration test, plus a wall-clock forward comparison against a param-matched MLP. *est_cost:* hours.

## 11. Open questions

1. Where does the reward signal's *credit assignment* go on a failed trajectory? The paper itself notes "response-level feedback from a terminal failure also leaves the responsible intermediate tool action unidentified" (§H.4). For our verdict labels this is the central practical gap.
2. Is the default MC path's internal full-vocabulary materialisation fixable on CPU (fused O(M) selected-ID scoring), or must the town use Binary/TopK to avoid the `[B,T,V]` tensor?
3. What is the actual variance of `M=1` token-regression vs `M=128` on real data? The paper proves unbiasedness but "finite-M noise does not guarantee a stable or monotone sample update" — unmeasured.
4. Does the sequence route's deterministic-transition assumption survive tool calls? The doc says use the **token** route for stochastic tools; our kid pipelines with tools may therefore be forced to the token route.
5. Can a spiking/oscillator readout expose an *exact* IID categorical cheaply? If not, MC-KL is unavailable to the substrate and only Binary/TopK remain.
6. Licence/attribution: our digest and any port must carry the Apache-2.0 notice and the FlashREINFORCE + labs-molt notices from `NOTICE`.

## 12. Source map (for the next reader)

- Loss: `klpo/loss.py` — `klpo_token_loss` (MC default), `klpo_sequence_mc_loss` (leave-one-out), `klpo_sequence_topk_loss`, `klpo_sequence_loss` (binary), `klpo_sequence_full_loss`.
- Contracts: `klpo/_validation.py` — `prepare`, `conditionals`, `mc_records`, `finite_result`.
- Optional Step 10: `klpo/budget.py` — `predicted_kl`, `kl_budget_scale`.
- Native adapter: `klpo/molt.py` — `KLPOLoss`, `loss_agg_mode = "seq-mean-token-sum"`.
- Launcher: `scripts/train_molt.py` (adapted from FlashREINFORCE), `scripts/check_molt.py`.
- Theory: `KLPO.pdf` §3 (derivation), §4 (replay), §5 (vs SKLPO), §6 (related work), Appendix H.1–H.2 (vs FlashREINFORCE), Appendix J (SPPO/GPO/BPO/AWR).
- Toy: `examples/train_toy.py` (CPU, 4-token vocabulary, `--mc-samples 128`, `--reuse`, `--publish-every`, optional `--kl-budget`).

## CRITIQUE

**Critic:** adversarial reader for the local-maxxing town (goal:g14). **Read on:** 2026-09-21.
**What I re-opened, myself:** the clone at `/tmp/klpo` (and `/tmp/klpo-digest/KLPO`), `KLPO.pdf` (56 pages confirmed by counting `=== PAGE n ===` markers in the extracted `KLPO.txt`), `README.md`, `docs/algorithms.md`, `docs/training.md`, `docs/website.md`, `klpo/loss.py`, `klpo/molt.py`, `examples/train_toy.py`, and `tests/*.py`. **No `torch` is installed on this box either**, so — exactly like the read stage — I could not execute the suite; every "validated on CPU" below is the repo's own assertion, not a run I witnessed.

### Spot-checks (5 quoted numbers/claims, re-derived against the source)

1. **README L97 verbatim** — confirmed word-for-word: "This release provides the theory, loss implementation, CPU verification, and native training integration. **GPU training and paper-scale benchmark reproduction have not been validated.**" The digest's central honesty point is real.
2. **`docs/training.md` L118–119 and L250–251** — confirmed: "The local validation is CPU-based; CUDA/vLLM training and multi-GPU performance have not been run on this machine." and "This does not validate a CUDA, Ray, FSDP, vLLM, or multi-node training run. No paper-scale result is claimed." The "no measured number exists" conclusion stands.
3. **Cost asymptotics, `docs/training.md` L93–94** — confirmed: "TopK-KL transfers O(TK) conditional records. Full transfers O(TV). The current MC capture also materializes full sampler logprobs internally before reducing them to O(TM) records on the engine host." The digest's most important caveat (MC saves transport, not the forward) is exactly what the doc says.
4. **`tests/test_mc.py`** — confirmed `product(range(2), repeat=steps * m)` at L34 and `torch.testing.assert_close(actual_grad, exact_grad, atol=1e-12, rtol=1e-11)` at L50. Note the tolerance is asserted in **float64** (`dtype` in the test file), which the digest does not mention and which matters for its own falsifier (see errors).
5. **Appendix H.2 / Eq. (H.4)** — confirmed: FlashREINFORCE's gradient carries `ρ = π_θ/ν` as a *multiplicative* token IS weight; KLPO's log-ratio sits in the regression residual. The "no multiplicative importance weight" quote is real (KLPO.txt L37, L669, L2659).
6. **56 pages** — confirmed (56 `PAGE` markers). The digest's metadata table is accurate.

**Verdict on the digest's factual accuracy: high.** I found no fabricated quote and no inverted claim. It is one of the more disciplined digests in this tree.

### Errors found (all minor)

- **The digest's own grep is misreported.** It states "'PPO' appears zero times" across `KLPO.txt, README.md, docs/*.md`. `docs/training.md` L100 contains a standalone "PPO" ("never PPO's old-policy log-probs"). The *substantive* claim — that the **paper** never names PPO/GRPO (only SPPO) — holds under a word-boundary grep (`\bPPO\b` = 0 in `KLPO.txt`; GRPO = 0; DPO = 1, the Rafailov citation). So the point survives; the reported measurement does not.
- **"The closest published relative the paper itself positions against is FlashREINFORCE"** (§3) is the digest's editorial call, not a paper claim. The paper positions against SKLPO, SPPO, GPO, BPO, AWR, REBEL, *and* FlashREINFORCE. Defensible, but flagged as interpretation.
- **T3's "~1/3 of a naive three-pass step"** is loose. A policy fwd + ref fwd + policy bwd step puts the ref forward nearer **1/4** of compute (the backward is ~2× a forward). The direction is right; the constant is soft.
- **§9's falsifier tolerance is copied from a float64 test.** Demanding `1e-12` from a *spiking/oscillator readout* (which will run in float32) is not a fair bar; the paper's own identity is proven in float64. The digest should state the dtype or the test will look failed for the wrong reason.

### Unsupported / overstated in the digest

- Nothing material is fabricated. The one real epistemic gap: **every "Validated on CPU" tag traces to the repo's own test suite, which the reader did not run** (no `torch`). The digest is honest that it "read, not executed", but its §8 table still reads as independent confirmation. It is not — it is the source's self-report.
- The digest **never assesses the paper's theory**, which is the paper's actual content. The PMD/mirror-descent derivation, the Bellman-telescoping sequence route, and the claim that "removing prompt value changes the population loss only by a parameter-independent constant" are taken as given. For a theory-only release, that is the whole object of study and it went unexamined.

### Missing angles

1. **Peer-review status.** No venue, no DOI; a single-commit shallow clone; the cited relatives (FlashREINFORCE 2026, BPO arXiv 2609.15987, Score Centering 2609.20807) are themselves fresh preprints. The digest treats the claims as a settled baseline. For a town deciding what to build on, "unrefereed" belongs in the header, not implicit.
2. **The reward bottleneck is under-weighted.** The town's trajectories are *verdict-labelled*: KLPO needs one terminal scalar per complete trajectory. The paper itself admits terminal failure "leaves the responsible intermediate tool action unidentified" (§H.4). That is not an "open question" — for agentic verdict data it is a possible blocker, and it is orthogonal to every compute trick.
3. **Capture subtlety unstated.** The recorded `log q(a_u)` must be the *raw* conditional log-probability **before** temperature/top-p truncation, or the sampler/trainer contract (and the KL reference) is wrong. The digest names the capture obligation but not this failure mode.
4. **Finite-M stability.** The paper warns MC estimates may be negative and must not be clamped; the digest repeats this but does not treat the practical `M=1` variance as a risk to the town's small-batch CPU runs.
5. **Memory accounting omits the record tensors themselves.** `[B,T,M]` for `behavior_mc_log_probs` + `mc_log_probs` at the default `M=128` is small (~4 MB at B=8,T=512) but is never counted; the digest's §7 is otherwise careful arithmetic.

### Strongest and weakest hypothesis seed (knowledge-per-token, CPU)

- **Strongest — seed #1 (MC-gradient equivalence on our own capture path).** Minutes of CPU, exercises the repo's own exact-enumeration harness on *our* verdict-labelled trajectories, and is the single test that decides whether the loss is even applicable to the town's data. It is foundational, cheap, and falsifiable (`1e-12` float64 mismatch). Seed #5 is the more strategically relevant one (it is the only seed aimed at the owner's bridge) and should run next, but it costs hours and presupposes a substrate; #1 is the highest knowledge-per-token.
- **Weakest — seed #3 ("the 8 GB box can score but not train").** The answer is essentially arithmetic already known (`4× params` for fp32 AdamW; 0.6B ≈ 9.6 GB > 8 GB). It confirms rather than discovers, and its "falsifier" is very unlikely to fire. Seed #4 ("estimators agree at matched policy") is a close second: it largely restates what `tests/test_combinations.py` already checks, so its novelty is low.

### Bridge verdict — oscillator / byte-neuron-SNN / looped layer

**Speculative, not supported — and not contradicted.** Every saving in this paper is a statement about *what the algorithm declines to compute*: no critic (T1), no same-prompt group (T2), no frozen reference (T3), no normalizer (T4), no collection barrier (T5), smaller records (T6–T8), no trust gate (T10). None of those depends on the policy substrate, so an oscillator/SNN/looped model inherits them unchanged — but inherits **nothing extra**. The digest's own §9 reaches this and I agree: the bridge cannot "supercharge" KLPO; it can only make the *one cost KLPO does not touch* — the forward pass — cheaper, and that is a property of the substrate, provable independently of this paper. There is a concrete technical obstacle on the MC path: unbiasedness requires `v_j ~ q` to be an **exact IID categorical**, and the current capture "materializes full sampler logprobs internally" — a deterministic bit-flip or oscillator readout that only *looks* stochastic, or that needs a dense logsumexp over bit-patterns to produce `log p(v)`, silently breaks the estimator (and the paper warns MC estimates can go negative and must not be clamped — the exact symptom a broken readout would produce). The **looped** angle is the only one with a structural rhyme: loop iterations map onto the sequence route's path-sum residual. Net: the honest statement is *"KLPO is substrate-agnostic and therefore transfers; the substrate may reduce the forward cost, but KLPO gives it no leverage to do so."* Claiming a supercharge is hype; claiming an incompatibility is over-correction.

**Confidence in this critique: 0.85** — high on the textual spot-checks (I re-read the source), lower on the theory assessment (not independently derived) and on the bridge (argued, not measured).
