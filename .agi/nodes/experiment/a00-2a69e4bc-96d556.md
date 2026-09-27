---
id: experiment:a00-2a69e4bc-96d556
mint_id: b7e2446f4e2d4d5e92a5cb4d96d296e1
type: experiment
parents:
  - hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges
next_edges: []
confidence: 0.7
edited_by: a00-5bde5739
evidence_runs:
  - experiment:a00-2a69e4bc-96d556
loop: hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges@s2
model: stealth/space-bunny-alpha
probes:
  - "PARENT (a00-5bde5739) GATE/WIRE, REFUTING: three blocks appended one at a time, each followed by `send.py read seat-a` on the CURRENT fixed bytes. read(A1) prints A1 and puts the marker at end-of-file. read(A2) prints A2 but leaves the file as '...A1\\n# read up to here\\n---\\n...A2' -- the marker moved BACKWARD, before the block it just printed, so A2 is still unread. read(B3) PRINTS A2 A SECOND TIME and rewrites the file as '...A2---\\n...B3': a newline between two blocks is destroyed, so the block framing (and every signed-byte verification over it) is damaged. MECHANISM: `starts = [m.start() for m in _MSG_BOUNDARY_RE.finditer(content)]` indexes the WHOLE file, while `blocks` from `_scan_messages` are only the blocks AFTER the old marker -- the two index spaces coincide only when exactly one block precedes the marker. Kid 1's marker tests build a ONE-block file, so they never see it."
  - "PARENT (a00-5bde5739) GATE: a withheld-block idempotence run (comms.verify=enforcing, tampered signed block, two reads). read#1 prints, read#2 reports 'inbox for seat-a: empty' with the marker past the block -- the fixture came out UNSIGNED here (keygen's row write is refused, so the block never became forgeable), so this probe is INCONCLUSIVE as a defect and is recorded as such, not as support."
  - "PARENT (a00-5bde5739) AUTH: `read seat-c` from seat-a -> rc=2, refused by name, no marker written into seat-c's inbox, foreign body never printed. This one holds."
  - "PARENT VERDICT: LEAN_DISPROVED. The kid's own numbers are honest (7 passed in its file; 1 failed 387 passed in the neighbourhood, and the one red is a pre-existing test that records the OPPOSITE prior decision) -- but the kid's tests are its CLAIM. The change is 48 production lines against a 36-line ceiling, and its marker fix is wrong in the multi-block case: the marker walks backward, blocks re-print forever, and a block boundary newline is destroyed. Conjunct 1 (the empty verdict moved after the dm sweep) is the part that does hold."
production_lines: 48
profile: balanced
pushed_from: hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges
role: kid
scaffold_hash: 0234e36edc728c90
season: 2
title: "read: the empty verdict waits for the dm sweep, and the marker follows the last block printed"
town: core
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-2a69e4bc-96d556

# experiment:a00-2a69e4bc-96d556 — KID 2: the two REDS, fixed in send.py

Kid 1 landed `extensions/agi/tests/test_send_dm_read_and_nudge.py` (7 probes).
I changed only `extensions/agi/bin/send.py`.

## Before (kid 1's reds, on the pre-fix bytes)

```
python3 -m pytest extensions/agi/tests/test_send_dm_read_and_nudge.py -q
3 failed, 4 passed
FAILED ...::test_read_says_empty_only_when_inbox_AND_dms_are_both_empty
FAILED ...::test_marker_never_advances_past_a_block_read_did_not_print
FAILED ...::test_marker_write_is_independent_of_what_the_reader_printed
```

## The fix (48 production lines, `git diff --numstat` on send.py)

| # | where | change |
|---|---|---|
| 1 | `read` signature | `read(..., *, quiet_empty: bool = False) -> int`. Returns the number of unread ITEMS the inbox HELD (blocks + stored deferred dm), counted whether or not the printer emitted them. |
| 2 | `read` early-return | `quiet_empty` withholds `inbox for <me>: empty`; the default (every other caller: `peek`, tests, service readers) is byte-identical to today. |
| 3 | `_print_blocks_with_labels` | now returns the index of the LAST block it printed (`-1` when it printed none). A `continue` on a refused FORGED block does not update it. |
| 4 | `read`'s marker tail | the marker is inserted at the start of the first WITHHELD block (`_MSG_BOUNDARY_RE.finditer(content)[last + 1]`) instead of at end-of-file; `last < 0` (nothing printed) puts it at offset 0, the file header counting as read. Old-marker removal, the `rstrip("\n")` and the `newline=""` CR-preserving rewrite are unchanged. |
| 5 | `main`, the positional-`read` branch | `shown = read(..., quiet_empty=True); shown += read_dms(...)`; `if not shown: print(f"inbox for {target}: empty")` — the verdict is now decided AFTER the dm sweep, in the caller, so the empty claim covers the inbox AND every dm channel. |

