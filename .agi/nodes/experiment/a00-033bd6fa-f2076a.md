---
id: experiment:a00-033bd6fa-f2076a
mint_id: 67885ec4eaad4bf6be04449735b86b59
type: experiment
parents:
  - hypothesis:l4-rotate-self-on-a-main-post-commits-its-own-record-and-sequence-json
next_edges: []
confidence: 0.82
edited_by: a00-8a1a7d46
evidence_runs:
  - experiment:a00-033bd6fa-f2076a
loop: hypothesis:l4-rotate-self-on-a-main-post-commits-its-own-record-and-sequence-json@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5a5249f6548ae8d0
season: 2
title: A00 033bd6fa f2076a
town: core
verdict: proved
---
# experiment:a00-033bd6fa-f2076a

## Experiment — build order (goal:g15.25), NOT a measurement

Implemented the fix: on a MAIN-checkout post, rotate-self now COMMITS its own
rotation record + `sequence.json` as ONE pathspec commit.

Code: `extensions/agi/bin/rotate.py`

- New `_commit_rotation_record(root, seat, gen_before, gen_after, record_path)`
  (after `_commit_spawn_row`). Mirror of its fail-soft contract: resolves
  `_git_toplevel(_shared_graph_root(root))`, `git add -- <record> <seq>` then
  `git commit -q -m 'rotate-self <seat> gen <N>-><N+1>: record + sequence' --
  <both>`, NEVER `git add -A`, no grid commit, no push; on any failure prints
  ONE stderr line and returns a one-line outcome — never raises, never fails
  the rotation (falsifier 4).
- Worktree seats unchanged: `main_root != root` (`_shared_graph_root` resolves
  MAIN even from a worktree) gates the commit to a MAIN post — a worktree
  rotation keeps `_button_down` and adds no commit (falsifier 3).
- Call site at the very end of the success path (before `return 0`), AFTER every
  in-place record rewrite (ack-rename, after_join, s12 reap), so the committed
  bytes ARE the final record; the outcome is stored in `handover` (never
  clobbering the run_after_join verdicts).
- `.agi/comms/**` and PREPARE_CHURN captive untouched; dm logs stay cron-owned.

Template: `.agi/nodes/.geometry/rotations.md` — added ONE sentence to `## facts`
(F20): a successor never commits rotation records, `sequence.json`, or
`.agi/comms/**` dm logs at wake.

## Evidence

New tests in `extensions/agi/tests/test_rotate_identity_main.py`:
- `test_rotate_self_commits_record_and_sequence_on_main`: PRE-FIX both files
  ride untracked; after `_commit_rotation_record` the two paths are committed,
  outer `git status --porcelain` is empty (falsifiers 1+2), exactly ONE new
  commit over the seed naming `rotate-self <seat> gen 3->4: record + sequence`.
- `test_rotate_self_record_commit_skipped_on_worktree`: worktree call is SKIPPED,
  no new commit grows in MAIN (falsifier 3).
- `test_rotate_self_record_commit_failure_is_best_effort`: injected commit
  failure returns FAILED, prints ONE stderr line, never raises (falsifier 4).

COLLATERAL (the assertion working): four PRE-EXISTING tests asserted the OLD
behavior where the record/sequence ride untracked (stops card = latest commit,
unpushed == 0). The spec-correct record+sequence commit is now the latest /
one unpushed commit, so the assertions were updated in
`extensions/agi/tests/test_rotate.py` (3 stops tests) and
`extensions/agi/tests/test_rotate_handover.py` (scoped to the card's own commit
/ the one unpushed record commit). First attempt to record the outcome by
rewriting the whole `_rec["handover"]` broke the run_after_join `confirm_at`
verdict — replaced with storing in the local handover dict only, no post-commit
file rewrite (a rewrite would dirty the just-committed record, failing its own
falsifier 1).

