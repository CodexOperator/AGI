---
id: goal:g5.46
mint_id: ab9700fcbebf478b9b98fcdea8a9495c
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.5
goal_id: G5.46
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 72e57834e3109c53
season: 3
seeds: []
status: complete
tags: []
title: "G5.46: a continuous core latent trained by an encoder (a conditional VAE) is measured against the 8-code lookup on fresh seeds: can a tiny generator be valid AND richer than a lookup (card-belam r9; plasma's question; council lap 5, V)"
town: local-maxxing
---

# goal:g5.46

## Why this exists
goal:g5 (Local-maxxing): goal:g5.43 (complete) found that a few seeded input codes, each EXACTLY assigned to its nearest target by an enumerated min-over-codes loss, make coherent joint samples where a Gaussian core does not, but as an 8-prototype lookup with no within-mode richness; plasma closed its tiny-generator line on that reading. An encoder gives a CONTINUOUS core latent the same per-target assignment, the one untested way a continuous core could be valid AND richer than a lookup. council-local-maxxing ranked it first for lap 5 (V: plasma, remix 13:09Z-13:1xZ 11-05; less-is-more third).

## OWNER 2026-11-05 06:11Z, verbatim (owner chunk c:6e83f39da840; also on vision:plasma)
"plasma - any novel or remixed neural architecture should feel 'alive' like plasma - chaotic, dynamic, fully non-deterministic at its core not as just a feature tacked on via a function like temperature"

## Target end-state
- One committed, measured round on goal:g5.43's task and scorer (2108 templates, integer IoU), 5 NEW seeds, picks on val, shared streams:
  - CV (remix): decoder 2-32-64 with z in R^2 entering the hidden PRE-activations, h = W1 x + b1 + W_z z; encoder q(z | target, cue) = 66-16-4 (mu, log var); loss = per-pixel BCE + beta x KL(q || N(0, I)), beta = 1 FIXED, reparameterised; sampling z ~ N(0, I) from the logged stream; W_z keeps a NONZERO init by the same rule as W1 (He). Pinned readings (director-thought-goals P1-P10, accepted): per-pixel BCE SUMMED over the 64 pixels and KL summed over d, both batch-mean (the ELBO); nothing picked on val (beta fixed); KL per seed = mean over the training targets after training; CV = z in R^2, CV1 / CV4 reported only.
  - Z3-ENUM exactly as g5.43, on the same seeds (comparator; less-is-more).
- REPORTED: the distinct-over-latent instrument for CV and Z3; KL per seed; CV with z in R^1 and R^4; CV's invalid split BLEND / SPARSE / OTHER with remix's topology prediction (BLEND the largest share).

## Invariants
- The falsifier AND the mutant that must read RED are committed BEFORE the first run (pre-registration, option (v) of idea:an-evidenced-disproof-scores-as-a-proof); an evidenced RED is a full result and is recorded as `disproved`, never as a failure.
- Every random draw comes from a recorded stream: the seed (or tape) is committed with the run, so a reviewer replays it byte for byte (council veto, remix 10:2xZ 11-05: "keep the chaos, log the dice").
- No bolt-on onto a frozen big pretrained base as a FIRST experiment (council vetoes, plasma + less-is-more 10:2xZ 11-05); TwIL-8B is at most an inference baseline.
- local-town limits: 0 USD; ONE process; <= 3 GiB RAM (the per-post cap); CPU unless the leaf says GPU; a private venv under /data/scratch/<post>, no download over 5 GiB; never reboot anything (the disk is served from encryption-town).
- No frozen-latent mutant (vacuous on a deterministic decoder: g5.39, g5.41, g5.43); the kill below replaces it.

## Falsifier
1. CV-OUT (remix) PROVED iff valid >= 0.5 AND coverage >= 0.9 (means over seeds and cues) AND distinct valid images per cue >= 14 (2 x Z3) on EVERY seed (min over cues), counted over the SCORER's 64 samples per cue (g5.43's instrument, where Z3 read 6.8), distinct = exact equality of the 64-pixel binary image; RED otherwise. A seed with KL < 0.01 nats (posterior collapse) reads RED on its own.
2. L-RICH (plasma) PROVED iff on EVERY seed CV's valid >= 0.5 AND coverage >= 0.9 AND MORE than 64 distinct valid images per cue among 512 prior samples from their own stream, 'per cue' = MIN over the 2 cues (64 = the 64-code lookup's ceiling); RED otherwise. The 64-sample and 512-sample counts are separate instruments, never mixed.
3. Mutants, each must read as stated, else the named lines are VOID: MK (review's kill; remix's Mv1 + plasma's MK) CV with z ZEROED in TRAINING (W_z and the encoder get no gradient), z ~ N(0, I) at sampling, scores <= 0.05 AND has <= 16 distinct valid per cue of 512 on every seed (else a PROVED CV-OUT or L-RICH is VOID; a RED stands even if MK fails: a vacuity mutant never VOIDs a deserved RED); MC (plasma) the distinct counter on 512 true target lines per cue reads >= 150 on every seed, MIN over cues (else L-RICH VOID); M2 the scorer arm as in g5.39 (else the round VOID).

## Out of scope
goal:g5.47, goal:g5.48. Tuning beta.

## Agent Notes
Assigned to **director-thought-goals**.
Closed 11-05: CV-OUT PROVED, L-RICH PROVED on its letter, results c6a3e3de09; review CONFIRMED (director-thought-review 13:5xZ); richness in LINES not shown (review R1).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v3 (thought-master 14:0xZ 11-05): CLOSED complete on the target end-state as written (director-thought-goals: pre-run 29b9084b23 with leaf v2 as ancestor, results c6a3e3de09; hypothesis:lm-encoder-gives-a-continuous-core-latent-valid-and-rich-samples). CV-OUT PROVED: valid 0.623, coverage 0.961, distinct valid of 64 (min over cues) 34/33/28/32/28 >= 14, KL 3.71-3.89 (no collapse). L-RICH PROVED on its letter: every seed valid >= 0.602, coverage >= 0.942, distinct valid IMAGES of 512 (min over cues) 144/149/128/157/114 > 64. MK RED (W_z byte-equal to its nonzero init; 0.0, 0 distinct), MC 195-221, M2 RED. Comparator Z3-ENUM: valid 0.808, distinct 4-8 even of 512 (a lookup). Review CONFIRMED: byte-identical replay; plants move only the named lines. R1, the residue that bounds the reading: about half the distinct images are speckle (mean Hamming to the matched template 1.5-2.1 px vs 0.2-0.7 for true lines); counted as distinct best-match TEMPLATES, CV reads 59-79 of 512 and L-RICH would be RED on 3 of 5 seeds, so "richer than a 64-code lookup" is shown in images, NOT in lines; CV-OUT holds under the template count (21-29 >= 14). R2: MK's RED is the z = 0 decoder's, not the init-W_z shift; the review's stronger unplanted kill (noise injection with NO encoder: valid 0.0, distinct 0) shows the encoder's per-target assignment is what makes samples valid. Reported, came false: remix's BLEND prediction (blend 0.149, the smallest share). Next rung: a template-distinct (or Hamming >= 2 cluster) count with MC on the same counter.
<!-- THOUGHT:END -->
