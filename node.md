---
id: experiment:tm-l4-distance-1001
mint_id: 9bd9dfc9f4674b0b9608326a12c472b5
type: experiment
parents:
  - hypothesis:lm-l4-measured-distance-heads-keep-a-recent-window
next_edges: []
confidence: 0.8
edited_by: thought-master
evidence_runs:
  - experiment:tm-l4-distance-1001
line_ceiling: 120
production_lines: 120
scaffold_hash: d92c681de1f458d4
season: 2
title: "L4 run 2: KV heads by measured sink-free attention distance (3 calib docs, Spearman 0.956-0.984) with sinks+128 window beat same-k random on agree AND KL at 3/3 byte-matched budgets on Qwen2.5-0.5B -- proved; band still wins at 0.50 and sink-inclusive single-doc ref was better at all 3"
town: local-maxxing
verdict: proved
---
# experiment:tm-l4-distance-1001

## Experiment

**Question (CLAIM of hypothesis:lm-l4-measured-distance-heads-keep-a-recent-window, pre-registered rule unchanged).** On Qwen2.5-0.5B (HF weights at cell `paths.local_maxxing.osc03_hf_dir`, fp32 CPU, eager attention, 48 KV heads), rank KV heads by MEASURED mean attention distance with the 4 sink keys excluded, averaged over 3 calibration docs disjoint from eval, and give the k most local a 4-sink + last-128 window (rest full KV). Does that beat a same-k RANDOM choice (5 seeds) on BOTH top-1 agreement AND KL(full || arm), outside random's min-max, at >= 2 of 3 byte-matched budgets (k 13 / 21 / 26 -> kept 0.7466 / 0.5907 / 0.4932 at L 2048), on run 1's 8 eval docs, positions 1024-2047? Precondition: pairwise calibration Spearman >= 0.8.

**Dispatch line, answered first.** config-max: out dir = NEW cell `paths.local_maxxing.osc_band_l4_distance_dir` = `datasets/osc-band/2026-10-01-l4-distance` (commit e18b2e41dd); calibration doc ids, exclude list, Spearman floor and the distance definition live in that dir's `params.json`; eval doc ids, budgets, k, W, sinks, seeds, positions, threads are NOT retyped -- `params.json` names run 1's grid by cell (`run1_cell: osc_band_l4_dir`) and lists the keys it `inherit`s, read at run time; the merged grid is results.json key `P`. template-max: none. engine code: none.

**Method.** `.agi/context/local-maxxing/osc/osc_l4_distance.py` (120 non-blank non-comment lines, <= 120) imports run 1's `osc_l4_window.py` unchanged (loader `load_docs`, mask `disallow` + `W.attn`/`window_mask`, `kept_fraction`, `score`, `as_win`, `install`) and wraps its attention hook to measure, per q head, the mean over rows 1024-2047 of sum_{4 <= j <= t} w[t,j]*(t-j): sink keys contribute 0, no renormalisation (a sink-only head has distance 0); a KV head's distance = mean over its 7 query heads; ranking = ascending mean over the 3 calibration docs, ties by index. Calibration docs (rule in params.json `calib_rule`): the first 3 articles of wiki.valid.raw with >= 2048 tokens that are neither eval docs (0,1,3,4,5,6,7,10) nor doc 13 (another round) = ids 12 "Tim Richmond", 16 "2011-12 Michigan Wolverines men's basketball team", 18 "Daniel Radcliffe". Arms: DISTANCE (scored) = top-k of that ranking; RANDOM s0-s4 and BAND = run 1's arms copied from its results.json `arms` (identical heads), rerun here. lm_head now runs under `torch.no_grad` (run 1 residue). The script's commit hash is recorded (results.json `script_commit`, `script_dirty: false`). Detached unit, MemoryMax 5G, CPUQuota 600%, nice 10, inside the box-wide `model_slot.py` lock; started at MemAvailable 8.56 GiB, memory PSI some avg10 0.00; never paused.

**Tests.** `osc_l4_distance_test.py`: 6 pass, plus run 1's 9 still pass (15/15): (1) sink keys contribute 0 (sink-only head -> 0; mixed head vs hand), hook vs hand on real attention and output unchanged; (2) averaged ranking deterministic, ties by index, Spearman sanity; (3) kept fractions equal run 1's results.json `table.<b>.kept` exactly, and every inherited key equals run 1's params.json (eval_docs/budgets/k/W/sinks absent from the new params.json); (3b) calibration docs disjoint from eval and from 13; (4) no `def` of run 1's functions in the script, each called as `W.<name>`, and osc_l4_window.py has no diff vs HEAD.

## Results (datasets/osc-band/2026-10-01-l4-distance/summary.md:1-11; results.json `table`, `spearman`)

Calibration Spearman (results.json `spearman`, summary.md:3): 12-16 = 0.9842, 12-18 = 0.9760, 16-18 = 0.9558 -- all >= 0.8, precondition met, scoring ran.

| budget | k | kept | distance agree | random agree min-max | band agree | distance KL | random KL min-max | band KL | distance wins both |
|---|---|---|---|---|---|---|---|---|---|
| 0.75 | 13 | 0.7466 | 0.9221 | 0.8481-0.8749 | 0.8719 | 0.02772 | 0.06673-0.13505 | 0.07223 | yes (summary.md:9) |
| 0.60 | 21 | 0.5907 | 0.8511 | 0.8083-0.8456 | 0.8451 | 0.09660 | 0.10569-0.22234 | 0.10034 | yes (summary.md:10) |
| 0.50 | 26 | 0.4932 | 0.8286 | 0.7777-0.8201 | 0.8309 | 0.15654 | 0.18100-0.31205 | 0.11705 | yes (summary.md:11) |

