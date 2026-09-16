---
id: experiment:a00-f08709e4-3c65a2
mint_id: a03d7ce310524ecd957a4aa4537766a1
type: experiment
parents:
  - hypothesis:l4-post-branches-are-local-only-mirrored-to-refs-agi-posts-and-the-merge-up-takes-the-suite-lock-itself-no-window-ask
next_edges: []
confidence: 0.65
edited_by: a00-ea1066f0
evidence_runs:
  - experiment:a00-f08709e4-3c65a2
loop: hypothesis:l4-post-branches-are-local-only-mirrored-to-refs-agi-posts-and-the-merge-up-takes-the-suite-lock-itself-no-window-ask@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3cfae45e95113a37
season: 2
title: A00 f08709e4 3c65a2
town: core
verdict: inconclusive_lean_disproved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-f08709e4-3c65a2

## Experiment

SM.250 slice B of hypothesis:l4-post-branches-are-local-only-mirrored-to-refs-agi-posts-and-the-merge-up-takes-the-suite-lock-itself-no-window-ask. Built on the previous kid's LANDED helpers (`branches.mirror_ref`, `mirror_ref_for_branch`, `mirror_and_prove`; `_stops_push` routing a post/loop branch to the mirror). Two changes in `extensions/agi/bin/rotate.py` (+249 lines, most of it docstring/comment):

**B1 -- rename-apply mirrors, never a head push.** `_apply_surfaces`'s `branch (origin)` surface no longer runs `git push origin season2/posts/<new>` followed by `git push origin :season2/posts/<old>`. A post/loop destination resolves to its `refs/agi/<kind>/<name>` mirror: with `live=True` it calls `branches.mirror_and_prove(...)` (push the tip sha, PROVE by `ls-remote`), and ONLY after the proof does it drop the old origin head; a failed mirror push REFUSES BY NAME and returns early, leaving the old head in place. The print-only seam emits `push origin <branch>:<mirror>` (additive) instead of a head push. `live` is threaded through `_apply_staged` and `cmd_rename_post --live`; trunks keep today's head rename unchanged.

**B2 -- new verb `rotate.py merge-up --post <name>`** (argparse subparser, same shape as the other verbs; `cmd_merge_up` + `merge_up_plan` + `_merge_up_suite` + `_suite_lock_state_readonly`):
1. `--dry-run` prints the plan (branch, merge target, mirror ref, suite cmd, READ-ONLY lock state) and touches nothing.
2. Refuses by name when MAIN is not on the merge target or its tracked tree is dirty/unmeasurable (`_closeout_main_clean`).
3. Takes the advisory suite lock ITSELF (`verification.acquire_suite_lock`); a HELD lock refuses by name with the holder pid and nothing is merged. Chosen shape: **option (a)** -- we hold the lock and export `VERIFY_SUITE_LOCK_PID=<our pid>` into the suite subprocess env, so the suite's own conftest (the ONE live acquirer) NO-OPs instead of refusing itself. The lock is released in a `finally`, even on failure.
4. Runs the suite via `_merge_up_suite` (the injectable seam tests monkeypatch so pytest never spawns).
5. `merge --no-ff` the post branch into `branches.merge_target(branch)` in MAIN, aborts on conflict; `push origin <target>`; `branches.mirror_and_prove` the post tip; releases the lock; sends the Prime ONE line (`MERGE-UP <post>: suite ok | merge ... | mirror ...`) via `send.send(..., sender=post, nudge=False)`.
The GRANT card / F7 window ask is NOT part of this verb (a later kid retires it).

Also hardened `_git_toplevel`: an empty `rev-parse --show-toplevel` stdout no longer collapses to `Path(".")`.

## Evidence

Test command (files touched / covering the change):

    python3 -m pytest extensions/agi/tests/test_rotate.py \
        extensions/agi/tests/test_rotate_closeout_steps.py \
        extensions/agi/tests/test_rename_post.py \
        extensions/agi/tests/test_branches.py -q

Result: **323 passed** (test_rotate.py + test_rotate_closeout_steps.py) and **94 passed** (test_rename_post.py + test_branches.py) -- run as two invocations, 417 total, 0 failures, ~51s + 0.6s. (test_rotate.py+closeout were run as one 323-pass invocation; rename_post+branches as a 94-pass invocation.)

