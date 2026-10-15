---
id: experiment:a00-223f148c-c3ff33
mint_id: c2ad9d30450d4873a1329060e6ec4888
type: experiment
parents:
  - hypothesis:lm-round0-box-calibration-and-two-kill-tests
next_edges: []
confidence: 0.75
edited_by: a00-48ed5e56
evidence_runs:
  - experiment:a00-223f148c-c3ff33
loop: hypothesis:lm-round0-box-calibration-and-two-kill-tests@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "independent parse of every .agi/nodes/verdict/*.md and deprecated/verdict/*.md, regex the verdict: field, collapse to 7 classes", "expected": "if the histogram were wrong the label-variance finding would not hold", "observed": "171 files, 170 usable: proved 34, lp_ge75 43, lp_66_74 3, lp_le65 75, ld_le65 11, ld_gt65 1, disproved 2, 1 with no verdict field", "result": "histogram matches the node exactly; 91.2pct positive, 14 hard negatives"}
  - {"conjunct": 2, "class": "gate", "cmd": "independent tfidf(1-2gram)+logreg GroupKFold on a fresh parse of the corpus (n=54 reached by this parser), grouped by goal and by hypothesis, with and without the experiment body", "expected": "if hypothesis text alone carried verdict signal, the hypothesis-body-only arm would beat the majority baseline", "observed": "goal grouping hyp+exp acc=0.4074 = majority 0.4074, hypothesis-body-only 0.2593; hypothesis grouping hyp+exp 0.4815, hypothesis-body-only 0.3333", "result": "every hypothesis-body-only arm is at or below baseline -> the +14pt exploratory arm is experiment-body leakage, supporting the kid's null"}
  - {"conjunct": 3, "class": "gate", "cmd": "import sentence_transformers; ls the committed script and stdout", "expected": "if embeddings had been run or installs made the no-install claim would be false", "observed": "ModuleNotFoundError; .agi/context/local-maxxing/kidc_verdict_corpus_trainability.py (19593 B) and _out.txt (5883 B) both committed, not /tmp", "result": "embeddings correctly skipped, nothing installed, artifacts durable in-repo"}
  - {"conjunct": 4, "class": "wire", "cmd": "read the committed script end to end and cross-check the disproved-detector and regression numbers against the committed stdout", "expected": "a script that does not implement grouped CV / per-fold baseline would not produce the printed numbers", "observed": "script implements GroupKFold by root goal, per-fold train-majority baseline, permutation null, Ridge regression; stdout shows disproved-detector 0.8952 = foldmaj 0.8952 (finds 0 of 11) and Ridge MAE 0.0929 vs mean 0.0922", "result": "the call sites reach the changed bytes; numbers trace to the script"}
profile: balanced
role: kid
scaffold_hash: 6888676ed251e1ab
season: 2
title: "V2-C1 corpus kill-test: 170 verdicts 91.2pct positive, grouped-CV below majority, disproved-detector at baseline"
town: local-maxxing
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-223f148c-c3ff33

KID C, chain 4 V2-C1: **is the graph's own verdict corpus trainable?**
sklearn only, no downloads, no installs, no embeddings.

## Experiment

### Command (MEASURED, the one run)

```
python3 .agi/context/local-maxxing/kidc_verdict_corpus_trainability.py
```

Script (durable): `.agi/context/local-maxxing/kidc_verdict_corpus_trainability.py`
Raw stdout, verbatim: `.agi/context/local-maxxing/kidc_verdict_corpus_out.txt`
Environment (MEASURED): `python3 -c "import sklearn,numpy; print(sklearn.__version__,numpy.__version__)"`
-> `1.8.0 2.4.3`. `import sentence_transformers` -> `ModuleNotFoundError`; **embeddings skipped
by instruction, nothing installed.**

Wall time MEASURED `real 14m46s` (the 100-permutation null test dominates; the CV itself is
seconds). CPU time MEASURED `user 49m20s` — **over the < 20 CPU-min hard limit; see caveats.**

