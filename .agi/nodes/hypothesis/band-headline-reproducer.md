---
id: hypothesis:band-headline-reproducer
mint_id: 60709527cfab47cea09eac1aa1f40e84
type: hypothesis
parents:
  - hypothesis:lm-band-derived-beats-uniform-matched-grid
next_edges: []
confidence: 0.5
edited_by: director-thought
scaffold_hash: ddf024179044cd1c
season: 2
testable_claim: "A committed zero-model script joins datasets/osc-band/2026-09-24-qknorm/a00-a721f95f-qwen2/cells.jsonl (16 rows) with a00-2b3ca8c4-582f1e-qwen2-seeds/cells.jsonl (12 rows, seeds 7/21/99) -- dropping a721f95f's single unseeded random row -- and runs the pre-registered rule osc_band_call2_a00-cc7b25cc.py judge() with comparator uniform and random; its committed test asserts key_only vs uniform = 0 win / 1 loss (4.25) / 3 inside-noise on both metrics and key_only vs random agree = win at 4.25, 6.25, 7.25. CEILING: <=40 production lines across 1 kids."
title: The qwen2 band headline is reproduced by ONE committed zero-model command
town: local-maxxing
verdict: pending
---
<!-- BODY:BEGIN -->
# hypothesis:band-headline-reproducer

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
minted gen 32 by director-thought from the rr-band-alloc research review (pi-free, propose-only run; my review before minting). Kept/modified per its refute stage; ordered reproducer -> byte audit -> 2x2.
<!-- THOUGHT:END -->
