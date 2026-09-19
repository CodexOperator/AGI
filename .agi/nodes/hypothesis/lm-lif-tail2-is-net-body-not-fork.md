---
id: hypothesis:lm-lif-tail2-is-net-body-not-fork
mint_id: f796cd365a9a45cb899394fc080ec08d
type: hypothesis
parents:
  - idea:lm-why-lif-first-reply-non-frontier
next_edges: []
edited_by: ubuntu
scaffold_hash: 23543e8a5b2068b4
season: 2
testable_claim: "Emit lif_trivial.bend: the identical batch(2n,7) 4-net fork but with net!(seed) = U32.add(seed,1n), so the body carries no sim/List/&2 continuations; instrument and read H[task_tail(r)+1] on the first corpus_eval work_loop return. Claim: it is 0 (the tail came from net's body); falsified if it is still 2 (the tail comes from the batch/pair construction, independent of net's body)."
thought_session: iter-TM.60
title: "\"Replacing the body of net with a trivial U32.add (4-net batch/pair construction held fixed) drops the first-reply tail to 0, so the owed arguments come from the body of net (its sim/List continuations), not from the batch/pair construction\""
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-lif-tail2-is-net-body-not-fork

## Hypothesis
## Hypothesis

`net`'s body is the source of the owed arguments. This is the complement of
`hypothesis:lm-lif-tail2-is-main-pair-destructure`: here the pair/batch
construction is held FIXED and the body is emptied.

### Claim
With the 4-net `batch(2n,7)` construction unchanged but `net!(seed)` reduced to
`U32.add(seed,1n)` -- no `sim`, no `List`, no `&2` pair in the body -- the first
`corpus_eval` `work_loop` return has `H[task_tail(r)+1] == 0`.

### How it is falsified
- `lif_trivial` still returns `tail=2` -> the owed arguments are created by the
  batch/pair construction alone and `net`'s body is exonerated; hypothesis
  disproved.
- `lif_trivial` returns `tail=0` -> the pending frame is produced by `net`'s own
  body (`net.fin(sim(...))` and the 9-arg `sim` frame); hypothesis proved.

### Cost
$0 compute. Host-only, same recipe as the sibling hypothesis: `bend` emit, apply
`instr2.py` + per-call wrapper, `clang-19 -DBEND_CUDA=1`, run WITHOUT `--gpu`.
The trivial body reduces in milliseconds, so this is the cheapest of the
variants. <= 10 min wall, no GPU slot.

### Experiment that tests it
ONE experiment node under this hypothesis: emit+instrument `lif_trivial`; record
`md5` of the emitted C, first-call `r`, `H[task_tail(r)+1]`, steps, wall, and
the current 4-net control row side by side.
