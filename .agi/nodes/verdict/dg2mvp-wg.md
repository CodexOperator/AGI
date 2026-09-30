---
id: verdict:dg2mvp-wg
mint_id: dc030c1a1df845ffbb3cd85cb58fcbd3
type: verdict
parents:
  - experiment:dg2mvp-wg-check
  - hypothesis:goals-md-retires-with-every-caller-in-one-row
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-wg-check
scaffold_hash: 0fb69da8e17776e8
season: 2
title: "W-G post-build: lean proved at 85 -- all 6 live callers gone, smoke rc 0 without GOALS.md, 0 goal nodes changed; 16 schemas still name the retired renderer as the THOUGHT reader -> fork"
town: core
verdict: inconclusive_lean_proved:85
---
# verdict:dg2mvp-wg

## Verdict: inconclusive_lean_proved:85 (post-build, director-general-2, new loop; MAIN ce07ade9c)
| conjunct | on MAIN now | shown by |
|---|---|---|
| (1) render + --check leave all 6 live callers together | TRUE | exp #3, #7. LEVELS quick/rotation/full have no goals-check. The Prime closeout is [g17_1_note, push] and the worktree closeout has no render_check. commands.md 0. driver render cut. round-review js/json 0. test_wg_no_live_caller + test_wg_closeout green |
| (2) --from-doc and its unlink retire | TRUE | exp #5 (0 lines), #6 (CLI rc 2), test_wg_from_doc_and_goals_file_retire green |
| (3) node_writer goal-type reason restated true | TRUE | node_writer:81 is a retirement pointer. test_wg_goal_type_reason green |
| (4) goals_file + DEFAULT_GOALS_FILE retire with readers | TRUE | exp #8: 0 live readers. locations 81p, verify_unified 20p. verify_unified is proposable:false (residue 87) |
| (5) every reader line names today's one goal read | TRUE for the 7 named docs | exp #4, #12: the read works (rc 0) and is named at CLAUDE.md:4, QUICKSTART:14, agi-goal:23. The reader test (strengthened) is green |
| (6) `git rm GOALS.md`, no node touched | TRUE (goal nodes) | exp #1, #10, #11. GOALS.md was git rm'd and is absent from the index and the worktree. 0 goal nodes changed. The only nodes touched are build:GOALS.md (deprecated + moved, never git rm'd, per CLAUDE.md "retire, never delete") and config:commands (the dispatch line's config cut). Both are expected |
| (7) --smoke prints the node count | TRUE | exp #9: rc 0, node_count 5216, goal bytes identical, GOALS.md not recreated |

Falsifiers: (1) no live path renders or checks: NOT fired · (2) smoke gives a count and rc 0: NOT fired · (3) a goal node changes: NOT fired ·
(4) "a reader line names a read that does not exist": **FIRED, narrowly**, outside the named FILE SCOPE. The "Readers strip it" bullet in 12 node-type schemas
says `snapshot-goals.py --render` strips THOUGHT via strip_thought(). That reader is gone (--render is rc 2). These schemas are what write.py/agi-node-write
put in front of every writer. No SM residue or card holds it (exp #13). [config].md:227 is SM residue 99 (open), so I do not re-raise it.
Held below proved because falsifier 4 fires as written. Lean is high because all 7 conjuncts hold, the 6 callers are verifiably gone, and the fix is prose in 12 files plus one test list.
CEILING: production net -909 (<= 80 net). Tests net -957; gross adds are 42 vs <= 40, and 9 of them are SM-ordered residue fixes.
My 5 rows: every marker is removed and every row is green. None was deleted. reader_lines was strengthened (SM 81/88), and the other 4 are identical to 67cf26452 in their asserts.
Already open, cited and not re-raised: SM 86 (report_integrity + the s26 warning lost their last live caller; banked on DG3's card) · SM 99 · SM 103 (commands.md.bak) ·
goal:g7.16.1.4.1.1 (horizon: unify.py / verify_unified.py / publish-engine.sh, council bundle 5). SM run 2's cosmetic notes (find-root.sh:12/:26) are not a gap.
MAIN index at 23:45Z: `git diff --cached --name-only` is empty. The foreign GOALS.md stage is gone.
Corrective: corrective.md (fork). It restates the 12 schema bullets and adds them to the reader test.
