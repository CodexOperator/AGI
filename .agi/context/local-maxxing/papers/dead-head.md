# Coherence-Guided Dead-Head Identification in Frozen Transformers: A Zero-Parameter Geometric Threshold from Coupled-Oscillator Criticality

Source key: `dead-head`. Kind: repo (paper bundle — manuscript source + frozen JSON artifacts + scripts). Author per `paper.tex`: Michael Sharpe, "Project 89 / Green Loom Association", dated "March 2026". Licence: PolyForm Noncommercial 1.0.0; README states "Patent Pending: U.S. Provisional Application No. 64/031,983 ... Filed April 7, 2026".

## Provenance

Fetched 2026-09-16, all HTTP 200, via `curl -sL -A 'Mozilla/5.0'`:

| What | URL | Bytes |
|---|---|---|
| README | https://raw.githubusercontent.com/project-89/coherence-guided-dead-head-identification/main/README.md | 7,547 |
| repo metadata | https://api.github.com/repos/project-89/coherence-guided-dead-head-identification | 7,804 (`created_at` 2026-04-03, `pushed_at` 2026-04-08, 51 stars, default branch `main`) |
| full tree | https://api.github.com/repos/project-89/coherence-guided-dead-head-identification/git/trees/HEAD?recursive=1 | 13,371 (48 entries) |
| paper source | .../main/paper.tex | 36,868 (787 lines) — `paper.pdf` (1,576,448 B) is in the tree, not fetched; `.tex` is declared "source of truth" in AGENTS.md |
| AGENTS.md | .../main/AGENTS.md | 4,310 |
| data/README.md, supporting/README.md, figures/README.md | .../main/data/README.md etc. | 1,865 / 495 / 1,124 |
| threshold_transfer_summary.json | .../main/data/threshold_transfer_summary.json | 3,598 |
| base_rate_analysis.json | .../main/data/base_rate_analysis.json | 3,190 |
| qwen25_05b_timing_proxy_v1.json | .../main/data/qwen25_05b_timing_proxy_v1.json | 5,593 |
| qwen25_05b_head336_small_theory_redundancy_v2_boundary2.json | .../main/data/qwen25_05b_head336_small_theory_redundancy_v2_boundary2.json | 468,498 (336 per-head records) |
| smollm2_level2_kv_compaction_v1.json | .../main/data/smollm2_level2_kv_compaction_v1.json | 20,604 |
| supporting/repeatability_summary_v1.json, qwen3_8b_role_aware_comparison.json | .../main/supporting/... | 6,368 / 949 |
| scripts/coherence_anatomy_scan.py | .../main/scripts/coherence_anatomy_scan.py | 29,148 |

**There is no `experiments/` folder in the repo.** The tree's top level is `data/ figures/ scripts/ supporting/` plus `paper.tex paper.pdf references.bib README.md AGENTS.md LICENSE NOTICE Makefile .gitignore`. The record of how the loop ran is `data/*.json` (frozen per-head results, six models), `scripts/98_*.py` (experiment "98" harness, plots, verifier, random-init control, GQA compaction, structural timing) and `supporting/` (3-seed repeatability). JSON paths inside the artifacts (`.../wayfaring/06_intelligence/coherence_lattice/out/exp98_pruning/...`, `device: mps`) show the runs were done on an Apple box out of a larger private "coherence_lattice" tree; only exp98's outputs were published. The paper the repo implements is the bundled `paper.tex` itself (no arXiv id anywhere in the README, AGENTS.md or tex).

## Summary (measured lines)

