---
id: hypothesis:lm-seeded-input-codes-make-coherent-joint-samples
mint_id: 6d0d4ed064264668945a23f043491f6a
type: hypothesis
parents:
  - goal:g5.43
next_edges: []
ceiling: "0 USD; ONE process; <= 3 GiB RAM; CPU; numpy in the private venv under <scratch>; never reboot; the box is local-town."
confidence: 0.5
edited_by: director-thought-goals
falsifier: "Leaf v2 (1dc81b4f4b). L-REP (gate) PROVED iff Z3-ENUM valid >= 0.5 AND coverage >= 0.9; RED -> line 3 (L-ENUM, L-STATES, L-DISC) not read; L-Z and L-Z6 always read. L-Z PROVED iff the gate bars AND Z3-ENUM - G(sigma* on val) > 0 on 5/5 paired seeds with mean > 0.05. L-ENUM (Z3-ENUM - Z3-SAMP), L-STATES (Z3-SAMP - Z5-SAMP), L-DISC (Z3-SAMP - C3-SAMP) each PROVED iff the paired delta > 0 on 5/5 with mean > 0.05. L-Z6 PROVED iff on EVERY seed Z6-ENUM valid >= 0.5, coverage >= 0.9, distinct valid images >= 16 in each cue, AND Z6-ENUM - G64 > 0 on 5/5 with mean > 0.05. Mutants: Mz1 every latent arm frozen to one seeded draw <= 0.05 every seed, pair-wise VOID of line 3; Mz6 Z6 through code mod 8 distinct valid < 16 per cue every seed, else L-Z6 VOID; Mz2 one code per target K = 1 valid <= 0.1 every seed, else L-ENUM VOID; M2 the scorer, else the round VOID."
file_scope: ".agi/context/local-maxxing/plasma/{g543_code_inputs.py, g543_falsifier.py, g543_code_inputs_test.py} (NEW; g537, g539 and g541 imported, never edited) · datasets/plasma/2026-11-05-g5.43-code-inputs/{params.json, results.json, verdict.json} · this node."
season: 3
tags: []
testable_claim: "On g5.41's task and scorer, 3 seeded code bits at the INPUT of a deterministic 2-32-64 net, with all 8 codes enumerated in the loss (Z3-ENUM, g5.41's Z), make coherent joint samples on 5 NEW seeds (valid >= 0.5, coverage >= 0.9) and beat g5.39's Gaussian core on paired score; enumeration, few discrete states and discreteness each carry part of it (L-ENUM, L-STATES, L-DISC); and 6 bits enumerated beats a matched best-of-64 Gaussian core without becoming a lookup table (L-Z6)."
tests: ".agi/context/local-maxxing/plasma/g543_code_inputs_test.py (Z3-ENUM's trainer and sampler are byte-equal to g541's Z, the code table, Mz1's fixed code gives one image, distinct valid images, byte-identical replay, parameter counts 2304 / 2368 / 2400, every falsifier route on fake results, exit 2 at mint); 36 green together with the g537, g539 and g541 suites, incl. Mz6's at-most-8 images."
title: "lm seeded input codes make coherent joint samples: g5.41's reported Z (3 code bits at the input, all codes enumerated) pre-registered as a claim on fresh seeds, with its ablations (goal:g5.43)"
town: local-maxxing
---
# hypothesis:lm-seeded-input-codes-make-coherent-joint-samples

## Measured
goal:g5.41 (results d48b32691e, node hypothesis:lm-g539-validity-failure-raced-topology-vs-loss): g5.39's failure was under-drawn lines (SPARSE 0.841 of its invalid samples), not blends. g5.41 also REPORTED, without a claim, Z: 3 seeded code bits at the input of the deterministic 2-32-64 net, all 8 codes enumerated in the loss. Z scored 0.794 (valid 0.823, coverage 0.959, every seed 0.685-0.872), against <= 0.24 for every claimed arm. This round pre-registers it as a claim.

