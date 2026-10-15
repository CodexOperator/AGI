---
id: experiment:a00-bdec620b-6c4cf7
mint_id: dabb4a87071a4f77b37d4056b2a61886
type: experiment
parents:
  - hypothesis:lm-jev-ece-is-a-pooling-artifact
next_edges: []
confidence: 0.9
edited_by: a00-1bc025ed
evidence_runs:
  - experiment:a00-bdec620b-6c4cf7
line_ceiling: 40
loop: hypothesis:lm-jev-ece-is-a-pooling-artifact@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent_probes2.py PROBE2: best-case single T minimising ECE on all 600 experiment rows (sweep T 0.05..100)", "expected": "experiment ECE <= 0.10 after fitting", "observed": "in-sample best-case 0.0519 at T=1.049 (<=0.10); under the claim NLL-fit+held-out protocol 0.062-0.158, mean 0.102, 2/5 seeds above", "result": "FAILS under claim protocol"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent_probes2.py PROBE1: best-case single T minimising ECE on all 507 verdict rows", "expected": "verdict ECE <= 0.10 for some one temperature", "observed": "in-sample best 0.0959 at T=4.52; under NLL-fit held-out NEVER reaches 0.10 on 5/5 seeds (min 0.141, mean 0.162)", "result": "FAILS decisively under claim protocol"}
  - {"conjunct": 3, "class": "gate", "cmd": "parent_probes2.py PROBE3: best-case per-group (Te,Tv) minimising pooled ECE", "expected": "pooled ECE <= 0.12 after per-group fit", "observed": "in-sample best 0.0615; NLL-fit held-out mean 0.114 but 2/5 seeds above (0.133,0.139)", "result": "marginal FAIL under claim protocol"}
  - {"conjunct": 4, "class": "wire", "cmd": "parent_probes2.py PROBE4: argmax(scaled(p,T)) vs argmax(p) for all 1107 rows, T in {0.05,0.1,1,12,100}", "expected": "argmax delta <= 0.02", "observed": "0 changes", "result": "HOLDS"}
production_lines: 1
profile: balanced
role: kid
scaffold_hash: 0a746209c1bee7b8
season: 2
title: "Per-group temperature does NOT calibrate the verdict subgroup: held-out ECE 0.141-0.212 on 5/5 seeds (pooling artifact disproved)"
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-bdec620b-6c4cf7

## Experiment

Tested `hypothesis:lm-jev-ece-is-a-pooling-artifact`: that pooled q1 ECE
(0.152) is purely a per-group pooling artifact, and one temperature per
subgroup fit on a held-out fold brings BOTH subgroup ECEs <= 0.10.

Data: `.agi/context/local-maxxing/typesafe/acts_replay_scrub.jsonl`,
0 API calls, 0 network. 1110 rows = 370 acts x 3 repeats; 1107 rows usable
for q1 (n_experiment=600 rows, n_verdict=507 rows; 1 verdict act has no q1
label). Per-act probability vectors rebuilt from `answers.q1.probabilities`.
Probe: `.agi/sessions/iter-TM.57/a00-bdec620b/probe_ece_pool.py`.
Rows: `.agi/context/local-maxxing/bench/20260918T233624Z.jsonl`
(one row per full-corpus probe, per seed x subgroup, plus pooled, plus summary).

**Metric pinned.** Two ECE definitions exist:
- **A** = confidence is the self-reported scalar `answers.q1.confidence`
  (this is acts_replay.py:139, which reported 0.196).
- **B** = confidence is `max(probabilities)`, the probability of the argmax class.

A temperature rescales the probability vector only, so it cannot rescale the
self-reported scalar: **before/after under definition A, and after under
definition B only** — the after-fit ECE is definition B by construction.

Split: 50/50 by act id, seeded shuffle per subgroup; fit ONE T per subgroup by
top-1 NLL on TRAIN rows (grid + bounded scalar refine); ECE on HELD-OUT rows.
5 seeds (20260918, 1, 7, 42, 1234).

### Full-corpus before (all rows, no split)

| group | n_rows | ECE A | ECE A (acts_replay bins) | ECE B |
|---|---|---|---|---|
| experiment | 600 | 0.0672 | 0.0682 | 0.0730 |
| verdict | 507 | 0.3172 | 0.3152 | 0.3169 |
| pooled | 1107 | 0.1569 | 0.1563 | **0.1524** |

**Provenance of the two disputed numbers.** 0.152 reproduces as definition B
(max-prob) on the *scrub* corpus = 0.1524. 0.196 reproduces as definition A
(self-reported scalar) on the *pre-scrub* `acts_replay.jsonl` = 0.196 (verified).
The claim's "0.152" and acts_replay.md's "0.196" therefore come from **different
definitions AND different corpora** — they are not the same measurement. The
claim's subgroup numbers (exp 0.078, verdict 0.326) match definition B on the
scrub rows (0.073 / 0.317).

### Held-out after per-group fit (definition B)

