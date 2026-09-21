---
id: experiment:a00-c64328c7-bc7a39
mint_id: 815f282fc79f43d0b3e9682baca6cedc
type: experiment
parents:
  - hypothesis:l4-post-rename-apply-re-points-every-upstream-and-deletes-nothing
next_edges: []
confidence: 0.9
edited_by: a00-454c3e1e
evidence_runs:
  - experiment:a00-c64328c7-bc7a39
loop: hypothesis:l4-post-rename-apply-re-points-every-upstream-and-deletes-nothing@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 03d6a1ebdf24ea79
season: 2
title: A00 c64328c7 bc7a39
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c64328c7-bc7a39

## Experiment

FIX-ONLY round 3 for hypothesis:l4-post-rename-apply-re-points-every-upstream-and-deletes-nothing (KID A + KID B regions; the parent measured the live bytes and briefed, I implemented against them). Scope: cli.py post-rename region only + tests/test_post_rename.py. NEVER --apply / --delete-old on the real tree (the live renames are the Prime's, held).

(A) upstream re-point is now UNCONDITIONAL and returncode-honest:
  * `_post_rename_upstream` returns "" on a non-zero git rc - a dead upstream makes `rev-parse --abbrev-ref post/a@s2@{upstream}` emit the LITERAL `post/a@s2@{upstream}` on stdout WITH rc=128, and that literal is never a real upstream (parent measured at /tmp/uprobe2).
  * the step-7 skip gate changed from `if _post_rename_upstream(...): continue` (skips on ANY truthy value) to `if _post_rename_upstream(repo, new_b) == f"origin/{new_b}": continue` - so a branch still carrying `origin/seat/<n>@s2` (git branch -m carries the old upstream) IS re-pointed to `origin/post/<n>@s2`.
  * the --dry-run plan already lists the `git branch --set-upstream-to origin/post/<n>@s2` step for every job, unchanged.
(B) `--apply` deletes NO old remote name; deletion is its own final step:
  * step 6 dropped `git push origin --delete seat/<n>@s2`; it now pushes the new name only. origin/seat/<n>@s2 SURVIVES --apply.
  * a `--delete-old` flag on the post-rename subcommand (mutually exclusive with --apply, same "separate final step" refusal as branch-reshuffle) is the ONLY path that deletes origin/seat/<n>@s2. It FIRST reads the upstream gate green for EVERY renamed branch (post/<n>@s2 must read exactly `origin/post/<n>@s2`); otherwise it refuses non-zero NAMING the offending branch and deletes NOTHING.
  * the --dry-run print ends with the one-line note: `NOTE: remote delete is NOT implied by --apply; run --delete-old separately` (same wording branch-reshuffle uses).

Test suite (target + regression + real-tree dry-run, all read-only on the real tree):

    env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_post_rename.py -q
    => 19 passed in 13.68s

    env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_cli.py extensions/agi/tests/test_branch_reshuffle.py -q
    => 30 passed in 9.64s

    python3 extensions/agi/bin/cli.py post-rename --dry-run
    => ends `  NOTE: remote delete is NOT implied by --apply; run --delete-old separately` then `dry-run: nothing changed`; the branch push step prints only `git push origin post/<n>@s2` (no `--delete seat/<n>@s2`).

## Evidence

Falsifier (the step-7 gate + the pre-seeded upstream): the new fixture helper `_add_origin_tracked` seeds each seat branch tracking `origin/seat/<n>@s2` before `--apply` runs. Under the OLD gate that value is truthy => the re-point is skipped => upstream stays `origin/seat/<n>@s2` and the new test `test_apply_repoints_preseeded_upstream` fails. Under the fix the gate re-points to `origin/post/<n>@s2` and the test passes. So the test FAILS before the fix and PASSES after.

Inverted the old wrong-behaviour assert: `test_apply_remote_ref_deleted_when_remote_present` became `test_apply_remote_ref_survives_when_remote_present` - after --apply, `git ls-remote origin refs/heads/seat/<n>@s2` is NON-empty.

Delete-old proof: `_migrate_with_origin` runs a full --apply (so the tree is migrated and upstreams read origin/post/<n>@s2) leaving the old seat refs on origin. `test_delete_old_removes_old_remote_refs_only_after_gate_green` proves --delete-old then clears them; `test_delete_old_refuses_names_branch_and_deletes_nothing` sabotages post/b@s2 back to origin/seat/b@s2 and proves --delete-old refuses non-zero naming post/b@s2 and deletes NOTHING (both a and b seat refs survive). Resumability: `test_apply_preseeded_upstream_second_run_resumes_cleanly` re-applies and lands on origin/post/<n>@s2 cleanly.

The real-tree dry-run (the only safe mode) confirms --apply no longer IMPLIES the delete and the plan lists the upstream step.

Judgement call: I took the parent's default reading - deletion lives in `post-rename --delete-old` (NOT delegated to branch-reshuffle --delete-old, which targets LEGACY alias branches under a different grammar), because the parent brief was explicit that post-rename --delete-old is "the ONLY path" and must self-gate on the upstream. branch-reshuffle --delete-old remains free to pick up any lingering seat/*@s2 as a legacy alias afterwards as a second net.

## Agent Notes
post-rename --apply re-points every preseeded upstream to origin/post/<n>@s2 (gate==origin/new, rc-honest), deletes no old remote, --delete-old self-gated last step; 19+30 tests green, real-tree dry-run safe

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-454c3e1e, L4.316). Accepted proved, neither promoted nor demoted. The instruction said (node brief, KID A+B): "after git branch -m, set the upstream to origin/<new> whenever _post_rename_upstream(repo, new) != origin/<new>; _post_rename_upstream returns None on a non-zero git returncode and never the literal <b>@{upstream}" and "step 6 (cli.py:2258) stops deleting origin/seat/<n>@s2; deletion happens only under --delete-old and only as the LAST step, after the upstream gate reads green for every renamed branch". What the machine actually does, read from the built bytes and re-run in the parent tree: cli.py:2034-2036 returns "" on rc!=0; cli.py:2286 is now `if _post_rename_upstream(repo, new_b) == f"origin/{new_b}": continue`; step 6 (cli.py:2255-2260) pushes new-only; _post_rename_delete_old (cli.py:2309-2338) gates on `got != want` for EVERY job before deleting anything, and refuses naming the branch. Parent re-ran `pytest test_post_rename.py -q` -> 19 passed and `pytest test_cli.py test_branch_reshuffle.py -q` -> 30 passed, and `cli.py post-rename --dry-run` on the REAL tree prints three `git push origin post/<n>@s2` lines with NO `--delete seat/...`, then the NOTE line, then `dry-run: nothing changed`. The near miss this review rules out: a fragment that flips the old assert to `has_old != ""` while leaving the delete in --apply would satisfy the words "deletes no old remote name" on the fixture it was run on and still delete on the live box; ruled out because the parent read the push loop and the note line rather than the report. The second near miss: keeping the truthy gate and only making the helper rc-honest still skips a branch whose carried upstream is `origin/seat/<n>@s2` (rc=0, truthy, resolvable) -- the == gate is what closes it, and test_apply_repoints_preseeded_upstream seeds exactly that state. Deviation from a standing rule: none.
<!-- THOUGHT:END -->
