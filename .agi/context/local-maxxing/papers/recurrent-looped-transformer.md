# "Recurrent Looped Transformer" (Zhang; README adds Feng, Qin) — RLT

Source key: `recurrent-looped-transformer`. Owner 2026-09-13: "Add this to our local-maxxing goal research treasury" — hint: depth recurrence, more compute per token from fewer parameters, the town's intended architecture. **Read the first Relevance line before hanging anything on that hint: RLT is temporal recurrence (state across tokens), not depth recurrence (loops per token).**

## Provenance

Fetched 2026-09-16 (UTC), `curl -sL -A 'Mozilla/5.0'`:

| what | URL | HTTP | bytes |
|---|---|---|---|
| abs page | https://www.alphaxiv.org/abs/2609.recurrent-looped-transformer | 200 | 273,714 (HTML; no publish date string found by grep) |
| PDF | https://www.alphaxiv.org/abs/2609.recurrent-looped-transformer.pdf | 200 | 613,049 — `pdfinfo`: 16 pages, Title "Recurrent Looped Transformer", CreationDate Sat Sep 12 17:20:06 2026 EDT; `pdftotext -layout` → 771 lines |
| project README | https://raw.githubusercontent.com/yifanzhang-pro/recurrent-looped-tranformer/HEAD/README.md (`master` also 200; `main` 404) | 200 | 11,186 |

Paper front matter: single author "Yifan Zhang", dated "September 12, 2026". README: authors "Yifan Zhang, Jichen Feng, Shihan Qin", "Report: September 12, 2026 · Updated: September 15, 2026", Apache-2.0. Project page named in the abstract: `https://github.com/yifanzhang-pro/recurrent-looped-tranformer` (sic, "tranformer").

**The PDF contains no measurements.** Its own words (PDF p.2): "The report develops these mechanisms; it does not report measured efficiency or scaling results." Every accuracy number below comes from the README's "Depth-eight experiments" section (snapshot "September 15, 2026 ... 16:11:47–16:12:10 UTC"), where "Of 48 runs, 21 had reached the planned 2,000 optimizer steps; 27 were unfinished."

## Summary (measured lines)

1. **Mechanism (PDF §2.3, eqs 2.4–2.6).** A causal encoder E_θ builds per-token features e_t and an encoder-derived global KV memory M_≤t; a decoder D_φ takes `u_t = Merge(e_t, s_{t-1})` and emits the complete state `H_t = (s_t, C_t^D)` — the final hidden vector s_t plus a per-layer sliding-window-attention (SWA) KV cache. The same transition runs over every prompt and response token; nothing resets at the prompt/response boundary (Prop. 3.1, "Invariance to the serving split").
2. **Depth arithmetic (PDF §1, §3.3, Fig. 2).** Per-token block count is fixed at L_E + L_D ("For a 48-layer encoder and 48-layer decoder ... 96 logical block evaluations per token"); the state path after t tokens "traverses tL_D decoder blocks" — "48t" in the figure. This is the paper's "infinite depth": temporal, not per-token. Explicit caveat: "structural depth alone is not a reasoning guarantee."
3. **Gating / state feedback (PDF §2.5, eqs 2.9–2.11).** `r = RMSNorm(s_{t-1}); g = σ(W_g [e_t; r] + b_g); u_t = e_t + α · g ⊙ W_s r`, with `W_g ∈ R^{d×2d}, W_s ∈ R^{d×d}` and "α controls the feedback scale" — i.e. 3d² extra parameters, one d-vector of carried state. README experiments use "feedback scale 0.1". "Scalar gating or a low-rank W_s reduces overhead."
4. **Parameter tying (PDF §2.6).** Reference tied config sets L_E = L_D = L and shares Q/K/V/O and FFN between encoder self-attention and decoder SWA at each layer — "two logical passes through one backbone"; "Parameter tying reduces stored weights but does not eliminate the second logical pass or either cache role." The README experiments are **untied** ("The experiments below use untied eight-layer layouts").
5. **KV / bytes per token (PDF eq 3.3).** Inference cache ≈ `O((L_E + G) t d_KV + L_D min(t, W−1) d^D_KV + d)`: full-context KV for every encoder layer plus G memory groups, a bounded W−1 window per decoder layer, plus one d-vector. Per-token work "L_E + L_D blocks, plus merge and memory projection"; prefill (eq 3.2) is `O((L_E+L_D)(T d² + T² d) + G T d² + L_D T min(W,T) d)` but "There is a sequential decoder path through T transitions" — "no reduced-prefill speedup is claimed."
6. **Depth-eight results (README table, shared checkpoints, val. accuracy %).** All models width 512, FFN 1,365, 4 heads, batch 512; RLT: SWA window 8, G=1, α=0.1, TBPTT 128; "RLT models have 26.10–28.73M parameters; Transformer 8 has 25.31M." Parity @ step 500 (n=3 seeds): RLT 6+2 **99.44 ± 0.98** vs Transformer 8 **48.48 ± 0.53**; RLT 8+0 48.70 ± 2.60. Mod-5 flat @ 2,000 steps, seed 42: RLT 7+1 **95.44**, RLT 8+0 **90.89**, Transformer 8 **20.57**. Mod-5 brackets @ 2,000: 78.26 / 75.52 / 79.56. "RLT 8+0 has no decoder blocks and still applies the recurrent merge."
7. **Community length-generalization (README, ~79K params, 3 seeds, train length 32 ops).** Parity at 128 ops (4×): RLT 60.8% vs Transformer ≈48% (chance 50%); five-state transitions at 128 ops: RLT 20.7% vs Transformer ≈21% (chance 20%). "Parameter and data budgets were matched; FLOPs were not."
8. **What is NOT shown.** README: "The comparisons change feedback, attention structure, parameter count and compute together; matched RLT w/o feedback runs will isolate hidden-state feedback." and "Hardware throughput and RL performance remain to be measured." The 4+4 no-feedback control "has no results in the tables below."