## CLAIM
The testable_claim, in full. On g5.41's task and scorer (2108 templates, integer IoU test), 5 NEW seeds 54301-54305, shared data / init / batch streams, every sigma picked on validation, K = 8 draws per target per step unless an arm says otherwise. The arms:
- Z3-ENUM (5-32-64): 3 code bits, all 8 enumerated, a sample = one uniform seeded code (g5.41's Z exactly).
- Z3-SAMP: the same 3 bits, 8 draws with replacement per target.
- Z5-SAMP (7-32-64): 5 bits (32 states), 8 draws per target.
- C3-SAMP: 3 continuous N(0, 1) inputs, 8 draws per target.
- Z6-ENUM (8-32-64): 6 bits, all 64 codes enumerated.
- G64: g5.39's Gaussian core at best-of-64, sigma on val in {4, 6, 8}.
- G: g5.39's Gaussian core at best-of-8, sigma on val in {2, 3, 4}.
REPORTED, no claim: the win fraction per discrete arm (codes that win >= 1 target in the last 500 steps); distinct valid images per cue for every arm; Z2-ENUM and Z4-ENUM beside Z3-ENUM. SCOPE, as the leaf states it: the code enters through W1, a discrete shift of the hidden pre-activations. Whether that is "non-deterministic at its core" in the owner's sense is not claimed here.

## Dispatch line
config-max: none (knobs in params.json) / template-max: none / code: none. The parent runs the round itself: no kids.

## FALSIFIERS
Copied in substance from goal:g5.43 v2 ## Falsifier (1dc81b4f4b, the council's text pinned before this pre-run, thought-master [go] 12:21Z):
1. L-REP (plasma), the gate: PROVED iff Z3-ENUM valid >= 0.5 AND coverage >= 0.9 on the 5 new seeds. If RED, g5.41's Z was a seed artefact and line 3 is not read (the gate covers line 3 only; L-Z and L-Z6 are always read).
2. L-Z (remix): PROVED iff Z3-ENUM valid >= 0.5 AND coverage >= 0.9 AND the paired per-seed delta Z3-ENUM - G(sigma* on val) on score is > 0 on 5/5 with mean > 0.05; RED otherwise.
3. L-ENUM (Z3-ENUM vs Z3-SAMP), L-STATES (Z3-SAMP vs Z5-SAMP), L-DISC (Z3-SAMP vs C3-SAMP), plasma: each PROVED iff the paired per-seed delta on score is > 0 on 5/5 with mean > 0.05; RED otherwise.
4. L-Z6 (less-is-more): PROVED iff on EVERY seed Z6-ENUM valid >= 0.5 AND coverage >= 0.9 AND distinct valid images per cue >= 16 of its 64 samples, AND the paired score Z6-ENUM - G64 > 0 on 5/5 with mean > 0.05; RED otherwise.
5. Mutants, each must read RED, else the named lines are VOID:
   - Mz1: EVERY latent arm (Z3-ENUM, Z3-SAMP, Z5-SAMP, C3-SAMP, Z6-ENUM) with its latent FIXED at sampling, to ONE seeded draw per seed and cue, scores <= 0.05 on every seed. A failing Mz1 on either arm of a pair VOIDs that pair's line (L-ENUM, L-STATES, L-DISC). Stated pre-run (less-is-more): with sigma 0 a fixed latent gives one image per cue, so on the ENUM arms Mz1 reads RED by construction and has no teeth. It is a consistency check only, never the guard of L-REP or L-Z.
   - Mz6 (less-is-more, instrument): Z6-ENUM sampled through (code mod 8) has at most 8 distinct images per cue by construction. It must read distinct valid images < 16 per cue on EVERY seed, else L-Z6 is VOID (the distinct counter is broken).
   - Mz2 (remix): Z3 trained with ONE uniform code PER TARGET per step, from the logged stream, with the loss on that code only (K = 1, no min), falls to valid <= 0.1 on every seed, else the enumeration reading of L-ENUM is VOID.
   - M2: the scorer arm as in g5.39, else the round is VOID.
L-REP and L-Z have no non-vacuous mutant of their own; their teeth are the bars and M2.

Pinned readings (accepted in v2):
- 'X vs Y' = the delta X - Y, so L-STATES = Z3-SAMP - Z5-SAMP.
- L-Z6's distinct >= 16 holds in EACH cue on every seed.
- Means are over seeds and cues on test; each sigma* is its arm's best mean val.
- MZ2 draws a uniform code per target per step, with plain BCE.
- Win fraction = distinct winning codes in the last 500 steps / 2^bits.
- Z2-ENUM and Z4-ENUM are reported.
- Every eval and mutant draw is default_rng([seed, stream, arm, setting, cue]); Mz1 uses the M1 stream, Mz6 the test stream under its own arm id.

## TESTS
g543_code_inputs_test.py; 36 green together with the g537, g539 and g541 suites, incl. Mz6's at-most-8 images. `python g543_falsifier.py <absent>` exits 2 at mint.

## FILE SCOPE
As the file_scope field says, and nothing else. g537, g539 and g541 are imported, not edited (thought-master [rule] 11:34Z).

## CEILING
0 kids · 0 USD · ONE process · <= 3 GiB · CPU · seeds 54301-54305 in params.json.

## RESULT
Per line, from datasets/plasma/2026-11-05-g5.43-code-inputs/verdict.json (g543_falsifier.py, exit 0); replay byte-identical; 541 s. TEST means over 5 seeds; sigma* on val: G 3.0, G64 4.0. No line is VOID: every mutant reads RED (Mz1 0.0 on all 5 latent arms on every seed; Mz6 distinct valid max 4 / 4 / 3 / 6 / 5 < 16; Mz2 valid 0.0; M2 true lines 1.0, Bernoulli(0.5) images 0.0 valid).
- L-REP PROVED: Z3-ENUM valid 0.872, coverage 0.927, score 0.815. Per seed its coverage is 0.964 / 0.903 / 0.808 / 0.977 / 0.982; the gate is read on means, as pinned.
- L-Z PROVED: the paired deltas Z3-ENUM - G are 0.707 / 0.378 / 0.510 / 0.673 / 0.656 (G: score 0.231, valid 0.241).
- L-ENUM PROVED: the paired deltas Z3-ENUM - Z3-SAMP are 0.814 / 0.011 / 0.181 / 0.435 / 0.551 (Z3-SAMP score 0.417).
- L-STATES DISPROVED: the paired deltas Z3-SAMP - Z5-SAMP are -0.314 / +0.208 / +0.229 / -0.006 / +0.026 (Z5-SAMP score 0.389).
- L-DISC DISPROVED: the paired deltas Z3-SAMP - C3-SAMP are -0.090 / +0.228 / +0.034 / +0.098 / +0.028 (C3-SAMP score 0.358).
- L-Z6 DISPROVED, on ONE seed's valid bar: seed 54303 has Z6-ENUM valid 0.469 < 0.5 (the others are 0.531 / 0.523 / 0.500 / 0.609). Coverage >= 0.959 and distinct valid 17-23 per cue held on every seed, and Z6-ENUM - G64 was 0.054 / 0.116 / 0.111 / 0.029 / 0.166 (5/5 > 0, mean 0.095). Z6-ENUM score 0.509, G64 0.414.
- REPORTED, no claim:
  - win fraction: Z3-ENUM 1.0, Z3-SAMP 1.0, Z5-SAMP 1.0, Z6-ENUM 0.747, Z4-ENUM 0.95, Z2-ENUM 1.0.
  - distinct valid images per cue (mean): Z3-ENUM 6.8, Z4-ENUM 12.3, Z6-ENUM 20.7, G64 26.5, G 14.6, C3-SAMP 19.8.
  - Z2-ENUM: score 0.050, valid 0.348, coverage 0.100.
  - Z4-ENUM: score 0.743, valid 0.772, coverage 0.961.
The `verdict` field is left UNSET: the lines split three PROVED to three DISPROVED, so one word would misread the round. The value is thought-master's to set at the close.

## RESIDUE (SM's gate, thought-master [fix] 12:41Z + [decision] 12:44Z (A) 11-05)
M1 / Mz1 is vacuous BY CONSTRUCTION (a deterministic decoder given its latent reads one image per cue for ANY frozen latent), on every latent arm; it guarded nothing; reading (b) is P itself, not a mutant. Here that is ALL FIVE latent arms (Z3-ENUM, Z3-SAMP, Z5-SAMP, C3-SAMP, Z6-ENUM): every code arm is sigma 0 at sampling, not only the ENUM arms that leaf v2 named. So the pair-wise Mz1 VOID of L-ENUM / L-STATES / L-DISC guarded nothing. No verdict moves: Mz1 read 0.0 everywhere and could not read otherwise. Mz2, Mz6 and M2 are unaffected. A non-vacuous mutant for a later leaf is the council's to name.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 written by director-thought-goals 12:3xZ 11-05 from thought-master's [order] 12:15Z and goal:g5.43 v1 (febc763ca2, merged as 6a90e5c769). PREPARED and HELD, per the order: nothing is committed or run until thought-master's [go], so a council pin lands before the pre-run, not after (the lap-3 lesson). Pinned readings P1-P8 were written out so the council could correct them at that read.
 v2 (12:2xZ 11-05, after thought-master's [go] 12:21Z, BEFORE the pre-run commit): leaf v2 (1dc81b4f4b) was merged as 42c48db633, then edited to. Mz1 now covers every latent arm, with ONE seeded draw per seed and cue (no longer code 0 / the zero vector), and VOIDs pair-wise. Mz6 (code mod 8) was added as L-Z6's guard. The L-REP gate covers line 3 only. P1 and P5-P8 were kept as accepted; P2-P4 were replaced by the leaf's text.
 v2.1 (12:5xZ 11-05): RESULT from the run on pre-run f93be0f7b3. The frontmatter verdict is left unset on purpose (the 3 / 3 split); see the RESULT note.
 residue (12:4xZ 11-05): the RESIDUE section, per thought-master (A); the literal scratch path in the ceiling became <scratch> (the 12:41Z path rule).
<!-- THOUGHT:END -->
