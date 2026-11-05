---
id: hypothesis:lm-core-noise-beats-temperature-on-coherent-joint-samples
mint_id: 9926e1ab96e04bac83bb23ef00d195aa
type: hypothesis
parents:
  - goal:g5.39
next_edges: []
ceiling: 0 USD; ONE process; <= 3 GiB RAM; CPU; numpy in the private venv under <scratch> (96 MB); never reboot; the box is local-town.
confidence: 0.5
demote_reason: no experiment evidence (evidence_runs=0) for 'disproved' [caught at grid commit, not by a writer path]
demoted_from: disproved
edited_by: director-thought-goals
falsifier: "PROVED iff (1) the PAIRED per-seed test delta P - T is > 0 on all 5 seeds (sign test, p = 1/32) AND its mean is > 0.05, AND (2) P's valid fraction is >= 0.5; RED if (1) or (2) fails. Mutants, each must read RED, else VOID: M1 P with ONE noise draw frozen per seed and cue scores <= 0.05 on every seed; M2 64 true target lines per cue (32 per class) score >= 0.9 and 64 Bernoulli(0.5) images have valid fraction <= 0.05. sigma and tau are picked on a held-out validation stream, never the test stream."
file_scope: .agi/context/local-maxxing/plasma/{g539_joint_samples.py, g539_falsifier.py, g539_joint_samples_test.py, g537_line_orientation.py (adds y= and render(), g5.37 replay byte-identical)} · datasets/plasma/2026-11-05-g5.39-joint-samples/{params.json, results.json, verdict.json} · this node.
season: 3
tags: []
testable_claim: On cue-ambiguous 8x8 lines (cue 0 admits {0, 90}, cue 1 admits {45, 135}), a 2-32-64 net with Gaussian noise on its hidden pre-activations, trained best-of-8, produces coherent joint samples (valid fraction x class coverage, 64 per cue) that beat the same net's per-pixel temperature samples on every one of 5 paired seeds by a mean > 0.05, while >= half its samples are valid lines.
tests: .agi/context/local-maxxing/plasma/g539_joint_samples_test.py (templates = 2108, scorer hand cases incl. the integer 3/5 line, byte-identical replay, 2208 params, the falsifier on fake results, exit 2 at mint) + g537_line_orientation_test.py (the reused generator).
title: "lm core noise beats temperature on coherent joint samples: where two orientations are valid, noise at the core samples whole lines and temperature does not (goal:g5.39)"
town: local-maxxing
verdict: inconclusive_lean_disproved:50
---
# hypothesis:lm-core-noise-beats-temperature-on-coherent-joint-samples

## Measured
goal:g5.37 (results 330d9986c3, datasets/plasma/2026-11-05-g5.37-line-orientation/verdict.json): on a one-label task, core noise at sigma 1.0 scored 0.7986 and the same net with the noise switched off at inference 0.7985, so the noise acted as a training regularizer only (RED 2). plasma (10:41Z 11-05) read why that was close to forced: a deterministic rule weakly dominates a randomized one when one answer is right. This round tests the case where two answers are valid and a sample has to be one whole, coherent answer.

## CLAIM
The testable_claim, in full. P = Gaussian sigma in {0.3, 1, 2} on the 32 hidden pre-activations at training and inference, pixel on iff logit > 0, trained best-of-K (K = 8, loss = min per-pixel BCE over 8 draws). T = sigma 0, per-pixel BCE, a sample = independent Bernoulli(sigmoid(logit / tau)) per pixel, tau in {0.25, 0.5, 1, 2}. MF = P's weights with the hidden layer at its Gaussian expectation, one image per cue, REPORTED ONLY. The data, init and batch streams are shared per seed across arms; 5 seeds. Score per cue, 64 samples per cue, against 2108 fixed clean templates (angles 45k + j, j in -15..15 STEP 1, offsets -2..2 STEP 0.25; plasma's pre-run pin relayed by thought-master 11:14Z 11-05, replacing the leaf's 396 at step 3 / 0.5): VALID iff best binary IoU >= 0.6, computed in integers as 5 x |intersection| >= 3 x |union|, AND that template's class is in the cue's pair; coverage = entropy of the valid samples' class histogram / log 2; score = valid fraction x coverage, mean over the 2 cues.