## Numbers

- per-token blocks = L_E + L_D = 96 for 48+48 (PDF §1, Fig. 2)
- state-path depth after t tokens = t·L_D = 48t blocks for L_D=48 (PDF §3.3, Fig. 2)
- merge params = W_g d×2d + W_s d×d = 3d² (PDF eqs 2.10–2.11); at d=512 → 786,432 (arithmetic from the stated shapes)
- carried recurrent state = one d-vector, "the O(d) term is the current recurrent output" (PDF eq 3.3)
- decoder SWA cache per layer ≤ W−1 = 7 positions at W=8 (PDF §2.1; README "SWA window 8")
- feedback scale α = 0.1 (README, depth-eight setup)
- TBPTT = 128, "which covers every training sequence here" (README)
- width 512, FFN 1,365, 4 heads, global batch 512, 2,000 planned steps (README)
- params: RLT 26.10–28.73M; Transformer 8 25.31M (README)
- runs: 48 total, 21 reached 2,000 steps, 27 unfinished (README)
- parity @500: RLT 6+2 99.44 ± 0.98; RLT 4+4 83.29 ± 28.94; 5+3 83.51 ± 28.00; 7+1 82.77 ± 29.84; 8+0 48.70 ± 2.60; Transformer 8 48.48 ± 0.53 (README table)
- parity: "All three RLT 6+2 seeds reach 100% by step 600; Transformer 8 reaches 94.84 ± 3.43% at step 2,000" (README)
- parity instability: "RLT 5+3 seed 42 drops from 100% at step 500 to 48.05% at step 600 and recovers at step 700" (README)
- mod-5 flat @2000, seed 42: 7+1 95.44; 8+0 90.89; T8 20.57 (README "Completed mod-5 subset")
- mod-5 brackets @2000: 7+1 78.26; 8+0 75.52; T8 79.56 (README)
- S5 swaps @1000: 4+4 100.00; 5+3 99.61; 6+2 95.70; 7+1 89.84; 8+0 86.33; T8 89.84 (README table)
- S5 standard @1000: all ≤ 3.52 (README table)
- training examples: 256,000 per seed at step 500; 1,024,000 per run at step 2,000; 768 validation examples (README)
- community: ~79K params, 3 seeds, 2,048 test programs per task/length; parity 128-op RLT 60.8% vs Transformer ≈48%; five-state 128-op RLT 20.7% vs ≈21% (README)

## Relevance to local-maxxing

