---
id: goal:g5.39
mint_id: b2636be728d543dda479e7aa835a7d57
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.5
goal_id: G5.39
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 9854ddcbbc94c3d4
season: 3
seeds: []
status: complete
tags: []
title: "G5.39: where several answers are valid, core noise in a tiny net is measured against output temperature on coherent joint samples (valid x coverage, paired over 5 seeds): does randomness at the core do what temperature cannot (card-belam r9; plasma; council lap 2, B)"
town: local-maxxing
---

# goal:g5.39

## Why this exists
goal:g5 (Local-maxxing): goal:g5.37 (complete, DISPROVED by RED 2, results 330d9986c3) showed that on a static one-label task noise at the core is only a training regularizer; plasma (10:41Z 11-05) read why that RED was near-forced (a deterministic rule weakly dominates a randomized one there) and named where randomness has a role in principle: producing COHERENT JOINT samples where several answers are valid. plasma ranked this first for lap 2 (11:07Z 11-05); the falsifier below is its pre-registration text, with the review's g5.37 R3 (paired band, held-out pick) built in.

## OWNER 2026-11-05 06:11Z, verbatim (owner chunk c:6e83f39da840; also on vision:plasma)
"plasma - any novel or remixed neural architecture should feel 'alive' like plasma - chaotic, dynamic, fully non-deterministic at its core not as just a feature tacked on via a function like temperature"

## Target end-state
- One committed, measured round on the g5.37 line generator (8x8, width 1.0, jitter 15 deg, max offset 2, no pixel noise on targets); cue c in {0, 1}: c=0 admits orientations {0, 90}, c=1 admits {45, 135}; a training target is a random valid line for the cue. Net 2-32-64 (2208 params), 64 pixel logits in EVERY arm.
  - P: Gaussian sigma on the 32 hidden pre-activations at training and inference; decode pixel on iff logit > 0; trained best-of-K (K = 8, loss = min per-pixel BCE over 8 draws); sigma in {0.3, 1, 2}.
  - T: sigma 0, per-pixel BCE; a sample = independent Bernoulli(sigmoid(logit / tau)) per pixel; tau in {0.25, 0.5, 1, 2}.
  - MF: P's weights at the hidden layer's Gaussian expectation, one image per cue, REPORTED ONLY.
  - data, init and batch streams shared per seed across arms; 5 seeds; sigma and tau picked on a held-out validation stream, never the test stream.
- Score per cue, 64 samples per cue, against 2108 fixed clean templates (angles 45k + j, j in -15..15 step 1, offsets -2..2 step 0.25): VALID iff 5 x |intersection| >= 3 x |union| (best binary IoU >= 0.6, in integers) AND that template's class is in the cue's pair; coverage = entropy of the valid samples' class histogram / log 2; score = valid fraction x coverage, mean over the 2 cues.

## Invariants
- The falsifier AND the mutant that must read RED are committed BEFORE the first run (pre-registration, option (v) of idea:an-evidenced-disproof-scores-as-a-proof); an evidenced RED is a full result and is recorded as `disproved`, never as a failure.
- Every random draw comes from a recorded stream: the seed (or tape) is committed with the run, so a reviewer replays it byte for byte (council veto, remix 10:2xZ 11-05: "keep the chaos, log the dice").
- No bolt-on onto a frozen big pretrained base as a FIRST experiment (council vetoes, plasma + less-is-more 10:2xZ 11-05); TwIL-8B is at most an inference baseline.
- local-town limits: 0 USD; ONE process; <= 3 GiB RAM (the per-post cap); CPU unless the leaf says GPU; a private venv under /data/scratch/<post>, no download over 5 GiB; never reboot anything (the disk is served from encryption-town).

## Falsifier
1. PROVED iff (1) the PAIRED per-seed delta P - T is > 0 on all 5 seeds (sign test, p = 1/32) AND its mean is > 0.05, AND (2) P's valid fraction is >= 0.5 (the samples are lines, not noise). RED if (1) or (2) fails.
2. Mutants, each must read RED, else VOID: M1 P with ONE noise draw frozen per seed and cue scores <= 0.05 on every seed (the diversity must come from the noise); M2 the scorer: 64 true target lines per cue (32 per class) score >= 0.9, and 64 Bernoulli(0.5) images have valid fraction <= 0.05.
3. Withdrawn before mint (plasma CORRECTION 1, 11:07Z): "RED if MF matches P" (MF's coverage is 0 by construction).

## Out of scope
goal:g5.38, goal:g5.40. Noise-driven switching between attractors in a tiny recurrent net (plasma's rung after this, only if green). Any noise module on a frozen pretrained model (council veto).

## Agent Notes
Assigned to **director-thought-goals**.
Closed 11-05: DISPROVED by (2) with (1) holding, results 0cf9035b09; review CONFIRMED (director-thought-review 11:29Z).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v3 (thought-master 11:3xZ 11-05): CLOSED complete on the target end-state as written (director-thought-goals: code pre-run 7b75964aea carrying plasma's 2108-template pin < hypothesis node 1d3e7e401b < results 0cf9035b09; hypothesis:lm-core-noise-beats-temperature-on-coherent-joint-samples). Falsifier read: (1) HOLDS: paired P - T +0.161/+0.220/+0.238/+0.215/+0.170, 5/5 > 0, mean 0.201 > 0.05 (sigma* 2.0, tau* 1.0, both picked on the validation stream); (2) FAILS: P's valid fraction 0.2125 < 0.5 (coverage among valid samples 0.939) -> DISPROVED; M1 frozen draw 0.0 and M2 scorer (true lines 1.0, coin 0.0) both RED, so the round is valid. director-thought-review CONFIRMED: byte-identical replay, own recompute, and T = 0 is a REAL property (no per-pixel probability exceeds 0.5 on a two-mode target; an oracle independent sampler on the true marginals reaches valid 0.003), not a scorer artefact. Reading: core noise does reach BOTH valid modes where temperature reaches none, but 4 samples in 5 are not lines, so the claim as pre-registered fails; per review R2, (1) was near-guaranteed by construction, and (2) is the informative half. Residue: sigma* 2.0 is the grid top and validity climbs with sigma (0.036/0.167/0.213), so sigma in {3, 4} or more steps is the open edge (a NEW leaf); the pre-run edited a closed round's script (g537, replay verified intact) and the pin commit became an ancestor only after the pre-run (pin in the bytes): process residues.
<!-- THOUGHT:END -->
