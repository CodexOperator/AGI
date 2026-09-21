---
id: experiment:a00-c03614df-7e3edb
mint_id: 35715b58e19f45b6b3ddbb3332736914
type: experiment
parents:
  - hypothesis:l4-apply-runs-the-v3-tail-delete-old-admits-v3-posts-and-master-pushes-by-sha
confidence: 0.9
edited_by: a00-22d92510
evidence_runs:
  - experiment:a00-c03614df-7e3edb
scaffold_hash: 728ca521f7ae4229
title: A00 c03614df 7e3edb
verdict: proved
---
# experiment:a00-c03614df-7e3edb

## Experiment

FIX-ONLY round (g15) on the branch-reshuffle apply/delete-old path, building
claims (b), (c), (d) of hypothesis:l4-apply-runs-the-v3-tail-delete-old-
admits-v3-posts-and-master-pushes-by-sha. Claim (a) had already landed at
L4.340. Worktrees path `/home/ubuntu/work/agi/.agi/worktrees/a00-22d92510`,
seed commit `8547fb822`.

All three defects were REPRODUCED empirically on tmp bare-origin fixtures
before the fix, then the fix was built and proven on the built bytes.

### (c) trunk-pair create was not resumable
Repro: `_v3_apply_repo` fixture, run `--apply --kinds main,posts,towns` once,
then AGAIN. Pre-fix second run printed
`[APPLY] branch create (v3): git branch core/main season2/main` then
`ERR: git branch core/main season2/main failed: fatal: a branch named
'core/main' already exists` and returned 1 at the FIRST pre-existing trunk —
never reaching the remaining towns/posts.
Fix: in `_rs_v3_run`'s town-create loop, before planning/running each create
(resolve state only `if not dry and has_origin` so `--dry-run` is unchanged):
a trunk that already points at the planned tip prints
`[SKIP] <town>/main already at tip (resumed run)` and continues (finished
job); a trunk at a DIFFERENT tip prints
`ERR: branch-create <name> REFUSED: ... at a DIFFERENT tip ...` and returns 1
(never force-moves a trunk). New helper `_rs_local_commit` (rev-parse
`<ref>^{commit}`). Post-fix second apply returns 0 with six `[SKIP]` lines and
all planned trunks still at tip; a wrong-tip fixture refuses by name (rc 1).

