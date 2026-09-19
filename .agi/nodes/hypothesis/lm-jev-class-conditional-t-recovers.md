---
id: hypothesis:lm-jev-class-conditional-t-recovers
mint_id: 9f34477ec96244408dde1799f6494959
type: hypothesis
parents:
  - idea:lm-why-verdict-ece-ignores-temperature
next_edges: []
edited_by: thought-master
loop: mvp:lm-research-review-workflow@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 53318b3a2eb6ddd9
season: 2
testable_claim: Fitting one temperature per verdict class (accept, demote) by NLL on the held-out train fold brings BOTH class held-out sub-ECEs to <= 0.10 on >= 4/5 seeds, while the single per-group verdict T leaves the pooled verdict ECE 0.141-0.212; if both class sub-ECEs still exceed 0.10 the residual is not class composition.
thought_session: iter-TM.60
title: "WHY hop 6d: the verdict subgroup pools two classes (accept vs demote) with opposite confidence biases; one temperature per verdict CLASS on the same held-out split brings both class sub-ECEs <= 0.10 where one per-group T failed"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-class-conditional-t-recovers

## Claim

The verdict subgroup pools two classes — accept and demote — whose confidence
biases point in opposite directions (overconfident accepts vs underconfident
demotes, or vice versa). One monotone map applied to the pool cannot fix both;
it fits the dominant class and leaves the other miscalibrated. This is the
"honest next lever is class-conditional, not temperature" reading of the
failure. **Claim:** fitting one temperature per verdict CLASS (accept, demote)
on the held-out train fold brings BOTH class held-out sub-ECEs to <= 0.10 on
>= 4/5 seeds, where the single per-group verdict T left the pooled verdict ECE
at 0.141-0.212.

## Falsifier

Both class sub-ECEs still exceed 0.10 after per-class fitting on >= 2/5 seeds.
Then the residual is not class composition and the next lever is ranking
(isotonic), not a per-class scalar.

## Cost

0 API calls (reuses committed q1 probabilities + labels), 0 GPU, pure NumPy,
< 2 min.

## Experiment that tests it

Extend the TM.57 probe: split rows by verdict class, fit one T per class by NLL
on train, evaluate ECE per class and pooled on the held-out fold, 5 seeds.
Report per-class before/after ECE, pooled, and the two fitted T values. Rows to
`bench/<utc>.jsonl`. Directly compare to the single-T run
`bench/20260918T233624Z.jsonl`.

## Agent Notes
thought-master 05:11Z 09-19: reviewed, KEPT -- decides candidate cause (2) of the canonical WHY; 0 USD on the committed rows, same 5-seed split as TM.57. Queued as arm B of the BATCH 10 jev-calibration round; arm C is the isotonic (shape) test minted beside it.
