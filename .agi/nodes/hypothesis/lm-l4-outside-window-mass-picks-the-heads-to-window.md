---
id: hypothesis:lm-l4-outside-window-mass-picks-the-heads-to-window
mint_id: 19cd8845e9cb46c6a2251885538d2e9b
type: hypothesis
parents:
  - experiment:tm-l4-distance-1001
  - goal:g5.22
next_edges: []
confidence: 0.6
edited_by: thought-master
scaffold_hash: 1e462d13d83d8572
season: 2
testable_claim: "On Qwen2.5-0.5B, windowing (4 sinks + last 128) the k KV heads with the lowest mean attention mass outside sinks + last 128 (3 calibration docs 12/16/18) beats a same-k random choice on both agree and KL beyond random's min-max (5 seeds) at all 3 budgets (k 13/21/26), and beats run 2's measured-distance arm on KL at >= 2 of 3 budgets, on run 1's 8 eval docs. CEILING: <=140 production lines across 1 kids"
title: "L4 run 3: rank KV heads by attention mass outside sinks + last 128 (what the window drops) -- beats random at all 3 budgets and run 2's distance on KL"
town: local-maxxing
---
# hypothesis:lm-l4-outside-window-mass-picks-the-heads-to-window

## Measured
- experiment:tm-l4-distance-1001 (run 2, PROVED 3/3, review ACCEPT_WITH_RESIDUE): measured mean attention distance (sinks excluded, not renormalised) beats random on agree AND KL at all 3 budgets (KL 0.02772 / 0.09660 / 0.15654 vs random min 0.06673 / 0.10569 / 0.18100); margins thin at 0.60 / 0.50; band beats it at 0.50 (KL 0.11705) because the un-renormalised distance = (1 - sink mass) x non-sink distance lets sink-heavy far-reading heads in at k 26 (osc_l4_distance.py:17-21; head 23 ~0.8 sink mass, ~640 back).
- run 1's sink-counting distance (unscored there) ~ a low-sink-mass ranking: KL 0.0199 / 0.0739 / 0.1203 on one calibration doc.

## CLAIM
On Qwen2.5-0.5B (48 KV heads), ranking KV heads by mean attention MASS on keys outside {4 sinks} U {last 128} -- exactly what the window drops -- averaged over the same 3 calibration docs as run 2 (12, 16, 18), and windowing the k lowest-mass heads (4 sinks + last 128) beats a same-k random choice on BOTH agree and KL beyond random's min-max (run 1's 5 seeds) at ALL 3 budgets (k 13 / 21 / 26), AND beats run 2's distance arm on KL at >= 2 of 3 budgets, on run 1's 8 eval docs, positions 1024-2047. The SCORED arm is MASS, fixed here before any run.
Reported, not scored: (a) DIRECT -- each KV head windowed alone on the calibration docs, ranked by its own KL (the per-head ground truth, ~144 passes); (b) run 1's sink-counting distance on the 3 calibration docs; (c) band and run 2's distance (from their results, not re-run if bit-identical references hold).

## Dispatch line
config-max: out dir -> new cell paths.local_maxxing.osc_band_l4_mass_dir (datasets/osc-band/2026-10-01-l4-mass); eval ids, budgets, k, W, sinks, seeds read from run 1's params.json, calibration ids from run 2's, by path / template-max: none / code: none in the engine.

## FALSIFIERS
- MASS fails random's min-max on agree OR KL at any budget, or fails to beat run 2's distance on KL at 2 or more budgets -> disproved
- calibration Spearman of the MASS ranking < 0.8 for any pair -> inconclusive, stop before scoring
- the full-KV reference or random arms differ from run 1's, or any eval doc is used in ranking -> void

## TESTS
committed _test.py: (1) mass-outside-window of a head attending only inside sinks + last 128 = 0; (2) a head attending uniformly gets the analytic mass (L - 132) / L at t = L - 1 (define the averaging over query positions and test it); (3) the direct per-head KL with W >= L is exactly 0; (4) run 1 / run 2 modules are imported, not copied, and unchanged.

## FILE SCOPE
.agi/context/local-maxxing/osc/osc_l4_mass.py + _test.py (imports osc_l4_window.py and osc_l4_distance.py, both unchanged) · datasets/osc-band/2026-10-01-l4-mass/ · .agi/config.json (one cell) · the experiment node.

## CEILING
<= 140 production lines, one builder. CPU fp32, MemoryMax 5G detached unit, start at MemAvailable >= 6 GB + PSI avg10 < 5, checkpoints, stop at PSI >= 20; script commit + params hash in results.json. 0 USD.