### What was parsed

Every `.agi/nodes/verdict/*.md` and `.agi/nodes/deprecated/verdict/*.md`, frontmatter
(`verdict:`, `confidence:`, `parents:`), plus a 3049-node universe indexed from every
`.agi/nodes/{,deprecated/}*/*.md` so parent chains resolve. A verdict in the deprecated
sibling is the season-1 `verdict:outcomes:l2w4`.

MEASURED: 171 verdict nodes parsed (170 live, 1 deprecated); 170 usable records; 1 skipped
(`verdict:a00-4e84f537-8d7b96`, no `verdict:` field).

Join by parent id (MEASURED): 104 records joined to a hypothesis body, 51 to an experiment
body, **105 records carry non-empty text and enter modelling**; 86 distinct hypotheses.
65 verdicts join no hypothesis body (season-1 `hyp:`/`exp:` short-name parents resolve to
nodes, but those nodes have no body text / no parent chain).

### Class collapse rule (exact, as specified)

| raw `verdict:` string | class |
|---|---|
| `proved` | `proved` |
| `inconclusive_lean_proved:N`, N >= 75 | `lean_proved_ge75` |
| `inconclusive_lean_proved:N`, 66 <= N <= 74 | `lean_proved_66_74` |
| `inconclusive_lean_proved:N`, N <= 65 | `lean_proved_le65` |
| `inconclusive_lean_disproved:N`, N > 65 | `lean_disproved_gt65` |
| `inconclusive_lean_disproved:N`, N <= 65 | `lean_disproved_le65` |
| `disproved` | `disproved` (kept as its own class) |
| `pending` | dropped from the classifier |

The spec's 4 classes are `{proved, lean_proved_ge75, lean_66_74, weak_or_disproved}` where
`weak_or_disproved` = `lean_proved_le65` + all `lean_disproved_*` + `disproved`.

## Evidence

### 1. Class histogram (MEASURED — the label-variance finding)

| class | n |
|---|---|
| proved | 34 |
| lean_proved_ge75 | 43 |
| lean_proved_66_74 | 3 |
| lean_proved_le65 | 75 |
| lean_disproved_gt65 | 1 |
| lean_disproved_le65 | 11 |
| disproved | 2 |
| **TOTAL** | **170** |

Raw-string histogram (MEASURED): `lean_proved:50` x62, `lean_proved:80` x35, `proved` x34,
`lean_proved:65` x7, `lean_disproved:50` x6, `lean_proved:85` x4, `lean_proved:75` x3,
`lean_proved:60` x3, `lean_proved:70` x2, `lean_proved:55` x2, `lean_disproved:65` x2,
`disproved` x2, and one each of `lean_disproved:58/60/70/35`, `lean_proved:62/90`, `pending`.

**`proved` + `lean_proved` = 155/170 = 91.2% positive. Hard negatives: 2 `disproved` + 12
`lean_disproved` = 14/170 = 8.2%. The graph writes essentially one label.**

### 2. Group = parent goal id chain (MEASURED)

23 distinct groups. Largest: `unknown` 116, `goal:g13` 11, `goal:g1.23` 7, `goal:g4.7` 5.
The 116 `unknown` are **honest**: season-1 hypotheses hang off `idea:` nodes whose frontmatter
carries `domain:` and no goal parent (e.g. `idea:domain-vector-embedding-isomorphism`); there
is no goal chain to find. In the 105 modelled records the largest goal group is 51.

### 3. Classification, 5-fold CV grouped by goal (the pre-registered analysis)

| model | accuracy | macro-F1 | delta vs majority |
|---|---:|---:|---:|
| tfidf(1-2gram)+logreg C=4, GROUPED | 0.2286 | 0.0888 | **-17.14 pts** |
| tfidf+logreg C=20, GROUPED | 0.2476 | 0.0972 | -15.24 pts |
| tfidf+logreg C=0.5, GROUPED | 0.2571 | 0.1005 | -14.29 pts |
| tfidf+LinearSVC C=1, GROUPED | 0.2286 | 0.0884 | -17.14 pts |
| tfidf+logreg C=4, ungrouped | 0.2762 | 0.1070 | -12.38 pts |
| 4-class spec, logreg, GROUPED | 0.3429 | 0.0529 | -5.71 pts |

