---
id: experiment:a00-580bb282-79e2d3
mint_id: 5164a4594b494f7cb7cfd7385899f971
type: experiment
parents:
  - hypothesis:l4-a-seat-is-a-post-everywhere
next_edges: []
confidence: 0.9
edited_by: a00-930daa46
evidence_runs:
  - experiment:a00-580bb282-79e2d3
loop: hypothesis:l4-a-seat-is-a-post-everywhere@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2b9f341fe4b078b1
season: 2
title: A00 580bb282 79e2d3
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-580bb282-79e2d3

## Experiment

L4.306 FIX-ONLY (kid 4 of 4). Owned `extensions/agi/bin/cli.py` (`cmd_post_rename`
+ helpers) and `extensions/agi/tests/test_post_rename.py`. The `post-rename
--dry-run|--apply` migration (landed L4.299) was held from the live step for
four gaps. I fixed all four on the throwaway git fixture only, never the live
tree:

1. **UPSTREAM after the branch rename.** New step 7 runs
   `git branch --set-upstream-to origin/post/<n>@s2` for each renamed branch
   when an `origin` remote exists (placed AFTER the push so the
   `origin/post/<n>@s2` remote-tracking ref exists to bind to). Without it a
   bare `git push` in a renamed worktree fails.
2. **COMMIT + PUSH posts.md as its own step.** New step 3 stages
   (`git add <dest>`), commits (`git commit -m "post-rename: seats.md ->
   posts.md"`), and pushes the current branch when origin exists. Leaves no
   dirty tree for the ack dirty-gate.
3. **`--apply` resumable per step, idempotent.** A plan file
   `<root>/sessions/post-rename-plan.json` records each finished step; a re-run
   skips done steps, and each sub-operation ALSO self-skips via an
   idempotency probe (posts.md present && seats.md gone -> skip git mv;
   post-<n> worktree present -> skip move; post/<n>@s2 branch present -> skip
   rename; origin ref state probed via ls-remote; upstream via
   `@{upstream}`). A failed step writes the plan recording what completed so a
   re-run resumes. Every step prints its ROLLBACK. `--dry-run` writes NO plan
   file and still changes nothing.
4. **`--seat` deprecated-alias line.** cli.py declares NO `--seat` argparse
   arg (verified by grep), so there was nothing to convert here; remaining
   `--seat` sites live OUTSIDE cli.py (heal.py, mail_alert.py, send.py,
   verification.py, sensei.py, rotate.py, season.py, dispatch.py,
   seat_status.py, brief.py, handoff.py) — another round owns those.

Key correctness note: the git-mv SOURCE is always `seats.md` (cfg.parent/
"seats.md"), never whatever geometry_config.resolve returns — post-first
resolve returns posts.md on a re-run, which would otherwise re-move the wrong
file. jobs come from `_post_rename_jobs` which only collects rows whose
worktree cell starts `seat-`, so on a re-run jobs==[] and all loops no-op.

Run: `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_post_rename.py -q`
  -> `11 passed in 3.63s`

## Evidence

- 4 existing tests (dry-run, apply-in-order, mint-id, worktree-dirs,
  remote-ref-delete) and the two L4.300 write-path tests all still pass.
- 4 new tests added, all green:
  * `test_apply_sets_upstream_and_commits_posts_clean` — (a)+(b): upstream ==
    origin/post/<n>@s2 after apply; posts.md committed (clean status, at HEAD)
    and current branch pushed to origin.
  * `test_apply_second_run_is_idempotent_noop` — (c): second --apply exits 0,
    status + refs byte-identical to after the first.
  * `test_dry_run_writes_no_plan_file_and_leaves_bytes_same` — (d): status
    unchanged, no posts.md, NO plan file written.
  * `test_apply_records_plan_and_rerun_resumes` — plan file records all six
    steps done; re-run exits 0 on the migrated tree.
- Full dry-run output (verified by hand) now prints commit/upstream steps and
  a rollback line for every step; ends with "dry-run: nothing changed".
- `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_post_rename.py extensions/agi/tests/test_cli.py extensions/agi/tests/test_cli_trimguard.py -q`
  -> `35 passed in 4.02s`

## Agent Notes
post-rename 4-fix: set upstream after branch rename; commit+push posts.md as own step; resumable/idempotent via sessions/post-rename-plan.json with per-step rollback; cli.py has no --seat so used SeatAction not needed (remains in 11 other bin files). 11 tests green.

L4.306 kid4 ACCEPTED proved (parent a00-930daa46): post-rename --apply gains upstream binding, an own commit+push posts.md step, resumable/idempotent plan file with per-step rollback; 35 passed on test_post_rename+test_cli+test_cli_trimguard. SeatAction --seat once-per-process sweep remains outside cli.py (11 bin files).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review L4.306 (a00-930daa46): reviewed the ARTIFACT, not the report. Verified in the bytes: cli.cmd_post_rename now (a) runs git branch --set-upstream-to origin/post/<n>@s2 after each branch rename when origin exists, (b) has a distinct commit-posts.md step (git add dest, git commit, git push origin cur) with its rollback so the tree is left clean, (c) records per-step completion in .agi/sessions/post-rename-plan.json and self-skips via idempotency probes (posts.md present and seats.md gone -> skip git mv; post-<n> worktree present -> skip move; post/<n>@s2 present -> skip rename) with a printed rollback per step, and dry-run writes no plan file. The git-mv source is always seats_abs, never geometry_config.resolve output, so a re-run cannot re-move posts.md. Ran the owned plus CLI files myself: 35 passed in 4.05s. ACCEPTED proved for this slice. CAVEAT recorded: the SeatAction clause (the deprecated --seat notice once per process at every accepting site) is UNSATISFIED -- cli.py declares no --seat arg, and the kid correctly listed the 11 other bin files that still declare --seat without geometry_config.SeatAction; that sweep is outside this round file list and is left for a later round.
<!-- THOUGHT:END -->
