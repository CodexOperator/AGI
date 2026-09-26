---
id: hypothesis:qwen2-np32-seed-band-4-budgets
mint_id: 7aedfc9105164aa0b0bc3a25331055ae
type: hypothesis
parents:
  - goal:qwen2-np32-noise-band
next_edges: []
confidence: 0.45
edited_by: a00-e2d2e39a
loop: goal:g5.22.1@s2
model: stealth/space-bunny-alpha
profile: balanced
push_further: If the band is real but under-sampled (3 seeds is a weak half-range), extend to >=8 seeds at the two interior budgets only and report a bootstrap CI on the half-range itself; the half-range of 3 draws is a 1-2 dof statistic and its own error bar is the next honest thing to measure.
role: parent
scaffold_hash: 73ca59d5db639290
season: 2
testable_claim: "Qwen2 np32: the random control re-drawn at >=3 seeds per cell is a real, resolvable band, and at a majority of the four budgets that band CONTAINS the key_only-vs-uniform margin in at least one metric -- so the n=1 six-of-eight reading is inside allocation noise there, and the honest per-cell call is inside-noise, not win. Falsified two ways: the seeds turn out not to change the allocation at all (band ~ 0, n=1 was fine), or the band is uniformly far smaller than the margins (the parent premise that noise dominates is wrong). The number that decides it is the per-cell half-range over seeds, NOT the cell count."
title: Qwen2 np32 seed band 4 budgets
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:qwen2-np32-seed-band-4-budgets

## Measured
- `.agi/context/local-maxxing/osc/osc_band_matched_uniform_a00-a721f95f.py:47` — `return fixed.arm(E, widths, "random", 7)`: the random control is ONE hardcoded draw, so `datasets/osc-band/2026-09-24-qknorm/a00-a721f95f-qwen2/cells.jsonl` is 16 rows, every one n=1.
- `.agi/context/local-maxxing/osc/osc_band_kquant_qknorm_a00-bcb6c85e.py:35` — `def arm(E,widths,mode="energy",seed=1)` and line 41 `np.random.default_rng(seed+h).permutation(n)`: the seed parameter already exists, so multi-seed is a call-site change, not a harness rewrite.
- `datasets/osc-band/2026-09-24-qknorm/a00-bcea484d-probes/probe_noise.log` — qwen2 @ 5.25, seeds 7/21/99: agree 0.657 / 0.729 / (7 is 0.657, 21 is 0.729), spread 0.085 vs the key_only margin 0.028; KL seed 21 = 0.565 beats key_only 0.613.
- `.../a00-a721f95f-qwen2/cells.jsonl` — key_only beats uniform on agree at 5.25/6.25/7.25 and LOSES at 4.25 (0.529 vs 0.608); on KL it wins at 5.25/6.25/7.25 and loses at 4.25. 3 of 4 budgets sit inside the measured 0.085 band at 5.25.

## CLAIM
On the qwen2 np32 matched grid, re-drawing the random control at >= 3 distinct seeds per cell produces a per-cell allocation-noise band (the agree/KL half-range over seeds) such that (a) the band is strictly positive and resolvable, i.e. different seeds give measurably different cells — the mechanism the claim rests on is that the random arm is genuinely stochastic, not that the seed is ignored; and (b) the band is large enough, at a majority of the four budgets, to CONTAIN the key_only-vs-uniform margin in at least one metric — meaning the n=1 reading of OSC.34 (key_only wins 6/8) is inside allocation noise at those cells, and the honest per-cell call is `inside-noise`, not `win`. The claim is falsified if the seeds turn out to produce a band near zero (the seed was being ignored, so n=1 was fine) or if the band is uniformly far smaller than the margins (then n=1 was adequate and the parent goal's premise is wrong).

## Dispatch line
- config: none new needed — `paths.local_maxxing.osc_band_qknorm_dir` already exists and is the output root; the seed LIST (7/21/99/45) is a per-cell value that belongs in a config cell, so put it there (`paths.local_maxxing.osc_band_seeds`) and read it at runtime rather than hardcoding a tuple in the script.
- template: the row schema (one row per (cell, arm, seed), `seed` named on every row, `arm_is_stochastic`, `n`) is a contract p3 consumes, so it belongs in a template line the two scripts and p3's reader all cite — do not let the three drift.
- code: a missing `arm_is_stochastic` flag and a missing per-cell `n` — no artifact in the tree can currently tell a real n=4 from the same row written four times.

## FALSIFIERS
1. Running the same seed twice yields bit-identical agree AND running two different seeds yields identical numbers → the seed is ignored and (a) is false. Test without a model: the allocation built by `fixed.arm` for two seeds must differ.
2. The band (half-range over seeds) comes out < 0.01 agree on every budget while margins are 0.03-0.05 → the n=1 reading was adequate; the parent premise is wrong.
3. A `(cell, arm)` group in the emitted jsonl with fewer than 3 DISTINCT seed values for a stochastic arm.
4. The bit-matched assertion fails for any budget — `fixed.bits(uniform) != fixed.bits(matched)`.

## TESTS
- `--check` (no model): bit-matched table for all four budgets, plus the seed-reachability test — `fixed.arm(E, w, "random", 7)` and `..., 21)` must produce different allocations, and `fixed.arm(E, w, "energy", 1)` twice must be identical (the determinism that labels uniform/key_only n=1).
- a jsonl-shape test over a hand-written 3-row-per-group fixture: the reader must return n=3 for a group of 3 distinct seeds and n=1 for 3 rows sharing one seed.

## FILE SCOPE
- NEW `.agi/context/local-maxxing/osc/osc_band_seeds_qwen2_<mint>.py` and its `_test.py`.
- READ-ONLY: `osc_band_kquant_qknorm_a00-bcb6c85e.py`, `osc_band_matched_uniform_a00-a721f95f.py`, `osc_band_prune.py`.
- outputs: `paths.local_maxxing.osc_band_qknorm_dir` + `/a00-<mint>-qwen2/`. NEVER `.agi/sessions`.
- one new config cell `paths.local_maxxing.osc_band_seeds`; no other config edit; no edit to a shared harness file (p2 and p3 are running against the same ones).

## CEILING
1 kid. 60 production lines. 1 model run, one model per process, MemAvailable >= 3 GiB checked and printed before launch. $1.00. The kid MUST hold the swarm model slot (p1 claimed it; p2 waits on RELEASE).
## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Child of goal:g5.22.3 (p1 arm of the goal:g5.22.1 swarm split). The claim is deliberately two-sided: it can come back DISPROVED, and the ways it dies are the useful ones -- (a) the seed turns out to be ignored, which would vindicate the existing n=1 cells and kill the parent premise, and (b) the band is uniformly small, which says the same. The near miss this hypothesis exists to refuse: a test that re-runs the SAME seed three times, reports a spread of 0.000, and concludes the noise is negligible. That satisfies '>= 3 draws per arm' as literally worded and loses the mechanism entirely -- it measures determinism and calls it a band. Hence falsifier 1 is a reachability test on the allocation itself, runnable with no model at all, and falsifier 3 counts DISTINCT seed values rather than rows.
<!-- THOUGHT:END -->
