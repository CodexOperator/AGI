---
id: experiment:a00-e06485ce-10a12d
mint_id: 0aad3bf81b1a4891a89c66631b08801c
type: experiment
parents:
  - hypothesis:l4-keygen-all-live-completes-a-deferred-pending-swap-for-every-live-row-not-only-the-rows-it-keyed
next_edges: []
confidence: 0.9
edited_by: a00-72c899ca
evidence_runs:
  - experiment:a00-e06485ce-10a12d
loop: hypothesis:l4-keygen-all-live-completes-a-deferred-pending-swap-for-every-live-row-not-only-the-rows-it-keyed@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 19522c798f4a136a
season: 2
title: A00 e06485ce 10a12d
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e06485ce-10a12d

## Experiment

FIX-ONLY build order (g15.26 claim (b)). Measured the pre-fix defect, implemented the
claim, proved it on the built bytes.

**The defect (measured):** `send.py::_commit_push_all_live`'s completion loop ran
rotate._finish_pending_swap_on_push only over `keyed_names` -- the seats THIS
--all-live pass keyed. But a `<seat>.key.pending` is persisted (rotate._persist_pending_key)
only for a seat whose COMMITTED row already names the successor pubkey -- i.e. an
ALREADY-KEYED seat, which the `--all-live` walk (send.py:496-502) SKIPS before it can
reach `keyed_names.append`. So no seat could be in `keyed_names` AND own a pending file:
the completion site was unreachable by construction.

**The fix (send.py):** the loop now iterates EVERY live row read from the same node read
the walk uses (`_seats_rows(_graph_root(root))` + `_live_row`), calling
`rotate._finish_pending_swap_on_push(root, name, push)` for each. The helper is a strict
NO-OP unless `push:` starts `push: OK` AND a pending file exists whose pub_hex matches the
committed row, so looping every live row is safe and idempotent. MUST-NOT-CHANGE surface
(intact: commit message `keygen --all-live: keyed <listed>`, keyed_names' role in the
keyed-only staging, the prime gate, the walk, all quorum-card fixtures) untouched.

**Test (1) re-seeded to the REAL shape:** seat `a` is ALREADY KEYED (live session_id, HEAD
row names the successor pubkey) and OWNS `a.key.pending`; `keyed_names` handed to
`_commit_push_all_live` is only `["b"]` (the freshly-keyed seat) -- production never hands
`a`. Asserted the deferred swap still completes (pending file gone, `a.key` = successor
priv, dm VERIFIED). This test FAILS on pre-fix code and PASSES after.

**Test (2) added:** a live keyed seat with NO pending file is byte-identical before/after
the all-live push (helper NO-OP guard).

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_rotate.py -q -k pending_swap
5 passed, 223 deselected in 3.91s          # post-fix, incl. re-seeded (1) + new (2)

# pre-fix (loop reverted to keyed_names) -- test (1) fails:
>       assert not pend.exists()
E       AssertionError: assert not True
E        +  where True = exists()
E        +    where exists = PosixPath('.../test_keygen_all_live_push_comp0/sessions/seats/a.key.pending').exists
extensions/agi/tests/test_rotate.py:7142: AssertionError
Captured stderr call:
  push: OK -- master
  note: keygen --all-live: keyed b; push: OK -- master

# full scope, post-fix:
$ python3 -m pytest extensions/agi/tests/test_rotate.py extensions/agi/tests/test_send.py -q
516 passed in 52.49s
```

Falsifiers guarded: live keyed seat with matching pending completes (test 1); seat with no
pending untouched (test 2); unkeyed seat this pass keys remains keyed (unchanged keygen
paths; 516-suite green); commit message unchanged (`keygen --all-live: keyed b` in
stderr). The merge-push / before-minting quorum-card closure is ALREADY CLOSED by
hypothesis:l4-the-dry-run-stops-test-refreshes-its-card-after-the-fixture-commit
(test_rotate.py:2391 fixture refresh) -- out of scope here, recorded closed.

## Agent Notes
FIX-ONLY: _commit_push_all_live now finishes pending swap for EVERY live row (not just keyed_names); re-seeded test to real shape + added no-pending untouched test; 516 pass, pre-fix failure captured.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW by parent a00-72c899ca (SL7.44). Accepted, no demotion. Verified the ARTIFACT, not the report: send.py:745-774 now loops `for _row in _seats_rows(_graph_root(root))` with `_live_row(_row)` and calls rotate._finish_pending_swap_on_push per live row -- the walk's own row list, so the already-keyed seat that owns a `.key.pending` is now in the loop. The commit message/keyed_names surface is untouched (still `keygen --all-live: keyed {", ".join(keyed_names)}` at :679 and :694). Re-seeded test_rotate.py:7094 passes keyed_names=["b"] while seat `a` is already-keyed+live+pending -- the real shape production produces -- and asserts the swap completes; I re-ran `pytest test_rotate.py -q -k pending_swap` here: 5 passed. The pre-fix failure the kid captured is the right one (loop over keyed_names never reaches `a`). New test test_keygen_all_live_no_pending_never_touches_key guards the no-op direction. Near miss rejected: reading live names from `_shared_graph_root(root)` instead of `_graph_root(root)` would satisfy the words and diverge from the rows the walk actually keyed -- the kid used the walk's own reader, matching (1) and (2) together. Residual weak point, left as caveat not defect: the node cites itself as its only evidence_run; an independent re-run is the parent run above.
<!-- THOUGHT:END -->
