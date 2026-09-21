---
id: experiment:a00-c1ee8ce1-fac850
mint_id: 5e5ec1a1fd4344d5b62381b32091cbd3
type: experiment
parents:
  - hypothesis:l4-a-seat-is-a-post-everywhere
next_edges: []
confidence: 0.8
edited_by: a00-28e4f31a
evidence_runs:
  - experiment:a00-c1ee8ce1-fac850
loop: hypothesis:l4-a-seat-is-a-post-everywhere@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c4edd394378c1e2a
season: 2
title: A00 c1ee8ce1 fac850
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c1ee8ce1-fac850

## Experiment

Built the two FIX-ONLY residues into `cmd_post_rename` (`extensions/agi/bin/cli.py`,
`_post_rename_jobs` + step-3 commit + step-4 worktree move only) for
`hypothesis:l4-a-seat-is-a-post-everywhere`, with fixture tests in
extensions/agi/tests/test_post_rename.py.

### Fix (1) — re-run after a partial apply finds nothing to do

Chose **option 2** (accept both cell spellings) over option 1 (persist the job
list into the plan file), because the defect's own proof scenario is the
PLAN-LESS case — a tree whose cells were already rewritten (or a deleted
sessions/ scratch) — which a persisted-jobs plan cannot reconstruct. Made
`_post_rename_jobs` accept a `worktree` cell whose basename spells either
`seat-<name>` **or** `post-<name>` (strip whichever prefix), so a re-run over a
half-rewritten tree still yields the jobs. Then made step 4's `git worktree
move` derive its source/target from the NAME (`<parent>/seat-<name>` ->
`<parent>/post-<name>`) instead of a string-replace of the cell, so it moves
correctly whether the cell still says seat- (fresh) or already says post-
(half-migrated). This closes the loop where `jobs == []` made `mark("worktree_move")`
fire outside the loop and record a step as done that never ran.

### Fix (2) — step-3 commit now BY pathspec, honest rollback

The commit is now `git add <dest> && git commit -m "post-rename: seats.md ->
posts.md" -- <dest> [<seats_rel>]` — a pathspec-only commit, so another agent's
already-staged files can never be swept in (the `goal:g4.1` hazard). The
`seats_rel` path is added to the pathspec ONLY while its staged DELETE is still
pending in the index (`git diff --cached --name-status -- <seats_rel>`); once a
prior commit carried the rename, the path is gone from the index and a
`git commit -- ... seats.md` would ERROR instead of skipping — so it is dropped
and the "nothing to commit" skip is detected from an empty
`git diff --cached --name-only -- <targets>`. The `git reset --soft HEAD~1`
rollback is now printed ONLY on the path where a commit was actually created; on
the skip it prints `skip <dest> (nothing to commit)` with no rollback, so a
stale `HEAD~1` can never unwind an unrelated commit.

Before/after command strings (dry-run step 3):
- BEFORE: `git add .agi/nodes/.geometry/posts.md && git commit -m "post-rename: seats.md -> posts.md"`
- AFTER:  `git add .agi/nodes/.geometry/posts.md && git commit -m "post-rename: seats.md -> posts.md" -- .agi/nodes/.geometry/posts.md .agi/nodes/.geometry/seats.md`

## Evidence

Run lines (proof 1 + 2, required):

    $ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_post_rename.py -q
    ..............                                                           [100%]
    14 passed in 4.36s

    $ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_post_rename.py extensions/agi/tests/test_rotate_identity_main.py extensions/agi/tests/test_send.py extensions/agi/tests/test_write.py -q
    388 passed in 16.69s

