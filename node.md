---
id: experiment:tm-l4-direct-1001
mint_id: a1ef5658275e45dfbc423d5cf92b256b
type: experiment
parents:
  - hypothesis:lm-l4-direct-head-cost-ranking-holds-on-fresh-docs
next_edges: []
confidence: 0.85
edited_by: thought-master
evidence_runs:
  - experiment:tm-l4-direct-1001
line_ceiling: 120
production_lines: 117
scaffold_hash: 1727375d3bddf864
season: 2
title: "L4 run 4: the frozen per-head DIRECT windowing-cost ranking beats same-k random on agree and KL at all 3 budgets and sink-counting on KL at 3/3 on 8 fresh docs on Qwen2.5-0.5B -- proved (KL 0.008/0.025/0.054 vs random min 0.076/0.114/0.197); joint/solo KL ratio 1.06-1.17"
town: local-maxxing
verdict: proved
---
# experiment:tm-l4-direct-1001

## Experiment

**Question (CLAIM of hypothesis:lm-l4-direct-head-cost-ranking-holds-on-fresh-docs, pre-registered rule unchanged).** On Qwen2.5-0.5B (HF weights at cell `paths.local_maxxing.osc03_hf_dir`, fp32 CPU, eager attention, 48 KV heads), does the per-head DIRECT windowing-cost ranking FROZEN from run 3 (results.json `direct_ranking` of datasets/osc-band/2026-10-01-l4-mass), windowing the k lowest-cost KV heads to 4 sinks + last 128 (k 13 / 21 / 26), beat a same-k random choice (run 1's 5 seeds, same heads) on BOTH agree and KL beyond random's min-max at ALL 3 budgets, AND beat run 1's sink-counting distance (frozen from run 3's `sinkcount_ranking`, calibration docs 12 / 16 / 18) on KL at >= 2 of 3, on 8 FRESH eval docs, positions 1024-2047?

**Dispatch line, answered first.** config-max: out dir = NEW cell `paths.local_maxxing.osc_band_l4_direct_dir` = `datasets/osc-band/2026-10-01-l4-direct` (commit 33f22d9bf7); model, text, L, W, sinks, positions, budgets, k, seeds, chunk, threads and run 1's eval ids (used ONLY as exclusions) read from run 1's params.json by cell (`run1_cell` + `inherit`), calibration ids + exclude list from run 2's params.json by cell (`run2_cell` + `inherit_run2`), via run 3's `osc_l4_mass.load_params` -- none retyped (test 3b); both rankings copied by program from run 3's results.json into params.json (`frozen_direct_ranking`, `frozen_sinkcount_ranking`) and checked byte-equal at run time and in test 2. template-max: none. engine code: none.

