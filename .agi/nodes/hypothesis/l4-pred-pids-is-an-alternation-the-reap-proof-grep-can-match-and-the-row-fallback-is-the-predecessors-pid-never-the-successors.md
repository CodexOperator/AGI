---
id: hypothesis:l4-pred-pids-is-an-alternation-the-reap-proof-grep-can-match-and-the-row-fallback-is-the-predecessors-pid-never-the-successors
mint_id: 7911527b77a84a20a079eb4cb12f6aa5
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 20fde4e86c181b94
season: 2
testable_claim: "goal:g15.25 SM.06 = SL7.98 re-cut (intake: belam XVIII 23:41Z queue B). MEASURED on season2/main @d22584a70: _derive_pred_pids rotate.py:10797-10845 returns `\" \".join(pids)` from the record s12_self_reap.chain — the template reap-proof entry is `ps … | grep -E {pred_pids}` (rotations.md:78 director, :120 prime), so a two-pid chain yields grep -E \"1234 5678\", a literal that matches NO ps line: the proof reads empty = gone even while both pids live (vacuous); the fallback `_find_seat(root, seat).pid` (:10835-10841) reads the ROW, which at rotate-self tail time has ALREADY been re-written with the successor pid (spawn writes pid at row write, F8/SL5.01) — the proof would grep the successor and read it as an unreaped predecessor; an empty derivation reaches the dry-run plan as `grep -E \"\"` (:11267 names this as the L4.179 class; the refusal map :11272 exists for the performer, not the plan). CLAIM: (1) `_derive_pred_pids` returns `\\b(1234|5678)\\b` for N>=1 pids (a single pid also word-bounded: `\\b1234\\b`) — the ONE shape every caller substitutes, so `grep -E` matches each pid as a whole field; (2) the row fallback reads the predecessor pid from the RECORD (`pred_pid` / `pid_before` — measure the field the seating + rotation records carry and name it) else from the row ONLY when the row generation == the record gen_before (the row not yet re-written); a row already at gen_after is never used; (3) an empty derivation in the dry-run plan prints the same named refusal line the performer map (:11272) prints for pred_pids — never `grep -E \"\"`; (4) the template lines stay byte-identical (the value is what changes; template-first: no template edit). FALSIFIERS: a joined value without `|`; a pattern that matches a pid as a substring of a longer pid (assert `\\b`); a fallback that returns the successor pid when row gen == gen_after; a dry-run plan containing grep -E with an empty pattern. TESTS (test_after_join_service.py, <= 5): chain [1234, 5678] -> pattern, and re.search on a fake ps line for each; chain [] + record pred pid -> that pid; chain [] + row at gen_after -> no fallback to the row; dry-run empty -> refusal line, no empty grep; single pid word-bounded. FILE SCOPE: rotate.py _derive_pred_pids + the dry-run plan substitution; one test file; fixture :48 \"123 456\" updated to the new shape. CEILING: <= 35 lines net, <= 5 tests."
title: pred_pids resolves to a word-bounded alternation the reap-proof grep can match (space-joined matched nothing on a multi-pid chain), the row fallback is the PREDECESSOR pid from the record never the row already re-written for the successor, and a dry-run with an empty derivation prints the named refusal (mur-SL2.26 residue on SL7.98)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-pred-pids-is-an-alternation-the-reap-proof-grep-can-match-and-the-row-fallback-is-the-predecessors-pid-never-the-successors

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
