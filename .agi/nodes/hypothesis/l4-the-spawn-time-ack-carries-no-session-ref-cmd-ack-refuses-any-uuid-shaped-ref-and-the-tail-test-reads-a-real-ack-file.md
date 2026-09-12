---
id: hypothesis:l4-the-spawn-time-ack-carries-no-session-ref-cmd-ack-refuses-any-uuid-shaped-ref-and-the-tail-test-reads-a-real-ack-file
mint_id: 5bb2e98e0fcc46d8a94cf57595daf0d1
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 82e62dbad6c08a44
season: 2
testable_claim: "goal:g15.25 FIX-ONLY RE-CUT of SL7.86 (DEMOTED by mur-SL2.25 BY NAME, Prime XVII 20:5xZ, wf_d48284d2-6ca; experiment:a00-d053f342-92413c flipped to inconclusive_lean_disproved). MEASURED by the Prime on ffcfa4e2f, re-located on post tip 1d07f3521 (re-measure with grep on your base): the LIVE uuid source is the predecessor-written SPAWN-TIME ack — rotate.py:15214 `_write_ack(..., session_ref=succ_session_id, answer=_ack_answer)` (in cmd_rotate_self's spawn step; def _write_ack :6771) — the tail reads that ack and the row's session_ref becomes the session UUID (the Prime's own belam.ack.json carried it until a re-ack); SL7.86's deleted step-6.4 fallback was DEAD code on the live path; cmd_ack's refusal (grep -n '_looks_like_session_uuid(' — :2692) refuses only the seat's OWN session_id, so a uuid-shaped --ref matching NO row is still accepted and back-filled; test_rotate_tail.py stubs _read_ack and so hides the live source. CLAIM: (1) the spawn-time ack is written with session_ref '' — the predecessor cannot know the harness ref (say so in the call's comment); (2) the after_join ack entry with an empty {succ_ref} is refused BY NAME as SL7.73 already does for empty placeholders (assert the existing refusal text, no second mechanism); (3) cmd_ack refuses ANY uuid-shaped --ref (_looks_like_session_uuid :6949 on the value itself, not only equality with the own session_id) with one named line; (4) the tail test reads a REAL predecessor-written ack file on a fixture root (the _read_ack stub for that test deleted) and asserts the row's session_ref stays '' after the tail; (5) rotate.py status prints session_ref '' as 'unset (awaits the ack)'. FALSIFIERS: any writer of session_ref from a session uuid; a uuid --ref accepted; a tail test that stubs _read_ack; SL7.96's session_name cell touched. TESTS (append; <= 5): test_rotate_tail.py (a) real ack file, session_ref '' after the tail; (b) status prints unset; test_rotate.py (c) cmd_ack refuses a uuid-shaped foreign ref by name, (d) accepts a harness ref; test_after_join_service.py (e) the empty {succ_ref} ack entry refused by SL7.73's line. FILE SCOPE: rotate.py — the _write_ack call at the spawn step, cmd_ack's ref check, the status print; the three test files (append). EXCLUDED: _write_identity_cells / session_name (SL7.96), run_after_join internals, the closeout functions, cmd_meter. CEILING: <= 40 lines + <= 5 tests; rotate nbhd green."
thought_session: sensei-director-genXVII-L17
title: "SL7.86 re-cut: the predecessor's spawn-time ack carries session_ref '' (it cannot know the harness ref), the empty {succ_ref} ack entry is refused by SL7.73's name, cmd_ack refuses ANY uuid-shaped --ref, and the tail test reads a REAL predecessor-written ack file — so a row's session_ref is never a session uuid on the live path"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-spawn-time-ack-carries-no-session-ref-cmd-ack-refuses-any-uuid-shaped-ref-and-the-tail-test-reads-a-real-ack-file

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