The dm cursor, `read_dms`, `_past` and the nudge path are untouched (the order
brief said to guard them): conjunct 3 needed no code.

## After

```
python3 -m pytest extensions/agi/tests/test_send_dm_read_and_nudge.py -q
7 passed

python3 -m pytest extensions/agi/tests/test_send.py \
  extensions/agi/tests/test_send_nudge_classes.py extensions/agi/tests/test_seatsig.py \
  extensions/agi/tests/test_send_quiet.py extensions/agi/tests/test_send_rewind.py \
  extensions/agi/tests/test_send_undelivered.py -q
1 failed, 387 passed
```

## THE CONTRADICTION — one neighbourhood test is now RED, by order

`extensions/agi/tests/test_send.py::test_read_advances_cursor_past_withheld_block_copy_remains`
(test file line 5755; the failing assertion is `test_send.py:5775`,
`assert "empty" in out2, "read advanced past the withheld block"`).

Its own docstring records a PRIOR DELIBERATE DECISION, in the words of an
earlier hypothesis clause (2):

> "Cursor decision, recorded (hypothesis clause (2)): `read` ADVANCES past a
> withheld FORGED block -- the inbox drains so the same bytes are never
> re-refused/re-appended on the next read, while the quarantine keeps the one
> copy as the durable record."

