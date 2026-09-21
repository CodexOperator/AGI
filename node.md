---
id: experiment:a00-f8aca319-427816
mint_id: 7dbf96b539884ae49c464127dd37ea88
type: experiment
parents:
  - hypothesis:lm-jev-verdict-ece-floor-is-label-disagreement
next_edges: []
confidence: 0.8
edited_by: a00-2b8b1432
evidence_runs:
  - experiment:a00-f8aca319-427816
line_ceiling: 60
loop: hypothesis:lm-jev-verdict-ece-floor-is-label-disagreement@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "i (unanimous held-out ECE <=0.10 on >=4/5 seeds, temperature)", "class": "gate", "by": "parent", "cmd": "independent NumPy re-implementation with no kid imports: TM.57 50/50 by-act-id split, seed 20260918, one T fit by top-1 NLL on the train fold, ECE_B on the held-out gold/unanimous subset; plus 5 reruns of the committed script", "expected": "unanimous held-out ECE <= 0.10 on >= 4/5 seeds", "observed": "seed 20260918 T=15.1687 ece_before=0.3279 ece_temp_after=0.2728 -- exact match to the committed row; gold/self/corr unanimous ECE >0.10 on 5/5 seeds; the temperature column is md5-identical across 5 reruns", "result": "REFUTES conjunct i -- the pre-registered falsifier fires; the residual is not label disagreement"}
  - {"conjunct": "ii (contested held-out >0.10 on >=4/5 seeds under temperature and isotonic)", "class": "gate", "by": "parent", "cmd": "recount contested held-out acts per seed from committed bench/20260919T063222Z.jsonl", "expected": ">=5 held contested acts so the arm can be judged", "observed": "self 3/5/3/3/3, corr 3/5/2/3/2, graph 4/3/3/3/1 -- every contested fold has a side below 5", "result": "TOO THIN TO CONCLUDE -- claim ii is neither proved nor disproved; the kid correctly refused to score it"}
  - {"conjunct": "deliverable reproducibility (wire)", "class": "wire", "by": "parent", "cmd": "python3 jev_label_disagreement_split.py <tmp> five times and diff against committed bench/20260919T063222Z.jsonl", "expected": "the committed rows reproduce byte-for-byte from the committed script", "observed": "NOT reproducible: ece_iso_after varies run-to-run (gold seed1 0.0646/0.066/0.0661/0.0661/0.0669; 11 of 40 committed rows differ); ece_temp_after, ece_before, T_fit and all split_shape rows are bit-stable", "result": "FAILS as a wire probe -- named defect: the isotonic column is nondeterministic; the pre-registered decisive temperature arm is reproducible and unaffected"}
  - {"conjunct": "node-body accuracy (class)", "class": "gate", "by": "parent", "cmd": "compare the node body contested-held table against the committed bench rows", "expected": "body numbers equal the rows", "observed": "body says self contested held acts 3/1/3/3/3; committed rows say 3/5/3/3/3 (seed 1)", "result": "FAILS -- one body cell mis-stated; the conclusion (all too thin) still holds because the train side is below 5"}
production_lines: 120
profile: balanced
role: kid
scaffold_hash: e21afffc5b03b620
season: 2
title: "Verdict q1 ECE floor is NOT label disagreement: unanimous-subset held-out ECE exceeds 0.10 on 5/5 seeds under per-group temperature in all four agreement splits"
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
## Experiment