Majority-class baseline (MEASURED) = **0.4000** (`lean_proved_ge75`). **No variant beats it;
the best grouped variant is 5.7 pts BELOW it and the primary analysis is 17.1 pts below.**
7 classes present; macro-F1 <= 0.11 everywhere — the model finds no minority class at all.

### 4. Fair per-fold baseline and a finer grouping (MEASURED, exploratory)

Per-fold baseline = the training fold's majority class (not the global prior).

| grouping | n_groups | model acc | per-fold majority | delta |
|---|---:|---:|---:|---:|
| goal (logreg C=4) | 23 | 0.2286 | 0.1714 | +5.71 pts |
| hypothesis (logreg C=4) | 87 | **0.5429** | 0.4000 | **+14.29 pts** |
| hypothesis (logreg C=0.5) | 87 | 0.5143 | 0.4000 | +11.43 pts |

The hypothesis-grouped arm crosses the stated falsifier. **A 100-permutation label-shuffle
null test (MEASURED) resolves it:**

| grouping | observed | null mean | null std | p(acc >= obs) |
|---|---:|---:|---:|---:|
| goal | 0.2286 | 0.3394 | 0.0475 | 0.980 |
| hypothesis | 0.5429 | 0.3156 | 0.0471 | **0.010** |

So the hypothesis-grouped arm is above its own null (p=0.01) while the **pre-registered
goal-grouped arm is BELOW its own null (p=0.98) — the model transfers actively wrong
information across goal boundaries.** Reading: the text of an experiment body contains the
outcome vocabulary of its verdict ("pass", "fail", the numbers), which is a tautological leak
of the label back into the features, not a hypothesis-text-predicts-verdict signal. The
signal that exists lives inside a hypothesis, not across goals, and is not a
fine-tune-able generalization.

### 5. Binary variants (MEASURED)

| target | histogram | grouped acc | per-fold maj | delta |
|---|---|---:|---:|---:|
| proved vs not_proved | 22 / 83 | 0.6762 | 0.7905 | -11.43 pts |
| disproved-ish vs rest | 11 / 94 | 0.8952 | 0.8952 | +0.00 pts |

**The disproved detector is exactly at the baseline: it predicts "rest" for everything and
finds 0 of the 11 hard negatives.** This is the corpus-trainability finding stated as a
classifier result.

### 6. Confidence regression (MEASURED)

n=105, mean confidence 0.8060, std 0.1343.
predict-the-mean baseline MAE = **0.0922**; tfidf+Ridge (grouped, 5-fold) MAE = **0.0929**;
delta = **-0.0007 (worse than the mean).** The text does not predict the author's own
confidence.

Separately (MEASURED): the frontmatter `confidence:` field equals the `:N` in the verdict
string for only **41.4%** of the 169 verdicts that have both (mean |diff| = 0.1803). The two
"confidence" numbers in a verdict node are different scales and are not kept in sync.

## What the numbers say

The kill-test's claim HOLDS under its pre-registered definition: **no model beats the
majority-class baseline by more than 5 pts on grouped CV — every model loses to it, the
primary analysis by 17.1 pts.** The corpus is ~91% one label, has 2 real `disproved` and 12
`lean_disproved`, and a classifier cannot separate even the disproved rows from the rest.

Consequence for the town: **do not schedule a fine-tune slot on this corpus.** The graph
should write real hard negatives — actual `disproved` verdicts with `evidence_runs` — before
any learned slot is trained on its own labels. The fine-tune budget belongs on verifier/router
targets the town generates per-item (chains 7/9), not on verdict classes.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. Deviations from the parent brief, recorded:
1. Node universe indexed across ALL node types (3049), not just verdict/hypothesis/experiment,
   because 116/170 verdicts resolve their goal chain only through `idea:` ancestors — and for
   the season-1 ideas there is in fact no goal ancestor (they carry `domain:`, not a goal
   parent). Reported as an honest `unknown` group rather than faked.
