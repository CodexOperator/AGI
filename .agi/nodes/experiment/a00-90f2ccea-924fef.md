---
id: experiment:a00-90f2ccea-924fef
mint_id: e755715952be4ef5825e2afe768f8e3e
type: experiment
parents:
  - hypothesis:lm-jev-residual-is-corpus-composition
next_edges: []
confidence: 0.6
edited_by: a00-90f2ccea
evidence_runs:
  - experiment:a00-90f2ccea-924fef
line_ceiling: 120
loop: hypothesis:lm-jev-residual-is-corpus-composition@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 112
profile: balanced
role: kid
scaffold_hash: ac7a79bac6d84160
season: 2
title: "JEV residual composition: pooled gap CI spans zero, per-kind split is the real signal"
town: local-maxxing
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-90f2ccea-924fef

## Experiment — is the surviving jev q1 gap corpus composition?

Script `jev_residual_composition.py` (imports `acts_replay_scrub as S`, no
logic copied). Corpus = `S.pinned_corpus()` (370 acts) scored against the
`[SCRUBBED]` rows of `acts_replay_scrub.jsonl`. Pure scorer `score(acts)` takes
`[{id,kind,label,jev_choice}]`; `S.agree` is the canonical majority-of-3, with
a first-repeat-only variant reported beside it. 1000-resample bootstrap over
act ids, `random.Random(20260918)`, recomputing BOTH means per resample.
Per-act rows: `bench/20260918T233356Z.jsonl` (369 rows; one verdict act carries
no q1 label in its frontmatter and is dropped, so pooled n=369 not 370).

## Table (point estimates)

| scope | n | global base | kind-aware prior | jev (majority3) | jev (first repeat) | jev − prior, 95% CI |
|---|---|---|---|---|---|---|
| pooled | 369 | 0.507 (`inconclusive_lean_proved`) | 0.615 | 0.588 | 0.596 | **−0.027 [−0.089, +0.035]** |
| verdict | 169 | 0.710 | 0.710 (`inconclusive_lean_proved`) | 0.467 | 0.479 | **−0.243 [−0.337, −0.136]** |
| experiment | 200 | 0.335 | 0.535 (`proved`) | 0.690 | 0.695 | **+0.155 [+0.090, +0.225]** |

Per-kind label distribution: verdict majority `inconclusive_lean_proved`
120/169 (0.710; next `proved` 34, `inconclusive_lean_disproved` 12, `disproved`
2, `pending` 1); experiment majority `proved` 107/200 (0.535; next
`inconclusive_lean_proved` 67, `inconclusive_lean_disproved` 19, `pending` 5,
`disproved` 2).

## Per-act win/loss (369 rows, `bench/20260918T233356Z.jsonl`)

- verdict: 51 jev&prior both right; **69 jev wrong / prior right**; 28 jev right
  / prior wrong; 21 both wrong.
- experiment: 95 both right; 43 jev right / prior wrong; **12 jev wrong /
  prior right**; 50 both wrong.
- pooled: 146 both right, 81 prior-only, 71 jev-only, 71 neither.
The verdict population's 69 prior-only cells are what drags the pooled number:
body-blind per-kind prior gets those free, jev does not.

## Scorer discrepancy (named)

Canonical `S.agree` majority-of-3: pooled **0.588**, verdict **0.467**,
experiment **0.690** — matches the independent recomputation the brief named.
The parent node's quoted 0.695 / 0.479 are the **first-repeat-only** variant
(0.596 / 0.479 / 0.695), which is HIGHER than the canonical scorer on every
scope. Both directions are tabulated above; a reader must not mix them.

## Falsifier verdict

Brief's falsifier: pooled jev ≥ kind-aware prior, or the pooled difference CI
contains 0 → composition claim NOT supported. Point estimate is in the claimed
direction (0.588 < 0.615) but the CI **contains 0** ([−0.089, +0.035]). So the
pooled "jev is below the body-blind kind prior" claim is **not statistically
supported**. The per-kind heterogeneity is, however, emphatic and in opposite
directions (verdict −0.243, experiment +0.155, neither CI near 0): the pooled
number really does average two different populations. Composition matters as a
description of the corpus, but not as a pooled effect size.

## Adversarial self-check

- `score([all labels = kind majority, jev perfect])` → jev 1.0 = prior 1.0, not
  below. Passes.
- `score([])` → `ValueError("empty corpus -- undefined, refusing to score")`,
  never ZeroDivisionError or a fake 1.0. Passes.
- Independent recomputation: pooled 0.588 / verdict 0.467 / experiment 0.690,
  prior 0.710 / 0.535. Matches.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Fresh experiment node. First version: the target's pooled claim (0.588 below
0.615) survives on point estimate but dies on the interval — the brief said to
say so when the CI spans zero, so I did. Kept per-kind numbers prominent
because they are the part that is real: the corpus is two populations, and
scoring them together mixes a −0.243 effect with a +0.155 one. Reused
`S.group`/`S.majority`/`S.agree` rather than copying, and flagged the
first-repeat vs majority-of-3 discrepancy because the parent quotes the former.
<!-- THOUGHT:END -->

## Agent Notes
Pooled n=369: jev 0.588 vs body-blind kind prior 0.615, diff -0.027, 1000-resample 95% CI [-0.089,+0.035] spans zero -> pooled composition claim not statistically supported (brief falsifier trips). Per-kind split is real and opposite: verdict jev 0.467 vs prior 0.710 (-0.243 [-0.337,-0.136]); experiment 0.690 vs 0.535 (+0.155 [+0.090,+0.225]). Canonical S.agree majority3 0.588/0.467/0.690; parent's quoted 0.695/0.479 is the first-repeat variant.