**The owner hint does not match the paper's mechanism.** RLT is not depth recurrence in the Geiping et al. 2025 sense (a block iterated K times per token, which the paper cites under "Depth-wise reuse" as prior art and distinguishes itself from). RLT keeps per-token block count fixed and instead carries state *across tokens*; "more compute per token from fewer parameters" is exactly what it does not claim. The only parameter-reduction axis is encoder/decoder weight tying (§2.6), and the paper says tying "does not by itself reduce block evaluations or guarantee lower latency." On the town's bandwidth-bound decode frame that matters: a tied 48+48 still streams the shared weights twice per token unless they are cache-resident, so the bytes-touched-per-token delta from tying is ~0 while the *stored* footprint halves. File this as an orthogonal axis to the town's looped transformer, not as its paper.

**What it does buy the ledger is cheap state.** The whole feedback path is 3d² params and one d-vector carried across tokens — at d=512 that is 0.79M params (≈3% of a 25M model, ~0.8 MB at Q8) and 512 floats of state — and the README's RLT 8+0 (zero decoder blocks, merge only) reaches 90.89% on mod-5 flat at 2,000 steps where Transformer 8 sits at 20.57%. That is a near-free bytes/token addition producing a state-tracking capability a same-size transformer lacks. Caveat the README itself gives: the ablation that isolates feedback has not been run, and 8+0 also differs from T8 in cross-attention wiring and +0.8–3.4M params.

**Flip/SNN and Kuramoto thread.** `s_t` is a persistent per-sequence state updated by a gated leaky-integrator merge (`u = e + α g ⊙ W_s RMSNorm(s_{t-1})`) — structurally the same object as an oscillator phase or an E3 byte-neuron state carried across ticks, and the token-to-token coupling is the temporal analogue of chain 2's flip-timing coupling. The paper's Appendix B warning that "A product involving only ∂s_t/∂s_{t-1} generally misses paths through decoder KV" and "Normalization alone does not bound products of these Jacobians" is the stability question chain 2 is already asking (R vs K). The parity-run instability (a seed dropping 100% → 48.05% → recovery between steps 500 and 700) reads as a phase-locking/unlocking event worth looking at through that lens.

**Cluster fit.** The reported experiments are 25–29M-param, width-512, 2,000-step synthetic-task runs — local-town's gpu-8g(8 GB) can reproduce them; the swarm box cannot train them but can decode them. Prefill is sequential in the decoder (§3.2), which hurts any config with L_D > 0 on the town's CPU boxes; the 8+0/7+1 configs keep prefill almost fully parallel and are the ones that scored on mod-5.

## Idea seed

- **slug:** `lm-token-state-feedback-merge`
- **lever:** Carry one d-wide hidden vector across tokens through a 3d² gated merge (`u_t = e_t + α g ⊙ W_s RMSNorm(s_{t-1})`, α=0.1) — 0.79M params and 512 floats of state at d=512 — which the README reports lifts a depth-8, 25M-param model from 20.57% to 90.89% on mod-5 flat at 2,000 steps with zero extra attention blocks and ~0 extra weight bytes streamed per token.
- **buys:** A state-tracking capability (parity, modular counting, permutation composition) that the town's sub-1B models fail, for a bytes/token cost that rounds to zero on the swarm box, and a persistent per-sequence state variable that the flip/SNN and Kuramoto threads can couple to directly.
- **first_falsifier:** Train Transformer-8 vs RLT 8+0 vs a matched "8+0 without feedback" (same wiring, merge removed) at width 512, seed 42, 2,000 steps on mod-5 flat; if 8+0 does not beat Transformer-8 by ≥20 points, or the no-feedback control matches 8+0, the feedback merge is not the lever.
- **cheapest_test_on_our_iron:** On local-town (gpu-8g, torch venv), three 25–29M-param runs (T8, RLT 8+0, 8+0-no-feedback) on the README's mod-5 flat generator at batch 512 for 2,000 steps — roughly 1–3 h wall-clock per run at $0, with parity at step 500 (RLT 6+2 99.44 vs T8 48.48) as a 25%-cost early read.

## Critique (adversarial, 2026-09-16)

