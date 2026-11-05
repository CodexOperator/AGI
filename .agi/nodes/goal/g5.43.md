---
id: goal:g5.43
mint_id: d051d7e6a9ad47068b48089f3d709207
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.5
goal_id: G5.43
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 4605d56702d44263
season: 3
seeds: []
status: complete
tags: []
title: "G5.43: a few seeded code bits at the input of a tiny deterministic generator, every code trained, is pre-registered on fresh seeds against a Gaussian core and its own sampled, many-state and continuous variants: which randomness a tiny generator can inhabit (card-belam r9; council lap 4)"
town: local-maxxing
---

# goal:g5.43

## Why this exists
goal:g5 (Local-maxxing): goal:g5.41 (complete, results d48b32691e) found g5.39's failure is under-drawn lines (SPARSE 0.841), not blends, and REPORTED an arm it could not credit: Z, three seeded code bits at the INPUT of the deterministic 2-32-64 net with all 8 codes enumerated in the loss, scored 0.794 (valid 0.823, coverage 0.959, every seed) against <= 0.24 for every claimed arm. director-thought-review's R1 and all three seats of council-local-maxxing (12:08Z-12:0xZ 11-05) asked for Z pre-registered as a CLAIM on fresh seeds, each with its own lines below.

## OWNER 2026-11-05 06:11Z, verbatim (owner chunk c:6e83f39da840; also on vision:plasma)
"plasma - any novel or remixed neural architecture should feel 'alive' like plasma - chaotic, dynamic, fully non-deterministic at its core not as just a feature tacked on via a function like temperature"

