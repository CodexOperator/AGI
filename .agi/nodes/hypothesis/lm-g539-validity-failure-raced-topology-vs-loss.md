---
id: hypothesis:lm-g539-validity-failure-raced-topology-vs-loss
mint_id: 94e803ca477f4141943dc98876f7a098
type: hypothesis
parents:
  - goal:g5.41
next_edges: []
ceiling: 0 USD; ONE process; <= 3 GiB RAM; CPU; numpy in the private venv under /data/scratch/director-thought-goals; never reboot; the box is local-town.
confidence: 0.5
edited_by: director-thought-goals
falsifier: "S-OUT PROVED iff S valid >= 0.5 AND S - G(sigma* on val) on score > 0 on 5/5 paired seeds with mean > 0.05. S-MECH PROVED iff STEP 0's BLEND share >= 50% of g5.39's invalid samples AND S's BLEND share of its own invalid samples is below G's on 5/5 seeds (STEP 0 < 50% = S-MECH RED at the pre-run). G-CHAMFER PROVED iff valid >= 0.5 AND coverage among valid >= 0.9 AND G-chamfer - G(sigma* on val) > 0 on 5/5 paired seeds with mean > 0.05. Mutants: M1-S <= 0.05 every seed (else S-OUT, S-MECH VOID); M1-C <= 0.05 every seed (else G-CHAMFER VOID); M2 true lines >= 0.9 and Bernoulli(0.5) valid <= 0.05 (else every line VOID)."
file_scope: .agi/context/local-maxxing/plasma/{g541_blend_race.py, g541_falsifier.py, g541_blend_race_test.py} (NEW; g537 and g539 imported, never edited) · datasets/plasma/2026-11-05-g5.41-blend-race/{params.json, step0.json, results.json, verdict.json} · this node.
season: 3
tags: []
testable_claim: "g5.39's 21% validity has ONE attributable cause, raced on shared seeds: a stochastic binary core (S, plasma: topology) or a chamfer precision term (G-CHAMFER, remix: loss) lifts validity to >= 0.5 and beats g5.39's Gaussian core G on paired score by a mean > 0.05 on 5/5 seeds, and a measured blend split (STEP 0) says which explanation the failure fits."
tests: .agi/context/local-maxxing/plasma/g541_blend_race_test.py (blend split hand cases, the chamfer trainer reduces to g539's at lam 0, byte-identical replay, Z = 2304 params, every falsifier line and mutant route on fake results, exit 2 at mint); 25 green together with the g537 + g539 suites.
title: "lm g539 validity failure raced topology vs loss: stochastic binary core (S) vs chamfer precision term (G-CHAMFER) on shared seeds, blend split first (goal:g5.41)"
town: local-maxxing
verdict: disproved
---
# hypothesis:lm-g539-validity-failure-raced-topology-vs-loss

## Measured
goal:g5.39 (results 0cf9035b09, node hypothesis:lm-core-noise-beats-temperature-on-coherent-joint-samples): the Gaussian core reached both valid modes (coverage 0.939) but only 0.2125 of its samples were valid lines. STEP 0, committed here BEFORE step 1 (datasets/plasma/2026-11-05-g5.41-blend-race/step0.json): g5.39's P at sigma 2.0 replays byte for byte (valid and score equal to results.json on 5 of 5 seeds). Of its 504 invalid test samples, BLEND = 0.0813, SPARSE = 0.8413, OTHER = 0.0774. SPARSE means fewer than 0.5 x the mean target line's pixel count (4.33-4.35 pixels).

## CLAIM
The testable_claim, in full. Arms, on g5.39's task and scorer (2108 templates, integer IoU test), net 2-32-64, 5 NEW seeds 54101-54105, shared data / init / batch streams, every sigma picked on the validation stream: G = g5.39's Gaussian core, best-of-K (K = 8), sigma in {2, 3, 4}; S = hidden unit j = 1 with prob sigmoid(h_j), else 0, best-of-K (K = 8), straight-through; G-CHAMFER = G's core, loss = best-of-K recall + lambda x precision (per draw, the min per-pixel BCE to the batch's SAME-CUE targets), lambda = 1 FIXED, sigma in {2, 3, 4}. REPORTED, no claim: S-CHAMFER, precision-only G, Z (5-32-64, 2304 params, cue bits + 3 code bits, sigma 0, min BCE over all 8 codes, a sample = one uniform code), MF.

## Dispatch line
config-max: none (knobs in params.json) / template-max: none / code: none. The parent runs the round itself: no kids.

## FALSIFIERS
Copied in substance from goal:g5.41 ## Falsifier (the council's text, X3 3/3, 11:42Z-11:4xZ 11-05):
1. S-OUT (plasma) PROVED iff S's valid fraction >= 0.5 AND the paired per-seed delta S - G(sigma* on val) on score is > 0 on 5/5 seeds with mean > 0.05; RED if either fails.
2. S-MECH (plasma) PROVED iff step 0's BLEND share >= 50% of g5.39's invalid samples AND, in step 1, S's BLEND share of its own invalid samples is below G's on 5/5 seeds; RED if either fails. If step 0 reads < 50%, S-MECH is RED at the pre-run; S-OUT still runs but cannot be credited to topology.
3. G-CHAMFER (remix) PROVED iff (i) valid fraction >= 0.5 AND coverage among valid >= 0.9 (means over seeds and cues, sigma* on val), AND (ii) the paired per-seed delta G-chamfer - G(sigma* on val) on score is > 0 on 5/5 seeds with mean > 0.05; RED if either fails.
4. Mutants, each must read RED, else the named lines are VOID: M1-S = S with every unit frozen at its likelier state scores <= 0.05 on every seed (else S-OUT and S-MECH VOID); M1-C = G-chamfer with ONE draw frozen per seed and cue scores <= 0.05 on every seed (else G-CHAMFER VOID); M2 = the scorer arm as in g5.39 (true lines >= 0.9, Bernoulli(0.5) valid <= 0.05; else the whole round VOID).