Re-fetched 2026-09-16 with `curl -sL -A 'Mozilla/5.0'`: abs HTTP 200 (273,718 bytes — 4 bytes of dynamic drift from the digest's 273,714, no date string on the page); PDF HTTP 200, 613,049 bytes, 16 pages, `pdftotext -layout` 771 lines, CreationDate Sat Sep 12 17:20:06 2026 EDT; README `HEAD`/`master` HTTP 200, 11,186 bytes, `main` HTTP 404; `assets/experiments-depth8/README.md` HTTP 200, 1,473 bytes; GitHub trees API for `master` (recursive) lists **LICENSE, README.md, two PDFs, index.html, figure1.png and figure assets only — no code, no task generator.** Every README table value, the PDF equations (2.9–2.11, 3.2, 3.3), "96 logical block evaluations per token", "48t", and every quoted sentence in the Provenance/Summary/Numbers sections above were found verbatim in the fetched bytes. The errors are in the reader's inferences and in the idea seed.

| # | Digest / idea claim | What the source says | Where |
|---|---|---|---|
| 1 | Idea lever: "~0 extra weight bytes streamed per token". | The merge adds W_g (d×2d) + W_s (d×d) = 3d² ≈ 786k params, applied every token; README: "RLT models have 26.10–28.73M parameters; Transformer 8 has 25.31M", and 25.31 + 0.79 = 26.10 lands exactly on the floor of that range. On the town's bandwidth-bound frame that is **+3.1% bytes/token**, not ~0. | PDF eqs 2.10–2.11; README "Depth-eight experiments" |
| 2 | Idea buys: "state-tracking capability (parity, modular counting, permutation composition)" from the merge-only config. | Merge-only RLT 8+0 vs Transformer 8 in the README tables: parity @500 **48.70 ± 2.60 vs 48.48 ± 0.53** (chance); addition @1000 100.00 vs 100.00; mod-5 flat @800 21.74 vs 20.70; mod-5 brackets @800 37.63 vs 35.55 and **@2000 75.52 vs 79.56 (8+0 loses)**; S5 swaps @1000 **86.33 vs 89.84 (8+0 loses)**; S5 standard 1.17 vs 1.17. The merge-only config beats T8 in exactly **one cell**: mod-5 flat, seed 42, step 2,000 (90.89 vs 20.57). The parity win (99.44 ± 0.98) belongs to 6+2, which has two decoder blocks with SWA and cross-attention. | README "Validation accuracy at shared checkpoints", "Completed mod-5 subset" |
| 3 | Relevance: "8+0 also differs from T8 in cross-attention wiring and +0.8–3.4M params". | "RLT 8+0 has no decoder blocks" (README); cross-attention is inside the decoder block (PDF eq 2.15), so 8+0 has none. The +0.8–3.4M spread is the range over *all* RLT configs; nothing in the source gives 8+0's own count (arithmetic in #1 suggests it is the 26.10M floor, i.e. +0.79M only). | README; PDF §2.5 |
| 4 | first_falsifier: third arm "8+0 without feedback (same wiring, merge removed)". | With L_D = 0 and no merge, the decoder input z_t^0 = e_t is also its output s_t (PDF eq 2.16, s_t = z_t^{L_D}; README: "The decoder receives z_t^0 = e_t directly"). That arm collapses to Transformer 8 up to the readout norm — it is not a third condition. The README's planned control is **4+4 w/o feedback**, "implemented after this snapshot ... no results in the tables below". | PDF §2.5; README "RLT without hidden-state feedback" |
| 5 | cheapest_test: "on the README's mod-5 flat generator", "roughly 1–3 h wall-clock per run". | **No generator or training code is released** (repo tree above); the community results "use a separate implementation". No source states hardware, wall-clock, or sequence length (only "TBPTT 128, which covers every training sequence here", so sequences ≤128). **1–3 h is invented.** By 6·N·D arithmetic (26.1M × 512 × 128 × 2,000 steps) a run is ≈2×10^16 FLOPs; wall-clock on the GPU2070S must be measured with a pilot. | README; GitHub trees API |
| 6 | cheapest_test: "parity at step 500 (RLT 6+2 99.44 vs T8 48.48) as a 25%-cost early read". | The proposed runs are 8+0, whose parity @500 is 48.70 ± 2.60 (chance). A 6+2 number is not an early read for an 8+0 run. | README parity table |
| 7 | Idea buys: capability "that the town's sub-1B models fail". | Not measured anywhere; not in the source. Unsupported. | — |
| 8 | Relevance: "'more compute per token from fewer parameters' is exactly what it does not claim." | Overstated. PDF §1: "Compatible weights can be shared between the two stacks, giving two logical passes through one backbone and 96 logical block evaluations per token" — the tied config *is* a fixed 2× weight reuse per token. What the paper declines to claim is a quality gain from it (§7: "Neither weight tying nor temporal recurrence alone establishes novelty or a quality improvement") and it has no measurements of tying (README experiments are untied). The owner hint is half-right, not mismatched. | PDF §1, §2.6, §7 |
| 9 | Relevance: under tying "the stored footprint halves". | PDF §2.6: decoder cross-attention "has separate query/output projections and the memory projections"; "Stage-specific normalizations, the merge, and readout remain explicit modules." §4.2 says only that tying "reduces the stored parameter footprint". Less than halves. "Streams the shared weights twice per token" is the reader's inference; the paper says tying "can favor weight residency". | PDF §2.6, §4.2 |
| 10 | Numbers: "merge params = 3d²". | Reader's count from stated shapes; omits b_g (d), the learned initial state s⋆ (d) and RMSNorm_s gain (d): 3d² + 3d ≈ 787,968 at d=512. Negligible, but the paper states shapes, not a count. | PDF §2.1, eqs 2.9–2.11 |
| 11 | Summary item 4 cites "two logical passes through one backbone" and "Parameter tying reduces stored weights but does not eliminate the second logical pass or either cache role" under §2.6. | First quote is §1; second is §3.2. | PDF |
| 12 | Relevance: "gated leaky-integrator merge"; parity dip "reads as a phase-locking/unlocking event". | Paper calls it "a concrete gated merge"; with L_D = 0 it is s_t = e_t + α g_t ⊙ W_s RMSNorm(s_{t-1}) — a gated nonlinear recurrence with no explicit decay term. The phase-locking reading is the reader's, unsupported by any source measurement. | PDF §2.5 |
| 13 | Numbers: "carried state = one d-vector". | True only for L_D = 0; for L_D > 0 the complete state H_t = (s_t, C_t^D) also holds per-layer SWA KV (PDF eqs 2.5, 3.3). The idea's "512 floats of state" holds for 8+0 only. | PDF §2.1, §3.2 |
| 14 | Omitted: at the shared mod-5 flat checkpoint (step 800) all six models sit at 20.83–22.53% (chance for 5 classes is 20%); the 8+0 advantage appears only between step 800 and 2,000 and only for seed 42. Parity SDs of 28–30 points across three seeds show that one seed is not evidence. | README shared-checkpoint table; "Parity: learning speed and variability" | README |

**Unsupported numbers:** "~0 extra weight bytes/token" (is +3.1%); "1–3 h wall-clock"; "25%-cost early read"; "+0.8–3.4M params" attributed to 8+0; "stored footprint halves".

**Corrected idea seed (supersedes the one above):**

- **slug:** `lm-token-state-feedback-merge`
- **lever:** A 3d² gated merge (`u_t = e_t + α g ⊙ W_s RMSNorm(s_{t-1})`, α = 0.1) that carries one d-vector across tokens adds +0.79M params (+3.1% bytes/token on a 25.31M model) and no attention blocks; the README's sole supporting cell is RLT 8+0 90.89% vs Transformer 8 20.57% on mod-5 flat, seed 42, 2,000 steps, while the same config ties T8 on parity@500 and addition and loses on mod-5 brackets and S5 swaps.
- **buys:** If that one cell replicates across seeds, a per-sequence recurrent state on a sub-30M encoder-only model for +3% weight bytes/token, and a concrete d-vector state variable the flip/SNN and Kuramoto threads can couple to.
- **first_falsifier:** Re-implement T8 and RLT 8+0 (no code is released) at width 512, 8 layers, batch 512, on a mod-5 flat generator built to the README's description, seeds 42–44 to 2,000 steps; if 8+0's three-seed mean does not beat T8's by ≥20 points, or T8 also climbs past 80% by step 2,000, the merge is not the lever.
- **cheapest_test_on_our_iron:** On local-town (gpu-8g, torch venv), a 100-step pilot of one ~26M-param 8+0 run at batch 512, seq ≤128 to measure step time, then six 2,000-step runs (T8 × 3 seeds, 8+0 × 3 seeds), ≈2×10^16 FLOPs each by 6ND arithmetic, $0.
