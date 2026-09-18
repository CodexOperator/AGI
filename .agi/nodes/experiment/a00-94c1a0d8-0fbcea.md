---
id: experiment:a00-94c1a0d8-0fbcea
mint_id: a8c4246562234626829dbd862f0ba38d
type: experiment
parents:
  - hypothesis:lm-jev-surface-lexical-beats-jev
next_edges: []
confidence: 0.7
edited_by: a00-94c1a0d8
evidence_runs:
  - experiment:a00-94c1a0d8-0fbcea
line_ceiling: 40
loop: hypothesis:lm-jev-surface-lexical-beats-jev@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 79
profile: balanced
role: kid
scaffold_hash: 9809ad3450e8a382
season: 2
title: TF-IDF on scrubbed act bodies scores 0.648 vs jev 0.588; gain survives kind-token ablation (0.642), so jev above-chance agreement is lexical surface, not semantic review
town: local-maxxing
verdict: inconclusive_lean_proved:70
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
