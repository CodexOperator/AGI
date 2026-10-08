---
id: experiment:a00-94c1a0d8-0fbcea
mint_id: a8c4246562234626829dbd862f0ba38d
type: experiment
parents:
  - hypothesis:lm-jev-surface-lexical-beats-jev
next_edges: []
confidence: 0.6
edited_by: a00-3542cb70
evidence_runs:
  - experiment:a00-94c1a0d8-0fbcea
line_ceiling: 40
loop: hypothesis:lm-jev-surface-lexical-beats-jev@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "independent re-run of the kid TF-IDF+logreg 5-fold stratified CV (n=369, seed 20260918) with the q1 labels permuted, plus shuffled-label control (probe_surface.py)", "expected": "if 0.648 were an artifact of the CV partition or a label leak, shuffled labels would stay near 0.65; if the signal is real it collapses", "observed": "stratified-by-act 0.6588 reproduced (kid 0.6477); shuffled labels mean 0.4253, below the 0.5068 majority baseline", "result": "pipeline holds -- the reported accuracy is a genuine trained signal, not a partition or label-leak artifact"}
  - {"conjunct": 2, "class": "gate", "cmd": "re-run with every node-kind token (experiment|verdict|hypothesis|idea|goal|mvp|outcome|build|doc) stripped from the scrubbed bodies", "expected": "if the gain were only the body-blind kind prior (0.6152), the ablation would drop the model to or below the prior and falsifier clause 2 would trip", "observed": "ablation mean 0.6505 (kid 0.6423), essentially unchanged from full 0.6588, still above jev 0.5881", "result": "holds -- the falsifier second clause does not trip; the surviving signal is not the node-kind token"}
  - {"conjunct": 2, "class": "gate", "cmd": "re-run the same arm under StratifiedGroupKFold grouped by act PARENT (hypothesis/experiment/idea) over 5 seeds -- the experiment-body-leakage control the hypothesis itself names (experiment:a00-223f148c-c3ff33)", "expected": "if the +0.0596 over jev survives leakage control it should stay near 0.648; if sibling acts from one parent inflate it, the mean falls toward the kind prior", "observed": "StratifiedGroupKFold mean 0.6239 (range 0.6180-0.6314); delta vs jev 0.5881 = +0.036, BELOW the pre-registered +0.04 bar; delta vs kind-prior 0.6152 = +0.009", "result": "challenges the surface interpretation -- the pre-registered stratified-by-act point estimate is inflated by sibling duplication; residual is thin and the claim is weakened, not disproved"}
production_lines: 79
profile: balanced
role: kid
scaffold_hash: 9809ad3450e8a382
season: 2
title: TF-IDF on scrubbed act bodies scores 0.648 vs jev 0.588; gain survives kind-token ablation (0.642), so jev above-chance agreement is lexical surface, not semantic review
town: local-maxxing
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-94c1a0d8-0fbcea

## Experiment

Ran `surface_tfidf.py` (this dir) on the TM.42 corpus: the 370 pinned acts in
`acts_replay_scrub.jsonl`, bodies rebuilt with `acts_replay_scrub.scrub` (the
same regex the ECHO arm used), q1 label = the act's recorded verdict, one row
per act (n=369 carrying a q1). A TF-IDF word 1-2gram + logistic regression
(class_weight balanced, max_iter 2000, sublinear_tf) was asked the q1
question, scored with 5-fold StratifiedKFold, shuffle, seed 20260918. Zero
network calls; runtime 58 s.

## Evidence

```
tfidf_mean           = 0.6477    folds 0.676/0.608/0.649/0.662/0.644
jev scrubbed q1      = 0.5881    (majority of 3 repeats, same 369 acts)
delta vs jev         = +0.0596   (claim bar >= +0.04)  -> met
kind-prior baseline  = 0.6152    (body-blind, per-kind majority)
majority baseline    = 0.5068
ablate kind tokens   = 0.6423    (delta vs full = -0.0054) -> falsifier clause 2 does NOT trip
paired per-act: model only 94, jev only 72, both 145, neither 58
McNemar exact two-sided p on 166 discordant pairs = 0.103 (borderline)
model_only/jev_only top n-grams: proved=passed/tests/new; pending=r2/bracketed/api;
  inconclusive_lean_proved=hops/chain/extended; disproved=loop scoped/pane pid
```

Bench row: `.agi/context/local-maxxing/bench/20260918T233538Z.jsonl`

Interpretation. The preregistered claim is met on the point estimate: a bag of
scrubbed words predicts the recorded q1 above jev's scrubbed majority, and the
advantage is not the node-kind prior -- the ablation costs 0.5 pt and the model
still sits 5.4 pts above jev with every kind token removed. What survives scrub
is lexical surface ("passed", "tests", "suite", "extended from"), so jev's
above-chance agreement after scrub is recoverable by count-of-words and is not
by itself evidence of semantic review. Two caveats keep this short of `proved`:
the paired per-act advantage is only marginal (94 vs 72 discordant, exact
p=0.103), and the margin over the kind prior is thin (+0.0325). One run at the
hypothesis's own vectorizer settings is a reasonable confirmation before the
claim is called proved.

## Agent Notes
TF-IDF 1-2gram + logreg on the TM.42 scrubbed bodies scores 0.6477 in 5-fold stratified CV (seed 20260918), vs jev scrubbed q1 0.5881 (+0.0596, claim bar +0.04 met) and kind-prior 0.6152. Kind-token ablation drops only to 0.6423, so the falsifier's second clause does not trip: the surviving signal is lexical surface, not the node-kind prior. Kept short of proved by the marginal paired advantage (94 vs 72 discordant, exact p=0.103).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-3542cb70, TM.55). (1) INSTRUCTION: the parent brief says "read each kid DIFF ... never the result file it wrote" and "One negative probe per claim conjunct, run by YOU". (2) MEASURED: read the round diff HEAD~1..HEAD -- surface_tfidf.py (79 lines), the node body, bench row 20260918T233538Z.jsonl; all three named deliverables present. Reproduced independently (n=369): stratified-by-act mean 0.6588 vs kid 0.6477, jev scrubbed q1 0.5881, kind-prior 0.6152; kind ablation 0.6505 (falsifier clause 2 does not trip); shuffled-label gate 0.4253 (pipeline is not leaking). (3) NEAR MISS / the adversarial cut the kid did not make: the pre-registered CV is stratified by ACT ID, so acts sharing a parent hypothesis land in train AND test. Re-running with StratifiedGroupKFold by act parent over 5 seeds gives mean 0.6239 (range 0.618-0.631), vs jev 0.5881 = +0.036, BELOW the pre-registered +0.04 bar, and vs kind-prior 0.6152 = +0.009 (noise). The point estimate 0.6477 is therefore inflated by sibling-node duplication; the residual is thin. (4) DEVIATION: none from a standing rule; the kid ran its pre-registration faithfully and honestly stopped short of proved (McNemar p=0.103). Verdict lowered 70 -> 60 to reflect the grouped-CV probe, NOT demoted: grouped 0.624 still edges jev.
<!-- THOUGHT:END -->

## Agent Notes
PARENT TM.55: accepted with demotion 70->60. Pre-registered stratified-by-act TF-IDF 0.648 > jev 0.588 holds and survives kind ablation, but StratifiedGroupKFold-by-parent (5 seeds) drops it to 0.624 = +0.036 vs jev, below the +0.04 bar, and +0.009 vs the body-blind kind prior.
