---
id: experiment:a00-d053f342-92413c
mint_id: 54b4ecbd22d7403899f2d9f3bf6261e0
type: experiment
parents:
  - hypothesis:l4-the-own-tail-after-join-passes-the-successors-acked-harness-ref-or-nothing-never-the-session-uuid-and-the-ack-refuses-a-session-id-as-ref
next_edges: []
confidence: 0.92
edited_by: a00-cefaa5a4
evidence_runs:
  - experiment:a00-d053f342-92413c
loop: hypothesis:l4-the-own-tail-after-join-passes-the-successors-acked-harness-ref-or-nothing-never-the-session-uuid-and-the-ack-refuses-a-session-id-as-ref@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 46fc799d46ee3445
season: 2
title: A00 d053f342 92413c
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d053f342-92413c
FIX-ONLY build (goal:g15.25 F15). Claim: (1) the own-tail after_join path
passes the successor's ACKED harness ref or nothing — never the JOIN's session
uuid — and (2) cmd_ack refuses BY NAME a --ref equal to the running seat's own
session_id cell (= the joined session uuid) and writes nothing.

Measured pre-fix state (the defect): rotate.py step 6.4 passed
`succ_ref=((ack or {}).get("session_ref") or succ_session_id or "")` — the
`or succ_session_id` fallback back-filled a JOIN's session UUID into the
after_join `{succ_ref}`, poisoning a row whose session_ref then equals its
session_id, which send.whois reads as NO-MATCH for every peer. cmd_ack's --ref
validation accepted the uuid because send._resolve_rows matches an EXACT
session_id as the seat's own row (WHOIS_OK), so the uuid slipped in.

Implemented on rotate.py:
1. step 6.4: `succ_ref=(ack or {}).get("session_ref") or ""` — deleted the
   `or succ_session_id` fallback (one line) + rewrote the director comment to
   document the F15 deletion. The own-tail path now mirrors the watch path.
2. cmd_ack --ref validation (:2080-2120): after `rows = send._locally_loaded_rows`,
   compute the running seat's own row session_id (name-or-role match); if a
   non-empty --ref equals it, print
   `ERR: --ref <x> is a session id, not your ListAgents ref (F15): pass the
   bare ref or omit --ref.` to stderr and return 2 — no ack file, no row write.
   An omitted --ref still leaves session_ref empty (the --key whois fallback
   fires), exactly as today.

Watch path (:10445-10449), the DM's `<your ListAgents ref>` wording, cmd_ack
--gen handling, _prepare_checks, run_after_join/heal.py, and send.py were all
left untouched (excluded sibling rounds, by function).

Tests added (3, of the <=4 budget): two in test_rotate_tail.py driving
cmd_rotate_self step 6.4 via a captured `_first_turn_values.succ_ref` (no acked
ref -> '' even with a non-empty session seam; acked ref -> that ref, never the
uuid); one in test_rotate.py (cmd_ack --ref == own session_id uuid -> rc 2,
stderr names "session id" + "F15", no ack file written). File-hint deviation:
the tail tests landed in test_rotate_tail.py (where the cmd_rotate_self `_fix`
fixture lives) rather than test_after_join_service.py, per the repo's layout.

## Evidence

All suites green on the built bytes:
  test_rotate_tail.py + test_after_join_service.py + test_heal_ack_rotation.py:
    82 passed in 11.00s
  test_rotate.py: 250 passed in 42.62s
  test_rotate_alert_two_tree ... test_sensei_rotate_out_audit:
    348 passed, 1 xfailed
  test_rotate_g1517 + test_rotate_next + test_rotate_launch_wrapper
    + test_rotate_autopsy: 37 passed in 6.47s
ast.parse of the edited rotate.py: valid.

The two F15 tail tests (no acked ref -> succ_ref ''; acked ref -> that ref,
never the join uuid) and the cmd_ack session-id refusal test each pass.
Falsifiers addressed: a uuid-shaped --ref is now refused by name + nothing
written; a row's session_ref can no longer equal its session_id via the
after_join ack (the uuid fallback is gone).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-cefaa5a4, SL7.86). State: ACCEPT as proved — the build order landed, not merely measured.

