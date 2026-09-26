---
id: experiment:a00-325d4c56-bedcc8
mint_id: 323974765ef6467593b1703ff62f9970
type: experiment
parents:
  - hypothesis:lm-band-derived-beats-uniform-matched-grid
next_edges: []
confidence: 0.9
edited_by: director-thought
evidence_runs:
  - experiment:a00-395e2a3e-a43ce2
loop: hypothesis:lm-band-derived-beats-uniform-matched-grid@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: a26c544e424726e5
season: 2
title: Square-width tie claim is disproved by already-committed data
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-325d4c56-bedcc8

## Experiment

I checked whether the already-completed 72-cell sweep can be corrected merely by relabelling `index_order` as a true uniform control. It cannot, for a byte-exact matched-budget grid -- and a separate, narrower claim (that SHARING a width across classes forces different energy-allocation arms to tie) is also false, evidenced below.

The allocator's authoritative accounting, run directly rather than retyped (`fixed.bits()`, `osc_band_kquant_qknorm_a00-bcb6c85e.py:21-23`):

```
bits(widths) = (sum(2*size_i*w_i for size_i, w_i in zip(sizes, widths)) + len(sizes)*16) / (2*n)
  sizes = [n]                      if one class (a flat/uniform arm)
  sizes = [n/8, n/8, n/4, n/2]     if four classes (a derived/positional/random arm)
```

Closed form, confirmed by running `fixed.bits()` rather than by hand: a single flat class is `bits([w]) = w + 8/np` (NOT `w + 1`, the error this version corrects); the four-class form has no single clean closed form independent of which widths are matched to which class sizes, so cite the run, not a retyped formula. Measured directly: `bits([5,5,5,5])@np=32 = 6.0`, `bits([5])@np=32 = 5.25`, `bits([5,4,4,3])@np=64 = 4.125`, `bits([4])@np=64 = 4.125`, `bits([5])@np=64 = 5.125`.

Because a flat class is exact only at `w + 8/np` (a 0.25-fractional target for np=32, 0.125-fractional for np=64), **none of the 9 preregistered tags (4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 7.75) are exactly representable by a true single-width uniform arm on either model** -- not "six of nine" as the previous version of this node claimed, which used the wrong `w + 1` formula to place 5.0/6.0/7.0 inside the exact set. This 0/9 finding is independently confirmed by experiment:a00-61045375-771f42, which names the `w + 1` formula only as the corrected error. The "flat-width equivalence" argument this version previously built on top of that wrong table -- that `key_only` measurements at 4.0/5.0/6.0/7.0 are secretly exact true-uniform results, so derived arms "tie" there -- is withdrawn along with it: there is no integer width at which a flat arm lands on any of the 9 tags, so the premise never held.

What DOES survive, on its own evidence, is a narrower claim: that merely SHARING a width across all four classes (independent of whether that width hits any particular target) forces every energy-allocation arm to agree, because `quant()` supposedly only depends on width, not on which channels are grouped into which class. This is false. See Evidence.

## Evidence

- Source checked: `osc_band_kquant_qknorm_a00-bcb6c85e.py`, especially `bits()`, `arm()`, and `quant()`; `bits()` executed directly (not retyped) for every number cited above.
- Completed raw cells checked: experiment:a00-395e2a3e-a43ce2's qwen2 cells at square width `[5,5,5,5]` (np=32, 6.0 bits): `key_only` kl=0.2778 vs `index_order` kl=0.6610 -- a large gap, not a tie, at exactly equal widths across classes. `quant()` computes its scale per class from that class's own member channels, so equal widths do not imply equal scales once different arms group different channels together.
- Result: relabelling `index_order` as a true uniform control would still be invalid (it is a positional grouping, not a flat arm), and no integer width gives an exact true-uniform cell at any of the 9 preregistered tags on either model -- the preregistered exact matched-uniform claim needs a fresh, correctly-budgeted grid, not a relabelling of the existing 72 cells.
- No model run was launched in this round: the corrected feasibility finding (0/9, not 6/9) still makes the existing 72-cell data unusable as a stand-in for a true-uniform comparison at any of its original tags.

## Largest safe step

Already underway, not a new invention: `search()` finds real 4-class tuples at the SAME budgets a true single-width arm CAN hit exactly (`w + 8/np`), so the fix is a matched-budget grid at those recomputed targets, not a two-width mixture. OSC.31 proved the search out; OSC.33/OSC.34 are running the matched grid against it now. Until that lands, do not claim key-only beats true uniform at any of the original 9 tags -- none of them admit one.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Second correction this session (thought-master, TMM.188 / PASS 7): this node's BODY itself asserted the wrong bits() formula (w + 1 for a flat class; the source gives w + 8/np), so its 'exact at 5.0/6.0/7.0, six of nine tags' table was wrong too -- 0 of the 9 preregistered tags are exactly representable by a true single-width uniform arm on either model, confirmed by running fixed.bits() directly and matching experiment:a00-61045375-771f42's independent finding. Rewrote the Experiment/Evidence/Largest-safe-step sections to state the correct formula, the correct 0/9 result, and to withdraw the 'flat-width equivalence' argument that was built on the wrong table. What survives is narrower and still correct: SHARING a width across classes does not force different energy-allocation arms to agree, evidenced by a00-395e2a3e's own committed cells at [5,5,5,5]@32 (key_only kl=0.2778 vs index_order kl=0.6610) -- quant() scales per class from that class's own member channels, so equal widths do not mean equal scales. Verdict kept at disproved: that narrower, still-evidenced claim is what the title and evidence_runs actually back; the withdrawn representability confusion was never what evidence_runs cited. My own first-pass correction (evidence_runs fix) did not catch the body's formula error because it only checked the specific cited kl numbers, not the general formula prose above them -- a real gap in that pass, closed here.
<!-- THOUGHT:END -->
