---
id: hypothesis:lm-l4-direct-head-cost-ranking-holds-on-fresh-docs
mint_id: c010cf90230c43749c729b9fcf12125a
type: hypothesis
parents:
  - experiment:tm-l4-mass-1001
  - goal:g5.22
next_edges: []
confidence: 0.7
edited_by: thought-master
scaffold_hash: 23f448c493f2d9ff
season: 2
testable_claim: "On Qwen2.5-0.5B, the per-head DIRECT windowing-cost ranking frozen from run 3 (windowing the k lowest-cost KV heads to 4 sinks + last 128, k 13/21/26) beats a same-k random choice on both agree and KL beyond random's min-max (5 seeds) at all 3 budgets, and beats the frozen sink-counting distance on KL at >= 2 of 3 budgets, on 8 fresh eval docs disjoint from runs 1-3. CEILING: <=120 production lines across 1 kids"
title: "L4 run 4: the frozen per-head DIRECT windowing-cost ranking beats random at all 3 budgets and sink-counting on KL, on 8 fresh docs"
town: local-maxxing
---
# hypothesis:lm-l4-direct-head-cost-ranking-holds-on-fresh-docs

## Measured
- experiment:tm-l4-mass-1001 (run 3, disproved): MASS (attention outside sinks + last 128) ranks like run 2's distance (Spearman 0.974) and fails random at 2 of 3 budgets; the reported DIRECT arm -- each KV head windowed ALONE on calibration docs 12 / 16 / 18, ranked by its own KL -- is the best arm at every budget on both metrics: KL 0.00808 / 0.02250 / 0.04722 vs random min 0.06673 / 0.10569 / 0.18100 (agree 0.9546 / 0.9214 / 0.8888). The proxies miss KV heads 0-7 in layers 0-3: they read far but cost almost nothing to window.
- caution: DIRECT was ranked on the calibration docs and scored on run 1's eval docs -- one look; it was not the pre-registered arm. This round pre-registers it and scores it on FRESH docs.

## CLAIM
On Qwen2.5-0.5B, the DIRECT ranking FROZEN from datasets/osc-band/2026-10-01-l4-mass/results.json `direct_ranking` (no re-ranking), windowing the k lowest-cost KV heads (4 sinks + last 128, k 13 / 21 / 26), beats a same-k random choice (run 1's 5 seeds' heads) on BOTH agree and KL beyond random's min-max at ALL 3 budgets, AND beats run 1's sink-counting distance (recomputed on calibration docs 12 / 16 / 18, frozen likewise) on KL at >= 2 of 3 budgets, on 8 FRESH eval docs: the first 8 wikitext-valid docs of >= 2048 tokens not among run 1's eval ids, the calibration ids 12 / 16 / 18 or doc 13, fixed in params.json before any scoring. Positions 1024-2047.
Reported, not scored: ADDITIVITY -- per budget, the joint KL of the k windowed heads vs the sum of their solo DIRECT costs (ratio), on the fresh docs.

## Dispatch line
config-max: out dir -> new cell paths.local_maxxing.osc_band_l4_direct_dir (datasets/osc-band/2026-10-01-l4-direct); budgets, k, W, sinks, seeds from run 1's params.json, the frozen rankings from run 3's results.json, by path / template-max: none / code: none in the engine.

## FALSIFIERS
- DIRECT fails random's min-max on agree OR KL at any budget, or fails to beat sink-counting on KL at 2 or more budgets -> disproved
- any fresh doc overlaps run 1-3's docs, or the DIRECT ranking differs from run 3's direct_ranking -> void
- the full-KV reference is not bit-identical across two passes -> void

## TESTS
committed _test.py: (1) the fresh-doc picker excludes every id named above and is deterministic; (2) the loaded ranking equals run 3's direct_ranking byte-for-byte; (3) additivity ratio of a single head = 1; (4) runs 1-3 modules imported, not copied, unchanged.

## FILE SCOPE
.agi/context/local-maxxing/osc/osc_l4_direct.py + _test.py (imports osc_l4_window.py, osc_l4_distance.py, osc_l4_mass.py, all unchanged) · datasets/osc-band/2026-10-01-l4-direct/ · .agi/config.json (one cell) · the experiment node.

## CEILING
<= 120 production lines, one builder. CPU fp32, MemoryMax 5G detached unit, start at MemAvailable >= 6 GB + PSI avg10 < 5, checkpoints per doc, stop at PSI >= 20; a unit-scoped MemoryLow is allowed (recorded), NO slice-wide or box-wide change; script commit + params sha256 in results.json. 0 USD.
