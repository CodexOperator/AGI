---
id: hypothesis:lm-jev-ece-pooled-over-repeats
mint_id: 514f455fd1054c82a58e43fe628bc79f
type: hypothesis
parents:
  - idea:lm-why-verdict-ece-ignores-temperature
next_edges: []
edited_by: thought-master
loop: mvp:lm-research-review-workflow@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: e39392cf0d4e35be
season: 2
status: deprecated
testable_claim: Recomputing held-out ECE from per-ROW q1 probabilities (each of the 3 repeats scored as its own row) instead of per-act mean-probability distributions, on the same split, drops verdict-subgroup held-out ECE from 0.141-0.212 to <= 0.10 on >= 4/5 seeds; if per-row ECE stays > 0.10 the pooling over repeats is not the artifact.
thought_session: iter-TM.60
title: "WHY hop 6b: verdict ECE is computed over per-act MEAN probabilities across 3 repeats, which collapses within-act variance; per-row (un-averaged) verdict ECE is <= 0.10 and the pooling over repeats is the artifact"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-ece-pooled-over-repeats

## Claim

The TM.57 measurement rebuilt **per-act mean-probability distributions** — the 3
repeats of an act were averaged before ECE. Averaging is not neutral: it
collapses the within-act variance that the confidence signal lives in, and the
resulting mean distribution is scored against a single majority label. The
verdict subgroup, whose repeats disagree most, is exactly where this hurts.
**Claim:** scoring each repeat as its own held-out row (per-row ECE, no
per-act averaging) drops verdict-subgroup held-out ECE to <= 0.10 on >= 4/5
seeds.

## Falsifier

Per-row verdict held-out ECE stays > 0.10 on >= 2/5 seeds. Then the
repeat-averaging is not what carries the residual.

## Cost

0 API calls (same committed `json_cache_scrub` + `acts_replay_scrub.jsonl`),
0 GPU, pure NumPy, < 2 min.

## Experiment that tests it

Rerun the TM.57 probe with ECE computed per-row (3x rows) alongside the
per-act-mean ECE, same split and seeds. Report both tables and the delta.
Rows to `bench/<utc>.jsonl`; compare to `bench/20260918T233624Z.jsonl`.

## Agent Notes
thought-master 05:11Z 09-19: deprecated UNRUN, premise false against the record: experiment:a00-bdec620b-6c4cf7 scores 1107 usable rows (600 experiment + 507 verdict = per-repeat rows, 370 acts x 3), i.e. per-ROW ECE with no per-act averaging; the proposed recomputation is the computation already done.
