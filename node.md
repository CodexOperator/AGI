---
id: experiment:a00-2dbbe087-39b905
mint_id: 8c0a08f798b142acb4884d06909a6129
type: experiment
parents:
  - hypothesis:l4-reshuffle-apply-gates-on-origin-new-and-both-delete-old-flags-honour-dry-run
next_edges: []
confidence: 0.9
edited_by: a00-de4869f3
evidence_runs:
  - experiment:a00-2dbbe087-39b905
loop: hypothesis:l4-reshuffle-apply-gates-on-origin-new-and-both-delete-old-flags-honour-dry-run@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0604465afedc0a7e
season: 2
title: A00 2dbbe087 39b905
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2dbbe087-39b905

## Experiment

KID A of 2 (region A only). Built the claim — the `branch-reshuffle --apply`
pass must (A1) re-point a branch that CARRIED `origin/<old>` through
`git branch -m` onto `origin/<new>`, and (A4) treat `master` as ADD-ONLY
(never `git branch -m`'d). Sibling KID B owns the `--delete-old` block and
`--dry-run` deferred-body reads; untouched.

**A1 — carried-upstream re-point.** `extensions/agi/bin/cli.py`, the `--apply`
upstream block (previously ~L2788). The old TRUTHY gate
`if not _post_rename_upstream(repo, new):` ran the re-point ONLY when the
upstream was unset — but `git branch -m old new` CARRIES `origin/<old>`
(truthy), so a branch tracking the legacy remote name was NEVER re-pointed.
Made the gate byte-for-byte the post-rename form (cli.py:2306):
`if _post_rename_upstream(repo, new) == f"origin/{new}": continue`, then run
`git branch --set-upstream-to origin/<new> <new>` and CHECK ITS RETURNCODE
(non-zero => ERR + return 1). Comment names the carried-upstream case.

**A2 — fixture precondition.** `test_branch_reshuffle.py` `_build_repo`
pushed legacy branches WITHOUT `-u`, so nothing tracked `origin/<old>` and the
truthy gate tested green. Seeded every legacy branch tracking its `origin/<old>`
(`git branch --set-upstream-to origin/<old> <old>` after the fetch); `_master_repo`
seeds `master` tracking `origin/master` too.

**A3 — falsifier test.** Added `test_apply_repoints_a_branch_that_carried_origin_old`:
asserts `season/s2@{upstream}` is `origin/season/s2` BEFORE apply and that
`season2/main@{upstream}` is `origin/season2/main` AFTER. FAILS under the
truthy gate; PASSES under A1.

**A4 — master add-only in --apply.** Added a `master` job branch in the apply
loop: a job whose old name is `master` is NEVER `git branch -m`'d; the new name
(`season1/main`) is pushed FROM master's tip (`git push origin master:season1/main`)
and master stands. Added `test_apply_keeps_master_standing_and_pushes_new_name_from_its_tip`
on `_master_repo`: local `master` present + no local `season1/main` after apply,
`origin/season1/main` tip == master tip, `master@{upstream}` == `origin/master`.

Never ran `--apply`/`--delete-old` against the real tree — fixtures/tmp only.

## Evidence

PROOF — exact commands and output:

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py -q
tier-gate: phantom running record ... (dead) -- skipped
..................                                                       [100%]
18 passed in 9.26s
```

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_cli.py -q
tier-gate: phantom running record ... (dead) -- skipped
...................                                                      [100%]
19 passed in 1.02s
```

FALSIFIER (A1 reverted to the truthy gate `if not _post_rename_upstream`, leaf-swap
then restored):

```
$ python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py -q -k carried_origin_old
E         ?               -----
E         + origin/season/s2
E         ?              ++
extensions/agi/tests/test_branch_reshuffle.py:330: AssertionError
1 failed, 17 deselected
```

**The assertion that flips when A1 is reverted:** in
`test_apply_repoints_a_branch_that_carried_origin_old`, the final
`assert up == "origin/season2/main", up` (test_branch_reshuffle.py:330) —
under the truthy gate `season2/main@{upstream}` stays the carried
`origin/season/s2` and the assert fails. cli.py verified AST-clean after the
leaf-swap restore.

Both suites green on the built bytes; the tree carries ONLY the two intended
edits (cli.py, test_branch_reshuffle.py) plus this node.

## Agent Notes
KID A: --apply carried-upstream re-point (A1 truthy->==origin/new gate + rc check), fixture seeds origin/<old> tracking (A2), falsifier test (A3), master add-only in --apply (A4). 18+19 tests green; falsifier confirmed failing under truthy gate.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-de4869f3, L4.320). (1) The brief said: cli.py:2788 is the reshuffle --apply upstream gate and it is TRUTHY, so a branch carrying origin/<old> is never re-pointed; make it identical to the post-rename gate (:2306), seed the fixture with -u, and make master add-only in the --apply pass. (2) Measured on the built bytes: cli.py now reads, in the --apply loop, `if _post_rename_upstream(repo, new) == f"origin/{new}": continue` then runs the set-upstream with its returncode checked (cli.py:2860-2870), a job `old == "master"` is pushed as `origin master:<new>` and `continue`s before any `git branch -m` (cli.py:2826-2838), and test_branch_reshuffle.py:_build_repo seeds `git branch --set-upstream-to origin/<old> <old>` for every legacy branch (test_branch_reshuffle.py:97-103). I re-ran the three named files myself: 61 passed. (3) Near miss: a gate that reads `if _post_rename_upstream(repo, new): continue` is still truthy and would skip a branch tracking origin/<old>; and a master skip placed AFTER `git branch -m` would satisfy "master stays" only when the rename failed. Both are excluded here by reading the exact line, not the prose. (4) Deviation: none; scope held to region A. Weakness: the falsifier was verified by the kid persisting a leaf-swap, not by a durable revert test, so the flip is trusted from a pasted transcript rather than reproducible from the repo in one flag.
<!-- THOUGHT:END -->
