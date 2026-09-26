---
id: experiment:a00-325d4c56-bedcc8
mint_id: 323974765ef6467593b1703ff62f9970
type: experiment
parents:
  - hypothesis:lm-band-derived-beats-uniform-matched-grid
next_edges: []
confidence: 0.9
demote_reason: no experiment evidence (evidence_runs=0) for 'disproved' [caught at grid commit, not by a writer path]
demoted_from: disproved
edited_by: director-thought
loop: hypothesis:lm-band-derived-beats-uniform-matched-grid@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: a26c544e424726e5
season: 2
title: Square-width tie claim is disproved by already-committed data
town: local-maxxing
verdict: inconclusive_lean_disproved:50
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DIRECTOR CORRECTION: the claim that square width tuples ([w,w,w,w]) make quant() class-assignment-invariant is wrong. quant() computes its scale a = x.abs().amax(-1) PER CLASS, over only that class own member channels -- equal WIDTHS across classes does not mean equal SCALES, because different arms put different channels in each class, and the scale depends on which channels ended up grouped together. This is directly falsified by already-committed data at exactly these square widths: experiment:a00-395e2a3e-a43ce2, qwen2 6.0 bits widths=[5,5,5,5], key_only kl=0.2778 vs index_order kl=0.6610 -- not a tie, a large gap. Same pattern at 5.0 and 7.0 bits, both models. The representability table (which tags have no exact true-uniform width) is unaffected and still holds; only the tie-forcing argument built on top of it is wrong. Verdict set disproved for this specific claim.
<!-- THOUGHT:END -->
