# KID BRIEF — SL7.44, parent a00-72c899ca

TARGET NODE: hypothesis:l4-keygen-all-live-completes-a-deferred-pending-swap-for-every-live-row-not-only-the-rows-it-keyed
PARENT: hypothesis:l4-keygen-all-live-completes-a-deferred-pending-swap-for-every-live-row-not-only-the-rows-it-keyed is itself the target (extend it).

## THIS IS A FIX-ONLY BUILD ORDER, NOT A MEASUREMENT

goal:g15 claims are BEHAVIOUR TO BUILD. Do NOT just reproduce the defect and
report `disproved`. You must IMPLEMENT the fix in the source, add the tests,
run them, and report. A node that only re-measures the bug is an unfinished
round and will be re-cut.

## WHAT THE TARGET NODE CLAIMS (read it in full before starting)

`extensions/agi/bin/send.py` `keygen --all-live` mints keys for every live row
it can, collects the newly-keyed names in `keyed_names`, and after its ONE
commit+push calls `rotate._finish_pending_swap_on_push(root, seat, push)` for
each name in `keyed_names` (send.py ~:761-762).

THE DEFECT, measured on this base (verify line numbers yourself, they drift):
- send.py:496-502 — the `--all-live` walk does `if row.get("pubkey"): print
  "skipped ..."; continue` BEFORE it can reach `keyed_names.append(name)` at
  ~:517. So a row that ALREADY carries a pubkey is never in `keyed_names`.
- rotate.py:10754 `_persist_pending_key` writes `<seat>.key.pending` ONLY for a
  seat whose COMMITTED row already names the successor pubkey — i.e. an
  ALREADY-KEYED seat. Such a seat is skipped by the walk.
- Therefore no seat can be in `keyed_names` AND own a `.key.pending`: the
  completion site inside `_commit_push_all_live` is unreachable by construction.
- extensions/agi/tests/test_rotate.py:7094
  `test_keygen_all_live_push_completes_pending_swap` currently passes ONLY
  because it calls `bin_send._commit_push_all_live(tmp_path, ["a", "b"])`
  directly with a hand-written list production never produces (seat `a` is
  already keyed in the sheet). Re-seed it to the real shape.

## THE FIX (do exactly this, no redesign)

In `_commit_push_all_live` (send.py:668), replace the `for _seat in keyed_names:`
completion loop with one that calls `rotate._finish_pending_swap_on_push(root,
seat, push)` for EVERY LIVE ROW, not only the rows this pass keyed. Compute the
live-row names from the same node read the walk uses — `_seats_rows(graph)` +
`_live_row(row)` (send.py:351) — or take the live names as a new parameter from
the caller; either is fine. The helper is a NO-OP unless `push:` starts with
`push: OK` AND a pending file exists whose `pub_hex` matches the committed row,
so looping every live row is safe and idempotent.

MUST NOT CHANGE:
- the commit message (`keygen --all-live: keyed <listed>`) and `keyed_names`'s
  use for `_all_live_seats_content` / the keyed-rows staging;
- `rotate._finish_pending_swap_on_push`, `rotate._persist_pending_key`, the
  prime gate at send.py:464-490, the walk at send.py:496-517, any quorum-card
  fixture.

FALSIFIERS to guard (the node's own list): a live keyed seat with a matching
`.pending` still holds the pending file after keygen --all-live pushes; a seat
with NO pending file has its `.key` touched; an unkeyed seat this pass keys is
no longer keyed; the commit message changes.

## TESTS (test-first where you can)

FILE SCOPE: `extensions/agi/bin/send.py` (the `_commit_push_all_live`
completion loop + the live-row list it needs); `extensions/agi/tests/test_rotate.py`;
`extensions/agi/tests/test_send.py`. Nothing else.

1. Re-seed `test_keygen_all_live_push_completes_pending_swap` (test_rotate.py:7094)
   to the REAL SHAPE: the pending seat is ALREADY KEYED in HEAD's row and is
   skipped by the walk, so the `keyed_names` passed to `_commit_push_all_live`
   must NOT include it (e.g. pass only the other, freshly-keyed seat) — and the
   swap must still complete. This test must FAIL on the pre-fix code and PASS
   after.
2. ONE new test: a live keyed seat with NO `.key.pending` is UNTOUCHED by the
   all-live push (its `.key` bytes are identical before/after).
3. `test_send.py` keygen tests stay unchanged and green.

## RUN

```
cd /home/ubuntu/work/agi/.agi/worktrees/a00-72c899ca
python3 -m pytest extensions/agi/tests/test_rotate.py -q -k pending_swap
python3 -m pytest extensions/agi/tests/test_rotate.py extensions/agi/tests/test_send.py -q
```
Record the exact pre-fix failure of test (1) and the post-fix pass — that is
your evidence. Put the run in the experiment node body.

## DELIVERABLE

Spawn/leave: the fix in the source, the two tests, and an
`experiment:` node recording what you ran and the result, parented to
`hypothesis:l4-keygen-all-live-completes-a-deferred-pending-swap-for-every-live-row-not-only-the-rows-it-keyed`.
Report DONE with the node id, verdict, and cite the experiment node in
`--evidence-runs`. Do NOT commit, push, or run git. `cli.py done` owns all
versioning.
