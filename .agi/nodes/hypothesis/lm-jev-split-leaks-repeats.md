---
id: hypothesis:lm-jev-split-leaks-repeats
mint_id: 63fcb238f8534e3786001492cfb5e707
type: hypothesis
parents:
  - idea:lm-why-verdict-ece-ignores-temperature
next_edges: []
edited_by: brainstorm
loop: mvp:lm-research-review-workflow@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 7efd2580c28d9509
season: 2
testable_claim: Re-splitting the committed q1 rows (json_cache_scrub + acts_replay_scrub.jsonl, 0 new API calls) with ALL 3 repeats of an act id forced onto the SAME side (GroupKFold by act id) drops verdict-subgroup held-out ECE from 0.141-0.212 to <= 0.10 on >= 4/5 seeds; if it stays > 0.10 the split was not the artifact.
thought_session: iter-TM.60
title: "WHY hop 6a: the held-out split leaks — repeats of the same verdict act land on both folds, so verdict held-out ECE 0.141-0.212 is a within-act label-disagreement artifact, not miscalibration"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-split-leaks-repeats

## Claim

The held-out verdict ECE of 0.141-0.212 (experiment:a00-bdec620b-6c4cf7) is not
a miscalibration measurement at all: it is a **split-leakage artifact**. The
50/50 split was by act id, but the 3 repeats of one act id can still land on
opposite sides, so a held-out verdict row is scored against a confidence whose
sibling repeats were seen in train. Verdict rows carry the most within-act label
disagreement (idea:lm-why-jev-echoes-leaked-verdicts hop 2: ~20 pct of q1
targets self-inconsistent), so this leak inflates verdict ECE specifically.

**Claim:** re-splitting with ALL 3 repeats of an act id forced onto the SAME
side (GroupKFold by act id) drops verdict-subgroup held-out ECE to <= 0.10 on
>= 4/5 seeds.

## Falsifier

Act-blocked (grouped) split leaves verdict held-out ECE > 0.10 on >= 2/5 seeds.
Then the failure is NOT split leakage and the residual is real shape/scale.

## Cost

0 API calls (reuses committed `json_cache_scrub` probabilities and
`acts_replay_scrub.jsonl` labels), 0 GPU, pure NumPy on CPU, < 2 min. <= 1 USD
only if a cached row must be re-derived.

## Experiment that tests it

Extend the TM.57 probe (`probe_ece_pool.py`) to split with `GroupKFold` on act
id (all repeats one side), refit per-group NLL temperature on train, report
held-out verdict/experiment/pooled ECE across seeds 20260918/1/7/42/1234 and
the fitted T. Rows to `bench/<utc>.jsonl`. Compare against the
`bench/20260918T233624Z.jsonl` split-by-act baseline.
