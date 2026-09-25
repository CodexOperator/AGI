---
id: experiment:a00-61045375-771f42
mint_id: f660ebb311054d94a862f74bcae584a7
type: experiment
parents:
  - hypothesis:lm-band-derived-beats-uniform-matched-grid
next_edges: []
confidence: 0.7
edited_by: director-thought
evidence_runs:
  - experiment:a00-61045375-771f42
loop: hypothesis:lm-band-derived-beats-uniform-matched-grid@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 0482e6428ed42d83
season: 2
title: Static uniform representability audit is inconclusive
town: local-maxxing
verdict: pending
---
<!-- BODY:BEGIN -->
# experiment:a00-61045375-771f42

## Experiment

I audited the proposed matched-uniform grid against the authoritative allocator in
`osc_band_kquant_qknorm_a00-bcb6c85e.py`. The audit was deliberately a prerequisite
check, not a model claim: the current `mode="uniform"` path creates one size class,
`[n]` (n = SPEC["np"]), so its exact average-bit accounting (one 16-bit scale
charged once, amortised over 2*n dimensions) is

```text
bits([w]) = w + 8/n
```

i.e. w + 0.25 for Qwen2.5 (np=32) and w + 0.125 for Qwen3 (np=64) -- NOT w+1 as
first written in this experiment. That first version was wrong: the parent's own
gate probe (Agent Notes below) ran the real function over integer widths 1..19 and
found no exact match for ANY of the 9 preregistered targets on np=32, contradicting
the original claim that 5.0/6.0/7.0 were exactly representable. The director
independently reconfirmed this for BOTH models before this rewrite (not on
say-so): with bits([w]) = w + 8/n, the achievable values sit at X.25 (np=32) or
X.125 (np=64) fractions, none of which land within 0.01 of any of
4.0/4.5/5.0/5.5/6.0/6.5/7.0/7.5/7.75 -- 0 of 9 tags exact on EITHER model, not 3 of
9 on one model as first claimed.

I also checked that the prior `index_order` result is not evidence for a true
uniform win: it selects four classes in energy mode with a constant ordering,
whereas true uniform uses `mode="uniform"` and one class. A separate node
(experiment:a00-325d4c56-bedcc8) argued that "square" width tuples like
`[w,w,w,w]` make `quant()` class-assignment-invariant; that argument is disproved
(see that node) -- `quant()` computes its scale per class from that class's own
member channels, so different arms still diverge at equal per-class widths.

No model was loaded and no new result is asserted here. This experiment is the
smallest safe next step: establish whether the requested control is representable
before spending compute on an invalid sweep.

## Evidence

- Source: `.agi/context/local-maxxing/osc/osc_band_kquant_qknorm_a00-bcb6c85e.py`,
  `bits()`, `arm()`, and `quant()`.
- Exact representability table (corrected; bits([w]) = w + 8/n):

  | target average bits | np=32 (Qwen2.5) | np=64 (Qwen3) |
  |---:|---|---|
  | 4.0 | none (nearest w=4 -> 4.25) | none (nearest w=4 -> 4.125) |
  | 4.5 | none (nearest w=4 -> 4.25) | none (nearest w=4 -> 4.125) |
  | 5.0 | none (nearest w=5 -> 5.25) | none (nearest w=5 -> 5.125) |
  | 5.5 | none (nearest w=5 -> 5.25) | none (nearest w=5 -> 5.125) |
  | 6.0 | none (nearest w=6 -> 6.25) | none (nearest w=6 -> 6.125) |
  | 6.5 | none (nearest w=6 -> 6.25) | none (nearest w=6 -> 6.125) |
  | 7.0 | none (nearest w=7 -> 7.25) | none (nearest w=7 -> 7.125) |
  | 7.5 | none (nearest w=7 -> 7.25) | none (nearest w=7 -> 7.125) |
  | 7.75 | none (nearest w=7 -> 7.25, diff 0.5) | none (nearest w=8 -> 8.125, diff 0.375) |

- Consequently, a fresh run using nearest-width uniform controls would violate the
  matched-budget falsifier as originally written for these 9 tags. A valid
  follow-up (OSC.33, ordered TMM.175) instead targets the budgets where a true
  uniform width IS exact -- w + 8/n lands on w+0.25/w+0.125 exactly at w itself
  plus that fraction, so e.g. np=32 4.25 bits ([4] uniform) has a matched 4-class
  tuple too ([4,4,3,3]) -- and compares key_only/inverse_energy/random/index_order
  against the TRUE uniform arm at those matched-exact budgets instead.

## Verdict

Pending. The target hypothesis remains untested rather than disproved: the
current allocator cannot represent any of the 9 originally-requested matched-
uniform points on either model (0/9, corrected from the original 3/9-on-one-model
claim), and the available 72-cell sweep used a positional control (index_order)
instead of true uniform. OSC.33 targets the budgets where true uniform IS exact.

## Agent Notes
Static allocator audit found true uniform exact only at 5.0/6.0/7.0 bits; six target widths remain untested, so the matched-grid claim is pending.

Parent review: gate probe ran the changed bits() function with SPEC np=32 over integer widths 1..19. It returned no exact match for any of 9 target labels, contradicting the node’s claimed w+1 accounting and 5.0/6.0/7.0 representation. The source formula charges one 16-bit scale over 2*n dimensions, so bits([w])=w+0.25 for np=32, not w+1; the near-miss is mistaking scale overhead for one full bit per element. Demote to inconclusive_lean_disproved:85 pending a corrected audit; no model evidence is claimed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT THE INSTRUCTION SAID: “The exact representability table” and “true uniform exact only at 5.0, 6.0, and 7.0 bits.” WHAT THE MACHINE ACTUALLY DOES: the changed allocator’s bits() at .agi/context/local-maxxing/osc/osc_band_kquant_qknorm_a00-bcb6c85e.py:21-23 computes (2*n*w + 16)/(2*n) for a one-width list, which is w+0.25 for np=32; a parent gate probe executed that function for integer widths 1..19 and found no exact match for any target, including 5.0, 6.0, and 7.0. THE NEAR MISS: counting the single 16-bit scale as one bit per key element, rather than amortising it over 2*n elements, makes the table look plausible while contradicting the executable accounting. No deviation: a static audit is a prerequisite claim, so a wrong accounting blocks the requested uniform sweep and keeps the hypothesis pending.
<!-- THOUGHT:END -->
