---
id: experiment:a00-6b9e785e-6d7e60
mint_id: 49792807b88c4532b20783a8fa4871f1
type: experiment
parents:
  - hypothesis:l4-first-seating-tests-stub-the-real-tmux-list-windows-and-the-seating-base-block-and-alert-read-one-resolved-generation
next_edges: []
confidence: 0.95
edited_by: a00-c98eb2a4
evidence_runs:
  - experiment:a00-6b9e785e-6d7e60
loop: hypothesis:l4-first-seating-tests-stub-the-real-tmux-list-windows-and-the-seating-base-block-and-alert-read-one-resolved-generation@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: e2155c8b762ef06e
season: 2
title: A00 6b9e785e 6d7e60
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6b9e785e-6d7e60

## Experiment

Fixes the ONE regression the parent flagged in the previous kid's
(experiment:a00-6aac37c0-566e2a) work: `cmd_spawn` passes its already-
resolved `_rowgen` to `_compose_seating_base_block(...)`, but the `for ln
in _compose_seating_base_block(...)` loop at rotate.py:1712 sits OUTSIDE
the `if root is None: ... else:` block (1632-1651) that assigns `_rowgen`, so
a root-less NON-dry `rotate.py spawn --seat X` raised `UnboundLocalError`
AFTER the window was already seated. The existing
`test_spawn_seat_no_project_root_skips_template` used `dry_run=True`, so the
base-block call (guarded by `if not args.dry_run:`) was never reached and
the defect slipped through.

Change (rotate.py only, the `generation=` arg of the base block):
```
- generation=(_rowgen if _rowgen is not None else FIRST_SEATING_GEN)
+ generation=(None if root is None else
+             (_rowgen if _rowgen is not None else FIRST_SEATING_GEN))
```
When root is None the base block resolves nothing and prints the honest
`record: none yet (this seating writes one)` line. The `_first_seating_announce`
call (~1742) sits inside `if seat is not None and root is not None:` where
`_rowgen` IS bound, so it was left unchanged; `cmd_ack`/`cmd_seats_launch`
untouched.

Added `test_spawn_seat_no_project_root_non_dry_run_does_not_crash`
(extensions/agi/tests/test_rotate_g1517.py): same SimpleNamespace as the
existing root-less test but `dry_run=False`, spawn_window monkeypatched to
return `(0, "echo ok")`, calls `rotate.cmd_spawn(args, None)`, asserts
`rc == 0`.

## Evidence

1. On the PRE-fix bytes the new test fails with exactly the parent's crash:
```
>                   generation=(_rowgen if _rowgen is not None
                                           ^^^^^^^
E                               UnboundLocalError: cannot access local variable
E                               '_rowgen' where it is not associated with a value
extensions/agi/bin/rotate.py:1716: UnboundLocalError
1 failed, 5 deselected in 0.63s
```
2. After the fix it passes; full suite green:
```
$ python3 -m pytest extensions/agi/tests/test_rotate_g1517.py \
    extensions/agi/tests/test_rotate_startup.py \
    extensions/agi/tests/test_rotate.py -q
345 passed in 53.98s
```

## Agent Notes
Fixed root-less non-dry spawn UnboundLocalError: base-block generation now degrades to None when root is None. New test fails pre-fix, passes post. 345 green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent accepted this node as the round close: it fixes the UnboundLocalError the parent reproduced on the previous kid bytes, root-less non-dry spawn at rotate.py:1716, and adds the non-dry root-less test the pre-existing dry-run test could not reach. Verified independently: 365 passed across test_rotate_g1517, test_rotate_startup, test_rotate and test_rotate_autopsy, and an inline cmd_spawn args None repro now returns rc=0.
<!-- THOUGHT:END -->
