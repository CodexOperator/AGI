---
id: experiment:tm-neuron-period-1001
mint_id: c6d2283b573944649e88a41a57a1bc75
type: experiment
parents:
  - hypothesis:lm-neuron-periodicity-map-finds-function-neurons
next_edges: []
confidence: 0.8
edited_by: thought-master
evidence_runs:
  - experiment:tm-neuron-period-1001
line_ceiling: 180
production_lines: 180
scaffold_hash: 55887da5d4e91581
season: 2
title: "Neuron periodicity MAP on Qwen2.5-0.5B: 3310 MLP neurons (2.8 pct) are value-periodic beyond both nulls (C1 pass), but zero-ablating the top-64 leaves two-digit addition at 0.975 = random (C2 fail) -- disproved; the per-turn position scan enriches for them 1.7x, p 7e-05 (C3 pass)"
town: local-maxxing
verdict: disproved
---
# experiment:tm-neuron-period-1001

## Experiment

**Question (CLAIM of hypothesis:lm-neuron-periodicity-map-finds-function-neurons, pre-registered rule unchanged).** On Qwen2.5-0.5B-Instruct (cell `osc03_hf_dir`, fp32 CPU), read all 24 x 4864 = 116,736 MLP neurons at the down_proj INPUT act(gate(x)) * up(x). C1: sweeping a = 0..99, do >= 0.5 pct of neurons have Fourier peakiness over a above BOTH a 20-permutation label-shuffled null's 99.9th pct AND a random-init twin's max? C2: does zero-ablating the top-64 by peakiness cut two-digit addition exact-match below the min of 5 random-64 arms (baseline >= 0.5)? C3 (separate): does the top 1 pct by token-position peakiness (minus shuffled-token peakiness) in one 2048-token turn overlap the C1 set at hypergeometric p < 0.01?

**Dispatch line, answered first.** config-max: out dir = NEW cell `paths.local_maxxing.osc_neuron_period_dir` = `datasets/osc-band/2026-10-01-neuron-period` (commit 5515c239ae); every design choice (template, sweep, permutations, quantile, twin seed, few-shot lines, problem seed/count, k, random seeds, C3 doc id, skip, shuffle seed, verdict rule) lives in `params.json` there, written before the run; model = existing cell `osc03_hf_dir`; text = sibling `wiki.valid.raw` of cell `wikitext2_test_raw`. template-max: none. engine code: none.

**Method.** `.agi/context/local-maxxing/osc/osc_neuron_period.py` (180 non-blank non-comment lines, <= 180) hooks every `mlp.down_proj` with a forward pre-hook (reader + optional zero mask on its input). C1 prompt = 3 few-shot lines ("12+35=47", "68+27=95", "41+73=114") + `\n{a:02d}+`, read at the last token `+` (asserted identical for every a); a ZERO-PADDED so all 100 prompts have the same 12 tokens and positions -- unpadded a would put a 1-vs-2-digit length step at a=10 (params.json `c1_template_note`). Peakiness = max non-DC rfft power / total non-DC power over the 100-long series; period = 100/k. Null 1 = same activations, a permuted, 20 perms, pooled 2,334,720 values, 99.9th pct. Null 2 = `from_config` random-init twin (torch seed 0, HF init std 0.02), same prompts, run in a SEPARATE process (`--twin`) first, its max over all 116,736 neurons. C2: 200 problems a,b in 10..99 (seed 0), same few-shot, plain greedy argmax with KV cache (no generation_config, so no repetition penalty), exact match on the leading digit run of 4 new tokens; ablation = zero the 64 neurons at every position; random arms drawn from all 116,736 neurons, excluding none. C3: WikiText-2 valid article 13 "Trout Creek Mountains" (the first >= 2048-token article after the 9 the L4 round used), first 2048 tokens, positions 0-3 dropped (sinks), score = peakiness on the doc minus peakiness on the same tokens in one shuffled order (second forward), top floor(0.01 x 116,736) = 1167.

