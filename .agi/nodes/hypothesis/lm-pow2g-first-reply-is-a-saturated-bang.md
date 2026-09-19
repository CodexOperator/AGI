---
id: hypothesis:lm-pow2g-first-reply-is-a-saturated-bang
mint_id: c91ef4a261b74776bbf58387168fffaa
type: hypothesis
parents:
  - idea:lm-why-lif-first-reply-non-frontier
next_edges: []
edited_by: ubuntu
scaffold_hash: 79d403a2dac0df3e
season: 2
testable_claim: "Read pow2g.bend and its emitted C and diff the first FID_ENTER of each program: claim pow2g's first task is entered with all fid_arity arguments present (remaining count 0) while lif's first task owes 2, and the difference is lif's extra def hop net.fin(sim(...)); falsified if pow2g also enters with owed args, or if lif's owed count is not tied to the wrapper hop."
thought_session: iter-TM.60
title: pow2g's first reply is frontier because its bang def is entered saturated (all args present), while lif reaches net! through the net.fin wrapper leaving a pending frame
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-pow2g-first-reply-is-a-saturated-bang

## Hypothesis
## Hypothesis

The direct contrast that the WHY question rests on. `pow2g` and `lif_gpu` are
both built with `net!`-style bangs and both reach `corpus_eval` with `io_gpu`
true, yet only `pow2g` returns a frontier first reply (`tail=0`, `launches=4`).
The hypothesis names the one structural difference: how many def hops stand
between `main` and the bang fid.

### Claim
In `pow2g.bend`, `main` applies the bang def in a saturated position, so the
first `FID_ENTER` finds `fid_arity(f)` arguments present and `H[tl+1] == 0`. In
`lif_gpu.bend`, `net!(seed)` is a wrapper (`net(+seed) -> net.fin(sim(...))`),
so the first reply is the `net`/`net.fin` frame with 2 arguments still owed.

### How it is falsified
- `pow2g`'s first `FID_ENTER` also shows owed arguments -> saturation is not the
  difference and this hypothesis is disproved; the contrast must lie elsewhere
  (e.g. the bang flag position or `term_aux`).
- `lif`'s owed count is not attributable to the `net.fin` wrapper hop -> the
  wrapper is exonerated.

### Cost
$0 compute, no GPU. Read `pow2g.bend` and the emitted `pow2g_i3.c` /
`lifgpu_i3.c` (both already on the rig), diff the `FID_ENTER`/`WL_CASE` sequence
for the first task, plus one printf of `fid_arity(term_aux(t))` and the frame's
remaining word at the first `FID_ENTER`. <= 10 min wall.

### Experiment that tests it
ONE experiment node under this hypothesis: quote the first-`FID_ENTER` rows for
both binaries (`war`, `H[tl+1]`, `fid_bangs`) and the `pow2g.bend`/`lif_gpu.bend`
`main` + bang-def lines with line numbers.