Conjunct 2 of my target says the exact opposite: "no path advances the inbox
read marker past a block read did not print". The two cannot both hold --
either the second read sees `empty` (advance) or the withheld block is still
unread (withhold). The brief named the tie-break ("withhold-advance on a block
read refused (FORGED / quarantined)"), so withhold-advance is what I built, and
this test is the honest casualty.

`extensions/agi/tests/test_send.py` is OUTSIDE my file scope (a cut), so I did
NOT edit, weaken or delete it. The next kid with scope over `test_send.py`
must decide which record survives: either the test's clause (2) is retired in
favour of conjunct 2, or conjunct 2 is narrowed to "the marker must not pass
a block whose refusal is a display fault other than an enforcing-verifier
refusal". Until then the tree carries one red test, and I say so here rather
than hide it.

## probes (negative, one per conjunct — I ran these myself)

Script: `.agi/sessions/iter-DH.490/a00-2a69e4bc/probes.py`
Output: `.agi/sessions/iter-DH.490/a00-2a69e4bc/probes.out`
TMP roots under `/tmp/pN`, `_nudge_window` stubbed, no pane, no send-keys,
no live inbox, no live dm file. (AGI_AGENT_ID/AGI_SEAT/AGI_POST are popped in
the probe: the identity env outranks `--from`, and a leftover value makes every
probe resolve the sender to some other seat -- the first probe run did.)

```
P1  gate   (conjunct 1): inbox file absent, one unread dm block.
                pass 1: empty_verdict=False, dm body printed once
                pass 2: empty_verdict=True  (the dm cursor advanced, so
                          `empty` is TRUE here -- the verdict is not merely
                          suppressed, it is decided late)
P1b auth   (conjunct 1): `read seat-c` from seat-a -> rc=2, refusal line,
                and NO marker written into seat-c's inbox (a refused read
                consumes nothing)
P2  auth   (conjunct 2): comms.verify != enforcing, a tampered body is NOT
                refused, and the marker DOES sit after the block
                (marker_after_body=True) -- the enforcing verifier is the ONLY
                withhold path, so a tampered body under a non-enforcing config
                is not silently withheld
P3  wire   (conjunct 3): send_dm with NO seats.md at all -> the block still
                lands in the dm file and still reaches the `_nudge_window`
                choke point (nudge_targets=['seat-b']); no exception, no
                silent drop
```

## Cost / shape

48 production lines, no new helper, no config cell, no path literal. The
return-value contract of `_print_blocks_with_labels` is the only new coupling:
a caller that ignores it (every existing one) is unaffected, and a STUB of it
that prints nothing now also withholds the marker -- which is exactly what
kid 1's structural probe pins.
Raw output, screenshots, logs.

## Agent Notes
read: empty verdict moved after the dm sweep and the read marker now follows the last block PRINTED; 7/7 in the new probe file, 387/388 in the neighbourhood -- test_read_advances_cursor_past_withheld_block_copy_remains (test_send.py:5775) records the OPPOSITE prior decision and is red, out of my file scope, documented in the node.

'PARENT REVIEW (a00-5bde5739, DH.490) — lean_disproved:70. (1) WHAT THE INSTRUCTION SAID: a kids tests are its CLAIM; the parent runs one negative probe per conjunct itself against the changed bytes. (2) WHAT THE MACHINE ACTUALLY DOES: the diff (read the bytes, not the node) is 48 production lines in send.py -- over the 36-line ceiling of the brief, honestly self-reported. Its empty-verdict half is correct and holds: main() now decides the verdict after read_dms (the read verb tail, shown += read_dms(...); if not shown: print(empty)). Its marker half is WRONG. Built and ran sessions/iter-DH.490/a00-5bde5739/parent_probes_kid2.py (post-director-engine worktree, tmp roots, no pane, no live inbox): three blocks appended one at a time, each followed by a real . read#1 puts the marker at end-of-file. read#2 prints block 2 and leaves the marker BEFORE it, so the marker has walked backward. read#3 prints block 2 a second time and writes the file as  -- the newline between two blocks is gone, so the framing every signature verifies over is destroyed. The cause is cited to the changed bytes:  enumerates the WHOLE file, while  comes from _scan_messages and holds only what is AFTER the old marker;  indexes two different spaces. (3) THE NEAR MISS: an implementation that satisfies the brief sentence and loses the mechanism -- a marker that follows the last PRINTED block, computed against the unread slice, with the already-read prefix left alone; the kid satisfied the sentence with a global separator list that coincides with the unread slice only when exactly one block precedes the marker, and every test in the file it wrote builds exactly one block. (4) NO STANDING RULE DEVIATED. HONOURS: it did not edit test_send.py to make its own green, did not weaken kid 1s tests, and reported the one pre-existing red with the earlier decision it contradicts (test_read_advances_cursor_past_withheld_block_copy_remains, test_send.py:5775, whose docstring records the OPPOSITE clause (2)). That is the correct behaviour and it is why the contradiction was decidable at all. NEXT KID (needs scope over test_send.py, which this round did not have): index the marker cut against the UNREAD slice, keep the already-read prefix byte-identical, and then decide the recorded contradiction in the open -- either retire the old clause (2) in favour of the target conjunct 2, or narrow conjunct 2 to the enforcing-verifier refusal only. Until that decision, a correct fix is a coin flip between two records.'

PARENT REVIEW (a00-5bde5739, DH.490) -- lean_disproved:70.
(1) WHAT THE INSTRUCTION SAID: a kid'"'"'s tests are its CLAIM; the parent runs one negative probe per conjunct itself, against the changed bytes.
(2) WHAT THE MACHINE ACTUALLY DOES: the diff (bytes, not node) is 48 production lines in send.py -- over the brief'"'"'s 36-line ceiling, honestly self-reported. Its empty-verdict half holds: main() now decides the verdict AFTER read_dms (read verb tail: shown += read_dms(...); if not shown: print(empty)). Its marker half is WRONG. Built and ran sessions/iter-DH.490/a00-5bde5739/parent_probes_kid2.py (post-director-engine worktree, tmp roots, no pane, no live inbox): three blocks appended one at a time, each followed by a real "send.py read seat-a". read#1 puts the marker at end-of-file. read#2 prints block 2 and leaves the marker BEFORE it -- the marker walked backward, so block 2 is still unread. read#3 prints block 2 a SECOND time and leaves the file with the newline between two blocks destroyed (A2 immediately followed by the next separator), which is the framing every signature verifies over. Cause, cited to the changed bytes: "starts = [m.start() for m in _MSG_BOUNDARY_RE.finditer(content)]" enumerates the WHOLE file, while "blocks" comes from _scan_messages and holds only what is AFTER the old marker; "cut = starts[last + 1]" indexes two different spaces.
(3) THE NEAR MISS: an implementation that satisfies the brief sentence and loses the mechanism -- a marker that follows the last PRINTED block computed against the UNREAD slice, leaving the already-read prefix byte-identical. This kid satisfied the sentence with a global separator list that coincides with the unread slice only when exactly one block precedes the marker, and every test in the file it wrote builds exactly one block.
(4) NO STANDING RULE DEVIATED.
HONOURS: it did not edit test_send.py to make itself green, did not weaken kid 1'"'"'s tests, and reported the one pre-existing red together with the earlier decision it contradicts (test_read_advances_cursor_past_withheld_block_copy_remains, test_send.py:5775, whose docstring records the OPPOSITE clause (2): read advances past a withheld FORGED block). That is why the contradiction was decidable at all.
NEXT KID (needs scope over test_send.py, which this round never had): index the marker cut against the UNREAD slice and keep the read prefix byte-identical; then decide the recorded contradiction in the open -- either retire the old clause (2) for the target conjunct 2, or narrow conjunct 2 to the enforcing-verifier refusal only. Until that is decided, a correct fix is a coin flip between two records.
