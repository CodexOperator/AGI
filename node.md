---
id: hypothesis:l4-the-prime-and-main-post-closeout-real-runners-are-driven-on-a-fixture-root-and-the-g17-1-note-runner-uses-the-one-arg-note-grammar
mint_id: 61bc783a72564e979d7acfd0ac813802
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 3fd2e80e014cd1f9
season: 2
testable_claim: "goal:g15 FIX-ONLY RE-CUT of SL7.90 (DEMOTED by mur-SL2.25 BY NAME, Prime XVII 20:5xZ; experiment:a00-22f6ce02-edd3ff flipped to inconclusive_lean_disproved). MEASURED by the Prime on ffcfa4e2f, re-located on post tip 1d07f3521 (grep on your base): the PRIME_CLOSEOUT_STEPS g17_1_note REAL runner (rotate.py:6608-6624 _g17_1_note) passes `note` and the text as TWO positionals to write.py (:6617 `[sys.executable, str(binp), 'goal:g17.1', 'note', text]`) — write.py's grammar is ONE script argument 'note <text>' (see write.py's verb table: `note 1 arg(s)`), so the live call exits rc 2; the live call site (:14432 `_co_entries, _co_err = _closeout_run_steps(`) passes no record= so the note/numbers steps run on ''; the pathspec_commit runner reports a FAILED _commit_rotation_record as (True, 'committed'); the render runner is executed by NO committed test and resolves the project from the subprocess cwd, not root (a closeout run from a worktree cwd renders the wrong tree). CLAIM: (1) _g17_1_note invokes write.py with ONE script arg 'note <text>' and --actor <seat> --role <role>, cwd root; (2) the live call site passes record=<the in-progress rotation record dict> and the numbers text is composed from it (never ''); (3) pathspec_commit returns (False, '<named refusal>') when _commit_rotation_record fails (rc, stderr head) and (True, committed) only on rc 0; (4) the render runner runs snapshot-goals.py --render with cwd=root and --root-equivalent explicit (whatever the script accepts), then --render --check, and returns the check's result; (5) EVERY PRIME/MAIN-post/worktree real runner is driven at least once by a committed test on a FIXTURE root (a tmp git repo with a minimal .agi/, a goal:g17.1 node, a seat row) through the real code path — write.py invoked for real, a real commit, a real render — asserting the observable (the note on the node, the commit in git log, GOALS.md byte-identical). FALSIFIERS: two-positional write.py call; a runner test that only fakes; render resolved from cwd; a failed commit reported committed. TESTS (append to test_rotate_closeout_steps.py, <= 6): one fixture-root test per real runner (g17_1_note, render, push-dry, pathspec_commit, numbers text non-empty) + the rc-2 regression. FILE SCOPE: rotate.py — the _make_closeout_seams real runners for the Prime and MAIN-post lists + the _closeout_run_steps call site; test_rotate_closeout_steps.py. EXCLUDED: the worktree-post merge_up/wait_grant/suite/grid/stamp runners (SL7.92/101 landed — do not restructure), _closeout_step_list, after_join*, cmd_ack. CEILING: <= 80 lines + <= 6 tests; closeout nbhd green. The Prime's no-closeout ruling stands until this lands."
thought_session: sensei-director-genXVII-L17
title: "SL7.90 re-cut: the PRIME / MAIN-post closeout REAL runners are driven by committed tests on a fixture root — g17_1_note calls write.py with the ONE-arg 'note <text>' grammar, the live call site passes the record, pathspec_commit reports a failed commit as failed, the render runner resolves the project from root not cwd"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-prime-and-main-post-closeout-real-runners-are-driven-on-a-fixture-root-and-the-g17-1-note-runner-uses-the-one-arg-note-grammar

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
