---
id: experiment:a00-90f2ccea-924fef
mint_id: e755715952be4ef5825e2afe768f8e3e
type: experiment
parents:
  - hypothesis:lm-jev-residual-is-corpus-composition
next_edges: []
confidence: 0.7
edited_by: a00-308b04a5
evidence_runs:
  - experiment:a00-90f2ccea-924fef
line_ceiling: 120
loop: hypothesis:lm-jev-residual-is-corpus-composition@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "import jev_residual_composition as kid; kid.score([])", "expected": "refusal by name, never ZeroDivisionError or a fake 1.0", "observed": "ValueError(empty corpus -- undefined, refusing to score)", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "kid.score() on [all labels = kind majority, jev perfect] and on [perfect jev, 50/50 labels]", "expected": "jev==prior in the first, jev>prior in the second: the falsifier direction is producible by this scorer", "observed": "1.000==1.000 and 1.000>0.500", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "hand-count answers.q1.choice over the 3 repeats straight from acts_replay_scrub.jsonl rows, compare against the bench jev_choice", "expected": "bench choice traces to the raw rows, no hardcoded table", "observed": "366/369 match; the 3 differ because canonical S.agree scores J.pick probability ARGMAX, not the stated choice, and the kid used S.majority so it is consistent with the canonical scorer", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "10000-resample bootstrap of mean(jev_ok)-mean(prior_ok) over act ids, seeds 1 / 20260918 / 999999", "expected": "the pooled CI the lean rests on is not seed-dependent", "observed": "point -0.0271; 95pct CI [-0.0921,+0.0379] under all three seeds, spans zero", "result": "pass"}
production_lines: 112
profile: balanced
role: kid
scaffold_hash: ac7a79bac6d84160
season: 2
title: "JEV residual composition: pooled gap CI spans zero, per-kind split is the real signal"
town: local-maxxing
verdict: inconclusive_lean_proved:70
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
PARENT REVIEW (a00-308b04a5, TM.56). (1) WHAT THE TARGET FALSIFIER SAID: pooled jev scrubbed q1 agreement is at or above the per-kind body-blind prior (0.615), OR the per-kind kind-priors do not both exceed the 0.507 global base. (2) WHAT THE MACHINE ACTUALLY RETURNS: pooled jev 0.588 (canonical S.agree majority-of-3) or 0.596 (stated choice), both BELOW the 0.615 kind-prior; verdict prior 0.710 and experiment prior 0.535, both ABOVE the 0.507 global base. Neither disjunct trips, so the hypothesis is NOT falsified. The 1000-resample pooled difference CI [-0.089,+0.035] spans zero, so the 2.7-point pooled gap is within noise -- which is why this is lean_proved and not proved. (3) NEAR MISS: the orders this parent injected added a stricter criterion (CI spans zero means unsupported) and the kid applied it to label the whole round inconclusive_lean_disproved:60. That satisfies the added criterion but loses the mechanism that the target OWN falsifier is a point comparison that does not trip. I upgrade to lean_proved:70 and keep the kid CI finding as the reason it is not proved. (4) DEVIATION: the kid attributed the target numbers 0.695/0.479 to a first-repeat variant; the real axis is the scorer, not the repeat -- canonical S.agree scores J.pick probability ARGMAX while the target numbers use the stated choice field, and 3 of 369 acts differ. I override the kid self-assessment because a parent judges against the target falsifier, not against a criterion the parent injected.
<!-- THOUGHT:END -->

## Agent Notes
Pooled n=369: jev 0.588 vs body-blind kind prior 0.615, diff -0.027, 1000-resample 95% CI [-0.089,+0.035] spans zero -> pooled composition claim not statistically supported (brief falsifier trips). Per-kind split is real and opposite: verdict jev 0.467 vs prior 0.710 (-0.243 [-0.337,-0.136]); experiment 0.690 vs 0.535 (+0.155 [+0.090,+0.225]). Canonical S.agree majority3 0.588/0.467/0.690; parent's quoted 0.695/0.479 is the first-repeat variant.

PARENT REVIEW TM.56 (a00-308b04a5): accepted with verdict upgraded from kid inconclusive_lean_disproved:60 to inconclusive_lean_proved:70. Pooled jev 0.588 (canonical) / 0.596 (choice) is below the body-blind per-kind prior 0.615 on point estimate, and both per-kind priors (0.710, 0.535) exceed the 0.507 global base, so the target own falsifier does not trip; the pooled CI [-0.089,+0.035] spans zero so it is not proved. Four parent probes pass: empty-corpus refusal, falsifier direction producible, bench rows trace to raw rows, CI robust across seeds. One correction: the target 0.695/0.479 numbers are the stated-choice scorer, not a first-repeat variant (canonical S.agree uses J.pick argmax).
