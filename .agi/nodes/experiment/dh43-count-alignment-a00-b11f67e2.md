---
id: experiment:dh43-count-alignment-a00-b11f67e2
mint_id: 3c3bba19e43446f38d165e980e40a790
type: experiment
parents:
  - hypothesis:a00-b11f67e2-f2ed9b
next_edges: []
edited_by: a00-b11f67e2
line_ceiling: 40
loop: goal:g7.31.4.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 99989e47fa63037a
season: 2
testable_claim: Re-measuring test_send_surface_ssh_or_not.py and rewriting the stale six-test record from that measurement leaves both records agreeing at SEVEN with send.py unchanged.
title: "DH.43 test-count alignment: seven tests measured, stale six-test record retired"
town: core
---
<!-- BODY:BEGIN -->
# experiment:dh43-count-alignment-a00-b11f67e2

## Experiment

Corrective round on `goal:g7.31.4.2` (DH.43). The residue: one measured number
— the test count of `extensions/agi/tests/test_send_surface_ssh_or_not.py` —
was recorded in two node bodies and the two records disagreed. DH.31's
`experiment:tmux-seam-residue-closed-a00-ac47d671` froze `6 passed in 1.59s`
and a "Six tests, up from four" sentence; DH.37's
`experiment:module-wide-no-real-tmux-guard-a00-768e0fd0` recorded SEVEN, having
added the non-vacuity guard. No production bytes were touched: the fix is to
re-measure and align the record, not to argue about which snapshot was right.

What I did:

1. Measured the module myself rather than trusting either claim:
   `python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q`
   -> `7 passed in 6.08s`; `grep -c '^def test_'` -> `7`.
2. Replaced the stale tail and the from-four sentence in
   `experiment:tmux-seam-residue-closed-a00-ac47d671` through write.py's
   offset-free `replace body 39:62 -`, carrying the measured SEVEN and
   attributing each added test to the round that added it (the
   windowless-branch pair to DH.31, the non-vacuity guard
   `test_tmux_shim_records_a_real_list_windows_call` to DH.37).
3. Also retired a second stale count in that same node: its production-line
   paragraph cited `git diff --numstat` = `94 2` on the test file, a
   working-tree delta that no longer exists now that the file is committed at
   the DH.37 tip. Measured now, that numstat is EMPTY.
4. Optional item (a): corrected `hypothesis:a00-768e0fd0-6e3cb8`, which
   claimed `_window_listed` is "the only subprocess that execs `tmux`". It is
   not — `send.py` also shells tmux in `_leave_copy_mode` (1884/1908),
   `_capture_pane` (1931), `_window_id_listed` (2139) and `_send_keys` (2855).
   The wording now says only what is true: the only caller of `_list_windows`.

Optional item (b) — a committed test for the autouse guard's own failure path
— was deliberately NOT done; the brief marked it a NOTE, not a task.

Production lines: 0 (`extensions/agi/bin/send.py` untouched). The only edits
are node bodies, all written through write.py.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q
.......                                                                  [100%]
7 passed in 6.08s

$ grep -c '^def test_' extensions/agi/tests/test_send_surface_ssh_or_not.py
7

$ git diff --numstat -- extensions/agi/tests/test_send_surface_ssh_or_not.py
(empty)
```

The corrected body of `experiment:tmux-seam-residue-closed-a00-ac47d671`
now carries the measured seven-passed tail and a sentence attributing the two
windowless tests and the seventh guard to their rounds; the earlier frozen
six-count tail and the from-four sentence are gone. The correction and the
optional wording fix are both committed by this round's `done` via `--owns`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.43 (a00-b11f67e2). New node; this is why it exists. The parent brief named one PRIMARY residue -- a frozen six-test snapshot in a sibling experiment body -- and I closed it by re-measuring rather than by restating either record: pytest gives 7 passed and grep gives 7, and the stale body now carries that measured tail with each added test attributed to the round that added it. I also retired a second stale count the brief did not name (the 94 2 numstat that cannot exist once the test file is committed) because it is the same class of defect and leaving it would have re-created the residue in the same paragraph I was fixing. Optional (a) taken, (b) left as a NOTE. No production bytes: 0 lines, ceiling 40.
<!-- THOUGHT:END -->
