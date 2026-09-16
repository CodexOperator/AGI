---
id: experiment:a00-6ded7d52-9ebf6c
mint_id: 72f6ec57e3f240abb48c0cef4e635ae3
type: experiment
parents:
  - hypothesis:l4-sm25b-post-branches-mirror-lock-rename-delete-fixes
next_edges: []
confidence: 0.7
edited_by: a00-4d31ec4c
evidence_runs:
  - experiment:a00-6ded7d52-9ebf6c
loop: hypothesis:l4-sm25b-post-branches-mirror-lock-rename-delete-fixes@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "python3 -c \"import branches; print(branches.mirror_ref_for_branch('core/season2/posts/sanctuary-director/main'), branches.mirror_ref_for_branch('core/season2/posts/sanctuary-director/loops/L4.332/a00-x'), branches.mirror_ref_for_branch('season2/main'))\"", "expected": "refs/agi/posts/sanctuary-director refs/agi/loops/L4.332-a00-x None", "observed": "refs/agi/posts/sanctuary-director refs/agi/loops/L4.332-a00-x None", "result": "held"}
  - {"conjunct": 2, "class": "auth", "cmd": "VERIFY_SUITE_LOCK_PID=<live non-holder pid>; lock file holds a live foreign pid; verification._suite_lock_guard(groot)", "expected": "a marker naming a pid that is NOT the lock holder must NOT unlock the guard; only marker==holder proceeds, and it must not touch the file", "observed": "foreign+no marker -> refusal naming pid; marker=live non-holder -> refusal naming pid; marker=holder -> None with the lock file byte-unchanged; marker=dead pid 999999 -> refusal", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "tmp repo: HEAD on main (2c69cd1d) != season2/posts/adv2 (b15337b9); rotate._apply_surfaces(graph, [{'kind':'branch (origin)','action':'seam-git','src':'origin/season2/posts/adv','dst':'origin/season2/posts/adv2'}], delete_old=False, run_git=real, live=True)", "expected": "refs/agi/posts/adv2 on origin proves the RENAMED BRANCH tip b15337b9, never HEAD 2c69cd1d; no post head pushed", "observed": "mirror=b15337b9 == branch tip, != head 2c69cd1d; origin heads = main + season2/posts/adv only", "result": "held"}
  - {"conjunct": 4, "class": "gate", "cmd": "rotate._origin_head_delete_gate(repo, 'season2/posts/adv', delete_old=...) on a fixture bare origin; mirror either absent, diverged, or containing the head tip; plus an unreachable origin", "expected": "no flag -> 'dry' with the head surviving; flag but no/diverged proof -> 'refused' with the head surviving; unreachable ls-remote -> 'refused' (UNKNOWN, never absent); flag + containing proof -> 'deleted'", "observed": "dry/default head present; no-proof 'refused' head present; diverged 'refused' head present; unreachable 'refused'; containing proof -> 'deleted' with the origin head gone", "result": "held"}
profile: balanced
push_further: the LIVE migration of the three existing origin post heads and the loops preserve-then-drop round (mirror push + ls-remote proof first, preserving unharvested head hypothesis:l4-the-ack-prints-onl-a00-b6b11bd7), and retiring the F7 window ask from WORKTREE_POST_CLOSEOUT_STEPS; plus the engine defect this round found -- _auto_commit_worktree (cli.py:1675) cannot commit a --branch KID because extensions/agi/hooks/agent-git/pre-commit refuses every AGI_TIER=kid commit, so a --branch kid's branch never advances
role: kid
scaffold_hash: f14ea3a6e2883fa9
season: 2
title: A00 6ded7d52 9ebf6c
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6ded7d52-9ebf6c

SM.25b — four post-branch defects built and proved on the rebased SM.250 bytes.
Base: `git merge --no-ff season2/loops/hypothesis-l4-post-branches-are--a00-ea1066f0`
into `season2/loops/hypothesis-l4-sm25b-post-branche-a00-6ded7d52`. Three
conflicts, resolved as ordered: the hypothesis node keeps OUR (SM demote) side;
`rotate.py` auto-merged (both sides kept); `test_rotate.py` keeps BOTH sides.

