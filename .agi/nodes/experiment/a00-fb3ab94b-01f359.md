---
id: experiment:a00-fb3ab94b-01f359
mint_id: 59cb78baa37543568843885cb52b5279
type: experiment
parents:
  - hypothesis:lm-jev-isotonic-per-group-fixes-verdict-ece
next_edges: []
confidence: 0.85
edited_by: a00-de483bb6
evidence_runs:
  - experiment:a00-fb3ab94b-01f359
line_ceiling: 40
loop: hypothesis:lm-jev-isotonic-per-group-fixes-verdict-ece@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "by": "parent", "cmd": "parent_isotonic_probe2.py: independent hand-written PAVA, same np.random.default_rng(seed) permutation split and same 10-bin ECE as the kid script", "expected": "verdict held-out ECE <=0.10 on >=4/5 seeds", "observed": "0.0756,0.1153,0.1048,0.0565,0.2034 -> 2/5 <=0.10, mean 0.1111; matches the kid table exactly", "result": "FAILS (claim disproved)"}
  - {"conjunct": 1, "class": "gate", "by": "parent", "cmd": "alt-label probe: correctness = argmax(probabilities)==labels.q1 (7/1110 rows differ from choice==label)", "expected": "verdict <=0.10 on >=4/5", "observed": "0.081,0.1185,0.1003,0.060,0.1995 -> 2/5", "result": "FAILS under both correctness definitions"}
  - {"conjunct": 2, "class": "gate", "by": "parent", "cmd": "same independent run, experiment subgroup", "expected": "<=0.12 on >=4/5 seeds", "observed": "0.1012,0.1801,0.1013,0.0736,0.0783 -> 4/5 <=0.12", "result": "HOLDS"}
  - {"conjunct": 2, "class": "gate", "by": "parent", "cmd": "leakage/oracle: isotonic fit on the held-out fold itself", "expected": "if no leakage and failure is generalization, train-fit stays high while oracle is near 0", "observed": "verdict oracle 0.0000-0.0058, experiment oracle 0.0084-0.0372; train-fit 0.057-0.203", "result": "HOLDS (no leakage; failure is generalization)"}
  - {"conjunct": 1, "class": "wire", "by": "parent", "cmd": "rerun .agi/context/local-maxxing/typesafe/jev_isotonic_residual.py to a temp file and diff against committed bench/20260919T055335Z.jsonl", "expected": "byte-identical; script reads the real corpus", "observed": "byte-identical; reads acts_replay_scrub.jsonl, 1107 usable rows", "result": "HOLDS"}
production_lines: 72
profile: balanced
role: kid
scaffold_hash: be6d7ca82a0048b8
season: 2
title: "Per-group isotonic does NOT calibrate the verdict subgroup either: held-out ECE 0.057-0.203, <=0.10 on only 2/5 seeds (shape fails where scale failed)"
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-fb3ab94b-01f359

## Experiment

Tested `hypothesis:lm-jev-isotonic-per-group-fixes-verdict-ece`: that the verdict
q1 residual left over after per-group temperature is **shape not scale**, and
per-group **isotonic regression** of top-1 confidence against top-1 correctness
fit on the train fold brings verdict held-out ECE <= 0.10 on >= 4/5 seeds.

Data: `.agi/context/local-maxxing/typesafe/acts_replay_scrub.jsonl` (read-only,
0 API calls, 0 network, CPU). 1110 rows = 370 acts x 3 repeats; 1107 usable q1
rows (n_experiment=600, n_verdict=507; 1 verdict act has no q1 label). Split:
50/50 by act id WITHIN each subgroup, seeded shuffle, held = second half of the
permutation; seeds exactly 20260918/1/7/42/1234.

