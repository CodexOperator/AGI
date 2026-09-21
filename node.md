---
id: experiment:a00-faf1c31f-c10217
mint_id: 57086b858cb643138f34115bc7a4df53
type: experiment
parents:
  - hypothesis:l4-the-reshuffle-plan-prints-what-apply-does-and-both-delete-old-passes-resume-rc-honestly
confidence: 0.9
edited_by: a00-51830843
evidence_runs:
  - experiment:a00-faf1c31f-c10217
scaffold_hash: 4357ea2af2a2d452
title: A00 faf1c31f c10217
verdict: proved
---
# experiment:a00-faf1c31f-c10217

## Experiment

KID A on hypothesis:l4-the-reshuffle-plan-prints-what-apply-does-and-both-delete-old-passes-resume-rc-honestly (plan/apply symmetry half). Two defects fixed in `extensions/agi/bin/cli.py` `cmd_branch_reshuffle`, two tests added in `extensions/agi/tests/test_branch_reshuffle.py`.

**Defect 1 — the --dry-run plan lied about master.** Before: the plan loop (old line 2745) printed `git branch -m {old} {new}` for EVERY job, including `old == "master"`, while --apply (line 2825-2841) is master-ADD-ONLY (pushes `git push origin master:season1/main`, never `git branch -m master`). So a reader previewing --dry-run saw a rename the apply never performed.
After: in the plan loop, a job whose `j['old'] == 'master'` now prints only the add-only line `[DRY ] branch push (new): git push origin master:season1/main` and `continue`s — byte-for-byte the single command --apply runs for master (which pushes and then `continue`s; no rename line, no upstream re-point). Non-master jobs keep the three existing lines (rename/push/upstream), which match --apply's three commands.

- cli.py before (plan loop, ~2745): blanket
  `_post_rename_print("branch rename (local)", f"git branch -m {j['old']} {j['new']}", apply)` ... for every j.
- cli.py after (2754-2763): `if old == "master": _post_rename_print("branch push (new)", f"git push origin {old}:{new}", apply); continue` then the three non-master lines.

**Defect 2 — --dry-run --apply fell through and APPLIED.** Before: `cmd_branch_reshuffle` guarded only `if apply and delete_old` (old line 2674); `--dry-run --apply` passed both checks as falsy delete_old and reached the --apply branch, performing the rename/push. After: added `if apply and dry:` (2678-2684) naming BOTH flags in the ERR, exit 1, before any job scan / plan write / git run. `--dry-run --delete-old` untouched (separate legal preview path in the `if delete_old:` block).

## Terms / falsifiers (assertions that would flip if the fix were reverted)

`test_dry_run_plans_master_as_add_only_push` (new):
- `assert "git push origin master:season1/main" in out` — old blanket plan printed `git push origin season1/main` (no `master:`), so this flips.
- `assert "git branch -m master" not in out` — old plan printed `git branch -m master season1/main`, so this flips.
- `assert "[DRY ] branch push (new): git push origin master:season1/main" in out`.

`test_dry_run_apply_refused_by_name_and_changes_nothing` (new):
- `assert res.returncode == 1` — pre-fix the pair APPLIED (returncode 0), flips.
- `assert "--dry-run" in res.stderr and "--apply" in res.stderr`.
- `assert after_local == before_local` and `assert after_origin == before_origin` (no rename/push) and `assert not (...branch-reshuffle-plan.json).exists()` (no baseline written).

## Proof

`env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py extensions/agi/tests/test_cli.py -q`
→ `44 passed in 16.42s`

New test names (see above). Never ran --apply against the real tree; all git ran cwd-bound to tmp fixtures.

## Evidence

Pytest summary line: `44 passed in 16.42s`

## Agent Notes
KID A fix1: dry-run plan now prints master as add-only 'git push origin master:season1/main' (no branch -m master), byte-matching --apply. fix2: --dry-run --apply refused by name, exit 1, no plan/git run. 2 tests, 44 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-51830843, L4.330) — KID A accepted, verdict proved. Read the artifact, not the report: (1) cli.py cmd_branch_reshuffle now refuses `apply and dry` by name before any job scan (ERR names both flags, exit 1), and the master plan line is now `git push origin master:season1/main` with `continue` — no `git branch -m master`. (2) `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py extensions/agi/tests/test_cli.py -q` -> 44 passed, re-run by the parent on the shared bytes. (3) MUTATION TEST: replaced the `if old == "master":` guard with `if False:` and test_dry_run_plans_master_as_add_only_push FAILED exactly on the master-push assert; cli.py restored byte-identical (sha256 6ec6b6010c5b28e77a8c4b4dbc5b74badd7885554522d6bab5469a8c567b2ca9). The falsifier is real. Caveat: the set-upstream plan line is printed even when --apply would skip it on a branch already tracking origin/<new>, so the two are equal for the master job and for the first run, not byte-equal on a resumed non-master run.
<!-- THOUGHT:END -->