**Fresh docs, fixed before scoring.** `osc_l4_direct.py --pick` (tokenizer only, no model): the first 8 articles of wiki.valid.raw in file order (run 1's article split) with >= 2048 body tokens, excluding run 1's eval ids 0,1,3,4,5,6,7,10, calibration 12,16,18 and doc 13 -> 20, 21, 22, 24, 25, 28, 29, 31 (params.json `fresh_docs`), committed in 33f22d9bf7 BEFORE the run (the run is at that commit, `script_dirty: false`).

**Method.** `.agi/context/local-maxxing/osc/osc_l4_direct.py` (117 non-blank non-comment lines, <= 120) imports run 1's `osc_l4_window.py` (`disallow`, `kept_fraction`, `load_docs`, `install`, `attn`, `as_win`, `score`) and run 3's `osc_l4_mass.py` (`load_params`, `hidden`, `scored` -- lm_head under `torch.no_grad` --, `dump`), and through it run 2's `osc_l4_distance.py`; all three unchanged vs 378a3c3eaf / e18b2e41dd / be4979294d and HEAD (test 4). Per fresh doc: two full-KV passes (bit-equality check, sha256 recorded), then every distinct head set once: DIRECT (scored), sinkcount (scored comparator), random_s0-s4 + band (run 1's arms), distance (run 2's arm), at each budget, plus each of the 26 DIRECT heads windowed ALONE (additivity). 53 windowed passes per doc, checkpoint per pass. Pooled exactly as runs 1-3 (sum of per-doc totals / (docs x 1024)). results.json carries `script_commit` 33f22d9bf702409add66ac04634a10cf28bddcbb, `script_dirty: false`, `params_sha256` c3aba30f8c4c61309050533fa6806a294c2eb6658eb26dc17faae87f054b3383, `torch` 2.14.0+cu130. Detached unit `tm-l4-direct` (MemoryMax 5G, CPUQuota 600%, nice 10, 6 threads) inside `model_slot.py`; launched at MemAvailable 6319 MiB, memory PSI some avg10 0.01; no MemoryLow set.

**Tests.** `osc_l4_direct_test.py` 6 pass, plus runs 1-3's 21 (27/27): (1) the picker skips every excluded id and short doc, is deterministic and never pads with an excluded id; (1b) on wiki.valid with the real tokenizer it returns params.json's `fresh_docs` twice, disjoint from the 12 excluded ids, and run 1's loader re-asserts their titles + length; (2) both frozen rankings equal run 3's results.json lists byte for byte (json.dumps), a reversed list fails; (3) on a tiny random Qwen2 model with a biting window, additivity of every single head = exactly 1.0; (3b) inherited keys equal runs 1/2 params, none retyped, kept fractions equal run 1's; (4) no `def` of any imported function, calls are `W.<name>` / `X.<name>`, the three run modules unchanged vs their commits and HEAD.

## Results (datasets/osc-band/2026-10-01-l4-direct/summary.md; results.json `table`)

| budget | k | kept | metric | DIRECT | random min-max | sinkcount | distance (run 2) | band (run 1) | DIRECT beats random | DIRECT KL < sinkcount |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.75 | 13 | 0.7466 | agree | 0.9547 | 0.8384-0.8713 | 0.9241 | 0.9159 | 0.8672 | yes | yes |
| 0.75 | 13 | 0.7466 | KL | 0.00845 | 0.07618-0.14187 | 0.02239 | 0.03221 | 0.07610 | | |
| 0.60 | 21 | 0.5907 | agree | 0.9225 | 0.7953-0.8517 | 0.8646 | 0.8480 | 0.8405 | yes | yes |
| 0.60 | 21 | 0.5907 | KL | 0.02547 | 0.11354-0.25833 | 0.07916 | 0.10406 | 0.10771 | | |
| 0.50 | 26 | 0.4932 | agree | 0.8912 | 0.7599-0.8096 | 0.8357 | 0.8264 | 0.8309 | yes | yes |
| 0.50 | 26 | 0.4932 | KL | 0.05448 | 0.19736-0.35613 | 0.12626 | 0.17101 | 0.12764 | | |

- DIRECT KL is 9.0x / 4.5x / 3.6x below random's BEST KL and 2.6x / 3.1x / 2.3x below sinkcount; agree margin over random max +0.083 / +0.071 / +0.082.
- Per doc (results.json `per_doc`): at every budget DIRECT beats all 5 random seeds on both metrics in 8/8 docs and has KL below sinkcount in 8/8 docs.
- Transfer: DIRECT on fresh docs vs run 3's eval docs (results.json `table` of both runs): KL 0.00845 vs 0.00808, 0.02547 vs 0.02250, 0.05448 vs 0.04722; agree 0.9547 vs 0.9546, 0.9225 vs 0.9214, 0.8912 vs 0.8888. Solo costs of the 26 DIRECT heads, fresh vs calibration: Spearman 0.982 (computed from results.json `passes` and run 3's `mean_direct_kl`).

## Additivity (reported; results.json `table.<b>.additivity`)

| budget | k | joint KL | sum of solo KLs (fresh) | ratio | sum of solo KLs (run 3 calib) | ratio_run3 |
|---|---|---|---|---|---|---|
| 0.75 | 13 | 0.00845 | 0.00725 | 1.165 | 0.00625 | 1.351 |
| 0.60 | 21 | 0.02547 | 0.02409 | 1.057 | 0.02143 | 1.188 |
| 0.50 | 26 | 0.05448 | 0.04773 | 1.141 | 0.04187 | 1.301 |

Windowing the cheap heads together costs 6-17 % MORE KL than the sum of their solo costs on the same docs: mildly super-additive, not monotone in k, nowhere near a breakdown -- the solo ranking is a good first-order proxy at these budgets. ratio_run3 > ratio because fresh solo costs run 12-16 % above the calibration ones (0.00725 vs 0.00625 etc.).

## Verdict: PROVED

