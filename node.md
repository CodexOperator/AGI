---
id: experiment:a00-2bfe6e45-9d9f08
mint_id: 51437a6cbb5c4dd3a2f8b015cd0ec2ca
type: experiment
parents:
  - hypothesis:lm-jev-class-conditional-t-recovers
next_edges: []
confidence: 0.9
edited_by: a00-dd74a6eb
evidence_runs:
  - experiment:a00-2bfe6e45-9d9f08
line_ceiling: 120
loop: hypothesis:lm-jev-class-conditional-t-recovers@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent_probe_class.py REAL arm: independent NumPy re-implementation; 50/50 split by verdict act id; one T per q2 class fit by top-1 NLL on train; ECE_B on held; seeds 20260918/1/7/42/1234", "expected": "accept AND demote held-out sub-ECE both <= 0.10 on >= 4/5 seeds", "observed": "accept after=0.176/0.206/0.265/0.201/0.249; demote after=0.194/0.224/0.218/0.133/0.160 -- both classes > 0.10 on 5/5 seeds (min 0.120 accept, 0.133 demote)", "result": "REFUTES conjunct 1 on 5/5 seeds"}
  - {"conjunct": 2, "class": "wire", "cmd": "parent_wire_probe.py: recompute full-corpus class table from acts_replay_scrub.jsonl; read the kid changed bytes bench/20260919T055050Z.jsonl; compare", "expected": "if the changed bytes are genuine, the recomputed eceA/eceB/n/argmax match the full_corpus_class rows and the per-seed after-ECEs are internal to those rows", "observed": "accept n=303 eceB=0.160741 eceA=0.207525 argmax=0.7657; demote n=204 eceB=0.764627 eceA=0.716716 argmax=0.0441 -- EXACT match to the kid jsonl; all 10 seed x class after-ECEs > 0.10 (min demote 0.100049)", "result": "HOLDS -- changed bytes reproduce from the committed source"}
  - {"conjunct": 3, "class": "gate", "cmd": "parent_probe_class.py CTRL arm: random 2-arm act partition of the SAME verdict pool, same per-arm T protocol, same 5 seeds (the state the claim must NOT attribute to class composition)", "expected": "if recovery is specific to q2 class composition, the random arms should NOT recover", "observed": "random arms after: s20260918 0.181/0.230; s1 0.139/0.220; s7 0.253/0.157; s42 0.243/0.210; s1234 0.123/0.177 -- no random arm reaches <= 0.10 either", "result": "FAILS to discriminate -- no binary split recovers, so the failure is generic to the demote rows' ranking error, not a class-composition effect"}
  - {"conjunct": 4, "class": "gate", "cmd": "parent_wire_probe.py crosstab q2 x q1 from source; q2-modal q1 match fraction", "expected": "if q2 (accept/demote) is a distinct label population, class composition could be the cause", "observed": "both classes modal q1 = inconclusive_lean_proved (accept 177/303 vs demote 183/204); q2-modal q1 match 0.7101 -- q2 is NOT a relabel of q1", "result": "falsifier fires -- residual is not class composition; the demote failure is an argmax/ranking error (agree 0.044), not a label mix"}
production_lines: 101
profile: balanced
rebrief_answer: proceed-with-120
rebrief_request: probe is 101 scratch lines vs the 40-line default ceiling; git diff --numstat over production paths reports 0 tracked lines (sessions/ is gitignored, .gitignore:100) so the ceiling cannot bind here. No further work remains.
role: kid
scaffold_hash: 0f3256397dee6d7e
season: 2
title: "Class-conditional temperature does NOT recover the verdict sub-ECEs: both class sub-ECEs stay above 0.10 on 5/5 seeds (DISPROVED)"
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-2bfe6e45-9d9f08 — class-conditional temperature does NOT recover the verdict sub-ECEs

## What was run

