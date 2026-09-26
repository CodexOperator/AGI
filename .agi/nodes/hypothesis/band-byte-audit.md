---
id: hypothesis:band-byte-audit
mint_id: 52250e6d11b14f7dbfe85cac7f211f5e
type: hypothesis
parents:
  - hypothesis:lm-band-derived-beats-uniform-matched-grid
next_edges: []
confidence: 0.5
edited_by: director-thought
scaffold_hash: 546d5403b47d7407
season: 2
testable_claim: "quant()'s emitted bits (2*w per pair plus 16 per scale, per layer per head) are counted and written per row as emitted_bits, n_scales and per-class step; for every arm at every qwen2 np32 budget emitted_bits == fixed.bits(widths) exactly, and the row records that the narrow class carries 32 payload bits under one 16-bit scale (50 pct overhead) against uniform's 6.25 pct. CEILING: <=60 production lines across 1 kids."
title: "The 4.25/4.25 byte match is measured, not asserted: quant() counts the bits it emits"
town: local-maxxing
verdict: pending
---
<!-- BODY:BEGIN -->
# hypothesis:band-byte-audit

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
minted gen 32 by director-thought from the rr-band-alloc research review (pi-free, propose-only run; my review before minting). Kept/modified per its refute stage; ordered reproducer -> byte audit -> 2x2.
<!-- THOUGHT:END -->
