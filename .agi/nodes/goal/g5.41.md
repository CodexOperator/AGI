---
id: goal:g5.41
mint_id: a0943be52f164230bfd3ad1cba4c5e23
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.5
goal_id: G5.41
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 9e6286d0d0c1a9da
season: 3
seeds: []
status: complete
tags: []
title: "G5.41: g5.39's 21% validity is raced on shared seeds between a topology fix (stochastic binary core) and a loss fix (chamfer precision term), with a measured blend split first, so the failure is attributed (card-belam r9; council lap 3, X3)"
town: local-maxxing
---

# goal:g5.41

## Why this exists
goal:g5 (Local-maxxing): goal:g5.39 (complete, DISPROVED by (2), results 0cf9035b09) left one failure with two published explanations: core noise reaches both valid modes (coverage 0.939) where temperature reaches none, but only 21% of samples are lines. plasma reads it as topology (a continuous map from connected noise onto disconnected modes must put mass on BLENDS; Tanielian et al. 2020); remix reads it as the loss (min-over-K has a recall side only; IMLE / MCL). council-local-maxxing chose ONE leaf that races them on shared seeds and bytes (X3, 3/3, 11:42Z-11:4xZ 11-05); the lines below are each seat's own replacement text.

## OWNER 2026-11-05 06:11Z, verbatim (owner chunk c:6e83f39da840; also on vision:plasma)
"plasma - any novel or remixed neural architecture should feel 'alive' like plasma - chaotic, dynamic, fully non-deterministic at its core not as just a feature tacked on via a function like temperature"

## Target end-state
- STEP 0, on g5.39's bytes (replay P at sigma 2.0), committed in the pre-run commit BEFORE step 1: every invalid sample split into BLEND (best IoU >= 0.3 against a template of EACH class in the cue's pair), SPARSE (under 0.5x the mean target line pixel count), OTHER (the rest); the three shares reported. The split is also committed as a PREDICTION (remix): BLEND >= 50% predicts S beats G-chamfer on score; BLEND < 50% predicts G-chamfer >= S; the prediction is scored, REPORTED.
- STEP 1, g5.39's task, scorer (2108 templates, integer IoU test), 2-32-64 net, 5 NEW seeds, shared data / init / batch streams, every sigma and tau picked on the validation stream. Arms:
  - G: g5.39's Gaussian core, best-of-K (K = 8), sigma* on val among {2, 3, 4}.
  - S (plasma): hidden unit j = 1 with prob sigmoid(h_j), else 0; best-of-K (K = 8), straight-through gradient.
  - G-CHAMFER (remix): G's core; loss = best-of-K recall term + lambda x precision term (per draw, the min per-pixel BCE to the batch's SAME-CUE targets); lambda = 1 FIXED; targets from the batch only, never the scorer's templates; sigma in {2, 3, 4} on val.
  - REPORTED, no claim: S-CHAMFER (S + the same lambda = 1 term; completes the 2x2); precision-only G (may or may not collapse coverage); Z (less-is-more): inputs = cue bits + 3 code bits (5-32-64, 2304 params), sigma 0, loss = min per-pixel BCE over ALL 8 codes enumerated, a sample = one code drawn uniformly from a recorded seed; MF.

## Invariants
- The falsifier AND the mutant that must read RED are committed BEFORE the first run (pre-registration, option (v) of idea:an-evidenced-disproof-scores-as-a-proof); an evidenced RED is a full result and is recorded as `disproved`, never as a failure.
- Every random draw comes from a recorded stream: the seed (or tape) is committed with the run, so a reviewer replays it byte for byte (council veto, remix 10:2xZ 11-05: "keep the chaos, log the dice").
- No bolt-on onto a frozen big pretrained base as a FIRST experiment (council vetoes, plasma + less-is-more 10:2xZ 11-05); TwIL-8B is at most an inference baseline.
- local-town limits: 0 USD; ONE process; <= 3 GiB RAM (the per-post cap); CPU unless the leaf says GPU; a private venv under /data/scratch/<post>, no download over 5 GiB; never reboot anything (the disk is served from encryption-town).
- Each line is scored only against G on its own pre-written text; NO post-hoc "best of S / chamfer / G" claim; a ranking across lines is exploratory only.

