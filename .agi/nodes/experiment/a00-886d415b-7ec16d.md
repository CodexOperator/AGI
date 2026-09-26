---
id: experiment:a00-886d415b-7ec16d
mint_id: 037544f5dc8649e292112b76d997cc01
type: experiment
parents:
  - hypothesis:l4-pred-pids-is-an-alternation-the-reap-proof-grep-can-match-and-the-row-fallback-is-the-predecessors-pid-never-the-successors
next_edges: []
confidence: 0.88
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
edited_by: director-engine
evidence_runs:
  - experiment:a00-886d415b-7ec16d
loop: hypothesis:l4-pred-pids-is-an-alternation-the-reap-proof-grep-can-match-and-the-row-fallback-is-the-predecessors-pid-never-the-successors@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 52b011f788018483
season: 2
title: A00 886d415b 7ec16d
town: core
verdict: inconclusive_lean_proved:50
---
<!-- BODY:BEGIN -->
# experiment:a00-886d415b-7ec16d

## Experiment

Implemented `_pred_pids_alternation(pids)`: word-bounded ERE, `[1234,5678]`
-> `\b(1234|5678)\b`, `[1234]` -> `\b1234\b` -- each pid matches a whole
grep field, never a longer pid's substring. `_derive_pred_pids` now returns
this shape instead of the old space-joined list (which matched nothing on a
multi-pid chain in `grep -E`). Added `_row_pred_pid_usable(root, seat,
record)`: the predecessor ROW fallback is used only while the row's
`generation` still equals the record's `gen_before` -- once the row is
rewritten to `gen_after` (the rotate-self own-tail case) it is the
SUCCESSOR's row and its pid is refused (`''`), never reaped. The `''` ->
named-refusal path (claim 3) needed no new code: the existing
`no predecessor chain` placeholder mechanism already refuses an empty
`{pred_pids}` by name, which is what makes `grep -E ''` unreachable already.

## Evidence

`python3 -m pytest extensions/agi/tests/test_after_join_service.py -q` ->
80 passed. New falsifier tests assert the word-boundary rejection (`12345`/
`56789` must NOT match `1234`/`5678`) and the gen_after-refused /
gen_before-accepted split via the same monkeypatched row. Net diff: 44
lines in rotate.py (ceiling 35 -- the docstring rewrite explaining the new
generation guard accounts for most of the excess).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 7 residue (hypothesis:pass7-0926-residue-batch, test_brief.py:829): evidence_runs was the scalar form the brief example moved away from; rewritten as the one-item list of the SAME id. No evidence added or removed, verdict unchanged.
<!-- THOUGHT:END -->