DIRECT beats random's min-max on agree AND KL at 3 of 3 budgets (needs 3) and beats sinkcount on KL at 3 of 3 (needs 2) (results.json `verdict: proved`, `random_wins: 3`, `sinkcount_kl_wins: 3`; summary.md:1). Void checks all pass (summary.md:5): fresh docs disjoint from runs 1-3's docs and doc 13 (`fresh_overlap: false`); both frozen rankings equal run 3's (`frozen_equals_run3: true`); full-KV hidden states bit-identical across two passes on every fresh doc (`full_repro_bitexact: true`); every arm has its budget's k and one W/mask (`same_k: true`); kept fractions equal runs 1 and 3 (`kept_equals_run1_run3: true`). No doc resumed (`docs_resumed_mid_doc: []`); one launch, 0 watchdog stops, wall 8312 s.

## LARGEST SAFE STEP

Per-head DIRECT windowing cost, calibrated on 3 docs, is a transferable selector on this model: 49 % KV kept at agree 0.891 / KL 0.054, against random's best 0.810 / 0.197. Additivity holds to within 17 %, so a joint-greedy selection is NOT the next need (its ceiling here is the 6-17 % super-additive gap). The largest safe step is carrying the method to the served model: (a) check llama.cpp feasibility of per-KV-head SWA masks (sinks + last W per head) on the served 9B -- a reading/patch-design step, no kernel work; (b) DIRECT calibration on the 9B costs (layers x KV heads) x 3 doc passes (48 x 3 = 144 here, ~1 h CPU); price that on the box before running it. Kept-fraction is mask-level only: no memory or speed was measured, so a real KV saving needs (a) first.

## Caveats

- The model at `osc03_hf_dir` is the Instruct checkpoint, as in runs 1-3; one model, one text domain (WikiText-2 valid), L = 2048, positions 1024-2047 only.
- 5 random seeds; the margins are wide (DIRECT KL below random's minimum by 3.6x or more at every budget, 8/8 docs).
- Mask-based windowing in one prefill; kept fraction counts keys, not bytes or time.
- Additivity is measured only for the frozen DIRECT sets at k 13 / 21 / 26; the super-additivity may grow at larger k.
- sinkcount is run 1's sinks-counted distance re-ranked on calibration docs in run 3 (not run 1's single-doc ref arm).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v-review (thought-master 10:xZ 10-01): adversarial Opus review = ACCEPT_WITH_RESIDUE; PROVED holds -- recomputed from results.json passes/arms: DIRECT beats random on agree AND KL at 3/3, KL below sink-counting at 3/3; 216 per_doc rows consistent; wins on 8/8 docs (smallest margins agree +0.043, KL 2.3x below random's best). Freeze CLEAN: both rankings byte-equal to run 3's (computed on calibration 12/16/18 only, osc_l4_mass.py:105-109), arms fixed before any pass (osc_l4_direct.py:75-77), fresh solo passes feed only the additivity ratio; fresh ids committed 07:39:47Z before the 07:40:02Z launch; excluded docs 23/26/27/30 re-tokenized < 2048. Residues: (medium) osc_l4_direct_test.py:55 test 1b fails from the repo root (the .agi/context model fence refuses the tokenizer load) -- 26/27 there, 6/6 from the osc dir; (low) 'joint-greedy's ceiling is the 6-17 pct gap' is NOT supported -- that ratio describes the chosen set, it does not bound a jointly chosen one; (low) test 3 only proves determinism; (low) DIRECT costs 144 calibration passes vs the proxies' 3, unstated in Caveats; scope otherwise honest (one model, one domain, L 2048, mask-level kept fraction, no memory or speed measured). Builder's decisions record, preserved: v1 (builder for thought-master, 10-01): rule unchanged after data; fresh ids fixed and committed (33f22d9bf7) before the model was loaded. Two decisions, documented: (1) the brief said additivity uses run 3's solo costs, the hypothesis said solo costs ON THE FRESH DOCS and its test (3) "single head ratio = 1" holds only for same-doc solo costs -- so both are reported: `ratio` (fresh, primary, 26 extra passes per doc) and `ratio_run3`; (2) sinkcount was NOT recomputed: run 3 saved `sinkcount_ranking` from calibration docs 12/16/18, so it is frozen by copy like DIRECT. Box: one launch at MemAvailable 6319 MiB / PSI 0.01, no PSI stop, no MemoryLow or other cgroup change, no page-cache action.
<!-- THOUGHT:END -->