**Definitions.** ECE = 10 equal-width bins, the repo's local definition
(`class_ranking_review_call.py:18`). `ece_B` confidence = `max(probabilities)`
(the claim's arm); `ece_A` confidence = the self-reported scalar
`answers.q1.confidence`. Correctness = `answers.q1.choice == labels.q1`.
Fit = **PAVA by hand** (pure NumPy, no sklearn dependency; cross-checked against
`sklearn.IsotonicRegression(out_of_bounds="clip")`, verdict numbers agree to
<0.002). The claim's numbers correspond to the **max-prob (ece_B)** arm; the
self-reported scalar is the secondary arm.

Probe: `.agi/context/local-maxxing/typesafe/jev_isotonic_residual.py` (kept
under `typesafe/` rather than `sessions/` on purpose: `.gitignore:100` hides
`session/`, which is exactly how the TM.57 probe became non-reproducible).
Rows: `.agi/context/local-maxxing/bench/20260919T055335Z.jsonl` (full-corpus
before per group, one row per seed x subgroup, plus pooled).

### Held-out ECE, per-group isotonic on max-prob (ece_B)

| seed | exp before | exp after | ver before | ver after | ver after (scalar input) | pooled after | argmax d (winner-only) | argmax d (elementwise) |
|---|---|---|---|---|---|---|---|---|
| 20260918 | 0.0932 | 0.1012 | 0.3465 | **0.0756** | 0.0887 | 0.0895 | 0.0000 | 0.119 |
| 1 | 0.1072 | 0.1801 | 0.3258 | **0.1153** | 0.1235 | 0.1505 | 0.0000 | 0.028 |
| 7 | 0.1005 | 0.1013 | 0.3197 | **0.1048** | 0.1019 | 0.1029 | 0.0000 | 0.770 |
| 42 | 0.0900 | 0.0736 | 0.3371 | **0.0565** | 0.0542 | 0.0658 | 0.0000 | 0.036 |
| 1234 | 0.0716 | 0.0783 | 0.2855 | **0.2034** | 0.1970 | 0.1354 | 0.0000 | 0.040 |
| **mean** | 0.0925 | 0.1069 | 0.3229 | **0.1111** | 0.1131 | 0.1088 | 0.0000 | — |
| min..max | 0.072..0.107 | 0.074..0.180 | 0.286..0.347 | **0.057..0.203** | 0.054..0.197 | 0.066..0.151 | 0.0000 | — |

Full-corpus before (no split): experiment ece_B 0.0624 / ece_A 0.0715;
verdict ece_B 0.3234 / ece_A 0.3211; pooled ece_B 0.1515.

## Evidence

Pre-registered decisifiers, reported per seed, not softened:

1. **verdict held-out ECE <= 0.10 on >= 4/5 seeds — FAILS DECISIVELY.** Isotonic
   reaches <= 0.10 on **2/5** seeds (0.0756, 0.0565), is just outside on 0.1048,
   and badly outside on 0.1153 and 0.2034. Mean 0.1111 (before 0.3229).
2. **experiment held-out ECE <= 0.12 on >= 4/5 seeds — HOLDS** at 4/5 (only
   seed 1 at 0.1801 trips it). The overfit guard is satisfied, so the verdict
   failure is not a global overfit of the method.
3. Pooled held-out ECE <= 0.12: 3/5 (0.0895, 0.1029, 0.0658 <= 0.12; 0.1505,
   0.1354 above). Mean 0.1088.

So the claim is **DISPROVED**. As the hypothesis itself pre-registers, this is
the trigger to move to **cause 3 (3-repeat agreement split)** or **cause 4
(elicitation channel A vs B)** — the residual is not fixed by shape either.

Two honest corrections that do not change the verdict:

- **Isotonic is not a rank-preserving calibration map when applied per class.**
  Remapping only the winning confidence changes argmax by exactly 0.0000
  (trivially — same class); remapping every class probability elementwise then
taking argmax moves up to **77%** of held-out verdict rows on seed 7 (0.02-0.04
  elsewhere). On seed 7 the elementwise map collapses many class probabilities to
  equal step values, so the large delta is a tie/degeneracy artifact of that
  application, not evidence that a calibrated map reshuffles verdicts. Either
  way the claim is not a pure calibration fix under the elementwise reading.
- **The oracle in-sample bound shows the failure is generalization, not method
  capability.** Fitting isotonic on the held-out fold itself drives verdict ECE
  to 0.000-0.006 on all 5 seeds. The train-fold map does not transfer: the
  verdict subgroup's per-seed miscalibration is unstable across the act split.

Reproduce: `python3 .agi/context/local-maxxing/typesafe/jev_isotonic_residual.py
.agi/context/local-maxxing/bench/20260919T055335Z.jsonl` (CPU, ~0.6 s, no
network, 0 API calls). Output is byte-identical to the committed bench rows.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW of a00-fb3ab94b (verdict disproved), TM.73, parent a00-de483bb6. The kid node is CONFIRMED, not overridden.
(1) INSTRUCTION: the tier-parent task says "One negative probe per claim conjunct, run by YOU, recorded as probes: in the kid node", and "read the bytes that moved, not the summary that describes them".
(2) MACHINE: I read the moved bytes -- .agi/context/local-maxxing/typesafe/jev_isotonic_residual.py -- and re-implemented the protocol independently (my parent_isotonic_probe2.py, hand-written PAVA, same np.random.default_rng(seed) permutation split, same 10-bin ECE, same 5 seeds). My held-out verdict-after numbers reproduce the kid table exactly: 0.0756 / 0.1153 / 0.1048 / 0.0565 / 0.2034 (<=0.10 on 2/5, mean 0.1111); experiment-after 0.1012 / 0.1801 / 0.1013 / 0.0736 / 0.0783 (4/5 <=0.12). A rerun of the kid script diffed BYTE-IDENTICAL against committed bench/20260919T055335Z.jsonl. An oracle fit on the held-out fold gives verdict ECE 0.0000-0.0058 while the train-fit stays 0.057-0.203, so there is no train/held leakage and the failure is generalization. Re-labelling correctness as argmax(prob)==label (7/1110 rows differ from choice==label) still leaves verdict <=0.10 on only 2/5. The claim conjunct "verdict held-out ECE <=0.10 on >=4/5 seeds" fails under both label definitions; the conjunction is disproved.
(3) NEAR MISS: the kid reported the elementwise argmax delta up to 0.77 on seed 7, which satisfies "argmax moved a lot" while losing the mechanism -- that delta is a step-map tie collapse where the monotone map assigns equal fitted values to distinct classes, not evidence that a calibrated map reshuffles verdicts; the winner-only convention delta is exactly 0.0000. Both conventions are kept in the body rather than the flattering one alone.
(4) DEVIATION: none. The claim pre-registers its own next lever (cause 3 repeat-agreement, or cause 4 elicitation channel A vs B); that next hypothesis belongs to the parent idea node, outside this target subtree, so this round judges and stops rather than fork a sibling or blind-rerun the disproved claim.
<!-- THOUGHT:END -->

## Agent Notes
Per-group isotonic on max-prob: verdict held-out ECE 0.0756/0.1153/0.1048/0.0565/0.2034 (mean 0.1111, before 0.3229) -> <=0.10 on only 2/5 seeds; experiment 4/5 <=0.12 (guard holds); pooled 3/5 <=0.12. Shape fails where scale failed: pre-registered trigger to cause 3 (repeat-agreement) or cause 4 (channel A/B). Oracle in-sample fit reaches 0.000-0.006, so failure is generalization not capability. Probe tracked at typesafe/jev_isotonic_residual.py, rows bench/20260919T055335Z.jsonl.

Parent review TM.73: kid disproved the isotonic claim and I reproduced it independently. Verdict-after 0.0756/0.1153/0.1048/0.0565/0.2034 (<=0.10 on 2/5) matches my own PAVA exactly; experiment-after 4/5 <=0.12; rerun byte-identical; oracle 0.000-0.006 rules out leakage; alt correctness definition still 2/5. Probes recorded under probes:. Claim disproved: shape fails where scale failed; next lever is cause 3 (repeat agreement) or cause 4 (channel A vs B).
