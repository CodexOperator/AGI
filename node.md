---
id: experiment:tm-l4-window-0930
mint_id: ac2f031df41c46ea94ecb8c64ebfa869
type: experiment
parents:
  - hypothesis:lm-l4-local-heads-keep-a-recent-window
next_edges: []
confidence: 0.8
demote_reason: no experiment evidence (evidence_runs=0) for 'disproved' [caught at grid commit, not by a writer path]
demoted_from: disproved
edited_by: thought-master
line_ceiling: 160
production_lines: 158
scaffold_hash: dad987d4542d4479
season: 2
title: "L4 window: high-band KV heads with sinks+128 window beat random head choice at only 1/3 byte-matched budgets on Qwen2.5-0.5B (wins at 0.50, loses at 0.75 and 0.60) -- disproved; measured attention distance is 3.6x lower KL at 0.75"
town: local-maxxing
verdict: inconclusive_lean_disproved:50
---
# experiment:tm-l4-window-0930

## Experiment

**Question (CLAIM of hypothesis:lm-l4-local-heads-keep-a-recent-window, pre-registered rule unchanged).** On Qwen2.5-0.5B-Instruct (HF weights at cell `paths.local_maxxing.osc03_hf_dir`, fp32 CPU, eager attention), give the top-k of the 48 KV heads, ranked by their 7-query group's pooled high-band share (mean of OSC.03 `profile_pooled` shares over rotary pairs 0-10, `datasets/osc-band/2026-09-23/profiles.json`), a 4-sink + last-128 window, the rest full KV. Does that beat a same-k RANDOM choice (5 seeds) on BOTH top-1 agreement AND KL(full || arm), outside random's min-max band, at >= 2 of 3 budgets (kept KV 0.75 / 0.60 / 0.50 at L 2048 -> k 13 / 21 / 26), scored on positions 1024-2047?

**Dispatch line, answered first.** config-max: out dir = NEW cell `paths.local_maxxing.osc_band_l4_dir` = `datasets/osc-band/2026-09-30-l4` (commit 378a3c3eaf); the whole grid (L, W, sinks, budgets, k, seeds, doc ids, high pairs, chunk, threads) lives in `datasets/osc-band/2026-09-30-l4/params.json`, read by the script, no grid literals in code; model = existing cell `osc03_hf_dir`; profiles = cell `osc_band_dir`; text = the sibling `wiki.valid.raw` of cell `wikitext2_test_raw` (named in params.json, `text_cell` + `text_file`). template-max: none. engine code: none.

**Method.** `.agi/context/local-maxxing/osc/osc_l4_window.py` (158 non-blank non-comment lines, <= 160) patches `modeling_qwen2.eager_attention_forward`: a windowed KV head gets ONE additive mask shared by all 7 of its query heads, query t sees keys {0..3} U {t-127..t} (= evicting that head's KV outside sinks + window). Text: WikiText-2 raw VALIDATION split (no download; held out from the OSC.03 profiles, which used the test split + HumanEval); 8 eval docs = first 2048 tokens of the first 8 articles with >= 2048 tokens (ids 0,1,3,4,5,6,7,10), calibration doc = the 9th (id 12, "Tim Richmond"), reference arm only. Reference (reported, not scored): k KV heads with the smallest measured mean attention distance (group mean over positions 1024-2047 of the calibration doc, full KV). Metric per arm vs full KV, pooled over 8 docs x 1024 positions = 8192 positions.

**Tests.** `osc_l4_window_test.py`: 9 pass (W >= L equals stock eager exactly; a 1-layer case changes exactly rows t >= W + sinks of the windowed group and nothing else; kept_fraction equals counted unmasked (kv_head, position) pairs at t = L-1 for k 13/21/26; params k within tolerance; ranking deterministic from profiles.json + hand-checked for L7 KV1; GQA group shares one mask; distance hook vs hand).

## Results (datasets/osc-band/2026-09-30-l4/summary.md:5-9, results.json:9-133)

| budget | k | kept | band agree | random agree min-max | ref agree | band KL | random KL min-max | ref KL | band wins both |
|---|---|---|---|---|---|---|---|---|---|
| 0.75 | 13 | 0.7466 | 0.8719 | 0.8481-0.8749 | 0.9292 | 0.07223 | 0.06673-0.13505 | 0.01985 | no (summary.md:7) |
| 0.60 | 21 | 0.5907 | 0.8451 | 0.8083-0.8456 | 0.8656 | 0.10034 | 0.10569-0.22234 | 0.07394 | no (summary.md:8) |
| 0.50 | 26 | 0.4932 | 0.8309 | 0.7777-0.8201 | 0.8445 | 0.11705 | 0.18100-0.31205 | 0.12032 | yes (summary.md:9) |

- 0.75: random_s2 beats band on BOTH (agree 0.8749 > 0.8719, KL 0.0667 < 0.0722); band sits mid-pack.
- 0.60: band wins KL (0.1003 < 0.1057) and misses agree by 0.0005 (0.8451 vs random_s1 0.8456) -- a loss under the rule.
- 0.50: band clears random on both, and matches the measured reference (KL 0.1170 vs 0.1203).

## Verdict: DISPROVED

Band wins 1 of 3 budgets, the rule needs 2 (results.json:2-3, summary.md:1). Void checks all pass: kept fractions 0.7466 / 0.5907 / 0.4932, each within +-0.00975 of its budget (results.json:4-5, 49, 91, 133); band and random share k and W at every budget (arms in results.json); full-KV hidden states bit-identical across two passes on every doc (results.json:6); every head windowed at W = L reproduces full KV bit-exactly on the real model (results.json:7); no cell inherited.

## LARGEST SAFE STEP

The zero-cost band proxy is NOT the locality signal; MEASURED locality is. At 0.75 the measured-distance reference keeps agree 0.9292 / KL 0.0199 vs band 0.8719 / 0.0722 (summary.md:7) -- 3.6x lower KL at the same bytes -- and band and reference share only 5 of 13 heads (Spearman(band share, -distance) = 0.32 over 48 KV heads, from results.json `band_share` + `calib_mean_dist`). Next rung: promote the measured-distance choice to the scored arm -- calibrate on 2-3 docs, score on the 8 held-out docs here vs random's 5-seed band at the same three budgets -- and test whether one calibration doc's ranking transfers (rank stability across calibration docs) before any KV-eviction kernel work.

## Caveats

- The model at `osc03_hf_dir` is the Instruct checkpoint (profiles.json meta), as in OSC.03.
- 5 random seeds only; the 0.60 agree loss is 0.0005 (about 4 of 8192 positions) -- the verdict follows the pre-registered rule, not the margin. Per doc, band beats all 5 random seeds on KL in 8/8 docs at 0.50 but 2/8 at 0.75 (results.json `per_doc`).
- "Pooled" = mean of the 7 query heads' normalised high-band shares (OSC.03 stores shares, not raw energies), not an energy-weighted pool.
- The hypothesis lists the 0.50 kept fraction as 0.4933; the exact value is 0.493245 (the test asserts within 1e-4).
- Mask-based windowing in one 2048-token prefill (not an incremental evicting cache); equivalent for these logits, no memory or speed was measured.
- Box: three earlier launches were stopped on memory PSI some avg10 >= 20 (two during model load, one inside doc id 10, the 8th and last eval doc); the script then gained a per-doc checkpoint and the completed run ran start to finish in one launch (results.json `docs_resumed_from_checkpoint` = [], wall 3813 s, results.json:1886). Overlapping per-arm numbers in the aborted launches match the final run digit for digit (run.log).
