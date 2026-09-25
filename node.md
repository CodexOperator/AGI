---
id: experiment:a00-325d4c56-bedcc8
mint_id: 323974765ef6467593b1703ff62f9970
type: experiment
parents:
  - hypothesis:lm-band-derived-beats-uniform-matched-grid
next_edges: []
loop: hypothesis:lm-band-derived-beats-uniform-matched-grid@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: a26c544e424726e5
season: 2
title: A00 325d4c56 bedcc8
town: local-maxxing
---
<!-- BODY:BEGIN -->
# experiment:a00-325d4c56-bedcc8

## Experiment

I checked whether the already-completed 72-cell sweep can be corrected merely by relabelling `index_order` as a true uniform control. It cannot, for a byte-exact matched-budget grid.

The allocator's authoritative accounting is:

```
bits([w]) = w + 1                         # one flat class, scale charged
bits([a,b,c,d]) =
  (a+b+2c+4d + 32) / (2*n)                 # n/8,n/8,n/4,n/2 classes
```

Therefore a true flat uniform arm can hit these target averages **exactly** only at targets 5.0, 6.0, and 7.0 bits in the tested range, using `[4]`, `[5]`, and `[6]`. Every half-bit target (4.5, 5.5, 6.5, 7.5, 7.75) and target 4.0 is unattainable by the current scalar-bit uniform API without rounding the budget. Using the nearest integer width would compare unequal budgets and would repeat the central matching error this round is meant to remove.

| target bits | exact true-uniform widths | comparison with completed 72-cell sweep |
|---:|---|---|
| 4.0 | none | `[3,3,3,3]` derived arms are quantization-equivalent to flat `[3]` (4 actual bits) |
| 4.5 | none | no exact scalar-width control |
| 5.0 | `[4]` | `[4,4,4,4]` arms are quantization-equivalent to flat `[4]` |
| 5.5 | none | no exact scalar-width control |
| 6.0 | `[5]` | `[5,5,5,5]` arms are quantization-equivalent to flat `[5]` |
| 6.5 | none | no exact scalar-width control |
| 7.0 | `[6]` | `[6,6,6,6]` arms are quantization-equivalent to flat `[6]` |
| 7.5 | none | no exact scalar-width control |
| 7.75 | none | no exact scalar-width control |

The flat-width equivalence matters because `quant()` applies the same scalar width to every class. At `[3,3,3,3]`, `[4,4,4,4]`, `[5,5,5,5]`, and `[6,6,6,6]`, changing the energy labels cannot change any quantized key value. Thus the existing `key_only` measurements at 4.0, 5.0, 6.0, and 7.0 are also exact true-uniform results, and all derived arms tie there rather than key-only beating uniform.

## Evidence

- Source checked: `osc_band_kquant_qknorm_a00-bcb6c85e.py`, especially `bits()`, `arm()`, and `quant()`.
- Completed raw cells checked: experiment:a00-395e2a3e-a43ce2's 36 Qwen2.5 and 36 Qwen3 records. Their flat-width rows and authoritative `bits` values match the table above.
- Result: a claimed hit from relabelling `index_order` would be invalid. The preregistered exact matched-uniform claim remains pending; six of nine width labels have no representable true-uniform cell under the current allocator.
- No model run was launched: the numeric feasibility contradiction is exact and makes a new run unable to fill the missing matched cells.

## Largest safe step

Change the uniform-control representation before another sweep: support a two-width uniform mixture with a deterministic alternating RoPE-pair split (and charge both scales), so every tested average can be represented exactly. Until then, do not claim key-only beats true uniform.
