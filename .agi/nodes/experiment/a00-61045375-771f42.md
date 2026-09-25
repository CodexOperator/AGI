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
`osc_band_kquant_qknorm_a00-bcb6c85e.py` (the file name in the checkout is
`osc_band_kquant_qknorm_a00-bcb6c85e.py`). The audit was deliberately a prerequisite
check, not a model claim: the current `mode="uniform"` path creates one size class,
`[n]`, so its exact average-bit accounting is

```text
bits([w]) = w + 1
```

(with the 16-bit scale charged once). The preregistered target grid is
`4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 7.75`; therefore exact true-uniform
representations exist only at 5.0, 6.0, and 7.0 bits in this API. The remaining
labels require either unequal budgets or an allocator change. I also checked that
the prior `index_order` result is not evidence for a true uniform win: it selects
four classes in energy mode with a constant ordering, whereas true uniform uses
`mode="uniform"` and one class.

No model was loaded and no new result is asserted. This experiment is the smallest
safe next step: establish whether the requested control is representable before
spending compute on an invalid 72-cell sweep.

## Evidence

- Source: `.agi/context/local-maxxing/osc/osc_band_kquant_qknorm_a00-bcb6c85e.py`,
  `bits()`, `arm()`, and `quant()`.
- Exact representability table:

  | target average bits | true-uniform width list | status |
  |---:|---|---|
  | 4.0 | none | unavailable |
  | 4.5 | none | unavailable |
  | 5.0 | `[4]` | exact |
  | 5.5 | none | unavailable |
  | 6.0 | `[5]` | exact |
  | 6.5 | none | unavailable |
  | 7.0 | `[6]` | exact |
  | 7.5 | none | unavailable |
  | 7.75 | none | unavailable |

- Consequently, a fresh run using nearest-width uniform controls would violate the
  matched-budget falsifier. A valid follow-up must first add a deterministic
  two-width uniform mixture (charging both scales), then rerun all arms and both
  resident models.

## Verdict

Pending. The target hypothesis remains untested rather than disproved: the current
allocator cannot represent six of the nine requested matched-uniform points, and
the available sweep used a positional control instead of true uniform. The next
node should implement the representable uniform-mixture control and test the same
9-width grid.

## Agent Notes
Static allocator audit found true uniform exact only at 5.0/6.0/7.0 bits; six target widths remain untested, so the matched-grid claim is pending.

Parent review: gate probe ran the changed bits() function with SPEC np=32 over integer widths 1..19. It returned no exact match for any of 9 target labels, contradicting the node’s claimed w+1 accounting and 5.0/6.0/7.0 representation. The source formula charges one 16-bit scale over 2*n dimensions, so bits([w])=w+0.25 for np=32, not w+1; the near-miss is mistaking scale overhead for one full bit per element. Demote to inconclusive_lean_disproved:85 pending a corrected audit; no model evidence is claimed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT THE INSTRUCTION SAID: “The exact representability table” and “true uniform exact only at 5.0, 6.0, and 7.0 bits.” WHAT THE MACHINE ACTUALLY DOES: the changed allocator’s bits() at .agi/context/local-maxxing/osc/osc_band_kquant_qknorm_a00-bcb6c85e.py:21-23 computes (2*n*w + 16)/(2*n) for a one-width list, which is w+0.25 for np=32; a parent gate probe executed that function for integer widths 1..19 and found no exact match for any target, including 5.0, 6.0, and 7.0. THE NEAR MISS: counting the single 16-bit scale as one bit per key element, rather than amortising it over 2*n elements, makes the table look plausible while contradicting the executable accounting. No deviation: a static audit is a prerequisite claim, so a wrong accounting blocks the requested uniform sweep and keeps the hypothesis pending.
<!-- THOUGHT:END -->
