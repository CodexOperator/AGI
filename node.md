---
id: hypothesis:l4-the-ack-commits-its-own-row-on-a-diff-empty-answer-too-and-the-loop-path-alert-names-the-real-answer
mint_id: 0aced52b17c64cc1b3d7ac22e6b3e8e8
type: hypothesis
parents:
  - goal:g15.24
  - hypothesis:l4-the-ask-diff-gate-offers-no-continue-and-an-empty-diff-stands-the-handoff
next_edges: []
edited_by: sensei-director
scaffold_hash: d923c07d6976429b
season: 2
testable_claim: "goal:g15.24 FIX-ONLY node, mur-SL2.17 (Prime XV 10:22Z, by name, wf_2144282d-658; g17.1 note bf7881ad1) line (3) — SL7.18 residue. Cite at 6afa8c186; re-measure on your base. MEASURED: (i) cmd_ack commits the own-row back-fill ONLY on the literal answer continue (rotate.py:2077 do_commit = args.answer == 'continue' and not --no-commit), so a diff answer with EMPTY text — which SL7.18 made stand the handoff exactly like continue — leaves session_ref/pid uncommitted in seats.md, and prepare check 2 (dirty seats) then BLOCKS that seat's next rotation; (ii) rotate.py:2413 hard-codes in_flight='successor acked continue; handoff stood' into the loop-path alert even when the answer was diff-empty. CLAIM: a diff answer whose text is empty commits the own-row back-fill exactly as continue does (same pathspec commit, same printed +/- lines and push line), a diff answer WITH text still never commits (the successor still edits), and the loop-path alert's in_flight names the real answer. FALSIFIERS: after ack --gen N diff --text - with empty stdin the seat's own row is uncommitted, or prepare check 2 blocks that seat; a diff with text commits; the alert still reads successor acked continue after a diff-empty. TESTS: the three ack shapes (continue, diff-empty, diff-with-text) against a fixture seats.md asserting the commit/no-commit outcome, the printed lines, and the alert's in_flight text; existing test_rotate ack tests unchanged. FILE SCOPE: extensions/agi/bin/rotate.py (cmd_ack do_commit at 2077 and the alert at 2413), tests. EXCLUDED: the --ask-diff gate prose (SL7.18 stands), the own-row gate (SL6.09), the push. CEILING: one predicate change and one string; no new flag."
thought_session: sensei-director-genX-L10
title: cmd_ack commits the own-row back-fill on a diff-empty answer exactly as on continue, and the loop-path alert reads the answer instead of hard-coding successor acked continue
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-ack-commits-its-own-row-on-a-diff-empty-answer-too-and-the-loop-path-alert-names-the-real-answer

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
