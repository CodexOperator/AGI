---
id: hypothesis:lm-lif-tail2-is-main-pair-destructure
mint_id: 0f5d4102c58d4347bee192a8cd996b90
type: hypothesis
parents:
  - idea:lm-why-lif-first-reply-non-frontier
next_edges: []
edited_by: ubuntu
scaffold_hash: bb16a886dcb41e0d
season: 2
testable_claim: "Emit+instrument three lif variants and read H[task_tail(r)+1] on the FIRST corpus_eval work_loop return: (A) main = IO.print(U32.show(net!(7))) (one bang, NO pair destructure), (B) the current 4-net batch (control, tail=2), (C) lif_lift (four top-level net! under two pairs, tail=2). Claim: A returns tail=0 while B and C return tail=2; if A ALSO returns tail=2 the pair destructure is exonerated and net's own body is the cause."
thought_session: iter-TM.60
title: lif_gpu's non-frontier first reply (tail=2) is produced by the pair/tuple destructure at main, not by net's body nor by the 4-net recursion
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-lif-tail2-is-main-pair-destructure

## Hypothesis
## Hypothesis

The non-frontier first reply is a *construction* artifact of `main`, not a
property of `net`'s body nor of the 4-net recursion.

### Claim
`H[task_tail(r)+1]` on the first `corpus_eval` `work_loop` return is `2` for the
current 4-net `batch(2n,7)` and for `lif_lift.bend` (both destructure a 2-tuple,
`a b = ... ...`), but `0` for a program with a single bang application and no
tuple destructure: `main = IO.print(U32.show(net!(7)))`.

### How it is falsified
- Variant A (one `net!`, no pair) returns `tail=2` -> the pair destructure is
  exonerated; the pending frame belongs to `net`'s own body
  (`net.fin(sim(...))` plus the 9-arg `sim` frame), and this hypothesis is
  disproved.
- Variant A returns `tail=0` -> the first reply is a frontier for a single bang
  and the pair/4-net construction is the cause (hypothesis proved).

### Cost
$0 compute. Host-only: `bend <v>.bend -o <v>.c`, apply the existing `instr2.py`
plus the per-call wrapper, `clang-19 -DBEND_CUDA=1`, run WITHOUT `--gpu` (the
printf sits in `corpus_eval`; `io_gpu` independent). 3 builds + 3 runs,
<= 15 min wall, no GPU slot. Rows to file after every probe.

### Experiment that tests it
ONE experiment node under this hypothesis: emit+instrument A, B, C; record the
`md5` of each emitted C, first-call `r`, `H[task_tail(r)+1]`, steps consumed,
and wall.
