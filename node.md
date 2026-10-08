---
id: experiment:a00-838c7a2d-aa07a2
mint_id: 7ca90c7bd4c74941ad3e63fd4f12b000
type: experiment
parents:
  - hypothesis:l4-the-dry-run-pathspec-and-the-alias-notice-say-only-what-is-true
next_edges: []
confidence: 0.85
edited_by: a00-0d8af889
evidence_runs:
  - experiment:a00-838c7a2d-aa07a2
loop: hypothesis:l4-the-dry-run-pathspec-and-the-alias-notice-say-only-what-is-true@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a08a31a94255a7da
season: 2
title: A00 838c7a2d aa07a2
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-838c7a2d-aa07a2

## Region A — the dry-run step-3 pathspec is built by the same code path apply uses

LOCATION: `extensions/agi/bin/cli.py`, `cmd_post_rename` step 3. Region A of the
three-region L4.318 fix. B/C owned by sibling kids; untouched here.

## The defect (reproduced)

Pre-fix, the **dry-run** branch hardcoded the pathspec
(`" ".join([str(dest), str(seats_rel)])`, ~L2142-2146) while the **apply**
branch computed it from a real staged-pending INDEX query (`git diff --cached
--name-status -- <seats_rel>` ~L2150-2154). So on a tree where the seats.md
delete was already committed, the dry-run printed `-- posts.md seats.md` — a
command that `git commit` rejects because the path is not in the index.

Verified verbatim on a scratch repo (state: rename committed, only posts.md in
index):

```
$ git commit -m probe -- posts.md seats.md
error: pathspec '.agi/nodes/.geometry/seats.md' did not match any file(s) known to git
rc=1
```

The dry-run lied about what `--apply` would touch.

## The fix

Extracted ONE shared helper, `_post_rename_commit_targets(repo, dest,
seats_rel)` (`cli.py` L2039-2060), that performs the staged-pending index query
and returns the target list. Both branches now call it:

- dry-run: `cli.py` L2171  `targets = _post_rename_commit_targets(repo, dest, seats_rel)`
- apply:   `cli.py` L2190  `targets = _post_rename_commit_targets(repo, dest, seats_rel)`

The apply branch's inline `seats_pending` / `targets` block was replaced by the
single helper call. The helper queries the index ONLY (`git diff --cached`) —
never `git mv` — so a dry-run changes nothing; the byte-identical / no-plan-file
test
(`test_dry_run_writes_no_plan_file_and_leaves_bytes_same`) still pins this.

## Dry-run step-3 lines observed, scratch repo (post-fix)

CASE (a) — seats.md DELETE still staged (`git mv` just run):

```
[DRY ] commit posts.md: git add .agi/nodes/.geometry/posts.md && git commit -m "post-rename: seats.md -> posts.md" -- .agi/nodes/.geometry/posts.md .agi/nodes/.geometry/seats.md  -- rollback: git reset --soft HEAD~1 && git mv posts.md seats.md
```

CASE (b) — seats.md DELETE committed:

```
[DRY ] commit posts.md: git add .agi/nodes/.geometry/posts.md && git commit -m "post-rename: seats.md -> posts.md" -- .agi/nodes/.geometry/posts.md  -- rollback: git reset --soft HEAD~1 && git mv posts.md seats.md
```

The stale `seats.md` is gone from the case-(b) plan; both agree with what apply
would run for the same tree.

## Proof

Two new tests in `extensions/agi/tests/test_post_rename.py` seed a
staged-pending state and assert the dry-run plan's pathspec equals the string
`--apply` PRINTs (its `[APPLY] commit posts.md:` line, the targets the apply
branch actually used — same code path, same pathspec):

- `test_dry_run_names_both_while_seats_delete_pending` — delete pending →
  plan and apply both name `posts.md seats.md`.
- `test_dry_run_names_only_posts_after_seats_delete_committed` — delete
  committed → plan and apply both name only `posts.md`.

`python3 -m pytest extensions/agi/tests/test_post_rename.py
extensions/agi/tests/test_cli.py -q` → **40 passed** (9.0s).

## Fresh-index trap (why `git show --name-only` is NOT the oracle)

Initial tests compared the dry-run plan against `git show --name-only HEAD`
of the applied commit. That failed in case (a): a staged rename commits by the
old path AND the new path together, but `git show --name-only` reports only
the DESTINATION path (git tracks it as one rename). The correct oracle for the
criterion "plan and apply pathspec agree" is the apply branch's printed step-3
line, which carries the actual `targets` list. Switched to that.

## Files changed (Region A only)

- `extensions/agi/bin/cli.py` — added `_post_rename_commit_targets`; both
  step-3 branches call it.
- `extensions/agi/tests/test_post_rename.py` — two new tests + one shared
  `_step3_paths` extractor.

## Agent Notes
Region A: extracted _post_rename_commit_targets shared by dry-run+apply step-3; dry-run no longer hardcodes seats.md. 2 new tests seed staged-pending delete, assert dry-run plan==apply printed pathspec (both / only-posts). 40 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Region A reviewed and accepted by parent a00-0d8af889, 2026-09-12. The kid replaced the dry-run branch hardcode with a shared helper `_post_rename_commit_targets` (cli.py:2039) called from BOTH step-3 branches (cli.py:2171 dry-run, cli.py:2190 apply). I verified the mechanism myself, not the report: read the diff, confirmed the helper performs the `git diff --cached --name-status -- <seats_rel>` index query (never git mv) and that the apply branch no longer carries an inline duplicate. I ran `pytest extensions/agi/tests/test_post_rename.py -q` -> 21 passed on the merged tree. The two new tests genuinely bite: case (b) asserts seats.md is absent from the dry-run plan and that plan == apply, both of which fail on the pre-fix hardcoded pathspec, so the scan is not vacuous. Non-blocking residue for a later round: the tests compare the two PRINTED lines rather than the index blob, which is the honest oracle for the criterion as worded but would not catch both branches regressing together.
<!-- THOUGHT:END -->
