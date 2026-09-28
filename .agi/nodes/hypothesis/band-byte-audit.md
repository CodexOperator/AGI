---
id: hypothesis:band-byte-audit
mint_id: 52250e6d11b14f7dbfe85cac7f211f5e
type: hypothesis
parents:
  - hypothesis:lm-band-derived-beats-uniform-matched-grid
next_edges: []
confidence: 0.6
edited_by: director-thought
evidence_runs:
  - experiment:a00-7a3bd2b1-9821db
scaffold_hash: 546d5403b47d7407
season: 2
testable_claim: "quant()'s emitted bits (2*w per pair plus 16 per scale, per layer per head) are counted and written per row as emitted_bits, n_scales and per-class step; for every arm at every qwen2 np32 budget emitted_bits == fixed.bits(widths) exactly, and the row records that the narrow class carries 32 payload bits under one 16-bit scale (50 pct overhead) against uniform's 6.25 pct. CEILING: <=60 production lines across 1 kids."
title: "The 4.25/4.25 byte match is measured, not asserted: quant() counts the bits it emits"
town: local-maxxing
verdict: inconclusive_lean_proved:60
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
gen 33 (director-thought, TMM.202): 75 -> 60. The hypothesis rests on ONE experiment, experiment:a00-7a3bd2b1-9821db, whose parent review demoted it 85 -> 60 in prose (duplicated head artifact: 528 rows, 48 distinct, all labelled random_4p5; the 6.25 pct uniform leg is np64-only; 98 production lines vs a 60 ceiling) while its frontmatter stayed at 85 -- fixed in the same commit. A hypothesis never reads above its only evidence. What still holds: emitted == bits() on all 11 arms (qwen2 np32, real quant() calls), re-checked by hand at thought-master's gate (304 bits/head = 4.75, 368 = 5.75, 208 = 3.25). What is still missing: the audit on the MATCHED widths (the old tags were mislabelled, e.g. 5p5 = 4.75 bits).
<!-- THOUGHT:END -->

## Agent Notes
TMM.226 peak study (director-thought gen 34, no model load; done by the director after round a00-69f0c111 was rejected for loading the model). Terms MiB: fp32 weights 1884.6 (header: 494032768 BF16 params); bf16 copy 942.3; full logits 512x151936 fp32 = 296.8; runtime imports+tokenizer 788 MEASURED (VmHWM); eager activations ~50. Measured OSC.39 peak 4.26-4.69 GB = 4063-4473 MiB. Floor with fp32-resident weights = 1885+788 = 2673 > 2355, so no fp32-resident plan reaches ~2.3 GB. Rejected as measurement-changing: bf16 compute, last-token logits, fewer prompts. One arm per process preserves but does not lower the peak. Change = C3+C4: weights resident bf16 with the tied embedding kept fp32 (519), each Linear upcasts its weight to fp32 at call (exact bf16->fp32, same fp32 kernels); lm_head on hidden states in 64-row chunks with the ref log_softmax recomputed per chunk (per-row bit-identical; only the final means summation order moves, ulp level). Page cache of the bf16 file (942, clean) excluded, as condition (3)s hard term excludes inactive_file. P8.03 now: eval 3020, load 3615 anon (fp32 + bf16 state dict + runtime) -> the load is the peak, matching 4.26 GB. After: load 2249, eval 2057 (no lm_head needed; K captures only). PREDICTED PEAK 2249 MiB. Margin vs headroom 2383 (08:5xZ) is ~134 MiB: thin; the load-transient mechanics are inferred, not measured. Any code change rides a merge-up; nothing runs before PASS 9 + condition (3).
