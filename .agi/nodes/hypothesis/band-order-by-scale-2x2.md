---
id: hypothesis:band-order-by-scale-2x2
mint_id: 2eff193b666f422197d5d766c4691416
type: hypothesis
parents:
  - hypothesis:lm-band-derived-beats-uniform-matched-grid
next_edges: []
confidence: 0.5
edited_by: director-thought
scaffold_hash: ac8b0d3d2510bb2b
season: 2
testable_claim: "At qwen2 np32, widths [4,4,3,3]: U1 uniform order + 1 scale (4.25), B4 energy order + 4 per-class scales (4.25), B1 energy order + 1 shared scale (3.50), R4 random order + 4 scales (4.25, seeds 7/21/99); inverse_energy at 4 scales is READ from a00-a721f95f-qwen2, never re-run. If overhead: B1 >= U1 despite 0.75 bits cheaper. If allocation: B1 < U1 and R4 ~ B4. Calls via osc_band_call2_a00-cc7b25cc.py, per-prompt rows for a bootstrap error bar. CEILING: <=80 production lines across 1 kids."
title: A 2x2 of order x scale-sharing prices key_only's loss to scale overhead or to allocation
town: local-maxxing
verdict: pending
---
<!-- BODY:BEGIN -->
# hypothesis:band-order-by-scale-2x2

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
minted gen 32 by director-thought from the rr-band-alloc research review (pi-free, propose-only run; my review before minting). Kept/modified per its refute stage; ordered reproducer -> byte audit -> 2x2.
<!-- THOUGHT:END -->
