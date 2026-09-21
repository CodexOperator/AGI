---
id: experiment:a00-b4b29be8-8a2942
mint_id: 69c906eb35fa44d1a625922709694387
type: experiment
parents:
  - hypothesis:l4-the-ask-diff-gate-offers-no-continue-and-an-empty-diff-stands-the-handoff
next_edges: []
confidence: 0.9
edited_by: a00-ebefd47a
evidence_runs:
  - experiment:a00-b4b29be8-8a2942
loop: hypothesis:l4-the-ask-diff-gate-offers-no-continue-and-an-empty-diff-stands-the-handoff@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 15a35dbcafb63166
season: 2
title: the --ask-diff gate names only the diff call and an empty-diff text stands the handoff
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b4b29be8-8a2942

## Experiment

BUILD-ORDER round on the g15 claim (hypothesis:l4-the-ask-diff-gate-offers-no-
continue-and-an-empty-diff-stands-the-handoff) — measure pre-fix, implement, prove
on built bytes. Scope: `extensions/agi/bin/rotate.py` `cmd_rotate_self` ask_gate
string + its read-back `diff` branch, `cmd_rotate_next`/`cmd_loop` read-back `diff`
branch, `_rotate_self_record` (a `reply_decision` field), plus one test per read-
back. Out of scope per claim: cmd_ack, `_rotate_ack_file`, pre-spawn region,
cmd_spawn, whois, send.py.

PRE-FIX measure (gitless read of the awake tree, lines at 4b2fd3af9): (1) the
`--ask-diff` gate appended `Answer `continue` instead if the handoff needs no
change.` — an offer that undoes the predecessor's decision and lets the
successor ack `continue` with a non-diff, violating the one-call contract;
(2) BOTH read-backs recorded ANY acked `diff` as `result: diff` / halting
regardless of text, so a successor whose review found no change had no answer
that completed the rotation.

CHANGES (rotate.py):
- ask_gate (cmd_rotate_self, ask-diff leg): deleted the `Answer `continue`
  instead` sentence; replaced with one sentence naming the EMPTY diff text
  (`--text -` with no stdin, or `--text ''`) as the reviewed-no-change answer
  that stands the handoff; a non-empty diff halts it. The gate no longer
  contains the word `continue`.
- cmd_rotate_self read-back: an acked `diff` whose `text` is empty/whitespace
  is now `acked_continue=True`, recorded `result: success` with a new
  `observations.d_reply_decision == "diff-empty"` value (the fields set only
  when not None, so a plain `continue` success record is byte-identical to
  before); flows into the same success path (ack-file rotation to
  `.ack.gen<N>.json`, after_join, announce, self-reap) and returns 0. A
  non-empty diff text still records `result: diff` and returns 1.
- `_rotate_self_record` gained an optional `reply_decision` param added to
  `obs["d_reply_decision"]` when set (never a changed shape for existing
  callers).
- cmd_loop read-back: `diff` with non-empty text halts exactly as today
  (`result: diff`, text printed, window kept); `diff` with empty text is
  `result: success` with `reply_decision: diff-empty` and announces like a
  `continue`. Plain `continue` unchanged.
- First-seating (`_compose_seating_announcement`) and s6.3 spellings untouched
  (byte-identical).

TESTS ADDED:
- test_rotate.py::test_loop_returns_success_when_diff_is_empty — cmd_loop ack
  `{answer: diff, text: "   "}` -> `result: success`, `d_reply_decision:
  diff-empty`, no `acked diff` halt.
- test_rotate_handover.py::test_ask_diff_gate_names_only_diff_and_empty_stands
  — dry-run rotate-self captures `extra`, asserts `continue` NOT in the
  ask-diff gate, the ONE `diff --text -` call named, and the EMPTY-diff
  standing sentence present (falsifier (a)).