- Observable: per head `c_h(i) = cos(s_h(i), x_i)` where `s_h(i) = sum_j A_ij V_h(x_j)` is the head's write-back and `x_i` the pre-head residual; head mean `c̄_h` over positions and calibration batches (paper.tex §"Transformer Observable"). Scanner hooks `attn.c_proj` / `self_attn.o_proj` pre-forward and the block pre-forward, calibration = 32 batches x 128 tokens of WikiText-2 train, seed 42 (`coherence_anatomy_scan.py` L92-142).
- Threshold: `tau_death(d) = chi_c / sqrt(d_model)`, `chi_c = 0.679*sqrt(2) = 0.96025`, from "BKT bond death cos(Δθ)=0.679 on S^1", divided by S^1 fluctuation scale `1/sqrt(2)`, times S^(d-1) scale `1/sqrt(d)` (abstract; AGENTS.md "Derivation"). "No parameter is fitted." Bundle actually uses `chi_c_artifact` in `[0.96000, 0.96025]` (threshold_transfer_summary.json `threshold_note`).
- Headline table (paper.tex Table `tab:main-matrix`): GPT-2 d=768 dead 42/144 precision 95.2%; GPT-2 Medium d=1024 114/384 98.2%; Qwen2.5 0.5B d=896 157/336 95.5%; SmolLM2 360M d=960 234/480 99.6%; OpenLLaMA 7B d=4096 286/1024 100.0%; Gemma 3 4B d=2560 30/272 100.0%. Precision = "individually safe to ablate" against a per-head ablation ground truth with tolerance = 1% of baseline loss (Qwen artifact `ground_truth_loss_threshold` 0.022858 vs `baseline_calibration.loss` 2.285843).
- The paper's own base-rate section undercuts the precision claim: "picking any 114 heads at random from the non-protected pool would yield ~99% precision" on GPT-2 Medium; base_rate_analysis.json gives lift over random of 1.0216 (GPT-2), 0.9881 (GPT-2 Medium), 1.0001 (Qwen2.5 0.5B: random 95.53% vs threshold 95.54%), 1.0189 (SmolLM2), 1.0010 (OpenLLaMA). Text: "We do not claim that precision is the primary evidence for the threshold."
- Naive simultaneous removal is "catastrophic": ΔLoss "+1.4 to +2.1 across models" (§`sec:naive-removal`); transfer summary `combined_delta_loss` = 1.847 / 1.430 / 2.125 / 2.051 / 1.604 for the five ablation-validated models. Qwen2.5 0.5B masked-proxy timing (qwen25_05b_timing_proxy_v1.json, mps, batch 1): dead_only ΔLoss +1.203 @128, +1.406 @256, +1.518 @512, +1.541 @1024 tokens, and `speedup_vs_baseline` -11.3% / -3.2% / -0.4% / -5.6% (mask, not structural removal: `parameter_count` unchanged at 494,032,768).
- Random-init control (Table `tab:randinit`): std(z_h) trained vs random = 4.17/0.47 GPT-2, 5.92/0.55 GPT-2 Medium, 2.71/0.20 Qwen2.5 0.5B, 3.84/0.22 SmolLM2 — "9-18x" — so the coupling structure is learned, not architectural.
- The one real bytes/token result: SmolLM2 360M GQA (group size 3) Level-2 compaction removes 44/160 fully-dead KV groups (27.5%), KV cache 81,920 -> 59,392 bytes/token (-27.5%), params 361.8M -> 340.2M (-5.98%), prefill "+30.96%" at seq 1024, at ΔLoss "+0.53206" (paper.tex §GQA; smollm2_level2_kv_compaction_v1.json). Qwen2 with group size 7: "only 3/48 KV groups are fully dead".
- "Dead heads are mildly toxic": Gemma 3 4B, SVD rank 64 (25% of head dim) on the 30 dead heads gives ΔLoss -0.075 (-1.5%) — model *improves* (paper.tex §"Dead Heads Are Mildly Toxic"); "full spectral filtering analysis ... will be reported separately".
- Side artifact: Qwen3-8B role-aware quantization "attn=4, ffn_read=4, ffn_write=6" gives Δloss 0.0375 at 4.24 effective bits vs a uniform "avg_bits 4.25" GPTQ run at Δloss 0.3393 (qwen3_8b_role_aware_comparison.json) — the "tensor-role asymmetry" cited as convergent evidence.

## Numbers

