---
id: experiment:a00-df6c2a0e-c4bf21
mint_id: bcb5ee2d4a134291be49299498a1c616
type: experiment
parents:
  - hypothesis:l5-branch-reshuffle-and-loop-prune-plan-exactly-todays-delta
next_edges: []
confidence: 0.72
edited_by: a00-27ce07b3
evidence_runs:
  - experiment:a00-df6c2a0e-c4bf21
line_ceiling: 40
loop: hypothesis:l5-branch-reshuffle-and-loop-prune-plan-exactly-todays-delta@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 81c0114e90929ac0
season: 2
title: "L5.01 round2: live-mirror-faithful fixture refuses 5 by name, hidden-ref fixture proves merge-up/behind-check"
town: core
verdict: inconclusive_lean_proved:72
---
<!-- BODY:BEGIN -->
# experiment:a00-df6c2a0e-c4bf21

## Experiment

KID A ROUND 2 on L5.01 (follow-up to the parent-demoted experiment:a00-841c14d5-844adf).
Fixture-proof ONLY — no live ref/branch/worktree touched. The parent review said the
round-1 fixture pre-pushed all 3 post + all 3 loop mirrors that the LIVE origin does not
have (measured at L5 open: only refs/agi/posts/sanctuary-director + sensei-director;
sanctuary-helper's post mirror and ALL refs/agi/loops/* are ABSENT), so "exactly today's
12" was true only against mirrors the live tree lacks, and claim (c) (hidden-ref
resolution) was NOT freshly fixture-proved. Round 2 closes both by TEST (changes live in
test_branch_reshuffle_v3.py; ZERO cli.py production lines — the mirror safety gate is
already sound and must stay; the parent ordered "do not weaken it").

(i) FIXTURE MADE FAITHFUL: `_build_l5_repo(tmp_path, mirrors="live")` is now the DEFAULT
and pushes ONLY the live mirror set; mirrors="full" (the round-1 bridge) pushes all 3 post
+ 3 loop mirrors. The two round-1 tests now run on the full state (l5repo_full) and still
assert EXACTLY the 12. Two NEW tests assert BOTH outcomes on the SAME command
`--dry-run --delete-old --kinds main,posts,towns,loops`:
  * FULL-mirror state -> exactly 12 deletes, nothing else (round-1 test held).
  * LIVE-mirror state (default fixture) -> plans the OTHER 7 delete lines and REFUSES the 5
    missing-mirror jobs BY NAME naming the absent ref (core/season2/posts/sanctuary-helper/main,
    season2/posts/sanctuary-helper -> refs/agi/posts/sanctuary-helper; season2/loops/l5-01-ag1,
    l5-01-ag2, l5-02-ag1 -> refs/agi/loops/*); the dry preview names them (rc 0) and a STAMPED
    real --delete-old REFUSES the whole pass non-zero (rc 1, "REFUSES 5 branch(es)"), deletes
    NOTHING (all 12 heads + trunks + 6 present towns still on origin). No silent drop ever,
    never a false "exactly 12 today" on a tree whose mirrors are incomplete.

(ii) CLAIM (c) FIXTURE-PROVEN with a real post worktree (`_hidden_ref_post_repo`): a v3
post branch exists ONLY as the local branch in its worktree + its hidden
refs/agi/posts/sanctuary-director mirror on a throwaway origin; NO
refs/heads/core/season2/posts/sanctuary-director/main head on origin (one of the 12 deletes).
Asserted: the origin head is GONE while the mirror SURVIVES; branches.mirror_ref_for_branch ==
the hidden mirror and branches.merge_target == derive_names("core",2)["town_season_main"]
("core/season2/main") — the merge-up path resolves by grammar, never the deleted head;
dispatch._stale_base_spawn(r, 2) (the F9 behind-check) fetches the season trunk and reports
status "current" (never a false stale claim, never "unchecked") with the post head gone;
and the post worktree still names the post branch (wired identity).

## Evidence

Measured outputs (probe, `--kinds main,posts,towns,loops`, LIVE-mirror fixture), dry-run:
```
[DRY ] branch delete (remote): ... core/season2/posts/sanctuary-director/main
[DRY ] REFUSE branch delete (remote, v3 successor absent on origin): core/season2/posts/sanctuary-helper/main -> would need refs/agi/posts/sanctuary-helper
[DRY ] branch delete (remote): ... core/season2/posts/sensei-director/main
[DRY ] branch delete (remote): ... season2/posts/sanctuary-director
[DRY ] REFUSE ... season2/posts/sanctuary-helper -> would need refs/agi/posts/sanctuary-helper
[DRY ] branch delete (remote): ... season2/posts/sensei-director
[DRY ] REFUSE ... season2/loops/l5-01-ag1 -> would need refs/agi/loops/l5-01-ag1
[DRY ] REFUSE ... season2/loops/l5-01-ag2 -> would need refs/agi/loops/l5-01-ag2
[DRY ] REFUSE ... season2/loops/l5-02-ag1 -> would need refs/agi/loops/l5-02-ag1
[DRY ] branch delete (remote): ... collaborator-branch
[DRY ] branch delete (remote): ... copilot/add-open-source-license
[DRY ] branch delete (remote): ... season2/sensei/genless-templates
NOTE: --delete-old would REFUSE 5 branch(es) ...
```
Stamped real run: rc 1, stderr names the 5, ls-remote confirms all 21 heads still present
(all-or-nothing wall). Round-1 full-mirror tests still pass exactly-12.

pytest (--basetemp /tmp/t-* subdirs): test_branch_reshuffle_v3.py + test_branch_reshuffle.py
+ test_post_wire.py + test_post_rename.py + test_branches.py + test_branches_v3.py -> **239 passed**.

## Agent Notes
fixture now faithful to live origin mirrors (only 2 post mirrors); asserts both: full-mirror=exactly12, live-mirror=7 planned+5 REFUSED BY NAME (stamped real rc1 deletes nothing, gate kept). Claim(c) hidden-ref post/worktree fixture proves merge-up grammar+dispatch F9 current. 0 cli production lines, 239 tests green.

PARENT REVIEW (a00-27ce07b3, L5.01) -- ACCEPT as inconclusive_lean_proved:72 (kept). Round 2 is TEST-ONLY (no cli.py production change; mirror gate kept sound) and closes every gap my round-1 probe named: (1) fixture now DEFAULT to the LIVE mirror state and asserts BOTH outcomes on the same command -- full-mirror state -> exactly 12 deletes nothing else; live-mirror state (measured origin: only posts/{sanctuary-director,sensei-director}, sanctuary-helper + all refs/agi/loops/* absent) -> the other 7 plan + the 5 REFUSED BY NAME naming the absent mirror, and a STAMPED real --delete-old REFUSES the whole pass rc 1 deleting NOTHING. My own probe_kidA_livemirrors.py (run before A2) produced exactly this 7+5 on the same live-mirror fixture, so A2 formalizes the parent probe as a passing test -- probe now consistent. (2) claim (c) fixture-proven with a real post worktree whose post branch exists ONLY locally + as refs/agi/posts/<post> (no refs/heads post on origin): branches.mirror_ref_for_branch/merge_target derive by grammar, dispatch._stale_base_spawn (F9) -> current, worktree names the post branch. 111 branch-reshuffle/loop-prune/post-wire tests pass on re-run. CAVEAT the round must carry: today live --delete-old reaches NEITHER 13 nor 12 -- it refuses 5 until the missing loop-post + loop mirrors are pushed (grid_sync/rotate, a SM.90-remnant state prerequisite, NOT a branch-reshuffle code gap); the Prime must satisfy that before L5.01-live.
