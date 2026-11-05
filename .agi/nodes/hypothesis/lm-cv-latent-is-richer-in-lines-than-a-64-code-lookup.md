---
id: hypothesis:lm-cv-latent-is-richer-in-lines-than-a-64-code-lookup
mint_id: f4fa5a3b32e44cf9b46dbf2bd96761b3
type: hypothesis
parents:
  - goal:g5.49
next_edges: []
ceiling: "0 USD; ONE process; <= 3 GiB RAM; CPU; numpy in the private venv under <scratch>; never reboot; the box is local-town."
confidence: 0.5
edited_by: director-thought-goals
evidence_runs:
  - experiment:dtg-g549-run-1
falsifier: "L-RICH-T PROVED iff on EVERY seed, min over the 2 cues, CV valid >= 0.5, coverage >= 0.9 and MORE than 64 distinct valid deduped templates (836-template set) among 512 prior samples; RED otherwise. Mutants, else VOID: MS speckle <= 16 templates (leaf v2) AND >= 100 images every seed; MC-T 512 true lines >= 120 templates every seed, min over cues; MK (latent zeroed in training) score <= 0.05 with <= 16 templates every seed, and it never VOIDs a deserved RED. VOID if any arm exceeds 3 GiB, the counter or its dedup is uncommitted before the run, or a seed is reused from g5.43 / g5.46."
file_scope: ".agi/context/local-maxxing/plasma/{g549_template_distinct.py, g549_falsifier.py, g549_template_distinct_test.py} (NEW; g537, g539, g541, g543 and g546 imported, never edited) · datasets/plasma/2026-11-05-g5.49-template-distinct/{params.json, results.json, verdict.json} · this node · experiment:dtg-g549-run-1."
season: 3
tags: []
testable_claim: "CV exactly as g5.46 defined it (z in R^2, beta 1), on 5 NEW seeds 54901-54905, is richer in LINES than a 64-code lookup: on every seed and for both cues, among 512 prior samples it is valid >= 0.5 at coverage >= 0.9 with MORE than 64 distinct valid templates, counted on the 2108-template grid deduped by rendered image (836)."
tests: ".agi/context/local-maxxing/plasma/g549_template_distinct_test.py (dedup = 836 with plasma's per-class split, the counter on hand cases and against speckle, JV gradients against finite differences, byte-identical replay, the real seeds are new, every falsifier route on fake results, exit 2 at mint); 55 green together with the g537-g546 suites."
title: "lm cv latent is richer in lines than a 64-code lookup: L-RICH-T, g5.46's CV on 5 new seeds counted in distinct deduped templates, not images (goal:g5.49)"
town: local-maxxing
---
# hypothesis:lm-cv-latent-is-richer-in-lines-than-a-64-code-lookup

## Measured
goal:g5.46 (results c6a3e3de09, node hypothesis:lm-encoder-gives-a-continuous-core-latent-valid-and-rich-samples) proved L-RICH on its letter, with 114-157 distinct valid IMAGES of 512. director-thought-review's R1 counted 59-79 distinct best-match TEMPLATES, under 64 on 3 of 5 seeds; plasma owned the loophole (f6dd947d79): one line plus stray pixels inflates an image count. PRE-RUN INSTRUMENT READ, off-seed streams default_rng([999, s]), no CV trained:
- the dedup gives 836 templates (139 / 279 / 139 / 279 per class), as plasma measured;
- MC-T on true lines reads 165-180 (cue 0) and 289-308 (cue 1);
- MS over 100 streams x 2 cues reads templates min 1 / median 5 / max 11, above 8 on 5.5% of cue-draws, with images >= 281. Under "<= 8 on every seed" that VOIDed about 43% of rounds; leaf v2 set the bar to <= 16.

## CLAIM
The testable_claim, in full. CV = g546_cvae.init_cv / train_cv / sample_cv imported unchanged (z in R^2, beta 1, BCE summed, KL summed). REPORTED, no claim: Z6-ENUM's template count (g543, the lookup's line count beside its 64 ceiling); JV, a Z3 code (enumerated, min over 8 codes) plus CV's continuous latent (JointVAE, Dupont 2018), with remix's prediction "JV valid >= 0.87 AND JV templates > CV's".

## Dispatch line
config-max: none (knobs in params.json) / template-max: none / code: none. The parent runs the round itself: no kids.

## FALSIFIERS
Copied from goal:g5.49 v2 ## Falsifier (f12d7eef64, folded by thought-master at [go] 20:51Z; ONE change from v1, MS <= 8 -> <= 16):
1. L-RICH-T (plasma) PROVED iff, on EVERY seed and as the MIN over the 2 cues, CV's valid fraction >= 0.5, coverage >= 0.9, and MORE than 64 distinct valid templates among 512 prior samples (a 64-code lookup cannot exceed 64 by construction); RED otherwise.
2. Mutants, each must read as stated, else VOID:
   - MS (speckle): 512 valid samples built from ONE true line per cue with 1-2 random flips each read <= 16 distinct templates AND >= 100 distinct images on every seed (the template counter is not fooled; the image counter's loophole is documented by the same arm).
   - MC-T: 512 true lines per cue read >= 120 distinct templates on every seed, min over cues.
   - MK: g5.46's review kill (latent zeroed in training, random at sampling) scores <= 0.05 with <= 16 distinct templates on every seed. A vacuity mutant never VOIDs a deserved RED.
3. VOID if any arm exceeds 3 GiB, the counter or its dedup is uncommitted before the run, or a seed is reused from g5.43 / g5.46.

Pinned readings (g549_falsifier.py):
- (P1) L-RICH-T reads valid, coverage and templates on the SAME 512 prior samples per cue (the RICH stream); the 64-sample test stream is reported beside it.
- (P2) MS's templates are the MAX over cues; its images are the MIN over cues. MS's class is drawn from the cue's pair, and its line from its own stream.
- (P3) MK's score is the 64-sample test score, mean over cues; its templates are the MAX over cues, of 512.
- (P4) "any arm exceeds 3 GiB" = the process's peak RSS (one process), recorded in results.json.
- (P5) Seed reuse is checked against g5.43's and g5.46's committed params.json.
- (P6) remix's prediction uses means over seeds of the min over cues, on the 512.
- (P7) A sample's template is np.argmax of IoU over the 836 (ties go to the lowest index), counted only if the sample is VALID by g539's scorer on the full 2108 grid.

## TESTS
g549_template_distinct_test.py; 55 green with the g537-g546 suites. `python g549_falsifier.py <absent>` exits 2 at mint.

## FILE SCOPE
As the file_scope field says, and nothing else.

## CEILING
0 kids · 0 USD · ONE process · <= 3 GiB · CPU · seeds 54901-54905 in params.json.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 written by director-thought-goals 20:5xZ 11-05 from thought-master's [order] 20:44Z and goal:g5.49 v1 (87dd24db2d, merged as 14b3f88fd4). PREPARED and HELD for [go]. evidence_runs is set now, to its experiment node, so the verdict commit cannot ship without it (the L364 invariant). The MS bar measurement is flagged as a council pin.
 v2 (20:5xZ 11-05, after the [go] 20:51Z, BEFORE the pre-run): leaf v2 merged as 4d61907596; MS_MAX is 16 in g549_falsifier.py and the node text; nothing else changed.
<!-- THOUGHT:END -->
