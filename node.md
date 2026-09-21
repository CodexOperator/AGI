---
id: hypothesis:lm-jev-classifier-pass-adds-classes-the-graph-lacks
mint_id: 0d3b0318adfb49908e9bcbe16a9ecca6
type: hypothesis
parents:
  - hypothesis:lm-session-data-capture-lands-every-role-under-datasets-sessions
  - goal:g14.10.2
next_edges: []
confidence: 0.4
edited_by: belam
scaffold_hash: c501ce7325b592e1
season: 2
tags:
  - local-maxxing
  - datasets
  - jev
  - classifier
testable_claim: "Over every landed data trunk (kid-sft, jev-typed-acts, trajectories, switch-rule, abl-01, and the new datasets/sessions/ capture once chunk 1 lands), a jev classifier pass adds ONLY the classes the graph does not already carry per record -- act type, reasoning shape (prose vs diagram-maxed), refusal, tool-error, rebrief -- never re-deriving a label the graph-provenance pre-label already supplies. Calibrated against a 200-record hand-checked slice: measured inter-rater agreement between jev's class and the hand label >= 0.80 (Cohen kappa or simple accuracy, whichever the calibration script reports first, named explicitly), cost per record recorded (extrapolated from the town's own triage.py rate, ~0.0004 USD/act, verified not assumed), CPU/API only, no GPU. Depends on chunk 1 (session capture) landing enough real records to calibrate against; the existing kid-sft/jev-typed-acts/trajectories/switch-rule/abl-01 trunks can seed an earlier partial calibration slice before chunk 1 lands, named as the cheaper first sub-step if attempted."
title: "G14.10.2 chunk 2 -- CLASSIFIER PASS: jev adds only the classes the graph lacks (act type, reasoning shape, refusal, tool-error, rebrief), calibrated on a 200-record hand-checked slice, CPU/API only -- waits on chunk 1"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-classifier-pass-adds-classes-the-graph-lacks

## Hypothesis

**Claim:** over every landed data trunk (kid-sft, jev-typed-acts,
trajectories, switch-rule, abl-01, and the new `datasets/sessions/` capture
once chunk 1 lands), a jev classifier pass adds ONLY the classes the graph
does not already carry per record -- act type, reasoning shape (prose vs
diagram-maxed), refusal, tool-error, rebrief -- never re-deriving a label
the graph-provenance pre-label already supplies.

**Measured:** calibrated against a 200-record hand-checked slice --
inter-rater agreement between jev's class and the hand label >= 0.80
(Cohen kappa or simple accuracy, whichever the calibration script reports
first, named explicitly, not silently picked to flatter the number); cost
per record recorded (extrapolated from the town's own `triage.py` rate,
~0.0004 USD/act -- verified against that script when dispatched, not
assumed); CPU/API only, no GPU.

**Falsifier:** agreement stays below 0.80 on the 200-record slice, or the
classifier re-derives a class the graph already supplies instead of adding
a new one (scope creep on the same corpus, not a new signal).

**Blocked on:** chunk 1 (session capture, sibling hypothesis) landing
enough real records to calibrate against. The existing kid-sft /
jev-typed-acts / trajectories / switch-rule / abl-01 trunks can seed an
earlier PARTIAL calibration slice before chunk 1 lands -- named here as the
cheaper first sub-step if a future round wants to start early, not required.

**Not claimed here:** any downstream USE of the added classes (e.g. as
`config:posts` inputs or a training signal for G14.7.2) -- this hypothesis
is the classification pass itself, not its consumers.

**Cost:** the classifier calls themselves are cheap (jev rate, ~0.0004
USD/act); the dispatching parent runs on `pi`/deepseek (cap $1-2 depending
on record count) per the usual round shape, once dispatchable.