## Pre-fix measurement (command + output, one per defect)

**(1) `mirror_ref_for_branch` returns None for every live seat's spelling**

    $ python3 -c "import branches; ..."
    core/season2/posts/sanctuary-director/main
      | parse.kind= v3_post | mirror_ref_for_branch= None
    core/season2/posts/sanctuary-director/loops/L4.332/a00-x
      | parse.kind= v3_loop | mirror_ref_for_branch= None

The helper recognised only `post`/`loop`, never `v3_post`/`v3_loop` — the feature
is dead for every real seat.

**(2) the suite-lock guard refuses the lock merge-up is itself holding**

    $ python3 -c "lock file <- pid 1; os.environ['VERIFY_SUITE_LOCK_PID']='1';
                  verification._suite_lock_guard('/tmp/slk')"
    'suite: lock held by 1 since 09:40:15Z — refusing, not spawning'

`guard reads VERIFY_SUITE_LOCK_PID: False` — the marker is not read at all, so
`verification.py --suite` exits `EXIT_SUITE_LOCKED` before pytest spawns.

**(3) rename-apply mirrors HEAD, not the renamed branch**

`rotate.py:3574` (incoming): `branches.mirror_and_prove(_top, _mirror, run=…,
label=…)` — `tip` left at its `"HEAD"` default, then `_src` is deleted on that
false proof.

**(4) merge-up deletes an origin head unconditionally**

`rotate.py:3999` (incoming): `hok, hdetail = _drop_origin_post_head(main,
branch)` with no flag, no containment check; `grep -n delete_old rotate.py`
showed the flag existed only on the rename-post subparser (`:19550`), none on
`merge-up`.

## The fixes (production lines: branches.py 4, verification.py 14, rotate.py 52 — under the 120 ceiling)

1. `branches.mirror_ref_for_branch` recognises `v3_post`/`v3_loop` and derives
   through `mirror_ref` exactly as the season-first arms do (`season` is 0 for a
   v3 record and does not enter the ref). Post-fix:
   `core/season2/posts/sanctuary-director/main -> refs/agi/posts/sanctuary-director`;
   `.../loops/L4.332/a00-x -> refs/agi/loops/L4.332-a00-x`.
2. `verification.SUITE_LOCK_MARKER` (`"VERIFY_SUITE_LOCK_PID"`) is defined next
   to `SUITE_LOCK`; `_suite_lock_guard` reads it FIRST and, when a marked live
   pid IS the lock file's current holder, returns None **without touching the
   file** — the caller keeps holding the lock across the suite. Reuses
   `_pid_alive`; no second liveness test. `rotate._merge_up_suite` now exports
   `verification.SUITE_LOCK_MARKER` into the child.
3. `_apply_surfaces` live arm proves `tip=_dst` — the RENAMED BRANCH'S OWN tip.
   An unresolvable tip is a refusal by name from `mirror_and_prove`; there is no
   fall back to HEAD.
4. One gate, `_origin_head_delete_gate(repo, branch, delete_old=…)`, used by
   `cmd_merge_up`; the rename live arm uses the shared `_containment_proof`.
   Both REUSE `cli._rs_ls_remote_sha` / `cli._rs_containment_state` (the ONE
   containment implementation) against the clause-(2) `refs/agi/…` mirror. No
   `--delete-old` ⇒ `dry`: the plan is printed and nothing is deleted. An
   `ls-remote` that fails is UNKNOWN and refuses. `merge-up` gained
   `--delete-old`; `--dry-run` now prints the delete plan too.