(1) INSTRUCTION: the hypothesis is FIX-ONLY — "(1) the own-tail path mirrors the watch path — succ_ref = the successor's acked ref when it acked with one, else "" — NEVER succ_session_id (delete the fallback, one line); (2) cmd_ack refuses BY NAME a --ref equal to the row's own session_id cell or to the joined session uuid ... and writes nothing".

(2) MACHINE, read on the built bytes: rotate.py:13745 now reads `succ_ref=(ack or {}).get("session_ref") or ""` — the `or succ_session_id` fallback is gone, matching the watch path at :10445-10458 (`(row or {}).get("session_ref") or ""`). rotate.py:2103-2120 computes `_own_session_id` from the running seat's row (name-or-role match) and returns 2 with `ERR: --ref ... is a session id, not your ListAgents ref (F15)` BEFORE any ack write or _resolve_rows. I ran the three new tests, not the kid's report: test_rotate_tail.py::test_tail_with_no_acked_ref_never_falls_back_to_join_uuid and ::test_tail_with_an_acked_ref_passes_that_ref_never_the_uuid PASS; test_rotate.py::test_cmd_ack_refuses_ref_equal_to_own_session_id_uuid PASSES (2 passed, 248 deselected). The tail tests drive the real cmd_rotate_self step 6.4 through a capturing _first_turn_values seam, so they assert the passed VALUE, not a helper.

(3) NEAR MISS: a fix that only added the cmd_ack refusal would satisfy (2) and leave the poisoning source live — the tail would still hand a uuid to the record, and a hand-passed uuid-of-another-seat is what _resolve_rows already refuses. Both halves were required and both are present. The other near miss: refusing only the OWN uuid but leaving the `or succ_session_id` fallback would pass the ack test while keeping the tail poisoning; the deletion is the load-bearing half.

(4) DEVIATION from the file hint (test_after_join_service.py): the two tail tests landed in test_rotate_tail.py, where the cmd_rotate_self _fix/_rs_args/_FakeTmux machinery lives. Property of this case: the tail value is only observable through cmd_rotate_self's step 6.4, whose fixture exists only in test_rotate_tail.py; duplicating that fixture into test_after_join_service.py would test a copy, not the seam.

CAVEAT CARRIED (residue, not a demotion): the hypothesis falsifier is broader than the claim text — "any record ... whose ack cmd carries a uuid-shaped --ref". The build refuses the OWN session_id uuid and any uuid that resolves to ANOTHER row (via _resolve_rows), but a uuid-shaped --ref matching NO row is still accepted and back-filled. The claim as written ("equal to the row's own session_id cell or to the joined session uuid") is fully met; the broad falsifier is a residue for the next digest.
<!-- THOUGHT:END -->

## Agent Notes
FIX-ONLY: deleted the one-line succ_session_id fallback in rotate.py step 6.4 (own-tail succ_ref now acked-ref-or-empty, mirrors watch path); cmd_ack refuses by name a --ref equal to the seat's own session_id uuid (F15, rc 2, nothing written). 3 new tests pass; rotate/after_join/heal/tail suites green.

PARENT VERDICT: ACCEPT, proved (confidence 0.92 stands). Read the artifact, not the report: rotate.py:13745 deleted the succ_session_id fallback; rotate.py:2103-2120 refuses by name a --ref equal to the seat own session_id before any write; three new tests pass under my own run (2 in test_rotate_tail.py, 1 in test_rotate.py). Watch path, DM wording, cmd_ack --gen, _prepare_checks, run_after_join/heal.py and send.py untouched as excluded. Residue for the next digest: a uuid-shaped --ref matching NO row is still accepted (the claim text only required the own-session_id / joined-uuid refusal; the hypothesis falsifier is broader).
