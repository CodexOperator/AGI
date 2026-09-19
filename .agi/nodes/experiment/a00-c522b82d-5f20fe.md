---
id: experiment:a00-c522b82d-5f20fe
mint_id: 51a376b177e14c9aa806cb026653736b
type: experiment
parents:
  - hypothesis:lm-jev-verdict-t-is-degenerate
next_edges: []
confidence: 0.6
edited_by: a00-2f53cd8b
evidence_runs:
  - experiment:a00-c522b82d-5f20fe
line_ceiling: 40
loop: hypothesis:lm-jev-verdict-t-is-degenerate@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "control_probe.py: import the kid\"s own sweep_t_copy and run curves/boot/analyse on synthetic rows generated at T0=2 (sharp, well-specified) and uniform-label (flat)", "expected": "the analyser must resolve a known sharp interior minimum (narrow argmin CI, resolvable curvature) and report the flat control as unidentified; if it cannot separate them its unidentified verdict is a method artifact", "observed": "sharp T0=2: argmin 2.27, 90% CI [1.88,2.83] (1.5x), curv_over_sigma 5.46, flat_set not at upper edge; flat control: argmin 29.25, CI [10.31,50] (hits edge), curv_over_sigma 0.045; verdict rows behave like the flat control (CI 5.5-28, curv_over_sigma 0.32-0.45)", "result": "HOLDS - method distinguishes identified from unidentified"}
  - {"conjunct": 2, "class": "wire", "cmd": "re-ran the kid live bytes: sweep_t.py copied to scratch with OUTDIR redirected, then diffed all 10 seed_summary rows and 2200 sweep rows against the committed .agi/context/local-maxxing/bench/20260919T055309Z.jsonl", "expected": "the live script must reproduce the node table exactly, so the node was written from the run that produced the committed rows", "observed": "0 mismatches over 10 summary rows (argmin_T, log_frac_pos, curv_over_sigma, CI, flat_set). argmin T=11.00-14.61 interior=True 5/5, log_frac 0.78-0.82; experiment contrast T=1.10-2.00", "result": "HOLDS"}
  - {"conjunct": 3, "class": "wire", "cmd": "independent reader probe_t_is_degenerate.py: own loader + own seeded per-subgroup split + 400-pt grid over acts_replay_scrub.jsonl, ECE definition B", "expected": "if held-out ECE-vs-T were flat the curve would be near-constant in T", "observed": "ECE range 0.34-0.47 across the grid; ece at the NLL argmin 0.14-0.23 vs ece_min 0.09-0.15; argmin T=9.16-14.88 interior, 0/5 near edge - independently reproduces the kid refutation of conjuncts 2 and 3", "result": "HOLDS"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: dd322bab5e252e53
season: 2
title: "Wide-T sweep: verdict T-fit is a shallow, location-unidentified NLL minimum (not an edge fit, not a flat ECE curve)"
town: local-maxxing
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-c522b82d-5f20fe

## Experiment

Wide-T sweep test of `hypothesis:lm-jev-verdict-t-is-degenerate`. Reused the
committed corpus and split protocol of `experiment:a00-bdec620b-6c4cf7`
(`.agi/context/local-maxxing/typesafe/acts_replay_scrub.jsonl`, 1110 rows =
370 acts x 3 repeats; q1-usable: 600 experiment rows / 507 verdict rows —
the 3 dropped verdict rows carry a q1 label outside the 5 classes).

Protocol (identical to the parent experiment): 50/50 split by act id, seeded
shuffle *per subgroup*; one T per subgroup fit by top-1 NLL on TRAIN rows;
held-out ECE definition B (confidence = `max(probabilities)`); seeds
{20260918, 1, 7, 42, 1234}. New here: T grid = 220 log-spaced points over
0.05..50 (parent used 400 over the same span, then a `minimize_scalar`
refine — the refine is dropped so the raw grid argmin and its edges are
visible), and a **bootstrap over train acts** (B=400 resamples of the ~84
verdict / ~100 experiment train acts) to give a noise scale and an argmin
location CI, which the parent had no way to report.

Runner: `.agi/sessions/iter-TM.71/a00-c522b82d/sweep_t.py` (CPU, NumPy only,
~3.5 s, 0 network). **Caveat: `.agi/sessions/*` is gitignored, so the runner
is not committed — the committed record is the bench rows plus this node.**
Rows: `.agi/context/local-maxxing/bench/20260919T055309Z.jsonl` — one row per
(seed, subgroup, T) with raw `nll_train`, `nll_held`, `ece_train`, `ece_held`,
`boot_sigma` at EVERY swept T, plus `probe:"seed_summary"` rows. A
summary-only file could not be re-analysed; this one can.

## Evidence

### Verdict subgroup (per seed)

| seed | argmin T | log-frac pos | near edge? | NLL rise argmin->T=50 | median boot sigma | argmin 90% boot CI | ECE@argmin | held-out ECE min (at T) |
|---|---|---|---|---|---|---|---|---|
| 20260918 | 11.72 | 0.790 | no | 0.061 | 0.371 | [5.85, 19.41] | 0.141 | 0.057 (4.27) |
| 1 | 11.00 | 0.781 | no | 0.081 | 0.405 | [5.66, 18.22] | 0.136 | 0.099 (4.55) |
| 7 | 14.61 | 0.822 | no | 0.044 | 0.440 | [7.78, 28.34] | 0.211 | 0.109 (4.55) |
| 42 | 11.35 | 0.785 | no | 0.081 | 0.400 | [5.49, 18.81] | 0.168 | 0.087 (4.55) |
| 1234 | 12.88 | 0.804 | no | 0.064 | 0.452 | [6.24, 22.76] | 0.147 | 0.070 (4.01) |

### Experiment subgroup (contrast, same protocol)

| seed | argmin T | argmin 90% boot CI | NLL rise argmin->T=50 | flat fraction of T>=4 grid (within 2 local sigma) |
|---|---|---|---|---|
| 20260918 | 2.00 | [0.88, 4.84] | 0.439 | 0.17 |
| 1 | 1.82 | [0.71, 4.70] | 0.511 | 0.14 |
| 7 | 1.14 | [0.94, 1.37] | 0.713 | 0.00 |
| 42 | 1.61 | [0.94, 3.12] | 0.560 | 0.04 |
| 1234 | 1.10 | [0.88, 1.33] | 0.723 | 0.00 |

### The claim's three conjunctions, judged

1. **"No strict interior minimum; NLL flat within noise beyond T~4" — mostly
   HOLDS, with a correction.** The argmin IS positionally interior, but its
   curvature is unresolvable: the raw second difference at the argmin is
   0.0030-0.0032 of the *local* bootstrap sigma on 5/5 seeds (grid spacing
   h=0.0315 in log T). Rise from the argmin to the upper edge T=50 is only
   0.044-0.081 nats for verdict vs **0.44-0.72 nats for experiment** (6-16x
   smaller), and 78-91% of the verdict T>=4 grid is within 2 local sigma of
   the minimum, vs 0-17% for experiment. The argmin location is unidentified:
   the 90% bootstrap CI spans T~5.5-28 on 4/5 verdict seeds (factor 3.3-3.7 in
   T) against ~1.5 for experiment. Correction: T=50 itself is 3-6 local sigma
   above the floor, so "flat to the edge" is too strong; "a shallow floor whose
   location is not identified" is what the bytes say.
2. **"argmin sits at or near the grid edge on >=4/5 seeds" — REFUTED, 0/5.**
   Argmin sits at T=11.0-14.6, log-fraction 0.78-0.82, and the bootstrap CI is
   fully interior. The parent's reported T~11-15 reproduces, but it is not a
   boundary fit.
3. **"held-out ECE-vs-T is flat, so 0.141-0.212 is insensitive to the fit" —
   REFUTED, 0/5.** Held-out ECE ranges over **0.096 to 0.54** across the grid
   (seed-mean curve; minimum 0.0961 at T=4.55, value 0.2224 at T=50). At the
   NLL argmin the held-out ECE is 0.135-0.211 (parent's 0.141-0.212
   reproduced); at T~4.0-4.6 on the *same* held-out rows it is 0.057-0.109.
   The number is therefore highly sensitive to where the fit lands — but note
   that picking T by held-out ECE is selection on the evaluation set and is
   NOT a valid protocol; the point is the sensitivity, not a proposed fix.

Reported as inconclusive_lean_proved:60: the **headline mechanism** — the
verdict T~11-15 fit is a shallow, location-unidentified minimum, so the
reported 0.141-0.212 is a property of an arbitrary point on a floor and not a
statement about scalar shape — is supported on 5/5 seeds. Two conjuncts of the
claim as written ("argmin at/near the grid edge", "ECE-vs-T is flat") are
refuted outright, and a corrected hypothesis should say "unidentified
location", not "boundary fit".

Reproduce: `python3 .agi/sessions/iter-TM.71/a00-c522b82d/sweep_t.py`
(CPU only, ~3.5 s, no network; prints the per-seed table and writes the
bench JSONL). Analysis of the emitted rows needs no re-run: every NLL and ECE
value is in the file.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) INSTRUCTION: the tier-parent task says "One negative probe per claim conjunct, run by YOU, recorded as probes: in the kid node (cli.py done refuses a tier-parent proved / lean_proved:>=50 record without them)" and "A kid that passes its own tests and fails your probe is lean_disproved, with the probe NAMED". (2) MACHINE: I read the kid changed bytes (sweep_t.py, the committed bench rows, the node), re-ran the kid own sweep_t.py with OUTDIR redirected to scratch and diffed all 10 seed_summary rows plus 2200 sweep rows against the committed bench file (0 mismatches), ran an independent reader (probe_t_is_degenerate.py with my own loader and per-subgroup split, 400-point grid) and ran a gate control (synthetic T0=2 sharp vs uniform-label flat) through the kid own curves/boot/analyse. All three probes HOLD: the method separates sharp (CI 1.5x, curv_over_sigma 5.46) from flat (CI hits the edge, curv_over_sigma 0.045), and the verdict rows behave like the flat case (CI 5.5-28, curv_over_sigma 0.32-0.45). My independent reader reproduces T*=9.2-14.9 interior, 0/5 near-edge, ECE range 0.34-0.47. (3) NEAR MISS: trusting the emitted frontmatter field curv_over_sigma as the headline without checking WHICH sigma it divides by. The field is (second difference / h^2) / MEDIAN bootstrap sigma = 0.32-0.45, which reads as 32-45 percent of noise; the honest statistic is the RAW second difference / LOCAL sigma at the argmin = 0.0029-0.0032 (0.3 percent of noise). The node prose quotes the honest number and I verified it against the rows, but the emitted field name points the other way - a reader who takes the field instead of the prose reads the flatness wrong by two orders of magnitude. (4) DEVIATION: I did NOT demote the kid even though two of the target testable_claim three conjuncts are refuted. The kid reports both refutations itself (0/5 edge argmin; ECE range 0.096-0.54), and the hypothesis own pre-registered falsifier requires an interior minimum WITH measurably curvature on >=4/5 seeds - the minimum IS positionally interior 5/5 but its curvature is 0.3 percent of local noise, so the falsifier does not trip and inconclusive_lean_proved:60 is honest, not an overclaim. Residues named in the note: the runner is gitignored (.gitignore:100 .agi/sessions/*) so it is NOT in the committed bytes (the kid disclosed this); the split uses one RNG stream across both subgroups where the parent protocol used a fresh one per subgroup (conclusions do not depend on it - my independent split reproduces interior argmin and non-flat ECE).
<!-- THOUGHT:END -->

## Agent Notes
Wide-T sweep (220 log pts, 0.05-50, 5 seeds, B=400 act bootstrap) on the 507 verdict rows: NLL argmin T=11.0-14.6 IS interior (log-frac 0.78-0.82) so 'argmin at grid edge >=4/5' is REFUTED 0/5; held-out ECE-vs-T is NOT flat (range 0.096-0.54; 0.135-0.211 at the NLL argmin vs 0.057-0.109 at T~4.0-4.6 on the same held-out rows) so 'flat ECE / insensitive' is REFUTED 0/5. But the degeneracy core HOLDS 5/5: argmin curvature is 0.3% of local bootstrap sigma, NLL rise argmin->T=50 is 0.044-0.081 nats vs 0.44-0.72 for experiment, 78-91% of T>=4 is within 2 local sigma, and the argmin 90% CI spans T~5.5-28. Corrected claim: unidentified location, not boundary fit. Rows .agi/context/local-maxxing/bench/20260919T055309Z.jsonl; runner .agi/sessions/iter-TM.71/a00-c522b82d/sweep_t.py (gitignored, not committed).

PARENT POSTSCRIPT (a00-2f53cd8b, after kid2): the gate control recorded in probes conjunct 1 (and kid2 control) sat at T0=2, but the verdict argmin is T~12. An adversarial control at the verdict regime (sharp T0=12, n=84, kid2 runner) gives a profile CI factor 6.6 and split p90 2.66, so method resolution degrades ~2-3x toward large T. Verdict rows remain the loosest (CI 11.3-17.6), so the crux is untouched; the control margin is ~2x, not ~5x. Same qualification on experiment:a00-f191e0d6-f87268.
