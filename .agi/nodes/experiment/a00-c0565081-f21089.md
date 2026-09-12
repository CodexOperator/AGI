---
id: experiment:a00-c0565081-f21089
mint_id: b7d51f75e83d43889d9287d64c3d0133
type: experiment
parents:
  - hypothesis:l4-the-spawn-time-ack-carries-no-session-ref-cmd-ack-refuses-any-uuid-shaped-ref-and-the-tail-test-reads-a-real-ack-file
next_edges: []
confidence: 0.9
edited_by: a00-423c75ac
evidence_runs:
  - experiment:a00-c0565081-f21089
loop: hypothesis:l4-the-spawn-time-ack-carries-no-session-ref-cmd-ack-refuses-any-uuid-shaped-ref-and-the-tail-test-reads-a-real-ack-file@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 94eef5554ee1ef8d
season: 2
title: A00 c0565081 f21089
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c0565081-f21089

## Experiment

FIX-ONLY build of SL7.102 on base 63c67f057. Implemented the claims and proved on the built bytes (rotate nbhd green).

CODE (rotate.py, +25/-14 = 39 touched lines <= 40):
1. Spawn-time ack (s6.3): `_write_ack(..., session_ref="", ...)` — the PREDECESSOR cannot know the successor's ListAgents harness ref at spawn (only arrives when the successor names it); pre-F15 `session_ref=succ_session_id` wrote the JOIN uuid into the ack, back-filled into the row (NO-MATCH for every peer). `succ_session_id` unchanged for the row's session_id write.
2. cmd_ack ref gate: own-session_id-only refusal replaced with `if ref and _looks_like_session_uuid(ref):` — ANY 36-char uuid-shaped --ref (own OR foreign) refused by name, rc 2, nothing written. Removed `_own_session_id` was used only by that check.
3. status --record latest --seat: EMPTY session_ref now prints `session_ref: unset (awaits the ack)` (was silently omitted); uuid still STALE-flagged; a real ref prints as-is.
Claims 2/4 needed only tests, no new mechanism: the empty `{succ_ref}` refusal is SL7.73's existing `_AFTER_JOIN_EMPTY_REASONS["succ_ref"]` line, and the tail already reads the real ack file once the s6.3 write carries ''.

TESTS (+4 new, <= 5):
(a) test_rotate_tail.py::test_tail_reads_real_predecessor_ack_keeps_row_session_ref_empty — NO `_read_ack` stub: rotate-self writes + reads the REAL ack; asserts ack session_ref == '' and the row's session_ref stays '' (never the JOIN uuid).
(b) test_rotate_tail.py::test_status_prints_unset_when_session_ref_empty.
(c) test_rotate.py::test_ack_refuses_any_uuid_shaped_ref_by_name — FOREIGN uuid ref (!= own sid) refused by name, rc 2, no ack file, no back-fill.
(e) test_after_join_service.py::test_empty_succ_ref_ack_entry_refused_named_never_runs — ack `--ref {succ_ref}` entry refuses by SL7.73's line (`row session_ref empty`), never runs on the empty slot.
(d) harness-ref acceptance already covered by test_ack_live_listagents_ref_is_not_a_session_id_prefix_and_is_accepted.
One existing test UPDATED (not added): test_rotate_handover.py::test_handover_writes_row_pin_identity_ack asserted the OLD spawn-ack uuid; now asserts ''.

## Evidence

- Touched rotate files (rotate.py, test_rotate.py, test_rotate_tail.py, test_rotate_handover.py, test_after_join_service.py): 407 passed.
- rotate_* neighbor suite (19 files): 375 passed.
- test_rotate/tail/after_join: 362 passed. test_rotate_tail/startup/seat_status/send: 432 passed.
- Only failing assertion found: the ONE test asserting the pre-fix spawn-ack uuid — updated to '' (claim 1 true on the bytes). No other rotate test asserted the old spawn-ack uuid.

## Agent Notes
SL7.102 re-cut built+proved: spawn-time ack session_ref '' (predecessor cannot know the harness ref); cmd_ack refuses ANY uuid-shaped --ref by name (_looks_like_session_uuid, rc2); status prints 'unset (awaits the ack)' for empty session_ref; +4 falsifier tests +1 updated handover assertion; rotate nbhd 407/375/362/432 green, rotate.py 39 lines <=40.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-423c75ac, SL7.102. (1) The dispatch said: extend the g15 FIX-ONLY re-cut so the predecessor cannot write a session uuid into the spawn-time ack, cmd_ack refuses any uuid-shaped --ref, and the tail test reads a real ack file. (2) The machine: read git diff --cached on rotate.py — the live writer at the s6.3 spawn step now passes session_ref="" (rotate.py), the cmd_ack gate at ~2164 tested the value itself through _looks_like_session_uuid instead of equality with the seat own session_id, and cmd_status now prints "session_ref: unset (awaits the ack)" for the empty cell. Ran the four touched test files (test_rotate_tail, test_rotate, test_after_join_service, test_rotate_handover): 407 passed, 0 failed. The new tail test installs NO _read_ack stub, so rotate-self writes and reads the REAL ack file on the fixture root. (3) Near miss: a fragment that only added _looks_like_session_uuid to the status print, or left the cmd_ack gate as own-id equality, would satisfy the wording "refuses a uuid-shaped ref" for the own row and still accept a FOREIGN uuid-shaped ref — the added test uses a foreign uuid (!= own sid) and is the one that catches it. (4) No standing-rule deviation; no file outside the declared scope was touched (test_rotate_handover.py was the one assertion asserting the old spawn uuid, updated in place).
<!-- THOUGHT:END -->

PARENT REVIEW PASS a00-423c75ac SL7.102: accepted as-is, verdict proved. Verified on the built bytes: spawn ack session_ref="" (the only live uuid writer is gone), cmd_ack refuses a foreign uuid-shaped --ref by name (rc2, no ack, no back-fill), status names empty as unset; +4 falsifier tests and 1 updated handover assertion; 407 passed across the four touched files. Scope matched the declared file set.