## Passing test output

    $ python3 -m pytest extensions/agi/tests/test_branches.py \
        extensions/agi/tests/test_rotate.py extensions/agi/tests/test_rename_post.py \
        extensions/agi/tests/test_verification.py -q
    440 passed, 339 warnings in 38.07s

    $ python3 -m pytest extensions/agi/tests/test_rotate_closeout_steps.py \
        extensions/agi/tests/test_branch_reshuffle_v3.py extensions/agi/tests/test_bin_help_smoke.py -q
    (1 failed, 64 passed, 3 skipped) — the 1 is the pre-existing `ws_raw.py
    --help` red (that binary has no `--help`), not this round.

    $ python3 -m pytest <every tests/*.py that imports rotate> -q
    1243 passed, 1 xfailed, 966 warnings in 135.76s

## Negative probes (one per fix, named)

- **(1)** `test_mirror_ref_for_branch_resolves_v3_town_first_post_and_loop` also
  asserts a v3 TRUNK (`core/season2/main`) still returns None — recognition is
  by kind, not "anything v3".
- **(2)** `test_suite_lock_guard_marker_naming_the_holder_proceeds` second arm: a
  marker naming a DIFFERENT live pid (7) is still a foreign hold and the guard
  still refuses, naming 424242; the pre-fix refusal test above it is unchanged.
- **(3)** `test_rename_apply_mirror_proof_is_keyed_to_the_branch_tip_not_head`
  parks HEAD on `master` (asserted `!=` the post tip) and asserts the mirrored
  sha `== post_sha` and `!= head_sha`. Pre-fix this mirrored `head_sha`.
- **(4a)** `test_merge_up_without_delete_old_prints_plan_deletes_nothing`: the
  head survives and the plan line `plan: would delete refs/heads/season2/posts/adv`
  is printed.
- **(4b)** `test_origin_head_delete_refuses_without_a_containment_proof`: the
  mirror holds `master` (an ANCESTOR of the head), `merge-base --is-ancestor`
  returns 1 ⇒ `('refused', '… diverged')` and the origin head survives.

## Evidence

```
parse v3_post -> v3_post | mirror_ref_for_branch -> refs/agi/posts/sanctuary-director
parse v3_loop -> v3_loop | mirror_ref_for_branch -> refs/agi/loops/L4.332-a00-x
POST-FIX guard (marker names the holder): None
POST-FIX guard (marker names a DEAD pid): suite: lock held by 1 … — refusing
```

Updated for the new contract: `test_merge_up_proves_mirror_then_drops_pre_existing_origin_head`
now passes `delete_old=True`; `test_live_apply_runs_real_git_argv`'s fake
`rev-parse` returns the branch tip and `--show-toplevel` for `_git_toplevel`.
<!-- BODY:END -->

## Agent Notes
SM.25b: all four post-branch defects built and proved on the rebased SM.250 bytes. (1) branches.mirror_ref_for_branch now recognises v3_post/v3_loop (live-seat spellings) -> refs/agi/posts|loops/<leaf>. (2) verification.SUITE_LOCK_MARKER + a marker arm in _suite_lock_guard: a marked live pid that IS the lock's holder PROCEEDS without touching the file, so merge-up's own lock no longer refuses its suite. (3) rename-apply proves tip=_dst (the renamed branch's own tip), never HEAD; unresolvable tip is a refusal by name. (4) one _origin_head_delete_gate: every merge-up origin-head delete is --delete-old-gated, dry-run by DEFAULT (plan printed), and refused without a containment proof reusing cli._rs_containment_state against the refs/agi mirror; merge-up gained --delete-old. Tests: 440 passed (test_branches/test_rotate/test_rename_post/test_verification); 1243 passed across every tests/*.py importing rotate. One negative probe per fix, named in the node.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) INSTRUCTION -- the target claim says to fix four defects IN ORDER and prove each with a parent-run negative probe: "(1) the mirror helper resolves the actual town-first spelling every live seat carries; (2) merge-ups own suite-lock acquisition never blocks on a lock it itself already holds; (3) rename-applys mirror-then-delete proves the sha of the BRANCH BEING RENAMED, never the toplevel HEAD; (4) every origin-head deletion in merge-up and rename-apply runs behind a --delete-old flag, requires a containment proof before deleting, and DEFAULTS TO A DRY RUN".

(2) WHAT THE MACHINE DOES -- measured by the PARENT on the bytes the kid produced, not read off the kid's report. (a) branches.py mirror_ref_for_branch now tests `kind in ("post","v3_post")` / `("loop","v3_loop")`; the parent probe prints refs/agi/posts/sanctuary-director for core/season2/posts/sanctuary-director/main, refs/agi/loops/L4.332-a00-x for the v3 loop spelling, and None for season2/main. (b) verification.py grows SUITE_LOCK_MARKER and a marker arm in _suite_lock_guard; the parent probe shows a live FOREIGN holder still refuses, a marker naming a LIVE NON-HOLDER still refuses, a DEAD marker pid still refuses, and marker == holder returns None with the lock file byte-unchanged. (c) rotate.py _apply_surfaces' `branch (origin)` arm calls mirror_and_prove(..., tip=_dst); on a two-sha fixture (HEAD main 2c69cd1d, renamed branch season2/posts/adv2 b15337b9) the parent probe finds refs/agi/posts/adv2 proving b15337b9 -- the renamed branch's OWN tip -- never 2c69cd1d, and no post head on origin. (d) rotate.py _origin_head_delete_gate is now the ONE caller of _drop_origin_post_head (single call site, rotate.py:3925) and the merge-up subparser carries --delete-old; the parent fixture shows no-flag -> 'dry' with the head surviving, no proof / diverged mirror / unreachable ls-remote -> 'refused' with the head surviving, containing proof -> 'deleted'.

(3) THE NEAR MISS -- the shape that satisfies the words and loses the mechanism. On (b): an arm written as "a marker pid is set and alive -> proceed" passes the kid's own test (which sets marker=holder) and hands any spawned runner the lock; the built arm requires `_holder == _mpid`, which is exactly why the adversarial probe still refuses. On (d): returning the string 'dry' while still reaching the delete would read as flag-gated; the gate is that _drop_origin_post_head has exactly ONE call site and it sits below `delete_old` and the containment walk. On (1): the merge could have satisfied "rebased onto the dispatching tip" by taking the SM.250 file whole and dropping the parent tip's later hunks; the parent checked the deletions instead of the claim -- `git diff HEAD --numstat` shows 9 deletions in rotate.py, all of them the pre-fix `run_git("push","origin",_dst)` / signature lines SM.250 itself replaced, so no parent-tip hunk was lost.

(4) DEVIATION AND ROUND DEFECT. The kid's own `done` COULD NOT COMMIT ITS WORK, and the cause is the round's shape, not the kid. cli.py:_auto_commit_worktree (cli.py:1675) runs `git commit` on every tier's `done`; dispatch exports core.hooksPath to extensions/agi/hooks/agent-git, whose pre-commit final block refuses every commit whose AGI_TIER is `kid`. Run directly with the kid's env the hook prints `agi: tier kid may not commit -- automation owns git (goal:s27)` and exits 1. So a `--branch` KID can never land its own branch -- the branch tip stays at the parent's tip -- and the kid's node and its 16 changed paths sat uncommitted in the kid's worktree. I repaired it by adopting those bytes into the parent's loop branch (the parent tier on season*/loops/* is the hook's ONE authorised commit) and byte-comparing each one. The defective decision is the PARENT's `--branch` on a kid: the sanctioned shape for a KID is the shared parent worktree, where the parent's `done` commits. Recorded here because the next parent to pass `--branch` to a kid will lose the round the same way.
<!-- THOUGHT:END -->

## Agent Notes
SM.25b ACCEPT: all four defects built and parent-probed on the rebased SM.250 bytes -- mirror helper resolves both v3 town-first seat spellings; the suite-lock marker arm proceeds only when the marker pid IS the holder (a live non-holder and a dead pid both still refuse); rename-apply proves the renamed branch's own tip, never HEAD; _drop_origin_post_head has one call site behind --delete-old + a containment proof, dry-run by default. Kid work reached me UNCOMMITTED: the kid-tier pre-commit hook refuses the auto-commit, so the parent adopted the 16 changed paths byte-for-byte.
