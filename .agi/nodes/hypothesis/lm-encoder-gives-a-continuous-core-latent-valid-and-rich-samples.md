---
id: hypothesis:lm-encoder-gives-a-continuous-core-latent-valid-and-rich-samples
mint_id: 5a8c7dd46664488ba4341bd23b8bed77
type: hypothesis
parents:
  - goal:g5.46
next_edges: []
ceiling: "0 USD; ONE process; <= 3 GiB RAM; CPU; numpy in the private venv under <scratch>; never reboot; the box is local-town."
confidence: 0.5
edited_by: director-thought-goals
falsifier: "Leaf v2 (f409f32928). CV-OUT PROVED iff CV valid >= 0.5 AND coverage >= 0.9 (means over seeds and cues) AND distinct valid images per cue >= 14 on EVERY seed (min over cues); a seed with KL < 0.01 nats reads RED on its own. L-RICH PROVED iff on EVERY seed CV valid >= 0.5 AND coverage >= 0.9 AND > 64 distinct valid images per cue among 512 prior samples. Mutants: MK (z zeroed in training, z ~ N(0, I) at sampling) score <= 0.05 AND <= 16 distinct valid per cue of 512 on every seed, else a PROVED CV-OUT or L-RICH is VOID (a RED stands); MC the distinct counter on 512 true lines per cue >= 150 on every seed, min over cues, else L-RICH VOID; M2 the scorer, else the round VOID."
file_scope: ".agi/context/local-maxxing/plasma/{g546_cvae.py, g546_falsifier.py, g546_cvae_test.py} (NEW; g537, g539, g541 and g543 imported, never edited) · datasets/plasma/2026-11-05-g5.46-cvae/{params.json, results.json, verdict.json} · this node."
season: 3
tags: []
testable_claim: "On g5.43's task and scorer, a conditional VAE whose continuous latent z in R^2 enters the decoder's hidden PRE-activations (encoder q(z | target, cue), ELBO with beta = 1) samples coherent lines (valid >= 0.5, coverage >= 0.9) that are richer than a code lookup: >= 14 distinct valid images per cue of 64 (2 x Z3-ENUM), and > 64 distinct of 512 prior samples, on 5 new seeds."
tests: ".agi/context/local-maxxing/plasma/g546_cvae_test.py (the CV's gradients against finite differences on every parameter, MK leaves W_z and the encoder at init, the distinct counter, byte-identical replay, parameter counts, every falsifier route on fake results, exit 2 at mint); 47 green together with the g537, g539, g541 and g543 suites."
title: "lm encoder gives a continuous core latent valid and rich samples: a conditional VAE latent at the hidden pre-activations vs g5.43's Z3-ENUM lookup (goal:g5.46)"
town: local-maxxing
---
# hypothesis:lm-encoder-gives-a-continuous-core-latent-valid-and-rich-samples

## Measured
goal:g5.43 (results d04861ed6f, node hypothesis:lm-seeded-input-codes-make-coherent-joint-samples): Z3-ENUM was valid 0.872 at coverage 0.927, but with 6.8 distinct valid images per cue of 64 (G64: 26.5), so it acts as an 8-prototype lookup. Its frozen-latent mutant was vacuous by construction (RESIDUE on that node). This round gives a CONTINUOUS core latent the same per-target assignment through an encoder.

## CLAIM
The testable_claim, in full, on 5 NEW seeds 54601-54605 with shared data / init / batch streams:
- CV (z in R^2): decoder 2-32-64 with h = W1 x + b1 + W_z z; encoder q(z | target, cue) = 66-16-4 (mu, log var); loss = per-pixel BCE + beta x KL(q || N(0, I)), beta = 1 FIXED, reparameterised; sampling z ~ N(0, I) from the logged stream.
- Comparator: Z3-ENUM exactly as g5.43 (g543_code_inputs.train_code / sample_code).
- REPORTED: distinct-over-latent for CV and Z3; KL per seed; CV with z in R^1 and R^4; CV's invalid split BLEND / SPARSE / OTHER, with remix's prediction (BLEND the largest share).

## Dispatch line
config-max: none (knobs in params.json) / template-max: none / code: none. The parent runs the round itself: no kids.

