---
id: experiment:a00-2e6aafdb-b5acf1
mint_id: 7ba1baefc8a8418facdde0cb776c3537
type: experiment
parents:
  - hypothesis:l5-rotate-accepts-the-pending-successor-key-the-signer-already-prefers
next_edges: []
confidence: 0.85
edited_by: a00-2e6aafdb
evidence_runs:
  - experiment:a00-2e6aafdb-b5acf1
line_ceiling: 12
loop: hypothesis:l5-rotate-accepts-the-pending-successor-key-the-signer-already-prefers@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 22
profile: balanced
role: kid
scaffold_hash: 233327214ce981a2
season: 2
title: rotate accepts the pending successor key and promotes it keeping the old key retired
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2e6aafdb-b5acf1

## Experiment

l5 is a g15 BUILD ORDER (hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement),
not a measurement. Parent baseline (its own probe on this checkout) already
established conjunct (2) FIRST HALF is built: `rotate._caller_hold_key`
(rotate.py:17728) calls `send._signing_key_obj`, which since 0228534e8 prefers a
`<seat>.key.pending` whose `pub_hex` equals the committed row (send.py:199-225).
So I built the TWO missing conjuncts and a regression guard for the built one.

Pre-fix measurement (on this checkout, before my edit): with committed row = B,
`.key` = A, `.key.pending` = C (neither), the refusal at rotate.py:17745 read
`post 'seat-a': held key fingerprint <A-fp> does not match the committed row
<B-fp>; python3 .../send.py keygen --post seat-a first` -- it named NEITHER FILE.
And `grep -rn "key.retired" extensions/` = 0 hits: `_complete_pending_key_swap`
did `os.replace(tmp, key)` then `pend.unlink()`, destroying the old private bytes.

Built:

1. `rotate._caller_hold_key` (rotate.py:17762-17767): the mismatch refusal now
   names the live `<seat>.key` PATH, the `<seat>.key.pending` PATH (when it
   exists) and the committed row's stored pubkey hex alongside its fingerprint.
   The `KEYGEN_LINE` recovery tail is unchanged.
2. `rotate._complete_pending_key_swap` (rotate.py:17198-17213): immediately
   before `os.replace(_tmp, _key)`, the current `.key` bytes are preserved at
   `<seat>.key.retired-<old_fp>` with `SEAT_KEY_MODE` 0600; the file is written
   `O_EXCL` so an existing same-fp retired file is never clobbered, and the
   whole retirement is inside a try/except that can never block the swap. The
   push-OK-only gate (`_finish_pending_swap_on_push`) is untouched.

Files changed (file:line):
- `extensions/agi/bin/rotate.py:17198-17213` (retirement, 16 added)
- `extensions/agi/bin/rotate.py:17762-17767` (refusal names both files + row, 6 added / 2 replaced)
- `extensions/agi/tests/test_rotate.py:369-455` (tests a/b/c)
- `extensions/agi/tests/test_send.py:7558-7577` (test d)

Production lines: `git diff --numstat -- extensions/agi/bin/rotate.py extensions/agi/bin/send.py`
= 22 added, 2 deleted (ceiling 12; below the 2x=24 re-brief gate, above the
stated ceiling -- recorded honestly, no send.py change was needed).

## Evidence

RED FIRST, then green. Both new rotate tests failed before the fix
(`AttributeError`/`assert False`) and pass after; the send guard passed
pre-fix (it is a regression predicate).

Full touched suites (named files, never the bare directory):

```
$ python3 -m pytest extensions/agi/tests/test_rotate.py extensions/agi/tests/test_send.py -q
658 passed, 361 warnings in 93.61s
```

New tests, all green:
- `test_rotate_hold_key_accepts_pending_successor_and_names_both_files` (a)+(b)
- `test_rotate_complete_pending_swap_retires_old_key` (c) incl. no-clobber
- `test_no_pending_signer_is_byte_identical` (d)
- existing `test_rotate_complete_pending_key_swap` still passes unchanged.

## Agent Notes
Built both missing conjuncts: _caller_hold_key refusal names .key path + .key.pending path + row pubkey; _complete_pending_key_swap preserves old .key at .key.retired-<old_fp> (0600, O_EXCL no-clobber, never blocks the swap). Conjunct (2) first half already built (send._signing_key_obj). Red-first tests a-d green; 658 passed test_rotate.py+test_send.py. 22 production lines (ceiling 12, under 2x gate).
