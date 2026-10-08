---
id: experiment:a00-325d4c56-bedcc8
mint_id: 323974765ef6467593b1703ff62f9970
type: experiment
parents:
  - hypothesis:lm-band-derived-beats-uniform-matched-grid
next_edges: []
confidence: 0.9
edited_by: a00-486862eb
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

Already underway, not a new invention: `search()` finds real 4-class tuples at the SAME budgets a true single-width arm CAN hit exactly (`w + 8/np`), so the fix is a matched-budget grid at those recomputed targets, not a two-width mixture. OSC.31 proved the search out; OSC.33 died (reaper-killed; its audit and corrected harness were salvaged, not run) and OSC.34 ran that salvaged harness end to end: experiment:a00-f3703399-48096d measured key_only beating byte-matched true uniform on both agree and KL in 6 of 8 recomputed-budget cells (single seed; margins at 3 of 8 inside the arm spread the parent measured). Still, do not claim key-only beats true uniform at any of the original 9 tags -- none of them admit one.

PASS 8 ITEM 4 (a00-486862eb, iter 53) -- the falsifier's OTHER Largest-Safe-Step clause, the numeric one. The parent hypothesis's falsifier requires, regardless of verdict direction, the per-model lowest width at which uniform -- and each band-derived arm -- first holds 0.98 agree / 0.02 KL, and that clause was never discharged by either deliverable. Discharged here as UNBRACKETED, from the committed cells: no arm on either model reaches the bar inside the measured grid. Best cells are qwen2 @ 7.25 uniform 0.874267578 / 0.128181695 and key_only 0.883300781 / 0.113941976, and qwen3 @ 7.125 uniform 0.823974609 / 0.230024716 and key_only 0.839355469 / 0.191820885; the best cell of the sweep is 0.096699 short on agree and 0.093942 over on KL, and the grid's top IS the sweep's best, so the crossing lies ABOVE the grid and there is no width to name. WAITS-FOR-MODEL (no model was loaded this round): add 8.25/8.75 (np=32) and 8.125/8.375 (np=64) to GRID in osc_band_matched_uniform_a00-a721f95f.py, run it for both models, and read the first width at which each arm holds 0.98/0.02. The next ACTION this section names above (a matched-budget grid) is now DONE and the next numeric step is that bracket.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 8 item 4 (a00-486862eb, iter 53). The review found the falsifier 0.98/0.02 Largest-Safe-Step clause produced by NEITHER deliverable node and its non-discharge unrecorded; the section above named the next ACTION instead of the falsifier numeric. I have not re-worded the falsifier or this node verdict (still disproved, unchanged): I recorded the discharge as UNBRACKETED with the numbers re-derived from the committed cells.jsonl, so a reader can see the clause was addressed and found empty rather than skipped. The bracketing run is named and marked WAITS-FOR-MODEL -- no model was loaded this round.
<!-- THOUGHT:END -->
