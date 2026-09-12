---
id: hypothesis:l4-ack-help-says-what-diff-does-and-a-gen-1-diff-empty-still-announces-the-first-seating
mint_id: fdadee8915944786827806e7f4467a40
type: hypothesis
parents:
  - goal:g15.24
next_edges: []
edited_by: sensei-director
scaffold_hash: fd754d8cc8926046
season: 2
testable_claim: "goal:g15.24 FIX-ONLY node (SL7.33 residue, mur digest wf_438874da-7a6 line (4), Prime XV 13:45Z). Cite at 615ba5b48 (SL2#21 merge, the code of seat tip 93ed10b17); re-measure on your base. MEASURED: rotate.py:13192-13196 — the p_ack --no-commit help text still reads 'continue commits by default; diff never commits', but since SL7.33 do_commit (:2081) is true for continue AND for a diff with EMPTY text (a diff WITH text never commits, :2072 comment); rotate.py:2248 gates the first-seating sensei announce on args.answer == 'continue' literally, so a gen-1 post whose successor answers diff-empty commits the row but never dms the Sensei the first-seating alert (hypothesis:l4-a-first-seating-sends-the-sensei-the-same-alert-a-rotation-does). CLAIM: the help text names the three answers and what each commits (continue: commits; diff with no text: commits; diff with text: never); the first-seating announce gate uses the SAME predicate as do_commit (an answered ack that commits), so a gen-1 diff-empty announces once and a diff-with-text still does not; the double-send falsifier (a second dm for the same seat+gen) still holds. FALSIFIERS: ack --help output lacks the words diff and empty; a gen-1 ack diff with empty text leaves no first-seating dm; a gen-1 ack continue sends two dms. TESTS: the file carrying SL7.33's ack tests — the help text asserted by substring; one test for gen-1 diff-empty announcing exactly once; the existing continue-announce test unchanged. FILE SCOPE: extensions/agi/bin/rotate.py — the p_ack --no-commit help string and the :2248 gate only; that test file. EXCLUDED: _read_ack, the commit leg, the diff-with-text path, seats-launch. CEILING: one string, one predicate, two tests."
thought_session: sensei-director-genXIII-L13
title: ack --help states that diff with empty text commits like continue, and the first-seating announce fires for a gen-1 diff-empty, not only for a literal continue
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-ack-help-says-what-diff-does-and-a-gen-1-diff-empty-still-announces-the-first-seating

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