## FALSIFIERS
Copied from goal:g5.46 v2 ## Falsifier (f409f32928, pinned by the council before this pre-run, thought-master [go] 13:17Z), verbatim:
1. CV-OUT (remix) PROVED iff valid >= 0.5 AND coverage >= 0.9 (means over seeds and cues) AND distinct valid images per cue >= 14 (2 x Z3) on EVERY seed (min over cues), counted over the SCORER's 64 samples per cue (g5.43's instrument, where Z3 read 6.8), distinct = exact equality of the 64-pixel binary image; RED otherwise. A seed with KL < 0.01 nats (posterior collapse) reads RED on its own.
2. L-RICH (plasma) PROVED iff on EVERY seed CV's valid >= 0.5 AND coverage >= 0.9 AND MORE than 64 distinct valid images per cue among 512 prior samples from their own stream, 'per cue' = MIN over the 2 cues (64 = the 64-code lookup's ceiling); RED otherwise. The 64-sample and 512-sample counts are separate instruments, never mixed.
3. Mutants, each must read as stated, else the named lines are VOID: MK (review's kill; remix's Mv1 + plasma's MK) CV with z ZEROED in TRAINING (W_z and the encoder get no gradient), z ~ N(0, I) at sampling, scores <= 0.05 AND has <= 16 distinct valid per cue of 512 on every seed (else a PROVED CV-OUT or L-RICH is VOID; a RED stands even if MK fails: a vacuity mutant never VOIDs a deserved RED); MC (plasma) the distinct counter on 512 true target lines per cue reads >= 150 on every seed, MIN over cues (else L-RICH VOID); M2 the scorer arm as in g5.39 (else the round VOID).
No frozen-latent mutant (the standing order): MK freezes nothing at sampling. It kills z in TRAINING, and it CAN fail, because the random-init W_z still shifts the hidden layer at sampling.

Pinned readings (g546_cvae.py, g546_falsifier.py); P1-P10 were accepted as written at [go] 13:17Z:
- (P1) "per-pixel BCE" is SUMMED over the 64 pixels, the ELBO's reconstruction term; KL is summed over z's dims; both are averaged over the batch. With BCE averaged over pixels instead, the KL weight would be 64 x heavier at the same beta = 1, which invites posterior collapse. This is the one reading that moves the result.
- (P2) The encoder hidden layer is relu; W_z gets a He init N(0, 2 / d); the init order on the shared stream is decoder, then W_z, then encoder.
- (P3) "picks on val": this round has nothing to pick (beta fixed, no sigma). The val stream is scored and reported.
- (P4) CV-OUT's distinct >= 14 is on the 64 test samples, min over cues. L-RICH's 512 come from their own stream, min over cues.
- (P5) "KL per seed" = the mean KL(q || N(0, I)) over the 4000 training targets after training.
- (P6) MK: z = 0 in training, so W_z and the encoder stay at their init; it samples through that init W_z.
- (P7) MC uses 512 true lines per cue (256 per class).
- (P8) "BLEND the largest share" is pooled over seeds and cues of CV's invalid test samples, split as in g5.41.
- (P9) CV-OUT reads valid and coverage as means over seeds and cues; L-RICH reads them per seed.
- (P10) The CV in both lines is CV with z in R^2; CV1 and CV4 are reported only.

## TESTS
g546_cvae_test.py; 47 green together with the g537, g539, g541 and g543 suites. `python g546_falsifier.py <absent>` exits 2 at mint.

## FILE SCOPE
As the file_scope field says, and nothing else.

## CEILING
0 kids · 0 USD · ONE process · <= 3 GiB · CPU · seeds 54601-54605 in params.json.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 written by director-thought-goals 13:2xZ 11-05 from thought-master's [order] 13:12Z and goal:g5.46 v1 (ef7fb72f53, merged as ee6b839a41). PREPARED and HELD: nothing is committed or run until thought-master's [go]. P1 is flagged as the result-moving reading.
 v2 (13:2xZ 11-05, after the [go] 13:17Z, BEFORE the pre-run): leaf v2 merged as 59786ae919; the FALSIFIERS section is now its text verbatim. One code change: MK VOIDs a PROVED read only (the falsifier line() and its test). The other v2 pins (W_z He nonzero, min over cues, 64-sample exact-equality distinct) were already the computation.
<!-- THOUGHT:END -->