## Target end-state
- One committed, measured round on goal:g5.41's task and scorer (2108 templates, integer IoU test), 5 NEW seeds, shared data / init / batch streams, every pick on the validation stream, K = 8 draws per target per step unless the arm says otherwise. Arms:
  - Z3-ENUM: 3 code bits as input (5-32-64), sigma 0, loss = min per-pixel BCE over ALL 8 codes enumerated; a sample = one uniform seeded code (g5.41's Z exactly).
  - Z3-SAMP: the same 3 bits, 8 draws WITH replacement per target (plasma).
  - Z5-SAMP: 5 code bits (32 states), 8 draws per target (plasma).
  - C3-SAMP: 3 continuous N(0, 1) inputs, 8 draws per target (plasma).
  - Z6-ENUM (less-is-more): 6 code bits (8-32-64), sigma 0, all 64 codes enumerated in the loss; a sample = one uniform seeded code; 64 samples per cue; G64: g5.39's Gaussian core at a MATCHED best-of-64, sigma on val in {4, 6, 8}.
  - G: g5.39's Gaussian core, best-of-8, sigma on val in {2, 3, 4} (the comparator for L-Z).
- REPORTED per discrete arm: the fraction of its codes that win at least one target in the last 500 steps (plasma's mechanism reading; the prediction is that score tracks it); distinct valid images per cue for EVERY arm; Z with 2 / 3 / 4 bits (remix: more codes than modes predicts dead codes).
- SCOPE, stated: the code enters through W1, a discrete shift of the hidden pre-activations; whether that is "non-deterministic at its core" in the owner's sense is a reading this leaf does not claim. It answers what makes coherent joint samples in a tiny generator.

## Invariants
- The falsifier AND the mutant that must read RED are committed BEFORE the first run (pre-registration, option (v) of idea:an-evidenced-disproof-scores-as-a-proof); an evidenced RED is a full result and is recorded as `disproved`, never as a failure.
- Every random draw comes from a recorded stream: the seed (or tape) is committed with the run, so a reviewer replays it byte for byte (council veto, remix 10:2xZ 11-05: "keep the chaos, log the dice").
- No bolt-on onto a frozen big pretrained base as a FIRST experiment (council vetoes, plasma + less-is-more 10:2xZ 11-05); TwIL-8B is at most an inference baseline.
- local-town limits: 0 USD; ONE process; <= 3 GiB RAM (the per-post cap); CPU unless the leaf says GPU; a private venv under /data/scratch/<post>, no download over 5 GiB; never reboot anything (the disk is served from encryption-town).
- Each line is scored only on its own pre-written text; no post-hoc best-of claim.

## Falsifier
1. L-REP (plasma), the gate: PROVED iff Z3-ENUM valid >= 0.5 AND coverage >= 0.9 on the 5 new seeds. If RED, g5.41's Z was a seed artefact and line 3 is not read (plasma: the gate covers line 3 only; L-Z and L-Z6 are always read).
2. L-Z (remix): PROVED iff Z3-ENUM valid >= 0.5 AND coverage >= 0.9 AND the paired per-seed delta Z3-ENUM - G(sigma* on val) on score is > 0 on 5/5 with mean > 0.05; RED otherwise.
3. L-ENUM (Z3-ENUM vs Z3-SAMP), L-STATES (Z3-SAMP vs Z5-SAMP), L-DISC (Z3-SAMP vs C3-SAMP), plasma: each PROVED iff the paired per-seed delta on score is > 0 on 5/5 with mean > 0.05; RED otherwise.
4. L-Z6 (less-is-more): PROVED iff on EVERY seed Z6-ENUM valid >= 0.5 AND coverage >= 0.9 AND distinct valid images per cue >= 16 of its 64 samples, AND the paired score Z6-ENUM - G64 > 0 on 5/5 with mean > 0.05; RED otherwise.
5. Mutants, each must read RED, else the named lines are VOID: Mz1 EVERY latent arm (Z3-ENUM, Z3-SAMP, Z5-SAMP, C3-SAMP with its 3 inputs frozen to ONE seeded draw per seed and cue, Z6-ENUM) with its latent FIXED at sampling scores <= 0.05 on every seed; a failing Mz1 on either arm of a pair VOIDs that pair's line (L-ENUM, L-STATES, L-DISC). NOTE, stated pre-run (less-is-more): with sigma 0 a fixed latent gives one image per cue, so Mz1 reads RED by construction on the ENUM arms and has no teeth there; it is kept as a harmless consistency check, never as the guard of L-REP or L-Z. Mz6 (less-is-more, instrument): Z6-ENUM sampled through (code mod 8), at most 8 distinct images per cue by construction, must read distinct valid images < 16 per cue on EVERY seed, else L-Z6 is VOID (the distinct counter is broken). Mz2 (remix) Z3 trained with ONE uniform code PER TARGET per step from the logged stream, loss on that code only (K = 1, no min), falls to valid <= 0.1 on every seed (else the enumeration reading of L-ENUM is VOID); M2 the scorer arm as in g5.39 (else the round is VOID).
6. Pinned readings (director-thought-goals, accepted): 'X vs Y' = the delta X - Y (L-STATES = Z3-SAMP - Z5-SAMP); L-Z6's distinct >= 16 holds in EACH cue on every seed; means are over seeds and cues on test; each sigma* is its arm's best mean val; win fraction = distinct winning codes in the last 500 steps / 2^bits; reported Z2-ENUM and Z4-ENUM.

## Out of scope
goal:g5.44. Any further sigma grid on a Gaussian core (review: sigma is not the failure). Tuning lambda (g5.41 is closed).

## Agent Notes
Assigned to **director-thought-goals**.
Closed 11-05: L-REP, L-Z, L-ENUM PROVED; L-STATES, L-DISC, L-Z6 DISPROVED, results d04861ed6f; review CONFIRMED (director-thought-review 12:57Z).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v3 (thought-master 13:0xZ 11-05): CLOSED complete on the target end-state as written (director-thought-goals: pre-run f93be0f7b3 with the pinned leaf as ancestor, results d04861ed6f; hypothesis:lm-seeded-input-codes-make-coherent-joint-samples). Falsifier read (test means over seeds and cues, pin P6): L-REP PROVED (Z3-ENUM valid 0.872, coverage 0.927; per seed coverage 0.964/0.903/0.808/0.977/0.982, so the gate rests on the MEAN, as pinned); L-Z PROVED (Z3-ENUM - G(sigma 3.0) 0.707/0.378/0.510/0.673/0.656); L-ENUM PROVED (Z3-ENUM - Z3-SAMP 0.814/0.011/0.181/0.435/0.551); L-STATES DISPROVED (-0.314/+0.208/+0.229/-0.006/+0.026); L-DISC DISPROVED (-0.090/+0.228/+0.034/+0.098/+0.028); L-Z6 DISPROVED on one bar on one seed (54303 valid 0.469 < 0.5; coverage, distinct >= 16 and Z6 - G64 5/5 held). Mutants: Mz2 a real kill (valid 0.0 on all seeds; review's own variant agrees), M2 RED, Mz6 an instrument check of the distinct counter. Mz1 is VACUOUS BY CONSTRUCTION on all five latent arms (a deterministic sigma-0 decoder gives one image per cue for any frozen latent), stated pre-run for the ENUM arms and confirmed for all by review: it guarded nothing; review's non-vacuous plants move no pair delta. Review CONFIRMED with a byte-identical replay. Reading: a few seeded input codes, every code trained (enumerated min-over-codes loss), make coherent joint samples where a Gaussian core does not, and enumeration (not the bits alone) is the operative piece; more states (5 bits sampled) and discreteness vs a continuous 3-dim latent did not win. Limits (reported, never credited): Z3 emits ~8 images per cue (6.8 distinct valid), an 8-prototype lookup, so L-Z says nothing about generative richness; a future L-Z6 PROVED needs a stronger diversity bar (review: an 8-code net passes distinct >= 16 on one seed). Next-rung mutant (review): replace Mz1 with a kill test (latents zeroed in training, random at sampling).
<!-- THOUGHT:END -->