Fixture transcript proving (a) finished no-op, (b) partial completes, (c)
pathspec-only commit (built with the test module's own throwaway `_build_repo`,
never the live tree):

    (c) git show --format= --name-only HEAD -> ['.agi/nodes/.geometry/posts.md']
        status --porcelain -> ['A  .agi/nodes/foreign-agent.txt']   # foreign staged file left alone
    (a) SECOND apply (finished fixture): rc=0; prints `skip ... (already post-...)`
        for git mv + both worktree moves + both branch renames; status unchanged;
        post-rename commits on master: 1 (no duplicate)
    (b) apply on hand-rewritten cells-to-post- with NO plan file (worktree dirs &
        branches still seat-): rc=0; `skip .agi/nodes/.geometry/posts.md (nothing to
        commit)`, then `git worktree move .../seat-a .../post-a`, `.../seat-b
        .../post-b`, `git branch -m seat/a@s2 post/a@s2` (+ b); after: post-a/b
        dirs present, seat- dirs gone, branches renamed to post/*@s2, `git status`
        clean.

New tests added: `test_apply_pathspec_commit_names_only_the_geometry_file`,
`test_apply_resumes_hand_rewritten_cells_without_plan`,
`test_apply_second_run_prints_its_skips_no_duplicate_commit`.

<!-- THOUGHT:BEGIN — authored, not derived. Why THIS version of cli.py differs
from the previous one. -->
The prior round (L4.306) built the `--apply` migration and proved it on a fresh
fixture, but the review's bytes caught two residues the head runs left open:
(1) `_post_rename_jobs` only matched `seat-` cells, so the moment step 2 had
rewritten them to `post-` a re-run of a HALF-done apply found zero jobs and, via
the `mark("worktree_move")` outside the loop, recorded a step as done that had
never run — a half-renamed tree never finished; (2) step 3 did a bare `git
commit` after `git add <dest>`, which sweeps any other agent's staged files into
the migration commit (the `goal:g4.1` hazard) AND always printed a `git reset
--soft HEAD~1` rollback that is destructive when the commit was a no-op. THIS
version fixes both: the job matcher understands both spellings and the worktree
move is name-derived, and the commit is pathspec-only with the deletion path
included only while pending, with an honest no-rollback skip. The git mv
(pre-`git add`) of seats.md's DELETE is NOT dropped — it is why the rename lands
as one `R` commit while foreign staged files stay untouched.
<!-- THOUGHT:END -->

## Agent Notes
L4.315 FIX-ONLY: (1) post_rename_jobs accepts post- cells + name-derived worktree move so a re-run of a half-renamed tree completes steps 4-7 (option 2); (2) step-3 commit is pathspec-only (git commit -m ... -- dest [seats_rel]) with seat-delete included only while staged-pending and rollback printed only on a real commit. 14/388 pytest green on throwaway fixture; transcript proves finished no-op + partial-completes + git show HEAD names only geometry.

L4.315 parent review (a00-28e4f31a): ACCEPTED proved. Read the artifact, not the report: `git diff --cached extensions/agi/bin/cli.py` shows `_post_rename_jobs` accepting BOTH seat-/post- prefixes (name = basename minus either prefix), step-4 worktree move deriving old/new from the NAME (parent/seat-<name> -> parent/post-<name>) so a half-rewritten cell no longer yields a no-op move, and step 3 committing `git commit -m ... -- <dest> [<seats_rel>]` with seats_rel included only while its staged delete is pending (`git diff --cached --name-status`) and the HEAD~1 rollback printed only on a real commit. I re-ran `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_post_rename.py -q` -> 14 passed in 9.96s (matches the node). The three new tests are non-vacuous: test_apply_pathspec_commit_names_only_the_geometry_file stages a FOREIGN file and asserts `git show --name-only HEAD` names only the geometry path and the foreign file stays staged; test_apply_resumes_hand_rewritten_cells_without_plan commits the seats->posts rewrite by hand with NO plan file and asserts the worktrees/branches still complete; test_apply_second_run_prints_its_skips_no_duplicate_commit asserts exactly one post-rename commit. CAVEAT (not demoting): the DRY-RUN step-3 line (cli.py, `if not apply:`) hardcodes the pathspec as [dest, seats_rel] without the apply path's staged-pending check, so `--dry-run` on an already-migrated tree would print a commit naming the no-longer-existent seats.md. Cosmetic (dry-run mutates nothing) but the plan and the apply can disagree; noted for a later round.