- chi_c = 0.96025 = 0.679*sqrt(2) (paper.tex abstract; scan.py L41 `CHI_C = 0.679 * (2 ** 0.5)`)
- tau_death: 0.03465 (d=768), 0.03000 (1024), 0.03207 (896), 0.03098 (960), 0.01500 (4096), 0.01897 (2560) (Table tab:main-matrix)
- Qwen2.5-0.5B artifact: 24 layers x 14 heads = 336; dead 157, protected 45 (boundary 42 = "first=2, last=1", bridge 3), alive 134; TP dead-safe 150, FP dead-unsafe 7, safe_recall 0.479, dangerous_keep_rate 0.696; seq_len 128, 8 calibration + 8 eval sequences, device mps (`clr_theory` block)
- Qwen2.5-0.5B per-layer dead counts (derived from `clr_theory.decisions`): L0-1: 0 (boundary), L2 8, L3 6, L4 10, L5 8, L6 5, L7 8, L8 9, L9 12, L10 11, L11 13, L12 6, L13 9, L14 6, L15 8, L16 11, L17 4, L18 5, L19 7, L20 1, L21 5, L22 5, L23 0
- Qwen2.5-0.5B per-head ablation delta_loss over all 336 heads: min -0.0119, median 0.00425, max 0.3949 (derived from `head_results`); sum over the 157 dead heads = 1.027 vs measured joint dead_only ΔLoss +1.203 @128 tokens (timing proxy) — joint damage is ~0.18 above additive
- Qwen2.5-0.5B dead-but-unsafe heads (layer, head, z_h, ΔL): (2,5,-0.078,0.395) (4,12,-4.56,0.023) (5,9,-5.31,0.030) (8,3,-3.33,0.027) (10,6,-2.92,0.061) (12,3,-0.93,0.025) (14,10,-6.19,0.034) — derived from the artifact; the worst single head in the model (ΔL 0.395) sits *inside* the dead set
- Qwen2.5-0.5B group means of z_h: dead -1.22 (std 1.86), alive 2.79 (std 1.78), unsafe 0.098; Cohen's d 2.20 (base_rate_analysis.json)
- Repeatability, Qwen2.5-0.5B seeds 7/11/19: dead_count 156/159/(third run cut in listing), dead_precision 0.9615/0.9811, dead_only_delta_loss 1.128/2.077/1.753 (repeatability_summary_v1.json)
- Redundancy pass (Qwen2.5-0.5B): 62 of 134 alive heads redundant, precision 0.9516; dead+redundant eval loss 4.371 vs baseline 2.246 (`redundancy_pass`)
- Naive removal ΔLoss: "+1.4 to +2.1" (paper); GPT-2 3-seed dead_only_delta_loss mean 2.794 std 0.158 (repeatability)
- Larger-scale unvalidated: "407 dead heads (26.5%) on REAP-25B MoE and 180 dead heads (54%) on Gemma 4 E4B" (paper.tex Discussion) — no ablation ground truth in bundle
- Cited convergent claim: key-projection "d_eff ~ 4 out of 128" (SpectralQuant, README)

## Relevance to local-maxxing

Bytes-per-token ledger: on the town's bandwidth-bound decoder the only thing a dead head saves is the bytes of its q-rows and o-columns (and, under GQA, a KV group only if *every* query head in it is dead). Derived for Qwen2.5-0.5B (d 896, head_dim 64): 157 dead heads x (896x64 + 64x896) = 18.0M params ≈ 18 MB/token at Q8 out of ~494 MB, i.e. ~3.6% of bytes touched, bought at +1.2 to +1.5 nats by the paper's own proxy — a bad trade as-is; the paper's own SmolLM2 result (KV -27.5% at +0.53) is the only lever that reaches the KV cache, and it needs a small GQA group size (Qwen2.5-0.5B has g=7, Qwen3-0.6B has 16 q / 8 kv, g=2 — untested here). What is directly usable is the frozen Qwen2.5-0.5B artifact: 336 per-head mean-ablation deltas on exactly the D1 model, so D1's per-layer-normalized importance can be scored against z_h head-by-head with no GPU; and the identification is one forward pass (32x128 tokens) versus 336 ablation passes. Flip/SNN thread: the paper's whole framing is the town's — LayerNorm puts tokens on S^(d-1), heads are Kuramoto/Lohe couplings, MLPs are intra-oscillator modes, and "dead" means coupling below a critical K_c; chain 2 measures R vs K in flip mode and could test whether a transformer's per-head z_h histogram actually shows a transition at 0.96 or whether (as base_rate lift 1.0001 on Qwen suggests) 0.96 is a label on a smooth ranking. Looped transformer: a depth-recurrent block reuses one head set every loop, so a head that is dead in one loop iteration and alive in another (the artifact's `death_persistence` field, e.g. 0.625 for L0H0) is the quantity to measure before any recurrence-aware pruning.