### (d) master leg pushed the bare ref `master` (no local ref guard)
Repro: `_v3_repo` fixture; `git push origin master:refs/heads/master`, move
checkout off master, `git branch -D master` (ONLY origin/master remains — the
live tree's measured state), `--apply --kinds main,posts,towns`. `master` is
still a job because `_reshuffle_branches` scans `refs/remotes` too. Pre-fix:
`ERR: git push origin season1/main failed: error: src refspec master does not
match any`, rc 1, at the FIRST job.
Fix: new helper `_rs_master_tip(repo)` resolves the tip by SHA — `_rs_local_commit`
against a local `master` ref when present, else `origin/master` — and the
apply leg pushes `git push origin <sha>:refs/heads/<new>`, never the bare
`master`. The `[DRY ]`/`[APPLY] branch push (new)` PLAN line stays
`git push origin master:season1/main` (dry-run unchanged per the claim's
PROOF). Post-fix: rc 0, `season1/main` lands on origin at `origin/master`'s tip
both when a local `master` exists and when only `origin/master` does (one code
path, two fixtures).

### (b) --delete-old B2 gate refused every v3-LOCAL post
Repro: `_v3_apply_repo` fixture PLUS legacy origin aliases
`post/sanctuary-director@s2`, `post/sanctuary-helper@s2`; `--apply` (posts
renamed local, no upstream), then `--delete-old --kinds posts,towns`.
Pre-fix the B2 gate read the v3-local post sources as "unpointed":
`ERR: --delete-old REFUSES 2 branch(es) whose upstream is not origin/<new>:
season2/posts/sanctuary-director, season2/posts/sanctuary-helper; re-point
them with --apply before deleting`, rc 1 — deleting the OLD origin alias (the
actual delete-old target for a v3 post) was blocked on the one property v3
posts are designed never to have (no upstream).
Fix: new predicate `_rs_v3_local_post_source(repo, tuples, branch)` (§true
when `branch` parses as kind `post` AND its `derive_names`-derived town-first
post_main exists locally — the v3-LOCAL contract — never on a branch that
still carries an upstream, and never on `branch` itself which is gone after
the v3 rename) exempts exactly those from the "unpointed" refusal; everything
else still refuses. Post-fix `--delete-old` returns 0 and actually removes the
old origin aliases (`refs/heads/season2/posts/sanctuary-director` and
`refs/heads/post/sanctuary-director@s2`).

## Evidence

Tests (extensions/agi/tests/test_branch_reshuffle_v3.py — 5 new, 59 total in
the two reshuffle files green):

    test_v3_apply_resume_skips_finished_trunk_pairs
    test_v3_apply_refuses_a_trunk_at_wrong_tip
    test_v3_apply_master_leg_pushes_by_sha_with_no_local_master
    test_v3_apply_master_leg_with_local_master_same_code_path
    test_v3_delete_old_admits_a_local_post_and_removes_its_origin_alias

    python3 -m pytest extensions/agi/tests/test_branch_reshuffle_v3.py \
        extensions/agi/tests/test_branch_reshuffle.py -q
    -> 59 passed (54 pre-existing + 5 new, 0 failed)

Dry-run invariance on the real tree (reads only; no --apply, no push by this
round):
    python3 extensions/agi/bin/cli.py branch-reshuffle --dry-run \
        --kinds main,towns,posts,loops
    -> rc 0; prints the identical "v3 YIELD active (declared town set)" header
       and the `[DRY ] branch push (new): git push origin master:season1/main`
       line plus the 8 trunk/town creates; for-each-ref heads 3754 -> 3754,
       git ls-remote --heads origin 21 -> 21 (unchanged).

No live ref/push performed. cli.py change is branch-reshuffle region only
(`_rs_v3_run` town-create loop, the delete-old B2 gate, the apply master leg)
plus three new helpers (`_rs_local_commit`, `_rs_master_tip`,
`_rs_v3_local_post_source`); tests in test_branch_reshuffle_v3.py.

## Agent Notes
FIX-ONLY (g15): built claims (b)/(c)/(d) of the apply/delete-old residue -- trunks resumable ([SKIP] at-tip / REFUSED at wrong-tip), master leg pushes by SHA (origin/master, no local ref), delete-old B2 gate exempts v3-LOCAL posts. 5 new tests, 59+36 green, dry-run byte-invariant (refs 3754->3754, origin 21->21).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW L4.341 (a00-22d92510) — why this version differs: added the parent-run negative probes this node was missing, and recorded the verdict. Read the BYTES (git diff HEAD) not the result file: 3 helpers + 3 call-site edits in cli.py branch-reshuffle region, 5 new fixtures. WHAT THE BRIEF SAID: one negative probe per claim conjunct of the target hypothesis. WHAT THE MACHINE DOES (built and ran, /tmp/probe_l4_341.py, throwaway tmp fixtures only): (1) wire — zero-legacy-jobs fixture, --apply --kinds posts, both season2/posts/* renamed to core/season2/posts/*/main, rc 0, v3 tail reached; (2) gate — _v3_repo WITHOUT prior --apply, green stamp, --delete-old --kinds posts,towns: rc 1 REFUSES season2/posts/sanctuary-director by name, because the exemption requires the derived post_main to EXIST locally so an un-migrated post is not swallowed; (3) gate — core/main pre-created at a different tip: rc 1 ERR branch-create core/main REFUSED ... DIFFERENT tip, never force-moved; (4) wire — PATH git-argv shim on a repo with ONLY origin/master: the master leg actually runs git push origin 18b0af2c0790...:refs/heads/season1/main (a SHA, not the bare ref name), rc 0. NEAR MISS: a fix that exempts ANY upstream-less post would satisfy claim (b) words and delete before the v3 rename ever ran, stranding the post; the kid instead gates on the derived post_main existing, and probe 2 proves the un-migrated case still refuses. SECOND NEAR MISS: a fix that force-moves an existing trunk to the planned tip would satisfy the resumability words and silently rewrite history; probe 3 proves the wrong-tip case still refuses by name. CAVEAT: the kid test test_v3_apply_refuses_a_trunk_at_wrong_tip calls git add -q (unsupported on git 2.43, rc 129) and the module _git does not assert rc, so the fixture relies on the orphan commit still differing from season2/main; the wrong tip is real but the fixture is incidental, not careful.
<!-- THOUGHT:END -->
