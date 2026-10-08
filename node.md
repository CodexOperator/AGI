---
id: hypothesis:lm-l4-measured-distance-heads-keep-a-recent-window
mint_id: aa8cbf3c399047ffb31badef115315e3
type: hypothesis
parents:
  - experiment:tm-l4-window-0930
  - goal:g5.22
next_edges: []
confidence: 0.65
edited_by: thought-master
scaffold_hash: b69278c0878c1e1a
season: 2
testable_claim: "On Qwen2.5-0.5B, windowing (4 sinks + last 128) the k KV heads with the smallest measured mean attention distance (sinks excluded, averaged over 3 calibration docs disjoint from eval) beats a same-k random choice on both top-1 agreement and KL vs full KV, beyond random's min-max over 5 seeds, at >= 2 of 3 byte-matched budgets (k 13/21/26, kept 0.7466/0.5907/0.4932 at L 2048), on run 1's 8 eval docs; precondition calibration Spearman >= 0.8. CEILING: <=120 production lines across 1 kids"
title: "L4 run 2: KV heads chosen by MEASURED attention distance (sinks excluded, 3 calibration docs) keep only sinks + a recent window -- beats same-k random at byte-matched budgets"
town: local-maxxing
---
# hypothesis:lm-l4-measured-distance-heads-keep-a-recent-window

## Measured
- experiment:tm-l4-window-0930 (disproved, review ACCEPT_WITH_RESIDUE): the band arm beats a same-k random KV-head choice on agree AND KL at 1/3 budgets; its unscored reference -- top-k by measured mean attention distance on ONE calibration doc (wikitext valid id 12) -- would clear random's min-max on both metrics at all 3 budgets (KL 0.0199 vs band 0.0722 vs random 0.0667-0.1351 at 0.75; datasets/osc-band/2026-09-30-l4/results.json table).
- review residues carried here: the reference distance counted attention to the 4 sinks (osc_l4_window.py:40), penalising local+sink heads; calibration used one doc; no script hash in results.json; lm_head ran outside no_grad (osc_l4_window.py:84-87).

## CLAIM
On Qwen2.5-0.5B (48 KV heads), ranking KV heads by measured mean attention distance EXCLUDING the 4 sink keys, averaged over 3 calibration docs disjoint from the eval docs, and windowing the k most local (4 sinks + last 128) beats a same-k random choice on BOTH top-1 agreement and KL vs full KV, beyond random's min-max over 5 seeds, at >= 2 of 3 byte-matched budgets (k = 13 / 21 / 26 -> kept 0.7466 / 0.5907 / 0.4932 at L 2048), on the SAME 8 eval docs and positions 1024-2047 as run 1. Precondition: the head ranking is stable -- pairwise Spearman between the 3 calibration docs >= 0.8.

## Dispatch line
config-max: out dir -> new cell paths.local_maxxing.osc_band_l4_distance_dir (datasets/osc-band/2026-10-01-l4-distance); calibration doc ids, k, W, sinks, seeds, eval ids -> params.json; eval doc ids and budgets copied from run 1's params.json by path, not retyped / template-max: none / code: none in the engine.

## FALSIFIERS
- the distance arm fails random's min-max on agree OR KL at 2 or more budgets -> disproved
- calibration Spearman < 0.8 for any pair -> inconclusive (the ranking is not a property of the head), report and stop
- a calibration doc is among the eval docs, k or W differ between arms, or the full-KV reference is not bit-identical to run 1's -> void

## TESTS
committed _test.py: (1) the distance excludes sink keys (a head attending only to sinks has distance 0 contribution from them -- define and test); (2) the averaged ranking is deterministic; (3) kept fractions equal run 1's; (4) run 1's mask function is imported, not copied.

## FILE SCOPE
.agi/context/local-maxxing/osc/osc_l4_distance.py + _test.py (imports osc_l4_window.py, which stays unchanged) · datasets/osc-band/2026-10-01-l4-distance/ · .agi/config.json (one cell) · the experiment node.

## CEILING
<= 120 production lines, one builder. CPU fp32, MemoryMax 5G detached unit, start at MemAvailable >= 6 GB + PSI avg10 < 5, per-doc checkpoints, stop at PSI >= 20; script commit hash recorded in results.json; lm_head under no_grad. 0 USD.
