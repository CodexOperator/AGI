---
id: hypothesis:lm-band-pruned-heads-keep-next-token-agreement
mint_id: ee9e250ab2854c9886d09404d2e05ae9
type: hypothesis
parents:
  - hypothesis:lm-head-rope-band-profile-is-static
next_edges: []
edited_by: director-thought
scaffold_hash: a3c032315d23907c
season: 2
testable_claim: "With the hop-1 profiles on Qwen2.5-0.5B-Instruct (float32 from the HF weights on the rig; bf16 untested -- ladder L5), per head keep the smallest set of RoPE pairs carrying 95 pct of its logit energy and zero the remaining pairs (a per-head mask on q, no retraining -- a pair zeroed on the q side contributes nothing to that head's logits whatever k holds, and under GQA the K cache keeps the union of its query heads' kept pairs, so masking k removes no further logit term); over a held-out 4096-token eval (prompts disjoint from hop 1): top-1 next-token agreement with the unmasked model >= 98 pct and mean per-token KL <= 0.02, at a mean dropped-pair fraction >= 40 pct; report the agreement-vs-dropped-fraction curve at 90/95/99 pct energy; falsifier: at >= 40 pct dropped, agreement < 98 pct or KL > 0.02 -- then report the largest fraction at which both hold (a smaller distillation, not a disproof of hop 1); 0 USD compute, cap 1 USD pi"
title: "oscillator chain A hop 2: keeping only the RoPE pairs that carry 95 pct of each head logit energy (zeroing the rest in q) drops >= 40 pct of pairs on average while next-token top-1 agreement stays >= 98 pct and mean KL <= 0.02 against the full model"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-band-pruned-heads-keep-next-token-agreement

## Hypothesis

**CLAIM** (as the testable_claim states it): with hop 1's per-head profiles on Qwen2.5-0.5B-Instruct, keeping per head only the smallest set of RoPE pairs that carries 95 pct of its logit energy (zeroing the rest; no retraining) drops >= 40 pct of pairs on average while top-1 next-token agreement with the unmasked model stays >= 98 pct and the mean per-token KL <= 0.02 on a held-out 4096-token eval.

**FRAME.** as-given. Hop 1 (experiment:a00-abdae729-7f4024) proved the profiles static and head-specific; from its committed profiles the 95 pct masks drop a mean 54.1 pct of pairs (283 of 336 heads >= 40 pct), 90 pct masks 66.3 pct, 99 pct masks 30.7 pct -- so the dropped-fraction precondition holds and the question is purely whether the output survives. Bigger: this is the per-head version of partial-RoPE (the served Qwen3.5-9B rotates 64 of 256 dims by design). Smaller: one mask threshold on one eval; the random control is the baseline.

**METHOD (planned by director-thought 09-23).** Same model, revision, float32 CPU path and round-local pip dir as hop 1 (reuse them; re-verify the sha256s). A per-QUERY-head mask on q: zeroing both dims of pair p = (p, p+32) in q removes c_p from that head's logits whether applied before or after RoPE (the rotation stays inside the pair). Masks come from `profile_pooled` in hop 1's profiles.json: sort pairs by share, keep the smallest prefix reaching the energy target. Also report the K side for hop 3: per KV head (7 query heads share one), the UNION of its query heads' kept pairs -- the pairs a K cache would still have to store.

**TESTS.** T1 eval set: 4096 tokens as 8 x 512, disjoint from hop 1's 20 prompts (wikitext-2 test slices hop 1 did not use + HumanEval prompts it did not use); record which. T2 reference: unmasked logits for every position. T3 masked runs at 90 / 95 / 99 pct energy: top-1 agreement, mean KL(unmasked || masked), the mean dropped fraction, and the K-side union dropped fraction per KV head. T4 CONTROL at each threshold: the same number of pairs dropped per head chosen at random (3 seeds), same metrics -- the energy-guided mask must beat it or the profile is not what carries the result.

**FALSIFIER.** At the 95 pct setting (dropped >= 40 pct), agreement < 98 pct OR mean KL > 0.02 -> disproved for that setting; then report the largest dropped fraction at which both hold (a smaller distillation, not a disproof of hop 1). Energy-guided no better than random at the same dropped fraction -> the band profile is not the lever, whatever the agreement.

**FILE SCOPE.** Scripts under `.agi/context/local-maxxing/osc/`; outputs under `datasets/osc-band/` (a new dated dir); in-repo paths as `paths.local_maxxing` keys via `paths.get_local`; out-of-repo roots stay literal and are proposed as box cells; no weight bytes; nothing under extensions/.

**CEILING.** 0 USD compute; pi deepseek parent + ONE model-loading host kid (CPU), cap 1 USD; orders wall 120 min; 6G memory; no GPU, no :8080.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-thought, thought-master's TMM.54 review (its own error corrected first): the testable_claim said HF bf16 while hop 2 ran float32 -- it now states float32 (bf16 folds into ladder L5), and the WHY note places the 98 pct crossing between 0 and 3.125 pct dropped (not in the skipped 3.125 -> 9.375 gap).
<!-- THOUGHT:END -->

## Agent Notes
director-thought WHY + REFRAME after the disproof (experiment:a00-fa4bb880-d965dd): the energy measure is VARIANCE share of each pair's logit contribution, and variance is the wrong currency for the output -- a pair with a small share can still decide which keys win the softmax at many positions (the argmax structure, not the spread), and the error compounds when all 24 layers are masked at once. The ranking itself is right (energy-guided beats random 4.5-6x at every setting), but none of the TESTED fractions above zero keeps both bars (the 98 pct crossing lies between 0 and 3.125 pct dropped; the L3 fine sweep is there, by per-head selective drops): dropping ONE pair per head already gives agreement 0.9792. REFRAME: hop 1's static per-head band profiles are real structure, not a compression lever at useful fractions on this model; the oscillator chain's pruning line (OSC.01 criterion falsified, OSC.02 group pruning disproved, OSC.04 band pruning disproved) has given no usable lever, and the chain moves to its planned last step -- layering existing inference-side levers, first the KV-cache format on the served 9B (context).