## Idea seed

- **slug**: lm-dead-head-coupling-scan
- **lever**: one forward pass over 32x128 WikiText tokens gives z_h = sqrt(d)·mean cos(write-back, residual) per head and labels z_h < 0.96 "dead", replacing 336 per-head ablation passes with 1 on Qwen2.5-0.5B (157/336 = 46.7% flagged; their q/o slices ≈ 18 MB of ~494 MB read per Q8 decoded token, derived, ~3.6%), but the paper's own proxy shows removing them costs +1.20 to +1.54 loss and base-rate lift is 1.0001.
- **buys**: a free per-head ranking to seed D1's drop list on Qwen2.5-0.5B — the bundled artifact already carries 336 per-head ablation deltas on the D1 model, so D1's per-layer-normalized importance can be tested head-by-head against z_h with no GPU; and a concrete K_c candidate (chi_c = 0.96 in 1/sqrt(d) units) for chain 2 to test the "coupling has a critical point" claim on real transformer heads.
- **first falsifier**: sweep chi_c over 0.2..4.0 on the bundled Qwen2.5-0.5B artifact (mean_cosine + delta_loss for all 336 heads) and plot dead-precision and safe-recall vs chi_c — if both curves are smooth through 0.96 with precision pinned at the 95.5% random base rate the repo's base_rate_analysis.json reports, there is no critical point and the idea reduces to "rank heads by coupling", saving no bytes beyond what D1 already yields.
- **cheapest test on our iron**: swarm box, python3 + json, ~5 min, $0: parse the 468 KB Qwen2.5-0.5B artifact, sweep chi_c, compute precision/recall and Spearman(z_h, delta_loss) over 336 heads; if it survives, `coherence_anatomy_scan.py --model Qwen/Qwen3-0.6B --device cuda` on local-town (GPU2070S 8 GB, 32x128 tokens, <10 min, $0) to get the town's own dead-head count on its decode model.

## Tags
dead-head, attention-pruning, kuramoto, bkt, coherence, qwen2.5-0.5b, gqa-kv-compaction, bytes-per-token, D1, chain-2, zero-parameter-threshold

## Critique (adversarial, 2026-09-16)

Re-fetched every file in the Provenance table (all HTTP 200, byte counts identical: README 7,547; paper.tex 36,868; Qwen artifact 468,498; etc.) plus `supporting/README.md` (495 B) and, to ground one number the reader had from memory, `https://huggingface.co/Qwen/Qwen3-0.6B/raw/main/config.json` and `.../Qwen2.5-0.5B/raw/main/config.json` (both 200). Every headline number in the digest traces to bytes in the source; the errors are in attribution, in what the numbers mean, and in the idea's framing. Critic-computed values below are marked **[critic]** and come from re-reading `data/qwen25_05b_head336_small_theory_redundancy_v2_boundary2.json` with python3 — nothing was run on a model.

### Errors and corrections

