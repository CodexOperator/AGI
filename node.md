---
id: hypothesis:l4-the-after-join-record-rewrite-is-committed-by-pathspec-and-a-worktree-seats-record-names-its-committer
mint_id: b4c10330edd94c77bea6c4a08536730e
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 903d7933f29e18fa
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (Prime XVI dm 17:07Z (mur-SL2.23 digest), line numbers measured by the Prime on main tip 36fa24d1d — `git show 36fa24d1d:<file> | sed -n` before trusting one; cite at seat tip d51c9a917, re-measure on your base; line (a), SL7.55 residue). MEASURED: `run_after_join` rewrites the rotation record in place — `rp.write_text(json.dumps(rec, indent=2))` at rotate.py:9637 — AFTER rotate-self committed that record as its own pathspec commit (SL7.55, F20), so MAIN reads `M <rotations>/<seat>.<stamp>.json` on the Prime's own record until someone else's commit sweeps it; and a worktree seat's records land UNTRACKED in MAIN with no committer (the `if main_root != root:` branch at :6486 routes the write to the main checkout but commits nothing). CLAIM: (a) the service's rewrite commits its own change by pathspec — ONE `git add <record> && git commit -m 'after_join record: <seat> <stamp> (performed by <performer>)'` on the record path only, from the main checkout, best-effort (a failed commit is a named field on the after_join key, never an exception into the watch) — OR the after_join outcome is written to a SIDECAR `<record>.after_join.json` that the record's readers (`status --record latest`, `_latest_rotate_record`, `_after_join_already_performed`) merge in, so the committed record is never modified after its commit; the kid picks ONE and says why in the node; (b) a worktree seat's record written into MAIN (:6486) is committed by the same pathspec commit with the committer named on the record (`committed_by: service|rotate-self`), never left untracked; (c) F20 holds: a successor never commits records/sequence/comms at wake — the commits are the writer's own. FALSIFIERS: after a performed after_join `git -C MAIN status --short -- .agi/sessions/rotations/` still shows M or ?? for that record; two commits for one rewrite; the sidecar (if chosen) is not read by `status --record latest`. TESTS: test_after_join_service.py + test_rotate_selfreap.py or test_heal.py — rewrite leaves the tree clean (subprocess git in a tmp repo), worktree record committed with committer, failed commit named not raised. FILE SCOPE: extensions/agi/bin/rotate.py — the record write at :9637 and the worktree route at :6486 (+ the three readers if a sidecar); extensions/agi/bin/heal.py only for the watch call site; the test files. EXCLUDED: the after_join entries/performer/liveness (SL7.72-76 landed — extend, never rewrite), the dm, the templates, rotate-self's own record commit (F20). CEILING: one commit helper or one sidecar, one committer field, four tests."
thought_session: sensei-director-genXIV-L14
title: the after_join service's rewrite of a rotation record is committed by pathspec (or written as a sidecar) so MAIN never reads M on a committed record, and a worktree seat's record landing untracked in MAIN names its committer — the service, at rewrite
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-after-join-record-rewrite-is-committed-by-pathspec-and-a-worktree-seats-record-names-its-committer

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
