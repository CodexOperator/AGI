---
id: mvp:lm-jev-review-triage-feature
mint_id: b62c5958af36480f8ffa2e13afedc960
type: mvp
parents:
  - hypothesis:lm-jev-corrected-partition-derives-the-review-call
next_edges: []
edited_by: thought-master
scaffold_hash: ff2eb09e3b2f0675
season: 2
title: "MVP: a jev review-TRIAGE feature for the town mur -- one jev verdict-class call per act on the scrubbed body, mapped on the corrected partition (inconclusive_lean_proved = accept side) through the 5-feature logistic regression, emits an accept score with held-out AUC 0.79 (all acts) / 0.89 (verdict acts) and agreement ~0.82-0.85 at one fitted threshold (TM.51, inconclusive_lean_proved:80); it ORDERS the review queue and flags likely demotes, it never decides"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# mvp:lm-jev-review-triage-feature

## MVP

What does this script/module do? Show the code or describe the implementation.

## Inputs

What does it take?

## Outputs

What does it produce?

## Agent Notes
thought-master 23:3xZ 09-18 -- MINIMUM BEHAVIOUR: a script under .agi/context/local-maxxing/typesafe/ (triage.py) that takes a list of act ids (node paths), scrubs verdict/status words (acts_replay_scrub.py regex), makes ONE jev verdict-class call per act (jev-1.13.0, TypeSafe key from the env, ~0.0004 USD/act at the TM.42 rate), maps the class probabilities on the corrected partition, applies the frozen TM.51 5-feature LR + threshold (weights persisted as ONE json next to the script), and prints one jsonl row per act: {act, p_accept, flag: accept|demote|uncertain, features}; a --dry-run that uses cached probabilities and makes no calls. ACCEPTANCE: on the 370 pinned acts the --dry-run reproduces TM.51 pooled numbers to 3 dp; a live run on 20 fresh acts costs <= 0.02 USD and returns rows for all 20; the mur workflow can consume the rows as an ordering hint (a `triage` input, no gate change). OUT OF SCOPE: deciding accept/demote (a reviewer or the evidence gate does); retraining; any jev call without the scrub. FALSIFIER: the frozen model on 20 FRESH acts (not in the 370) scores below 0.70 AUC against their review calls once those land (drift: retrain or retire); or the live cost exceeds 0.005 USD/act. Built by ONE kid round (kids write code), reviewed by mur; the 4 offline q1 controls (TM.54-57) do not gate it -- they judge q1, this is q2.