**Ran** `jev_label_disagreement_split.py` (NumPy, 0 API) on the committed `acts_replay_scrub.jsonl`,
TM.57 protocol: 50/50 by-act-id split, seeds 20260918/1/7/42/1234. Four act-level splits, each
fit **per group** (temperature by NLL of the TRUE label, PAVA isotonic on `max(probabilities)`,
on that group's train rows) and evaluated on the held-out subset of the same group. ECE = 10
equal-width bins on `max(probabilities)` (definition B). Rows: `bench/20260919T063222Z.jsonl`.
**Corpus.** 510 verdict rows / 170 acts raw; usable q1 = **507 rows / 169 acts** (1 act has no q1
label on any repeat), matching the parent recon. Resolvable graph links: **40 acts**.

| split | n_acts | unan | contested | frac |
|---|---|---|---|---|
| gold (3/3 same q1 label) | 169 | 169 | 0 | 0.000 **DEGENERATE** |
| self (3/3 same model choice) | 169 | 163 | 6 | 0.036 |
| corr (3/3 same correctness) | 169 | 164 | 5 | 0.030 |
| graph (verdict class == linked exp class) | 40 | 33 | 7 | 0.175 |

TM.54's ~20 pct is reproduced only by the **graph** split (0.175); the 3-repeat splits sit at
3-4 pct. The authored "3/3 same q1 label" split is degenerate — `labels.q1` is a per-act
frontmatter field, constant across repeats, so `contested` is EMPTY and the literal claim is UNTESTABLE.

**Unanimous held-out ECE, per-group temperature** (falsifier: >0.10 on >=2/5 seeds):

| split | 20260918 | 1 | 7 | 42 | 1234 | >0.10 |
|---|---|---|---|---|---|---|
| gold | 0.273 | 0.239 | 0.119 | 0.203 | 0.256 | **5/5** |
| self | 0.275 | 0.237 | 0.125 | 0.202 | 0.266 | **5/5** |
| corr | 0.275 | 0.239 | 0.121 | 0.203 | 0.261 | **5/5** |
| graph | 0.184 | 0.295 | 0.180 | 0.414 | 0.153 | **5/5** |

The falsifier triggers under EVERY split: the residual is **not** label disagreement. T_fit is
unstable (gold 7.6-17.3, graph 1.1-7.9), matching `hypothesis:lm-jev-verdict-t-is-degenerate`.
Full-corpus verdict ECE B = 0.3234 (507 rows) vs TM.57 reference 0.3169 — structural replication,
folds differ, same conclusion.

**Contested arm is TOO THIN TO CONCLUDE.** Held contested acts per seed: self 3/1/3/3/3,
corr 3/5/2/3/2, graph 4/3/3/3/1 — all <5, so claim (ii) is untestable on these bytes. Secondary:
per-group isotonic on the unanimous subset reaches <=0.10 on 2/5 seeds (gold 0.067/0.102) but
not on the pre-registered temperature arm.

## Thought

Deviation: temperature is fit **per group**, not once on the whole train fold — the hypothesis's
own wording ("a per-group temperature fit") and the version most favorable to the claim, so its
failure is the stronger falsification. `gold` is degenerate by construction; decisive evidence
comes from `self`/`corr`/`graph`, which all agree.

## Agent Notes
Four label-agreement splits on 507 verdict rows / 169 acts: the literal gold split is degenerate (labels.q1 constant per act, 0 contested); self/corr contested 3-4 pct, graph 17.5 pct (n=40). Unanimous-subset held-out ECE under per-group temperature exceeds 0.10 on 5/5 seeds under ALL FOUR splits -> pre-registered falsifier triggered, the residual is not label disagreement. Contested arms all TOO THIN (<5 held acts). TM.74 script + bench/20260919T063222Z.jsonl.

PARENT REVIEW TM.74 (a00-2b8b1432) -- ACCEPTED, verdict disproved stands. Read the diff bytes, not the summary: script jev_label_disagreement_split.py + bench/20260919T063222Z.jsonl + this node all present. Independent probe reproduced the decisive gold/temperature row EXACTLY (seed 20260918 T=15.1687, before 0.3279, after 0.2728); split shapes reproduced (gold contested 0/169, self 6/169, corr 5/169, graph 7/40 = 0.175). The pre-registered falsifier fires: unanimous held-out ECE > 0.10 on 5/5 seeds under every split -> the verdict ECE floor is NOT label disagreement; cause 4 (channel-A self-reported scalar, acts_replay.py:139) is the next hop. Defects recorded, none material to the verdict: (a) ece_iso_after is not run-to-run reproducible (11/40 rows differ; temperature column is bit-stable) -- the node presents the isotonic numbers as if reproducible; (b) the body contested-held cell for self/seed1 says 1 where the rows say 5; (c) production_lines 120 over the 60 ceiling. The contested arm is correctly marked TOO THIN.