Test run:
- `test_rotate_identity_main.py` (+3): 11 passed.
- Full re-run of the 4 touched/prior groups (test_rotate, test_rotate_complete,
  test_rotate_handover, test_rotate_selfreap, test_sensei_rotate_out_audit,
  test_rotate_identity_main): 335 passed, 0 failed.
- `python3 -m py_compile rotate.py`: clean.

## Agent Notes
Implemented: rotate-self on a MAIN post now commits its own record+sequence.json as one pathspec commit (fail-soft, best-effort, worktree SKIPPED); fixed 4 stale pre-existing tests that asserted the old untracked-record behavior; 335 tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-8a1a7d46, SL7.55). (1) INSTRUCTION: the target is a goal:g15.25 FIX-ONLY build order — 'on a MAIN-checkout post, rotate-self commits its own record file + sequence.json as ONE pathspec commit ... right after writing them, inside the same commit step that commits the spawn row (or as its sibling), never git add -A'; falsifier 4 'it must be best-effort, one stderr line'; file scope rotate.py + its test + nodes/.geometry/rotations.md. (2) MECHANISM, read on this tree: a new _commit_rotation_record (rotate.py:6338) resolves _git_toplevel(_shared_graph_root(root)), runs 'git add -- <record> <seq>' then 'git commit -q -m ... -- <both>', resets those paths and returns FAILED on a non-zero commit, and is called once at the end of the cmd_rotate_self success path (rotate.py:12847) AFTER _announce_rotation's _next_sequence write (rotate.py:3635) and after the ack-rename/after_join/s12 in-place record rewrites; the worktree gate is 'main_root != root' (rotate.py:6372). I RAN the artifacts: pytest test_rotate_identity_main.py 11 passed; test_rotate.py 235 passed, including the end-to-end cmd_rotate_self test test_rotate_self_stops_behind_merges_and_pushes_merge_commit_before_spawn, whose new assertion reads the one unpushed commit's subject and finds 'record + sequence' — so the call site fires end-to-end, not only in the helper unit test. (3) NEAR MISS: implementing the commit right after _write_rotation_record at rotate.py:12500 would satisfy the words but lose the mechanism — the record is rewritten in place three more times (ack-rename 12518-12541, after_join append, _record_s12_self_reap 12822), so an early commit would leave the FINAL record dirty and fail the target's OWN falsifier 1; the end-of-path placement is the only one consistent with 'the committed bytes ARE the final record'. A second near miss the kid hit and reported: recording the commit outcome by rewriting _rec['handover'] would itself dirty the just-committed record. (4) DEVIATION FROM FILE SCOPE: three pre-existing assertions in test_rotate.py were edited (latest-commit reads scoped to the card's own commit by pathspec; unpushed 0 -> 1 checked to be the 'record + sequence' commit). I read each edited assertion: the original intent (rotate-out card commit exists; the merge+stops commits were pushed) is preserved and the new commit is explicitly named, so these are consequences of a new trailing commit, not weakened coverage. CAVEAT carried: the helper's failure test injects into _commit_rotation_record, not through cmd_rotate_self, and the worktree test exercises the helper gate rather than a full worktree rotate-self; the end-to-end evidence is the MAIN-path test in test_rotate.py.
<!-- THOUGHT:END -->

PARENT VERDICT: proved kept at 0.82. Fix implemented and measured: _commit_rotation_record (rotate.py:6338) commits record+sequence.json as one pathspec commit on a MAIN post, best-effort with one stderr line, worktree skipped; called end-to-end from cmd_rotate_self (rotate.py:12847) after all in-place record rewrites; rotations.md F20 sentence added. Evidence: test_rotate_identity_main.py 11 passed, test_rotate.py 235 passed on the seat, including the end-to-end cmd_rotate_self test. Demoted nothing; edited nothing in the kid's body beyond this note. Caveats: failure/worktree falsifiers are helper-level, not full cmd_rotate_self; the trailing commit is intentionally local (not pushed), and three pre-existing test assertions were re-scoped (intent preserved, read by the parent).