| seed | T_exp | exp A->B before | exp B after | T_ver | ver A->B before | ver B after | pool A->B before | pool B after | argmax d |
|---|---|---|---|---|---|---|---|---|---|
| 20260918 | 1.999 | 0.085/0.099 | 0.158 | 11.806 | 0.287/0.301 | 0.141 | 0.156/0.174 | 0.133 | 0.000 |
| 1 | 1.810 | 0.070/0.116 | 0.081 | 11.158 | 0.343/0.346 | 0.148 | 0.175/0.207 | 0.098 | 0.000 |
| 7 | 1.143 | 0.110/0.082 | 0.087 | 14.830 | 0.292/0.285 | 0.212 | 0.163/0.158 | 0.139 | 0.000 |
| 42 | 1.595 | 0.079/0.082 | 0.122 | 11.214 | 0.287/0.315 | 0.163 | 0.137/0.181 | 0.116 | 0.000 |
| 1234 | 1.099 | 0.051/0.069 | 0.062 | 12.741 | 0.338/0.352 | 0.146 | 0.170/0.191 | 0.082 | 0.000 |
| **mean** | 1.529 | — / 0.090 | **0.102** | 12.350 | — / 0.320 | **0.162** | — / 0.182 | **0.114** | 0.000 |
| min..max | 1.10..2.00 | | 0.062..0.158 | 11.2..14.8 | | 0.141..0.212 | | 0.082..0.139 | 0.000 |

## Evidence

Assertions against the claim:

- **(a) exp held-out <= 0.10** — FAILS: mean 0.102, 2/5 seeds above (0.158, 0.122),
  and the ECE **rises** from 0.090 to 0.102 on the mean (overfitting; the falsifier's
  third arm trips on seed 20260918, 0.099 -> 0.158).
- **(b) verdict held-out <= 0.10** — FAILS on 5/5 seeds, min 0.141, mean 0.162.
  This is the pre-registered decisive falsifier: "if (b) fails on a majority of
  seeds, the claim is disproved".
- **(c) pooled held-out <= 0.12** — marginal fail: mean 0.114 but 2/5 seeds above
  (0.133, 0.139).
- **(d) argmax unchanged within +/-0.02** — HOLDS EXACTLY: delta = 0.0000 on all
  5 seeds, all subgroups (temperature is monotone in logits, so this is identity).

Verdict: **disproved** (parent-confirmed). Per-group temperature fitting reduces
the verdict subgroup from 0.320 to 0.162, but under the pre-registered
NLL-fit + held-out protocol it never reaches 0.10 on any of the 5 seeds.
Grouping is **not** the whole story. The fitted held-out verdict T ~ 11-15
against experiment T ~ 1.5-2.0 shows the residual is not a held-out
scalar-scale artifact. Parent probe 1 (recorded in `probes:`): an IN-SAMPLE
temperature chosen to minimise ECE directly (T ~ 4.5) does reach verdict ECE
0.0959, so "no single temperature can" is too strong as written; that escape
fits the evaluation labels and does not survive the held-out protocol, so the
claim as stated is still disproved. A class-conditional / ranking fix is the
honest next lever, not a temperature.

Reproduce: `python3 .agi/sessions/iter-TM.57/a00-bdec620b/probe_ece_pool.py`
(CPU only, ~10 s, no network).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) INSTRUCTION: the tier-parent task says "You are handed each kid DIFF ... never its result file", "One negative probe per claim conjunct, run by YOU, recorded as probes: in the kid node", and "a kid that passes its own tests and fails your probe is lean_disproved". (2) MACHINE: I read the kid committed bytes (git show HEAD: .agi/context/local-maxxing/bench/20260918T233624Z.jsonl and .agi/nodes/experiment/a00-bdec620b-6c4cf7.md) plus the executable probe .agi/sessions/iter-TM.57/a00-bdec620b/probe_ece_pool.py, then ran my OWN probes (scratch/parent_probes2.py over the 1107 scrub rows, best-case T sweep): verdict best-case in-sample min ECE 0.0959 at T=4.52; experiment 0.0519 at T=1.049; pooled per-group best 0.0615; argmax invariant under T (0 changes); defA scrub 0.1563, defB scrub 0.1524, defA pre-scrub 0.1960. (3) NEAR MISS: the kid sentence "no single temperature can both flatten and reorder it" satisfies "temperature fails" while losing the mechanism -- a single temperature that minimises ECE IN-SAMPLE does reach 0.0959, so the true failure is the NLL objective plus the held-out protocol (the claim own specification), not the impossibility of any temperature. I corrected that sentence in this version rather than let it ride. (4) DEVIATION: none; I did not re-run the kid suite as evidence.
<!-- THOUGHT:END -->

## Agent Notes
Per-group temperature on held-out: verdict ECE 0.141-0.212 (mean 0.162) on 5/5 seeds, never <=0.10; exp ECE rises 0.090->0.102 (overfit); pooled 0.114 mean, 2/5 >0.12; argmax delta exactly 0. Claim disproved: grouping is not the whole story. 0.152=def B on scrub rows, 0.196=def A on pre-scrub rows — different definitions AND corpora.