1. **"336 per-head mean-ablation deltas" — the source's ground truth is zero-ablation, not mean-ablation.** paper.tex L373-374: "a head is ablation-safe if *zeroing* it alone causes loss increase below a conservative tolerance". D1 is mean-ablation, so the artifact is a *different* ablation than D1's; a head-by-head comparison is still worth doing, but it is a zero-vs-mean comparison, not a like-for-like check.
2. **`death_persistence` is not about recurrence or loop iterations.** It is `death_count / calibration_sequences` (L0H0: `death_count` 6 over 8 calibration sequences = 0.625; 197 heads have 0.0, 68 have 1.0 **[critic]**), i.e. the fraction of calibration batches on which the artifact's "consecutive-batch death timer" fired (artifact `notes`). Nothing in the source connects it to a depth-recurrent block; the relevance paragraph's "dead in one loop iteration and alive in another" is the reader's. L0H0 is boundary-protected and never a removal candidate anyway.
3. **The dead rule is not "z_h < 0.96".** In the artifact: 190/336 heads have z_h < 0.96 but only 157 are dead; 3 dead heads have z_h >= 0.96; 8 unprotected below-threshold heads stay alive because their `death_max_streak` < `death_patience` = 3 **[critic]**, and a bridge veto ("per-layer bridge > mean + 2.00 sigma and top-3", 3 heads) plus a structural-score gate (artifact `notes`) also apply. The shipped `coherence_anatomy_scan.py` uses a *different* rule (mean < tau AND below-threshold on >= 50% of batches, `--consistency 0.5`; no bridge veto, no structural gate), 32 batches x 128 WikiText-2 tokens by default. The artifact used 8 calibration sequences x 128 tokens on an unstated corpus (WikiText appears nowhere in paper.tex; the bundle's timing/compaction evals read a `tinystories_corpus/val.txt`). The idea's lever splices the two: "32x128 WikiText tokens ... labels z_h < 0.96 dead ... 157/336" is not one measurement in the source. Re-running scan.py will not reproduce 157.
4. **Qwen3-8B "vs uniform 4.25-bit GPTQ" is not what the JSON says.** `old_stored`: `n_gptq` 216 + `n_simple_absmax` 36, `avg_bits` 4.25 but **`effective_bits` 3.69**; `new_role_aware_4b` `effective_bits` 4.24. The comparison is 4.24 vs 3.69 effective bits — not iso-bit, and "uniform" appears nowhere in the file. paper.tex never mentions Qwen3-8B; `supporting/README.md` calls the file "secondary". Drop it as evidence for anything.
5. **Repeatability was quoted selectively.** Qwen2.5-0.5B seeds 7/11/**19**: dead_count 156/159/**156**, dead_precision 0.9615/0.9811/**0.9295** (the lowest, omitted), `dead_only_delta_loss` 1.128/2.077/1.753 → mean 1.653, **std 0.483** (the digest quoted only GPT-2's tight std 0.158). SmolLM2 3-seed dead_only_delta_loss 0.854/1.054/0.937 (mean 0.948) and GPT-2 mean 2.794 both fall *outside* the paper's "+1.4 to +2.1 across models" (paper.tex L633), which the digest repeated unchallenged; the bundle's own range is 0.85 to 2.92.
6. **SmolLM2 dead count: the paper's table contradicts its own bundle.** paper.tex L384 / README L80 say 234/480; `base_rate_analysis.json`, `threshold_transfer_summary.json` and `smollm2_level2_kv_compaction_v1.json` all say **261** (`dead_query_heads` 261). The digest reported 234 without a flag. Also "+30.96% prefill" is the seq-1024 point of a non-monotone series: speedup +4.07% @128, **-14.76% @256**, +14.50% @512, +30.96% @1024 (mps, batch 1, 50 passes) with dLoss +0.377/+0.444/+0.501/+0.532 — the KV figure (-27.5%) is exact and structural; the speed figure is Apple-MPS timing noise.
7. **Gemma 3 4B (30/272, "100.0%") has no artifact in the bundle.** `threshold_transfer_summary.json` `claim_scope`: "Five ablation-validated decoder checkpoints"; the tree has no gemma file. The Gemma row and the "mildly toxic" SVD result (-0.075) are paper-text-only, unverifiable from the repo.
8. **`safe_recall` 0.479 and `dangerous_keep_rate` 0.696 include protected heads.** `false_negative_alive_safe` 163 = 128 alive-safe + 35 protected-safe; `true_negative_alive_unsafe` 16 = 6 alive-unsafe + 10 protected-unsafe **[critic]**. Within the non-protected pool (291): 278 safe, 13 unsafe (matches `base_rate_analysis.json`); recall of safe heads 150/278 = 0.54, unsafe kept alive 6/13.
9. **"9-18x"**: the table's ratios are 8.9x / 10.7x / 13.6x / 17.5x (paper.tex Table tab:randinit); "9-18x" is the paper's rounding, not a measured span. Minor.
10. **The artifact's `notes[0]` reads "Head-only phase-1 experiment on frozen GPT-2"** inside the Qwen file — copied template text; treat the `notes` block as boilerplate, not run metadata.
11. **The "K_c / critical point" framing is already falsified by the bundled bytes**, so the idea's first falsifier need not wait for anything. Sweeping chi_c on the artifact over the non-protected pool (dead = z_h < chi, precision = fraction with delta_loss <= 0.022858) **[critic]**:

   | chi_c | n_dead | precision | safe-recall | sum delta_loss |
   |---|---|---|---|---|
   | -2 | 40 | 0.875 | 0.126 | 0.258 |
   | -1 | 64 | 0.922 | 0.212 | 0.330 |
   | 0 | 110 | 0.936 | 0.371 | 0.864 |
   | 0.96 | 162 | 0.957 | 0.558 | 1.034 |
   | 1.5 | 196 | 0.964 | 0.680 | 1.187 |
   | 2 | 218 | 0.968 | 0.759 | 1.302 |
   | 4 | 259 | 0.961 | 0.896 | 1.677 |

   Precision *rises* monotonically through 0.96 up to chi ~ 2; the most weakly coupled heads (z < -2) are the *least* safe (0.875), and the single most damaging head in the model (L2 H5, dL 0.395) has z = -0.078. Spearman(z_h, delta_loss) over all 336 heads = **+0.268** **[critic]**. There is no feature at 0.96 in ablation-safety space; the paper itself concedes this (lift 1.0001, "We do not claim that precision is the primary evidence"). Chain 2's R-vs-K apparatus has nothing to test here beyond what a ten-line script already shows.

### Unsupported or reader-derived numbers (not in the source)

- "~494 MB per Q8 decoded token", "18 MB", "~3.6%", "46.7%" — reader arithmetic from `parameter_count` 494,032,768 and d=896/head_dim 64; plausible, but the source measures **no** bytes/token or speed gain for Qwen2.5-0.5B: its only Qwen timing is a *masked* proxy with `parameter_count` unchanged and `speedup_vs_baseline` negative at every length.
- "Qwen3-0.6B has 16 q / 8 kv, g=2" — not in the source; now grounded by the HF config fetched above (`num_attention_heads` 16, `num_key_value_heads` 8, `head_dim` 128, `num_hidden_layers` 28 → 224 KV groups, 448 q heads). Qwen2.5-0.5B config: 14 q / 2 kv → g=7, 48 groups, as the paper says.
- "~5 min", "<10 min on the GPU2070S" — estimates; the scan is 32 forward passes of 1x128 tokens on a 0.6B model in fp32 (2.4 GB), which fits either local-town (cuda or cpu) or the swarm box's 23 GB in CPU mode if torch is present.
- Repo "51 stars" — from `api.github.com` `stargazers_count`, fine.

### What survives, tightened

The oscillator/K_c story does not survive contact with the bundle. The one cost-saving mechanism the source actually demonstrates is **Level-2 GQA compaction**: when every query head sharing a KV head is dead, drop the whole group — K/V/Q/O slices and, decisively for a bandwidth-bound decoder, that group's KV-cache bytes on every token (SmolLM2 g=3: 81,920 → 59,392 B/token, -27.5%; params -5.98%; +0.53 nats @1024). It is gated combinatorially by group size (g=7 on Qwen2.5-0.5B: 3/48 groups). Qwen3-0.6B's g=2 is the town's live question: 224 groups, each dead only if a *pair* is dead. The artifact's 336 zero-ablation deltas remain a free ground truth to score D1's per-layer-normalized (mean-ablation) importance against, with the caveat in (1).