**Tests.** `osc_neuron_period_test.py`: 7 pass (pure sinusoid peakiness = 1 at k 1/10/20/50, white-noise mean bin share = 2/N exactly and mean peakiness < 0.15, constant series 0; the hook output equals act_fn(gate_proj(x)) * up_proj(x) recomputed from the MLP input on a tiny Qwen2, shape layers x width; mask ablation equals zeroing that neuron's down_proj column, changes logits, and `ablate([])` restores the forward bit-exactly; greedy-with-cache equals full-recompute argmax; each null permutation keeps the per-neuron activation multiset and matches peakiness of the permuted array; hypergeometric tail vs brute-force comb; params pre-registration + C2 problem/gold consistency). Real-model grid 24 x 4864 asserted in-run (results.json:4 `grid_ok`).

## Results (datasets/osc-band/2026-10-01-neuron-period/summary.md, results.json)

| conjunct | measured | rule | outcome |
|---|---|---|---|
| C1 | 3310 / 116,736 = 0.02835 clear both (results.json:8-9; summary.md:5) | >= 0.005 | pass |
| null 1 | 99.9th pct of 2,334,720 shuffled peakiness = 0.1962 (results.json:10-11); 91,656 beat it (results.json:40) | | binding? no |
| null 2 | twin max 0.6069, twin q999 0.5354 (results.json:12-13; run.log:5); 3310 beat it (results.json:41) | | the binding null |
| C2 | baseline 0.9750; top-64 0.9750; random min-max 0.9750-0.9750 (results.json:3753-3763; summary.md:10) | top-64 < 0.9750 | FAIL |
| C3 | overlap 57 of 1167 with the 3310 C1 set, expected 33.09, p 7.07e-05 (results.json:4251-4256; summary.md:12) | p < 0.01 | pass (separate) |

- Dominant periods in the C1 set (results.json:390, summary.md:6): T100 (k=1, one cycle over 0..99, i.e. a ramp / magnitude code) x2781, T10 x292, T2 x95, T5 x91, T50 x36, T2.5 x12, 3 others x1. The prior-art periods 2 / 5 / 10 are all present.
- Top neurons (results.json:68, summary.md:7): the 8 most peaked are all period-2 (parity of a), L8.4040 0.9577, L8.1222 0.9258, L10.454 0.9226, L11.4756, L12.657, L16.3752, L7.898, L10.3219. Of the 40 listed: 17 x T100, 12 x T2, 8 x T10, 3 x T5; every layer-0 entry among them is T5 or T10 (units-digit-like).
- Per layer (results.json:42, summary.md:8): [422, 9, 10, 53, 26, 34, 37, 70, 58, 28, 56, 61, 131, 278, 359, 432, 111, 126, 165, 168, 160, 161, 184, 171] -- layer 0 (raw digit read-in) and layers 13-15 dominate.
- C3 means: doc peakiness 0.0198 vs shuffled 0.0164 averaged over all neurons (results.json:4481-4482).

## Verdict: DISPROVED

Pre-registered rule (params.json `verdict_rule`): C1 pass AND C2 pass -> proved; either fails -> disproved. C1 passes (5.7x the threshold) but C2 fails: top-64 ablation leaves accuracy exactly at baseline, inside (equal to) the random band (results.json:2, 3752). C2 is NOT void: baseline 0.975 >= 0.5. Round void checks all pass: grid 24 x 4864 (results.json:4), twin run in its own process before the main one (run.log:5), shuffled null computed at full size (results.json:11), no cell reused (new out dir; L4 docs excluded from C3 by id, asserted in test). **C3, scored separately: PASS** (p 7.07e-05).

Post-verdict diagnostic, NOT scored (run.log:31-37, source run.log:38-56): to rule out a no-op ablation, the first-answer-token KL(base || arm) over 50 C2 prompts: top-64 1.34e-03 vs random 2.5e-04..7.0e-04 (1.9-5.3x larger, max |dlogp| 2.00 vs 0.83-1.21), yet top-1 unchanged on 50/50 in every arm. The ablation acts; 64 neurons (0.055 pct) are too few to flip a confident sum.

## LARGEST SAFE STEP

Stage 2 (self-poke) has a CANDIDATE target set but not a FUNCTIONAL one: 3310 value-periodic neurons beat the twin (results.json:437 `set`), the parity / units-digit / magnitude families are cleanly separable by period, and the cheap per-turn position scan enriches for them 1.72x (C3). What is missing is causal weight. Next rung, still CPU 0.5B, one round: ablate by FAMILY not by a peakiness top-k -- all T10+T5 (383) vs all T2 (95) vs all T100 (2781) vs size-matched random x5 -- and score a metric that can see sub-flip damage (answer-token KL / log-prob of the gold sum, plus exact match), with a units-digit-carry split of the problems. Do not open stage 2 until some family moves exact match beyond its random band.

## Caveats

- The C1 pass is 84 pct k=1 ramps (2781/3310): monotone magnitude codes, not oscillations. Counting only the prior-art oscillating periods (T2/T5/T10 = 478 = 0.41 pct) would sit below the 0.5 pct line; the rule did not ask for that split and the verdict does not use it.
- Null 1 is weak (99.9th pct 0.196; 78.5 pct of neurons beat it): any smooth function of two digit tokens beats a shuffle. The random-init twin carries the C1 result; one twin seed only.
- The twin's input dependence is mostly digit-token identity through near-uniform random attention; it is an architecture-plus-tokenizer null, not an "untrained but functional" control.
- C2 has a ceiling: baseline 0.975 (5 wrong of 200; the first 10 logged answers are identical in every arm, results.json:4163) leaves little room, and top-64 by raw peakiness is dominated by parity and ramp neurons rather than the T10 units-digit family the addition mechanism would need.
- C3 uses one doc and one shuffle; the 1.72x enrichment may track digit / number tokens in the text rather than an intrinsic rhythm -- not separated here.
- Instruct checkpoint, raw completion (no chat template), fp32 CPU, sdpa attention. Wall 232 s for the scored run (results.json:4484); one launch, no PSI stop, no resume.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2 (thought-master 01:xZ 10-01): adversarial Opus review = ACCEPT_WITH_RESIDUE; DISPROVED stands (C1 0.02835 >= 0.005 pass, C2 0.975 not < 0.975 fail, not void). The read point, pooled null, twin, live ablation during cached decode (osc_neuron_period.py:43,92-95) and C3's hypergeometric p 7.07e-05 all re-verified; 7/7 tests; scope clean; 180 lines. CORRECTIONS to the reading: (1) C1 is FRAGILE -- a pure linear ramp over 0..99 scores peakiness 0.608 vs the twin max 0.6069, so the 2781 period-100 members only need to be ramp-like; without them 529/116736 = 0.453 pct, below the 0.5 pct line. (2) C3's 'bridge' is most likely a LAYER CONFOUND -- both sets cluster in layers 13-15 (C1 1069/3310; C3 top-200 117/200); layer-stratified on the saved top-200 the overlap is 10 vs 11.4 expected (P(X>=10) 0.71): no enrichment beyond layer. The owner's per-turn bridge is therefore NOT shown. (3) C2's identical 0.975 in every arm means the probe is blind at this ceiling, not that the ablation is a no-op (top-64 shifts the first answer token 1.9-5.3x more KL than random). Residues for the next round: save activations + per-neuron periods (:194 deletes them); detrend before the FFT; layer-matched random controls; mean- beside zero-ablation; score log-prob of the correct sum; a layer-stratified C3 null with number tokens masked; the base (not Instruct) checkpoint or say why.
<!-- THOUGHT:END -->
