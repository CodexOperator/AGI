---
id: idea:lm-token-state-feedback-merge
mint_id: 61b24ef5923c4c0194917b3f73e71094
type: idea
parents:
  - goal:g5.28
next_edges: []
edited_by: thought-master
scaffold_hash: 590396603c052ca1
season: 2
tags:
  - local-maxxing
  - treasury
title: "One d-vector of cross-token state via a 3d² gated merge: +3% weights, one measured win"
town: local-maxxing
---
# idea:lm-token-state-feedback-merge

## Source
doc:recurrent-looped-transformer — "Recurrent Looped Transformer" (https://www.alphaxiv.org/abs/2609.recurrent-looped-transformer); digest `.agi/context/local-maxxing/papers/recurrent-looped-transformer.md`; critic grounded=4/5 — Every quoted number traces to the README/PDF bytes; the errors are the reader's inferences — the merge costs +3.1% bytes/token not ~0, merge-only 8+0 wins exactly one README cell (mod-5 flat seed 42) and loses two, the proposed no-feedback 8+0 control is just T8, and no code/generator/wall-clock exists in the source.

## Lever
A 3d² gated merge (u_t = e_t + α g ⊙ W_s RMSNorm(s_{t-1}), α = 0.1, PDF eqs 2.9–2.11) carries one d-vector across tokens for +0.79M params (+3.1% bytes/token on a 25.31M model) and no extra attention blocks; the README's sole supporting cell is RLT 8+0 90.89% vs Transformer 8 20.57% on mod-5 flat, seed 42, 2,000 steps, while the same config ties T8 on parity@500 and addition and loses on mod-5 brackets and S5 swaps.

## What it buys the town
If that one cell replicates across seeds, a per-sequence recurrent state on a sub-30M encoder-only model for +3% weight bytes/token, plus a concrete d-vector state variable the flip/SNN and Kuramoto threads can couple to.

## First falsifier
Re-implement T8 and RLT 8+0 (no code is released) at width 512, 8 layers, batch 512 on a mod-5 flat generator built to the README's description, seeds 42–44 to 2,000 steps; if 8+0's three-seed mean does not beat T8's by ≥20 points, or T8 also climbs past 80% by step 2,000, the merge is not the lever.

## Cheapest test on our iron
On local-town (gpu-8g, torch venv), a 100-step pilot of one ~26M-param 8+0 run at batch 512, seq ≤128 to measure step time, then six 2,000-step runs (T8 × 3 seeds, 8+0 × 3 seeds) at ≈2×10^16 FLOPs each by 6ND arithmetic, $0.

## Numbers (quoted in the digest)
- per-token blocks = L_E + L_D = 96 for 48+48 (PDF §1, Fig. 2)
- state-path depth after t tokens = t·L_D = 48t (PDF §3.3, Fig. 2)
- merge params = W_g d×2d + W_s d×d = 3d^2 → 786,432 at d=512 (PDF eqs 2.10-2.11; arithmetic)
- carried state = one d-vector, "the O(d) term is the current recurrent output" (PDF eq 3.3)
- SWA window W=8 → ≤7 retained positions per decoder layer (README setup; PDF §2.1)
- feedback scale alpha = 0.1; TBPTT 128; G=1 memory group (README)
- width 512, FFN 1,365, 4 heads, global batch 512, 2,000 planned steps (README)
- params: RLT 26.10-28.73M; Transformer 8 25.31M (README)
- runs: 48 total, 21 reached 2,000 steps, 27 unfinished (README)
- parity @500: RLT 6+2 99.44 ± 0.98; 4+4 83.29 ± 28.94; 5+3 83.51 ± 28.00; 7+1 82.77 ± 29.84; 8+0 48.70 ± 2.60; T8 48.48 ± 0.53 (README table)
- parity: T8 reaches 94.84 ± 3.43% at step 2,000; all RLT 6+2 seeds 100% by step 600 (README)
- parity instability: RLT 5+3 seed 42 100% @500 → 48.05% @600 → recovers @700 (README)

## Provenance
Ingestion 2026-09-16 on the owner's GO ("idea is exactly the node type meant for deeper research"): reader → adversarial critic (corrected seed) → this node. Hypotheses hang from here.
What is the concept? `scale:` big (new chain) or small (extension)?