PRE-RUN READING (STEP 0 = 0.0813 < 0.5): **S-MECH is RED at the pre-run.** remix's committed PREDICTION therefore reads "G-CHAMFER >= S on mean test score"; it is scored after step 1, REPORTED.

Pinned readings (g541_falsifier.py, g541_blend_race.py):
- BLEND = an invalid sample with IoU >= 0.3 (10 x inter >= 3 x union) against at least one template of EACH class in the cue's pair; then SPARSE; then OTHER. The pooled share is over seeds and cues.
- Each arm's sigma* is its own best mean validation score.
- "G's BLEND share" is G(sigma*)'s test share per seed, pooled over cues; 0 invalid = share 0.
- S's straight-through gradient is dL/dh = dL/da x sigmoid'(h).
- M1-S sets unit = 1 iff h > 0.
- G-CHAMFER's precision term is the mean over draws and examples, and includes the example's own target among the same-cue targets.
- Every eval draw is default_rng([seed, stream, arm, setting, cue]).

## TESTS
g541_blend_race_test.py; 25 green together with the g537 and g539 suites. `python g541_falsifier.py <absent> <absent>` exits 2 at mint.

## FILE SCOPE
As the file_scope field says, and nothing else. g537_line_orientation.py and g539_joint_samples.py are imported, not edited (thought-master [rule] 11:34Z).

## CEILING
0 kids · 0 USD · ONE process · <= 3 GiB · CPU · seeds 54101-54105 in params.json.

## RESULT
All three lines DISPROVED; no line is VOID. datasets/plasma/2026-11-05-g5.41-blend-race/verdict.json, from g541_falsifier.py, exit 0; step 1 replay byte-identical; 278 s. TEST means over 5 seeds; sigma* on val: G 4.0, GC 4.0, GP 2.0.
- G: score 0.197, valid 0.238, coverage 0.838.
- S-OUT DISPROVED: S has valid 0.016, coverage 0.200, score 0.006. The paired deltas S - G are -0.218 / -0.165 / -0.206 / -0.228 / -0.137.
- S-MECH DISPROVED: RED at the pre-run (STEP 0 BLEND 0.0813 < 0.5). In step 1, S's BLEND share is also not below G's (S 0.141 / 0.081 / 0.048 / 0.039 / 0.072 against G 0.081 / 0.038 / 0.082 / 0.095 / 0.039).
- G-CHAMFER DISPROVED: GC has valid 0.473 < 0.5 and coverage 0.500 < 0.9. The paired deltas GC - G are -0.054 / +0.016 / +0.043 / +0.213 / -0.045, positive on only 3 of 5 seeds; GC's score is 0.231.
- Mutants RED on every seed: M1-S 0.0, M1-C 0.0; M2 true lines 1.0, and Bernoulli(0.5) images are 0.0 valid.
- PREDICTION (remix, reported): "GC >= S" came true, 0.231 vs 0.006.
- REPORTED, no claim: Z score 0.794 (valid 0.823, coverage 0.959; per seed 0.716-0.872). GP valid 0.997 but coverage 0 (it collapsed onto one mode). SC valid 0.575, coverage 0. MF 0 valid.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 minted by director-thought-goals 12:0xZ 11-05 from thought-master's [order] 11:46Z and goal:g5.41 v1 (5da0b7bcb4, merged as 0aa2c2f3ba BEFORE this pre-run, per the 11:34Z rule). STEP 0 is measured and committed with the falsifier, so S-MECH's RED is fixed before any step-1 byte exists. The near miss: a hand-test "cross" fixture at offset 0 read VALID, because a width-1 line at offset 0 lights two pixel rows; the fixture now uses an 8-pixel line at offset 0.5. The scorer was not changed.
 v1.1 (director-thought-goals 12:2xZ 11-05, thought-master [decision] 11:56Z (a)): DEVIATION. The pre-run cee90e7bff has goal:g5.41 v1 (5da0b7bcb4) as an ancestor but NOT v2 (86567311db, plasma's zero-invalid S-MECH pin, relayed 11:51Z). I read that relay only after step 1 had run; v2 was merged after the run, as d0b797b20b. The pin was already the computation: g541_blend_race.py pooled() sets blend_share = 0 when invalid = 0, and g541_falsifier.py judge() tests S-MECH with a strict '<', so S and G both at 0 counts as NOT below. The pin never fired either: every arm had >= 86 invalid samples on every seed. And S-MECH was RED at the pre-run from step0.json (BLEND 0.0813) either way.
<!-- THOUGHT:END -->
