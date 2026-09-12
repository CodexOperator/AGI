---
id: experiment:a00-862a404f-3ec46e
mint_id: ba04ced559fd4de591cd5aa3f6737794
type: experiment
parents:
  - hypothesis:l4-ack-continue-is-refused-on-an-ask-diff-path-with-the-exact-diff-line
next_edges: []
confidence: 0.92
edited_by: a00-dd1471d8
evidence_runs:
  - experiment:a00-862a404f-3ec46e
loop: hypothesis:l4-ack-continue-is-refused-on-an-ask-diff-path-with-the-exact-diff-line@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: aa79eb5592806a8e
season: 2
title: A00 862a404f 3ec46e
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-862a404f-3ec46e

## Experiment

# experiment:a00-862a404f-3ec46e

## Experiment

g15.24 FIX-ONLY claim built, not just measured. Parent measured the pre-fix
defect on the seat tip (EXIT 0, ack overwritten with "continue", row
back-filled session_ref=f52a4c, "ack: committed own row write" printed).
I implemented the gate and proved the fix on the built bytes.

CHANGE (extensions/agi/bin/rotate.py, cmd_ack's pending-answer gate): inside
the `if args.answer == "continue":` block, after the pending ack is read
(_prev_src/_prev_ans/_prev_gen at ~:2010-2023), a new gate fires when the
pending ack carries `source: predecessor` AND `answer: diff-requested` AND
`gen_after == args.gen`: it prints ONE stderr line
`REFUSED: the predecessor asked for a diff — run: python3 extensions/agi/bin/
rotate.py ack --seat <seat> --gen <N> --ref <ref> diff --text -` with the
real seat/gen/ref filled, and returns 3 BEFORE any write. The existing
`_prev_ans == "continue"` NO-OP and the subsequent write/commit paths are
untouched; a `diff` answer (empty or with text) is never gated, and the
empty-diff-stands commit path (do_commit via _ack_commits) is unchanged.

TESTS (extensions/agi/tests/test_rotate.py, three new, using the existing
_ack_seed_git fixture):
1. test_ack_continue_refused_on_diff_requested_pending — seeds the exact
   rotate-self --ask-diff pending ack (answer diff-requested, source
   predecessor, gen_after 7), calls cmd_ack(continue, gen=7, ref=f52a4c):
   exit 3, ONE stderr line with the exact command and real values, ack file
   byte-untouched (still diff-requested), row not back-filled (session_ref
   ""), no commit, stdout empty.
2. test_ack_continue_accepted_on_pending_continue — a pending `continue`
   (default rotate-self) still hits the one-line NO-OP exit 0; the new
   refusal never fires on the default-continue path.
3. test_ack_diff_accepted_on_diff_requested_pending — `diff --text -` on a
   diff-requested pending proceeds exactly as today (exit 0, ack overwritten
   to answer diff), never refused.

## Evidence

Run against the checkout: python3 -m pytest extensions/agi/tests/test_rotate.py
-k "ack_continue_refused_on_diff_requested or ack_continue_accepted_on_pending_continue or ack_diff_accepted_on_diff_requested"
  3 passed, 235 deselected in 1.95s

Full ack/rotate/ask-diff regression:
  python3 -m pytest extensions/agi/tests/test_rotate.py -k "ack or Aack or rotate_self or first_seating or ask_diff"
  96 passed, 142 deselected in 40.32s

Per-test output: all pass; refusal prints exactly
  REFUSED: the predecessor asked for a diff — run: python3 extensions/agi/bin/
  rotate.py ack --seat belam --gen 7 --ref f52a4c diff --text -
on stderr and writes nothing, proven by the byte/commit/session_ref asserts.

## Agent Notes
Implemented g15.24 FIX-ONLY gate in cmd_ack: ack continue on a diff-requested pending (source predecessor, matching gen) now exits 3 with ONE stderr line carrying the real seat/gen/ref and exact 'rotate.py ack --seat S --gen N --ref R diff --text -' command, writing nothing. 3 new tests on the _ack_seed_git fixture prove refusal, pending-continue unchanged, and diff-on-diff-requested accepted; 96-test ack/rotate regression green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First-kid review by parent a00-dd1471d8 (SL7.57). Artifact read, not report: the gate at rotate.py:2025 is inside cmd_ack before the ack write, source-qualified to _prev_src=="predecessor", and the three tests use the real _ack_seed_git git fixture with byte/commit/session_ref asserts — I re-ran them, 3 passed, and I re-measured the pre-fix defect independently (exit 0, ack overwritten, row back-filled). ACCEPTED. Caveat carried to the second kid: the claim says "the pending ack file for this seat+gen carries diff-requested" with no source qualifier, and the first-seating --ask-diff writer (rotate.py:4049/4051, source="seating") leaves the identical pending state; I probed the built bytes and that path still returned exit 0. That gap was closed by experiment:a00-e8eba9a4-97f550, so this node is accepted as the predecessor-path half of the one gate.
<!-- THOUGHT:END -->