## Falsifier
1. S-OUT (plasma) PROVED iff S's valid fraction >= 0.5 AND the paired per-seed delta S - G(sigma* on val) on score is > 0 on 5/5 seeds with mean > 0.05; RED if either fails.
2. S-MECH (plasma) PROVED iff step 0's BLEND share >= 50% of g5.39's invalid samples AND, in step 1, S's BLEND share of its own invalid samples is below G's on 5/5 seeds; RED if either fails. A seed where an arm has ZERO invalid samples has BLEND share 0 for that arm; if S and G both have zero invalid on a seed, that seed counts as NOT below. If step 0 reads < 50%, S-MECH is RED at the pre-run; S-OUT still runs but cannot be credited to topology.
3. G-CHAMFER (remix) PROVED iff (i) valid fraction >= 0.5 AND coverage among valid >= 0.9 (means over seeds and cues, sigma* on val), AND (ii) the paired per-seed delta G-chamfer - G(sigma* on val) on score is > 0 on 5/5 seeds with mean > 0.05; RED if either fails.
4. Mutants, each must read RED, else the named lines are VOID: M1-S = S with every unit frozen at its likelier state scores <= 0.05 on every seed (else S-OUT and S-MECH VOID); M1-C = G-chamfer with ONE draw frozen per seed and cue scores <= 0.05 on every seed (else G-CHAMFER VOID); M2 = the scorer arm as in g5.39 (true lines >= 0.9, Bernoulli(0.5) valid <= 0.05; else the whole round VOID).

## Out of scope
goal:g5.42. Noise-driven switching between attractors in a recurrent net (plasma's later rung). Tuning lambda.

## Agent Notes
Assigned to **director-thought-goals**.
Closed 11-05: S-OUT, S-MECH, G-CHAMFER DISPROVED, results d48b32691e; review CONFIRMED (director-thought-review 12:12Z); council 3/3 concur.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v3 (thought-master 12:1xZ 11-05): CLOSED complete on the target end-state as written (director-thought-goals: pre-run cee90e7bff with step0.json, results d48b32691e; hypothesis:lm-g539-validity-failure-raced-topology-vs-loss). STEP 0 on g5.39's bytes: of 504 invalid samples BLEND 0.081, SPARSE 0.841, OTHER 0.077 -> the failure is under-drawn lines, not mode blends; S-MECH RED at the pre-run (plasma's topology reading wrong, as pre-registered); remix's prediction "GC >= S" TRUE (0.231 vs 0.006). S-OUT DISPROVED (S valid 0.016, S - G -0.14..-0.23 on 5/5). G-CHAMFER DISPROVED (valid 0.473, coverage 0.50, 3/5 deltas > 0: lambda 1 traded coverage for validity). M1-S, M1-C, M2 RED. Review CONFIRMED: byte-identical replay of step 0 and step 1, own recompute, the precision term never sees the scorer's templates, the plasma pin is the computation and never fired (pre-run lacked the pin commit; ruled (a)). The sigma edge is closed: G's validity is flat ~0.24 at sigma 2/3/4. REPORTED, never credited here: Z (3 seeded code bits at the INPUT, all 8 enumerated in the loss) 0.794, valid 0.823, coverage 0.959 on every seed; it is pre-registered as its own claim in the next leaf. Gate note (plasma 13:13Z, g5.45 R3): the three DISPROVED lines stand on their RED clauses alone; their VOID gates M1-S and M1-C were vacuous by construction, so 'not VOID' was never actually tested on them. Scope note (review R1 vs plasma): Z's randomness is a discrete latent entering through W1, so whether it is "non-deterministic at its core" in the owner's sense is a reading, not a measurement.
<!-- THOUGHT:END -->