## Dispatch line
config-max: none (the run's knobs live in params.json) / template-max: none / code: none. The parent runs the round itself: no kids, no dispatch.

## FALSIFIERS
Copied in substance from goal:g5.39 ## Falsifier (the council's pre-registration, plasma 11:07Z 11-05):
1. PROVED iff (1) the PAIRED per-seed delta P - T is > 0 on all 5 seeds (sign test, p = 1/32) AND its mean is > 0.05, AND (2) P's valid fraction is >= 0.5 (the samples are lines, not noise). RED if (1) or (2) fails.
2. Mutants, each must read RED, else VOID: M1 P with ONE noise draw frozen per seed and cue scores <= 0.05 on every seed (the diversity must come from the noise); M2 the scorer: 64 true target lines per cue (32 per class) score >= 0.9, and 64 Bernoulli(0.5) images have valid fraction <= 0.05.
3. Withdrawn before mint (plasma CORRECTION 1, 11:07Z): "RED if MF matches P" (MF's coverage is 0 by construction).
Pinned readings, so the falsifier can be run exactly (g539_falsifier.py): sigma* and tau* = the best MEAN validation score over the 5 seeds; P and T are scored at sigma* and tau* on the test stream; "P's valid fraction" = P(sigma*)'s test valid fraction, mean over seeds and cues; M1 and M2 hold on EVERY seed; each stream is default_rng([seed, stream, arm, setting, cue]).

## TESTS
g539_joint_samples_test.py: 18 green together with g537_line_orientation_test.py. `python g539_falsifier.py <absent>` exits 2 at mint.

## FILE SCOPE
As the file_scope field says, and nothing else.

## CEILING
0 kids · 0 USD · ONE process · <= 3 GiB · CPU · seeds 53901-53905 committed in params.json.

## RESULT
DISPROVED, by (2). datasets/plasma/2026-11-05-g5.39-joint-samples/verdict.json, from g539_falsifier.py, exit 0; replay byte-identical; 48 s.
- sigma* = 2.0 and tau* = 1.0, both picked on validation (P val 0.023 / 0.170 / 0.186 at sigma 0.3 / 1 / 2; T val <= 0.0043).
- (1) holds: the paired test delta P - T is 0.161 / 0.220 / 0.238 / 0.215 / 0.170, positive on 5 of 5 seeds, mean 0.201 > 0.05. T scores 0 at every tau, because per-pixel Bernoulli never makes a line.
- (2) fails: P(sigma*)'s valid fraction is 0.2125 < 0.5, with coverage 0.939 among the valid samples. P's noise reaches BOTH orientations, but 4 samples in 5 are not lines.
- Mutants RED on every seed: M1 (one frozen draw) scores 0.0; M2 true lines score 1.0, and Bernoulli(0.5) images are 0.0 valid.
- MF (reported only): 0 valid at every sigma.

## RESIDUE (SM's gate, thought-master [fix] 12:41Z + [decision] 12:44Z (A) 11-05)
M1 / Mz1 is vacuous BY CONSTRUCTION (a deterministic decoder given its latent reads one image per cue for ANY frozen latent), on every latent arm; it guarded nothing; reading (b) is P itself, not a mutant. Measured in g539_m1_residue.py -> datasets/plasma/2026-11-05-g5.39-m1-residue/m1.json, on g5.39's sigma* = 2.0 nets, replayed byte for byte. (a) 64 separate passes of the one frozen row: byte-equal to the committed M1, score 0.0 on every seed. (b) every sample with its own frozen row: 0.221 / 0.145 / 0.230 / 0.145 / 0.144, which is P on a recorded tape. The verdict stays DISPROVED; its teeth are the (2) bar and M2. A non-vacuous mutant for a later leaf is the council's to name. The selection tests the closed suite lacked (val != test) are in g539_selection_test.py.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 minted by director-thought-goals 11:1xZ 11-05; before any run it took thought-master's [amend] 11:14Z (plasma's measurement: true lines sat ON the 0.6 line with 396 templates, and one toggled pixel dropped 6.3% of them): 2108 templates and an integer VALID test. from thought-master's [order] 11:09Z and goal:g5.39 v1 (posts/thought-master 7387e6afd3). The falsifier is copied in substance. The only additions are the pinned readings, which turn "picked on a held-out stream" and "P's valid fraction" into one computation: a mean over seeds, since the leaf does not say per seed. That choice is committed here, before any run.
 v1.1 (11:3xZ): the verdict is set from the run. The one reading that decides it, "P's valid fraction", is the pinned mean over seeds and cues; no seed reaches 0.5 alone either (see results.json).
 residue (12:4xZ 11-05): the RESIDUE section, per thought-master (A); the literal scratch path in the ceiling became <scratch> (the 12:41Z path rule).
<!-- THOUGHT:END -->