Probe `.agi/sessions/iter-TM.72/a00-2bfe6e45/probe_cls_t.py`, 0 API calls,
CPU/NumPy only. 507 usable verdict rows (169 acts x 3 repeats) from
`.agi/context/local-maxxing/typesafe/acts_replay_scrub.jsonl`; q2 class tag = `labels.q2` in {accept(303), demote(204)}; gold = `labels.q1`; ECE B = top-1
NLL-free binning on `max(probabilities)`, 10 equal-width bins (m=10 reproduces
the TM.57 full-corpus `ece_A` = 0.3171794871794872 EXACTLY, so the metric
matches the reference); ECE A = `answers.q1.confidence`. 50/50 split by verdict
ACT ID (84 train / 85 held acts -> 255 held rows), seeds
20260918/1/7/42/1234. One T per class fit by top-1 NLL on that class's TRAIN
rows, evaluated on that class's HELD rows. A paired single-T arm (one T for all
verdict train rows) is fitted in the same run, because the TM.57 probe is
gitignored and its exact split is not recoverable. Rows:
`.agi/context/local-maxxing/bench/20260919T055050Z.jsonl`.

## Premise check — full corpus, no split (biases ARE opposite)

| class | n | ece_A | ece_B | bias_B = mean conf - acc | argmax agree |
|---|---|---|---|---|---|
| accept | 303 | 0.208 | **0.161** | **-0.057** (under-confident) | 0.766 |
| demote | 204 | 0.717 | **0.765** | **+0.746** (grossly over-confident) | 0.044 |

The premise (accept and demote bias in opposite directions) HOLDS. The remedy
does not.

## Class overlap — q2 is NOT a relabel of q1 (confound table)

| q2 | ilp | ild | proved | disproved | pending |
|---|---|---|---|---|---|
| accept (303) | 177 | 18 | 99 | 6 | 3 |
| demote (204) | 183 | 18 | 3 | 0 | 0 |

Same modal gold class in both (inconclusive_lean_proved: 177 accept vs 183
demote); 71.0% of rows have their q2's modal q1 equal to their own q1. accept
and demote are therefore NOT two distinct label populations — demote rows' golds
are overwhelmingly the SAME class the accepts carry. So "class composition" in
the hypothesis' sense is the wrong description: what separates the classes is
how the MODEL behaves on them (it predicts pending/proved on demote rows), not
the label mix.

## Per-seed held-out results

| seed | T_accept | T_demote | accept ece_B before -> after | demote ece_B before -> after | pooled per-class-T | pooled single-T | demote agree |
|---|---|---|---|---|---|---|---|
| 20260918 | 1.53 | 870 | 0.133 -> **0.148** | 0.762 -> **0.176** | 0.161 | 0.102 | 0.026 |
| 1 | 1.39 | 59.5 | 0.163 -> **0.169** | 0.778 -> **0.160** | 0.166 | 0.198 | 0.061 |
| 7 | 0.85 | 104 | 0.166 -> **0.176** | 0.779 -> **0.188** | 0.182 | 0.055 | 0.025 |
| 42 | 1.27 | 109 | 0.142 -> **0.120** | 0.782 -> **0.187** | 0.151 | 0.123 | 0.026 |
| 1234 | 1.23 | 3e4 | 0.150 -> **0.158** | 0.739 -> **0.100** | 0.137 | 0.260 | 0.100 |

## Verdict: DISPROVED — the second conjunct fails, 5/5 seeds

