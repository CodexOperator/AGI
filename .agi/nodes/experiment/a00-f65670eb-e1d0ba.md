---
id: experiment:a00-f65670eb-e1d0ba
mint_id: 0da6bc3575bf418b81cb09d4c73cec77
type: experiment
parents:
  - hypothesis:l4-the-step-3-pathspec-names-seats-md-too-on-an-unmigrated-tree
next_edges: []
confidence: 0.9
edited_by: a00-f1668349
evidence_runs:
  - experiment:a00-f65670eb-e1d0ba
loop: hypothesis:l4-the-step-3-pathspec-names-seats-md-too-on-an-unmigrated-tree@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0806ad175af8dcc9
season: 2
title: A00 f65670eb e1d0ba
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f65670eb-e1d0ba

## Experiment

G15 fix-only round 4 (Prime mur-46 by name). The defect: on an UNMIGRATED tree
(seats.md present, posts.md absent -- this live tree), the shared step-3
pathspec understated the commit. `_post_rename_commit_targets` decided by
querying only the current INDEX (`git diff --cached --name-status -- seats_rel`).
In a --dry-run the `git mv` has not run, so no pending delete is staged and
seats.md was dropped from the pathspec -- while --apply runs the git mv first,
staging the delete, so the apply commit carried seats.md too. Dry-run printed
`posts.md` only; apply committed `posts.md + seats.md`. The two call sites
disagreed on the SAME tree state (the pre-fix real dry-run on this unmigrated
live tree printed `-- .agi/nodes/.geometry/posts.md` alone).

FIX (extensions/agi/bin/cli.py, `_post_rename_commit_targets` + its two call
sites ONLY): one helper now computes the pathspec for BOTH branches, predicting
apply's writes on the SAME tree state. seats.md is included whenever apply's
own git mv WOULD stage its delete: it is PENDING in the index (git mv ran) OR
still PRESENT ON DISK (this tree; the apply git mv will stage it). Signature
gained a `seats_abs` param, passed by both the dry-run (Region) and the --apply
commit site; the --delete-old region (L4.320's) was NOT touched. The docstring
was rewritten to state the new union rule.

PROOF (acceptance / build order):

1. NEW test `test_dry_run_unmigrated_matches_apply_commit` seeds the DEFAULT
   unmigrated fixture (seats.md present, posts.md absent), captures the dry-run
   step-3 path set, runs --apply, and asserts the dry-run path set EQUALS the
   committed rename-aware file set from `git diff-tree --no-commit-id
   --name-status -r HEAD`. It FAILED against the pre-fix helper (named
   `posts.md` only) and PASSES post-fix -- non-vacuous.

   The initial reading used `git show --name-only HEAD`, which collapses the
   step-3 commit (a git RENAME R068 seats.md->posts.md on an unmigrated tree)
   to the new path only; fixed by reading `--name-status` and taking every path
   field (both sides of the rename are paths the commit carried).

2. Existing `test_dry_run_names_both_while_seats_delete_pending` (staged-pending
   git mv) and `test_dry_run_names_only_posts_after_seats_delete_committed`
   (migrated + uncommitted edit) remain GREEN -- cases (3) and (4) of the spec.

3. Real-tree dry-run on this live UNMIGRATED tree from this checkout now names
   BOTH posts.md and seats.md and reports it changed nothing (never ran
   --apply against anything real).

Suite: `python3 -m pytest extensions/agi/tests/test_post_rename.py
 extensions/agi/tests/test_cli.py -q` -> 43 passed (was red: the new test
failed pre-fix, dry-run missing seats.md).

## Evidence

Real-tree dry-run (this live unmigrated checkout, `cli.py post-rename
--dry-run`, grep of step-2/3 + tail):

    [DRY ] git mv: git mv .agi/nodes/.geometry/seats.md .agi/nodes/.geometry/posts.md  -- rollback: git mv .agi/nodes/.geometry/posts.md .agi/nodes/.geometry/seats.md
    [DRY ] commit posts.md: git add .agi/nodes/.geometry/posts.md && git commit -m "post-rename: seats.md -> posts.md" -- .agi/nodes/.geometry/posts.md .agi/nodes/.geometry/seats.md  -- rollback: git reset --soft HEAD~1 && git mv posts.md seats.md
    dry-run: nothing changed

The step-3 pathspec names BOTH `posts.md` and `seats.md` (pre-fix named
`posts.md` only), and the tree stayed clean.

New test, pre-fix (proves non-vacuity):

    AssertionError: unmigrated dry-run must name BOTH posts.md and seats.md: ['.agi/nodes/.geometry/posts.md']

New test, post-fix (whole suite):

    43 passed in 14.87s

The commit really carried both paths (rename-aware read, from the fixture):

    R068	.agi/nodes/.geometry/seats.md	.agi/nodes/.geometry/posts.md

## Agent Notes
FIX: _post_rename_commit_targets one call predicts apply writes on SAME tree state — seats.md in pathspec when pending in index OR on disk; unmigrated dry-run names both, apply commit carries both, migrated stays posts-only. New test proved non-vacuous; 43 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-f1668349, L4.323 rung 4 fix-only). ACCEPTED as proved, parent-verified. Instruction: the dry-run plan and the apply commit compute their step-3 pathspec from ONE call that PREDICTS the apply writes on the SAME tree state; on an unmigrated tree (seats.md, no posts.md) the pathspec names BOTH, posts.md alone once migrated; a test seeds an unmigrated fixture and asserts dry-run printed pathspec == files in the apply commit, and migrated stays posts-only.

WHAT THE MACHINE DOES (cited to artifacts I built and ran, not to how code reads):
- PRE-FIX, my own run on this live unmigrated tree: cli.py post-rename --dry-run printed "git commit ... -- .agi/nodes/.geometry/posts.md" ONLY. The live tree has seats.md present and posts.md absent (confirmed by ls), so --apply would git mv first and stage the seats.md delete.
- POST-FIX, my own re-run: same command now prints "-- .agi/nodes/.geometry/posts.md .agi/nodes/.geometry/seats.md" followed by "dry-run: nothing changed".
- PARENT-RUN SUITE: pytest test_post_rename.py test_cli.py -q -> 43 passed in 13.55s.
- ARTIFACT READ: _post_rename_commit_targets now takes seats_abs and unions bool(seats_pending.stdout.strip()) or seats_abs.exists(); its two call sites pass seats_abs; the --delete-old region (L4.320) is untouched.

NEAR MISS: satisfying the words with a disk-only check (seats_abs.exists()) and dropping the index query would break the existing STAGED-PENDING case (git mv ran, seats gone from disk, delete still in the index) -- the pathspec would drop seats.md exactly where apply's git commit -- ... seats.md still needs it. The union keeps both. Conversely, an index-only check is the pre-fix bug. Both halves are load-bearing.

DEVIATION: the brief asked the new test to compare against git show --stat; the kid used git diff-tree --no-commit-id --name-status -r HEAD and documents why -- on an unmigrated tree the step-3 commit is a git RENAME (R068), and git show --name-only collapses it to the new path only, which would make the equality assertion vacuous. That is a STRENGTHENING, not a deviation from the criterion (the criterion is dry-run set == committed set); the rename-aware read is the honest oracle. ACCEPTED.

RESIDUE (for the Prime): the union rule keys on seats_abs.exists(), so a tree where seats.md is present but UNTRACKED, or where posts.md already exists AND seats.md is still on disk (a state apply would refuse), is not a case the new test covers; and the helper still trusts the index/filesystem at call time rather than reading the committed blob, so both branches regressing together would not be caught. Neither blocks this round.
<!-- THOUGHT:END -->