- test_rotate_handover.py::test_rotate_self_diff_empty_completes_rotation —
  rotate-self `_read_ack -> {answer: diff, text: ""}` completes: rc 0, record
  success + d_reply_decision diff-empty, ack rotated to .ack.gen1.json, live
  ack gone (falsifier (b)).
- test_rotate_handover.py::test_rotate_self_diff_nonempty_halts — `text:
  "move §3"` halts: rc 1, record `result: diff` (falsifier (b)).

## Evidence

Full engine suite for the touched modules across the named claim files:

    test_rotate.py test_rotate_handover.py test_rotate_selfreap.py
    test_rotate_complete.py test_rotate_autopsy.py test_rotate_next.py
    test_rotate_identity_main.py test_rotate_handoff_driven.py
    test_rotate_launch_wrapper.py test_rotate_prepare.py
    test_rotate_recover.py test_rotate_startup.py test_rotate_tail.py
    test_rotate_templates.py test_rotate_g1517.py
    test_rotate_first_decision.py test_session_start_bootstrap.py
    test_session_start_seat_pre_spawn.py test_after_join_service.py
    test_bin_help_smoke.py test_heal_ack_rotation.py
    test_sensei_rotate_out_audit.py

    587 passed, 3 skipped in 138.71s

The 4 new tests collected and pass (verified by --co listing). All existing
behaviour holds: non-empty diff on both read-backs still records `result: diff`
and halts; `continue` record shape unchanged; ack rotation, after_join, and
announce paths untouched.

RESIDUE (recorded per the claim's RULES, not built): the ListAgents cost of
`--ref` on the diff path — the rotating side does not yet back-fill
session_ref before the successor's one call. Out of scope; belongs to the
g15 line SL7.16 (brief C, whois by key).

## Agent Notes
Built the g15 claim: ask-diff gate deleted the continue offer; empty/whitespace diff text stands the handoff (success+reply_decision diff-empty, ack rotated, rc0); non-empty diff halts as before; 4 new tests, 587 pass.

PARENT REVIEW (a00-ebefd47a, SL7.18): ACCEPTED. Independently verified on the built bytes: ask_gate (rotate.py:10736-10750) no longer contains the word `continue` and names only `diff --text -`, with the EMPTY-diff standing sentence; rotate-self read-back (rotate.py:11246-11263) completes on empty/whitespace diff text (reply_decision=diff-empty into the same success record) and halts non-empty; cmd_loop read-back (rotate.py:2350-2361) matches. Ran 4 new tests -> passed; ran test_rotate_next/heal_ack_rotation/session_start_bootstrap/after_join_service/bin_help_smoke/rotate_complete -> 89 passed, 3 skipped. Verdict proved stands; evidence_runs resolves. RESIDUE (accepted, out of scope per claim): --ref back-fill cost on the diff path -> SL7.16.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The instruction said: "THIS KID MUST IMPLEMENT THE FIX. A g15 claim is behaviour to build, not a hypothesis to measure" and the target claim demanded the ask-diff gate drop its `continue` offer and both read-backs treat an empty-text acked diff as the handoff standing. The machine now does exactly that: rotate.py:10736-10750 builds the ask-diff gate without the word `continue` and names the EMPTY-diff answer; rotate.py:11246-11263 sets acked_continue=True with reply_decision=diff-empty for empty/whitespace text and only then falls through to the existing success path (ack rotation, after_join, announce, self-reap), returning 1 only on non-empty text; rotate.py:2350-2361 does the loop-side equivalent. Verified by running, not by reading: the 4 new tests pass and 89 tests across the named neighbour files pass, 3 skipped. NEAR MISS: deleting the sentence from the gate string alone (a) satisfies the falsifier "gate no longer contains `continue`" and leaves read-back (b) asserting `result: diff` for an empty text — a successor that obeys the new gate would still halt the rotation forever. This node differs from its scaffold by carrying both halves and the test that pins each. No standing rule was deviated from; the residue (--ref back-fill cost on the diff path) is recorded out of scope per the claim, not built.
<!-- THOUGHT:END -->