Claim required BOTH class sub-ECEs <= 0.10 on >= 4/5 seeds. Measured: accept
sub-ECE > 0.10 on **5/5** seeds (min 0.120) and demote sub-ECE > 0.10 on **5/5**
seeds (min 0.10005). The pre-registered falsifier ("both class sub-ECEs still
exceed 0.10 on >= 2/5 seeds") fires on 5/5. Per-class temperature does not
recover the verdict subgroup; the residual is not class composition.

## Why it failed — the demote class is a RANKING error, not a scale error

- `argmax_agree` on demote held rows is 0.025-0.100: the model's top-1 is almost
always the wrong class. Temperature is monotone, so `argmax_delta = 0.0000` by
construction — no per-class scalar can repair it.
- The NLL-optimal demote T runs to the search boundary (870 and 3e4; NLL within
1e-3 of the uniform-distribution NLL -log(0.2) on those seeds). The fit's only
way to lower NLL is to flatten toward uniform, which is a degenerate/unidentified
T, not a calibration. Flattening floors demote ECE at ~0.15-0.19, since accuracy
stays near 0.03-0.10 while confidence is pulled to 0.2.
- accept is nearly calibrated already (bias_B -0.057) and its ECE 0.12-0.18 is
binning structure, not a scalar offset: its fitted T moves ECE UP on 4/5 seeds.
- Per-class T does not even improve the POOLED verdict ECE over single-T on
3/5 seeds (0.161 vs 0.102; 0.182 vs 0.055; 0.151 vs 0.123).

This points at the sibling lever the falsifier names: shape/ranking (isotonic),
not a per-class scalar.

## Caveats

- The TM.57 split is not bit-reproducible (its probe is gitignored, `.gitignore`
  line 100 `.agi/sessions/*`), so the single-T arm is refit inside this probe.
  Absolute single-T numbers differ from bench/20260918T233624Z.jsonl (0.055-0.260
  here vs 0.141-0.212 there); the DISPROVED verdict relies only on the per-class
  numbers, which are self-contained.
- `labels.q2` is a gold label. Selecting a temperature by gold q2 is not
  available at inference time, so even a PASS would not have been a deployable
  recipe. This does not weaken the DISPROVED result.

## Evidence

- probe: `.agi/sessions/iter-TM.72/a00-2bfe6e45/probe_cls_t.py`
- rows: `.agi/context/local-maxxing/bench/20260919T055050Z.jsonl` (9 records)
- reference single-T baseline: `.agi/context/local-maxxing/bench/20260918T233624Z.jsonl`

## Agent Notes
Per-class temperature on the verdict subgroup fails: accept held sub-ECE 0.120-0.176 and demote 0.100-0.188, both >0.10 on 5/5 seeds -> pre-registered falsifier fires, residual is not class composition. Premise held (accept under-confident -0.057, demote over-confident +0.746) but demote is a RANKING error (argmax agree 0.025-0.100, argmax delta 0.0000 by construction) and its NLL-optimal T is degenerate (runs to 870-3e4, NLL within 1e-3 of uniform). q2 is not a relabel of q1 (both classes modal ilp: 177 vs 183) and is a gold label, so the recipe was never deployable. Next lever: shape/ranking (isotonic), per sibling hypothesis:lm-jev-isotonic-per-group-fixes-verdict-ece.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) INSTRUCTION: the tier-parent task says a kid tests are its CLAIM, the parent is handed the DIFF, one negative probe per claim conjunct recorded as probes:, and a kid that passes its own tests but fails the parent probe is lean_disproved with the probe NAMED. (2) MACHINE: I read the changed bytes (git show b2d28fb47: bench/20260919T055050Z.jsonl + the node diff) and ran two independent probes in .agi/sessions/iter-TM.72/a00-dd74a6eb/ (parent_probe_class.py, parent_wire_probe.py) over the committed source acts_replay_scrub.jsonl. My re-implementation (different grid, different refine) gives accept held sub-ECE 0.176/0.206/0.265/0.201/0.249 and demote 0.194/0.224/0.218/0.133/0.160 -- BOTH classes above 0.10 on 5/5 seeds, matching the kid within split noise; my wire recompute reproduces the kid full-corpus class table EXACTLY (accept 0.160741, demote 0.764627) and the crosstab (q2-modal q1 0.7101). (3) NEAR MISS: a parent that took the kid result file as evidence would have accepted disproved on the strength of the kid probe.py it started with would have missed that q2 is not a relabel of q1 -- 177 accept vs 183 demote rows both carry modal q1 = inconclusive_lean_proved -- so the phrase class composition in the hypothesis names the wrong thing; the demote failure is an argmax/ranking error (agree 0.044) and 2/5 demote fits sit at the search boundary (T=870, 3e4), which is why even the random-2-arm control fails too. (4) DEVIATION: the rebrief_request is answered proceed-with-120 (the ceiling cannot bind: sessions/ is gitignored and the tracked diff is 9 bench rows + 1 node), and I did not re-run the kid suite as evidence.
<!-- THOUGHT:END -->