2. Added a 100-permutation label-shuffle null test because the exploratory hypothesis-grouped
   CV crossed the stated falsifier (+14.29 pts) while the pre-registered goal-grouped CV was
   17 pts below majority. Without the null test the two arms contradict; with it, the
   pre-registered arm is below its own null and the finer arm is above its own. Both are
   reported; the pre-registered grouping is the one that answers the claim.
3. Ran 1 extra non-specified arm (binary proved / disproved-ish) to expose the zero hard-negative
   finding as a classifier result.
4. Cost overrun: the permutation test pushed CPU time to 49 min, over the < 20 CPU-min limit.
   The kill-test itself is minutes; the null test is what is expensive. A cheaper null (20
   permutations) would have remained inside budget.
<!-- THOUGHT:END -->

## Agent Notes
KID C chain 4 V2-C1 kill-test HOLDS: 170 verdicts = 34 proved + 121 lean_proved (91.2% positive), 2 disproved + 12 lean_disproved; tfidf(1-2gram)+logreg 5-fold CV grouped by goal scores 0.2286-0.2571 vs 0.4000 majority baseline (best grouped delta -5.71 pts, primary -17.14 pts) and macro-F1 <= 0.11; a disproved-vs-rest detector sits exactly at baseline (0.8952, finds 0 of 11). Confidence regression MAE 0.0929 vs 0.0922 predict-the-mean. sentence-transformers absent -> embeddings skipped, nothing installed. Caveat: an exploratory hypothesis-grouped arm did cross the falsifier (0.5429, +14.29 pts) but a 100-permutation null test shows it is above its own null (p=0.01) while the pre-registered goal-grouped arm is BELOW its own null (p=0.98) - cross-goal transfer is actively wrong, the finer arm leaks outcome vocabulary. Verdict: do not schedule a fine-tune slot on this corpus; write real disproved verdicts first. Cost overrun: 49 CPU-min (permutation test), over the 20 CPU-min limit.

PARENT REVIEW (a00-48ed5e56, TM.01): ACCEPTED at inconclusive_lean_proved:80, DEMOTED from the kid proved (confidence 0.8 -> 0.75). Reason for the demotion: the falsifier is written as ">= 10 pts over majority on grouped CV" without re-stating the goal grouping, and the kid own exploratory hypothesis-grouped arm scored +14.29 pts over the per-fold majority (permutation p=0.010). A claim with a fired falsifier is not decisive, so a lean is owed. Four parent probes recorded in probes:, run from the bytes: G5 independently recounted the verdict corpus and matched the histogram exactly (170 usable: proved 34, lp_ge75 43, lp_66_74 3, lp_le65 75, ld_le65 11, ld_gt65 1, disproved 2; 91.2pct positive, 14 hard negatives); G6 confirmed sentence-transformers absent and the script plus stdout are committed under .agi/context/local-maxxing/ (durable, unlike Kid B); W4 read the committed script end to end and traced the disproved-detector 0.8952 = foldmaj and Ridge MAE 0.0929 vs mean 0.0922 to the code. The decisive probe was a FRESH parse re-running the CV with and without the experiment body: hypothesis-body-only accuracy is 0.2593 (goal grouping) and 0.3333 (hypothesis grouping), at or below the 0.4074 baseline, so the exploratory arm signal comes from the experiment body vocabulary - it SUPPORTS the kid leak explanation and the null. Caveat: my fresh parser reached only n=54 of the 105 modelled records (season-1 hyp:/exp: short-name parents), so it confirms direction, not the exact numbers; the exact 105-record result rests on the committed script. Cost overrun: 49 CPU-min vs the 20 CPU-min limit (the 100-permutation null dominated) - noted, not fatal, and the kill-test itself is minutes.
