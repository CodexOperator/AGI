---
id: hypothesis:lm-jev-verdict-t-is-degenerate
mint_id: 8224f9b783a645588a59716276995533
type: hypothesis
parents:
  - idea:lm-why-verdict-ece-ignores-temperature
next_edges: []
edited_by: brainstorm
loop: mvp:lm-research-review-workflow@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: fd23badb6a529fc0
season: 2
testable_claim: "Sweeping T over a wide grid (0.05-50) on the committed verdict rows shows the NLL curve has no strict interior minimum: it is flat within noise beyond T~4 and the argmin sits at or near the grid edge on >= 4/5 seeds; the held-out ECE-vs-T curve is likewise flat, so the reported 0.141-0.212 is insensitive to the fit and is not evidence about scalar shape."
thought_session: iter-TM.60
title: "WHY hop 6c: the fitted verdict T~11-15 is a degenerate boundary fit — the NLL-vs-T curve is flat past T~4, so the 'fit' is unidentified and the held-out verdict ECE verdict is a fit-stability artifact, not a shape statement"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-verdict-t-is-degenerate

## Claim

The fitted verdict temperatures (T ~ 11.2-14.8) are ~6-8x the experiment
subgroup's (T ~ 1.1-2.0) and ~2.5-3x the in-sample ECE-minimising T=4.52
(parent probe 1). A T that far out with that much held-out failure is the
signature of a **flat, unidentified NLL objective**: past T~4 the verdict NLL
surface is nearly constant, so the argmin is noise-driven and sits at/near the
grid edge. If so, the reported held-out ECE 0.141-0.212 is not a property of
"the best scalar" — it is a property of an arbitrary point on a plateau.
**Claim:** a wide T sweep (0.05-50) shows no strict interior minimum on >= 4/5
seeds; the held-out ECE-vs-T curve is flat beyond T~4.

## Falsifier

The NLL curve has a strict interior minimum with measurable curvature (a
clear unique argmin well inside the grid) on >= 4/5 seeds. Then T is identified
and the failure is a real shape statement, not a fit artifact.

## Cost

0 API calls, 0 GPU, pure NumPy, < 2 min.

## Experiment that tests it

Sweep T over 0.05-50 (e.g. 200 log-spaced points) on the committed verdict
rows; for each seed report the NLL(T) curve, its argmin, boundary distance, and
local curvature (second difference at argmin); overlay held-out ECE(T). Rows
to `bench/<utc>.jsonl`.
