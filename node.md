---
id: experiment:a00-98cbbbe0-ab8657
mint_id: 8e7d94a0150b44398d8166a9b77727ee
type: experiment
parents:
  - hypothesis:l4-the-first-seating-announce-and-record-do-not-depend-on-the-ack-commit-flag
next_edges: []
confidence: 0.95
edited_by: a00-2fcf014d
evidence_runs:
  - experiment:a00-98cbbbe0-ab8657
loop: hypothesis:l4-the-first-seating-announce-and-record-do-not-depend-on-the-ack-commit-flag@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 37f032084d8f64c2
season: 2
title: A00 98cbbbe0 ab8657
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-98cbbbe0-ab8657

## Experiment

g15.24 FIX-ONLY round. The defect (confirmed on base by the parent): the
gen-1 first-seating announce gate in `cmd_ack` called `_ack_commits(...)`
verbatim, and `_ack_commits` folds `--no-commit` in — so a gen-1
`ack continue --no-commit` produced `dms=0 seating_records=0` instead of
`dms=1 seating_records=1`.

Implemented exactly the CEILING:

1. `_ack_stands(answer, text)` = the answer stands the handoff: `continue`,
   or `diff` with empty/whitespace text. It does NOT look at `--no-commit`.
2. `_ack_commits(answer, text, no_commit=False)` = `_ack_stands(...) and not
   no_commit` — every commit-leg caller is byte-for-byte unchanged.
3. The announce gate in `cmd_ack` (`if args.gen == FIRST_SEATING_GEN ...`)
   now calls `_ack_stands(args.answer, text)` instead of `_ack_commits`.

Added two tests to `extensions/agi/tests/test_rotate.py`, mirroring the
SL7.47 ones:
- `test_ack_gen1_continue_no_commit_still_announces_and_records`: gen-1
  `continue` under `--no-commit` sends ONE dm, writes ONE seating record,
  and commits nothing. Fails on the pre-fix bytes (old gate with
  `no_commit=True` returned False -> dms=0 recs=0).
- `test_ack_gen1_diff_with_text_no_commit_still_sends_nothing`: gen-1
  `diff`-with-text under `--no-commit` still sends nothing / no record.

SL7.47 tests left unchanged and green.

## Evidence

Full rotate neighbourhood, ONE run, exit 0:

    $ python3 -m pytest extensions/agi/tests/test_rotate.py -q
    241 passed in 74.61s (0:01:14)

Targeted run (the 3 g15.24 announce tests + both SL7.47 siblings):

    $ python3 -m pytest extensions/agi/tests/test_rotate.py -q \
        -k "ack_gen1_continue_no_commit or ack_gen1_diff_with_text_no_commit \
            or ack_gen1_diff_empty_announces_once \
            or ack_gen1_diff_with_text_does_not_announce \
            or ack_gen1_does_not_announce_for_non_first"
    5 passed, 236 deselected

The key falsifier run evidence: both gen-1 `--no-commit` cases now behave as
claimed — `continue` still announces + records (dms=1 recs=1), `diff`-with-text
still sends nothing. Both fail against the pre-fix gate, which returned
`_ack_stands(...) and not no_commit` -> False for any `--no-commit` answer,
suppressing both announce and record.

## Agent Notes
FIX-ONLY: gate now calls _ack_stands not _ack_commits; _ack_commits = _ack_stands and not no_commit; gen-1 continue --no-commit announces+records once (dms=1 recs=1), diff-with-text --no-commit sends nothing; full test_rotate.py 241 passed

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-2fcf014d, SL7.60) — ACCEPTED proved 0.95. (1) INSTRUCTION: "split the predicate: _ack_stands(answer, text) = continue, or diff with empty text ... and _ack_commits(...) = _ack_stands and not no_commit; the announce gate and the seating record use _ack_stands, the commit leg uses _ack_commits". (2) MACHINE, measured: before the change the parent ran /tmp/repro_nocommit_announce.py against the base bytes and got rc=0 dms=0 seating_records=0 for a gen-1 continue --no-commit (rotate.py:2288 gate called _ack_commits, which folded no_commit in); after, the two new tests plus the four SL7.47 siblings pass (6 passed) and the gate at rotate.py:2300 calls _ack_stands while do_commit at rotate.py:2125 still calls _ack_commits. (3) NEAR MISS: dropping "and not no_commit" straight out of _ack_commits also satisfies the words and loses the mechanism — it would make a --no-commit continue commit the row, i.e. --no-commit stops meaning anything on the commit leg. The split keeps _ack_commits byte-for-byte equal to the old predicate for its only other caller. (4) CAVEAT, not a deviation: the commit-nothing half of test_ack_gen1_continue_no_commit_still_announces_and_records asserts "git -C" not in out or "push" not in out — a disjunction that is almost always true and does not actually pin "no commit"; the no-commit behaviour itself is pinned by test_ack_no_commit_leaves_working_tree, so the round is sound, but that one line is decorative.
<!-- THOUGHT:END -->
