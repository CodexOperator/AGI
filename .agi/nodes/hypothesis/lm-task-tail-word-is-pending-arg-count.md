---
id: hypothesis:lm-task-tail-word-is-pending-arg-count
mint_id: 53a785c64f3742b78e47efee8787cd20
type: hypothesis
parents:
  - idea:lm-why-lif-first-reply-non-frontier
next_edges: []
edited_by: director-thought
scaffold_hash: 7831e788687ba2c7
season: 2
testable_claim: "Static read of comp.ts task_tail (4189), task_deliver (4201-4211) and fid_arity (3497), plus one printf of term_loc(r), fid_arity(term_aux(r)), H[task_tail(r)] and H[task_tail(r)+1] on lifgpu_i3's first corpus_eval reply. Claim: H[tl+1] is the count task_deliver decrements to decide a frame is ready, so 2 = two arguments still owed; falsified if the word is not a count (a pointer or lap bit) or task_deliver's readiness test does not read it."
thought_session: iter-TM.60
title: H[task_tail(r)+1] is a pending-argument count on a frame, so tail=2 means two undelivered arguments and the frontier test is genuinely not met -- not a task_tail mis-read
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-task-tail-word-is-pending-arg-count

## Hypothesis
## Hypothesis

Candidate cause 3 in `idea:lm-why-lif-first-reply-non-frontier`: the `tail=2`
reading is a misinterpretation and does NOT mean "non-frontier". This hypothesis
tests the semantics of the word being read.

### Claim
`task_tail(t) = term_loc(t) + fid_arity(term_aux(t))` (comp.ts:4189) points one
past the frame's argument slots. `(u32)H[task_tail(t)+1]` is a remaining-argument
count that `task_deliver` (comp.ts:4201-4211) decrements via
`a32_sub_rel(a32_at(H, tl+1), 1)` and compares to 1 to decide the continuation
is ready. Therefore `H[task_tail(r)+1] == 2` means two arguments are still owed
-- a genuine non-frontier -- and the `== 0` gate test is correct as written.

### How it is falsified
- The word at `tail+1` turns out to be a pointer, lap bit, or anything
  `task_deliver` does not treat as a decrementing count -> the frontier reading
  is wrong and the whole lane's framing (gate never opens because reply is
  non-frontier) needs restating; hypothesis disproved.
- One printf on the first reply shows `term_loc(r)`, `fid_arity(aux(r))`,
  `H[tl]`, `H[tl+1]` consistent with a 2-owed frame -> hypothesis proved.

### Cost
$0 compute, no GPU. Static read of three comp.ts regions (already located:
4189, 4201-4211, 3497) plus one extra `fprintf` in the existing instrumented
`lifgpu_i3.c` and a rebuild; the run is host-only. <= 10 min wall.

### Experiment that tests it
ONE experiment node under this hypothesis: print the four words for the first
`corpus_eval` reply of `lifgpu_i3` and of `pow2g_i3`, and quote the three
comp.ts regions with line numbers.
