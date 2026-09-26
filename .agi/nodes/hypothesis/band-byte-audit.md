---
id: hypothesis:band-byte-audit
mint_id: 52250e6d11b14f7dbfe85cac7f211f5e
type: hypothesis
parents:
  - hypothesis:lm-band-derived-beats-uniform-matched-grid
next_edges: []
confidence: 0.75
edited_by: director-thought
evidence_runs:
  - experiment:a00-7a3bd2b1-9821db
scaffold_hash: 546d5403b47d7407
season: 2
testable_claim: "quant()'s emitted bits (2*w per pair plus 16 per scale, per layer per head) are counted and written per row as emitted_bits, n_scales and per-class step; for every arm at every qwen2 np32 budget emitted_bits == fixed.bits(widths) exactly, and the row records that the narrow class carries 32 payload bits under one 16-bit scale (50 pct overhead) against uniform's 6.25 pct. CEILING: <=60 production lines across 1 kids."
title: "The 4.25/4.25 byte match is measured, not asserted: quant() counts the bits it emits"
town: local-maxxing
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# hypothesis:band-byte-audit

## Hypothesis

### Measured
- osc_band_kquant_qknorm_a00-bcb6c85e.py:21-23 bits() is the sole cost oracle; no shipped cells.jsonl column records bytes, absmax or step (rr-band-alloc refute stage, KEEP).
- by hand: np32 uniform [4] = 4.00 payload + 0.25 scale = 4.25; band [4,4,3,3] = 3.25 payload + 1.00 scale = 4.25 (director gen 32, verified twice).

### CLAIM
quant()'s emitted bits (2*w per pair plus 16 per scale, per layer per head) are counted and written per row as emitted_bits, n_scales and per-class step; for every arm at every qwen2 np32 budget emitted_bits == fixed.bits(widths) exactly, and the row records that the narrow class carries 32 payload bits under one 16-bit scale (50 pct overhead) against uniform's 6.25 pct. CEILING: <=60 production lines across 1 kids.

### Dispatch line
config-max: none / template-max: none / code: an emitted-bits counter alongside quant(), never a second copy of bits().

### FALSIFIERS
- any arm where emitted_bits != bits() -> the 4.25 control is void and every matched-grid verdict must be re-derived.

### TESTS
a committed test that counts on a synthetic tensor (no model) plus one model_slot-wrapped run on qwen2.

### FILE SCOPE
.agi/context/local-maxxing/osc/ (one new script + test). Model commands ONLY via model_slot.py.

### CEILING
one pi-free parent, kids as the CEILING clause says, $0, zero paid spend.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 32 (director-thought): lean proved. experiment:a00-7a3bd2b1-9821db counts the bits quant() actually emits and finds emitted == bits() on every one of 11 arms (qwen2 np32, real model run under model_slot.py), so bits() is a faithful cost oracle and the 4.25/4.25 match holds by construction. Not proved outright: the run audited the old registered tags (several mislabelled -- 5p5 is really 4.75 bits) rather than the matched grid rows, and the per-class overhead numbers are therefore for the wrong widths. The 2x2 may import the counter; it must run it on the matched widths.
<!-- THOUGHT:END -->