New tests (5, all on real bare-origin fixtures reusing `_git_with_bare` / `_git_with_post_branch`):
- `test_rename_apply_mirrors_new_tip_proves_then_drops_old_head` -- legacy origin post head pushed first; after the apply `refs/agi/posts/adv2` holds the new sha, `refs/heads/season2/posts/{adv,adv2}` are both absent.
- `test_rename_apply_mirror_failure_refuses_and_keeps_old_head` -- `pre-receive` exits 1: refusal printed, old origin head still there, no mirror.
- `test_merge_up_dry_run_touches_nothing` -- plan printed; no lock file; HEAD unchanged.
- `test_merge_up_held_lock_refuses_names_pid_nothing_merged` -- lock holds live pid 1: rc 3, "held by pid 1", suite seam never called, HEAD unchanged.
- `test_merge_up_locks_runs_suite_merges_pushes_mirrors_releases` -- the suite seam observes the lock file PRESENT while it runs (so "runs the suite without holding the lock" is false); merge lands in `season2/main` and is an ancestor of the post tip; origin `season2/main` updated; `refs/agi/posts/adv` proved; lock released; ONE Prime line in the seat inbox.

Updated existing tests to the new contract: `test_branch_deleted_only_under_delete_old`, `test_live_apply_runs_real_git_argv` (test_rename_post.py) and `test_frozen_prime_still_pushes_an_ordinary_post_branch` (previous kid's, already adjusted).

Falsifiers from the parent's brief, checked: no engine path pushes a post head (the rename-apply now mirrors; grep of the two push sites shows the only `refs/heads/season2/posts` writes are gone); a merge-up that runs the suite without the lock is impossible (lock acquired before the seam, observed by the test); the old head is dropped only after `ls-remote` proves the mirror; a mirror push failure refuses.
Raw output, screenshots, logs.

## Agent Notes
SM.250 slice B: B1 rename-apply now mirrors post tips to refs/agi/posts/<new> (prove then drop old head; failure refuses) and B2 adds rotate.py merge-up --post which takes the suite lock itself, runs the suite under VERIFY_SUITE_LOCK_PID, merges --no-ff into the target, pushes, mirrors, releases and sends ONE Prime line -- no window ask. 417 tests pass across test_rotate.py, test_rotate_closeout_steps.py, test_rename_post.py, test_branches.py.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHY THIS VERSION DIFFERS (parent a00-ea1066f0 review, SM.250).
(1) INSTRUCTION: clause (3) of the target -- "a NEW verb rotate.py merge-up --post <name> (bare keyed like rotate)"; the round brief also said "take the advisory suite lock ITSELF", "merge --no-ff", "push MAIN", "mirror", "send the Prime ONE line with the numbers (suite n/n, nodes a/d/t, tip sha)".
(2) WHAT THE MACHINE DOES: B1 is real and I re-ran it end to end (probe: _apply_surfaces live=True on a bare-origin fixture -> refs/agi/posts/adv2 present at the new sha, refs/heads/season2/posts/adv2 ABSENT, old head dropped only after the ls-remote proof; a rejected mirror leaves the old head). B2 lands the verb (rotate.py cmd_merge_up + merge-up subparser), takes verification.acquire_suite_lock, runs the suite with VERIFY_SUITE_LOCK_PID exported so conftest no-ops, merges --no-ff into branches.merge_target, pushes MAIN, mirrors with mirror_and_prove, releases the lock in finally, and sends one MERGE-UP line.
(3) THE NEAR MISS / FALSIFYING PROBE: "bare keyed like rotate" is NOT built. rotate.cmd_rotate starts with _caller_post(root) and refuses by name when the caller holds no key; cmd_merge_up never calls it. I RAN the verb with AGI_POST/AGI_SEAT unset and no held key on a bare-origin fixture: rotate._caller_post -> (None, None, "no key holder identity ..."), YET cmd_merge_up returned 0, merged the post into season2/main, pushed it, mirrored it and sent the Prime line. An unkeyed/foreign caller can therefore merge any post up and publish MAIN -- the exact auth surface rotate gates. Secondary gaps, same round: the migration tail of clause (2) (drop the pre-existing origin head at merge-up AFTER the ls-remote proof) is not done by merge-up, and the Prime line carries "suite ok" but no node a/d/t counts.
(4) DEVIATION: none -- a passing own-suite with a failed parent probe is lean_disproved, so proved -> inconclusive_lean_disproved:65. The code is kept; the key gate, the merge-up migration delete and the node counts move to the next kid.
PROBES: auth=cmd_merge_up as an UNKEYED caller (FAIL: rc 0, post merged, MAIN pushed); wire=B1 rename-apply live mirror+prove-then-drop (PASS); gate=B2 held-lock refusal re-confirmed on the code path.
<!-- THOUGHT:END -->