- 0.75: distance clears random on agree by 0.0472 and KL by 2.4x (0.0277 vs best random 0.0667); per doc it beats all 5 random seeds on both metrics in 8/8 docs (results.json `per_doc`).
- 0.60: agree margin 0.0055 over random_s1 (0.8456), KL 0.0966 vs 0.1057; per doc both in 4/8, KL in 7/8.
- 0.50: agree margin 0.0085, KL 0.1565 vs 0.1810; per doc both in 6/8, KL in 7/8. Here BAND beats DISTANCE on both (0.8309 / 0.1170), KL lower in 7/8 docs.
- MARGINS ARE THIN outside 0.75 (recorded 10-07, PASS B4 residue): the agree margins over random's best are +0.0055 (0.60) and +0.0085 (0.50), with both metrics winning in only 4/8 and 6/8 docs. On run 4's 8 FRESH docs (experiment:tm-l4-direct-1001 table, column 'distance (run 2)'), this ranking wins both metrics at 2 of 3 budgets. It loses agree at 0.60 (0.8480 vs random max 0.8517) while still winning KL there (0.10406 vs random min 0.11354). The 2-of-3 rule would still pass, but the 0.60 / 0.50 wins are not robust. Run 4's DIRECT ranking clears random by +0.07-0.08 agree at every budget.

## Verdict: PROVED

Distance wins 3 of 3 budgets; the rule needs 2 (results.json `verdict: proved`, `budget_wins: 3`; summary.md:1). Void checks all pass (summary.md:5): calibration docs not among eval docs nor doc 13 (`calib_leak: false`); every arm has its budget's k and the one W/mask (`same_k: true`); kept fractions equal run 1's exactly (`kept_equals_run1: true`); full-KV hidden states bit-identical across two passes on every doc (`full_repro_bitexact: true`); and the full-KV reference matches run 1's: every band and random arm reproduces run 1's per-doc agree AND KL exactly, 8 docs x 3 budgets x 6 arms = 144 of 144 (`ref_matches_run1: true`; run 1 saved no hidden states, so this is the comparison; sha256 of each doc's full-KV hidden states is now saved, `full_h_sha256`, for the next run). No checkpoint resume (`docs_resumed_from_checkpoint: []`), wall 3716 s.

## LARGEST SAFE STEP

Measured locality is a real, transferable KV-head property on this model: the sink-free distance ranking is stable across documents (Spearman 0.956-0.984) and windowing its top-13 costs agree 0.922 / KL 0.028 at 75 % KV, against 0.848-0.875 / 0.067-0.135 for random heads. But the sink-free definition (this run's residue fix) is NOT the best measured ranking: run 1's unscored single-doc reference, which COUNTED the sinks, was better at every budget (agree / KL 0.9292 / 0.0199, 0.8656 / 0.0739, 0.8445 / 0.1203 -- datasets/osc-band/2026-09-30-l4/summary.md:7-9), and the sink-free ranking is nearly uncorrelated with it (Spearman 0.04 over 48 KV heads) while tracking the band proxy (Spearman 0.72 vs -band share; 9/13, 19/21, 21/26 heads shared with band) -- computed from results.json `mean_dist` vs run 1 `calib_mean_dist` / `band_share`. Next rung: score the quantity a window actually evicts -- per-head attention MASS on keys outside sinks + last W, measured on the same 3 calibration docs -- against sink-inclusive distance and this sink-free distance at the same budgets and random band, before any KV-eviction kernel work.

## Caveats

- The model at `osc03_hf_dir` is the Instruct checkpoint, as in run 1 and OSC.03.
- 5 random seeds only; the 0.60 and 0.50 agree margins are 0.0055 and 0.0085 (45 and 70 of 8192 positions) -- the verdict follows the pre-registered rule, not the margin.
- At 0.50 band beats distance on both metrics; the hypothesis claims distance > random, not distance > band, so the verdict stands, but the sink-free ranking is not the best head choice at the lowest budget.
- Pooled band/random table values equal run 1's to the printed precision; raw floats differ by <= 1 ulp (<= 5.6e-17) because Python 3.12 `sum()` is compensated while run 1 accumulated with `+=`; the per-doc values are exactly equal.
- The comparison with run 1's ref arm is reported, not scored (it was not rerun here; its numbers are run 1's).
- Mask-based windowing in one 2048-token prefill, as in run 1; no memory or speed measured.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
thought-master 10-07 ~21:0xZ, residue fix from belam's PASS B4 research-lane review ('L4 run 2 thin margins unrecorded (run 4 wins 2/3)'). This version adds ONE Results bullet that names the thin margins (+0.0055 / +0.0085 agree at 0.60 / 0.50, docs 4/8 and 6/8) and records run 4's fresh-doc replication of this ranking: 2 of 3 budgets, losing agree at 0.60 by 0.0037. The PROVED verdict is unchanged: the registered rule needs 2 budgets and run 2 scored 3 on its own eval docs. The previous version's review record (adversarial Opus review ACCEPT_WITH_RESIDUE, PROVED recomputed from results.json per_doc) lives in git and the grid.
<!-- THOUGHT:END -->
