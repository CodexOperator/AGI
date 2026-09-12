---
id: experiment:a00-222e8a6b-f4c7cd
mint_id: 541a138cddb14157a543a71f6ffffa84
type: experiment
parents:
  - hypothesis:l4-the-reshuffle-plans-the-final-town-first-tree-from-the-town-tuples-and-the-mirror-line-lands-inert
next_edges: []
confidence: 0.85
edited_by: a00-b1d92d36
evidence_runs:
  - experiment:a00-222e8a6b-f4c7cd
loop: hypothesis:l4-the-reshuffle-plans-the-final-town-first-tree-from-the-town-tuples-and-the-mirror-line-lands-inert@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a283ee073bdc1c7b
season: 2
title: A00 222e8a6b f4c7cd
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-222e8a6b-f4c7cd

## Experiment

L4.334 — implemented the v3 APPLY execution in the branch-reshuffle region of
`extensions/agi/bin/cli.py`, ran from the `--apply` tail, and proved it on the
tmp fixture (never the live tree).

What was there (Kid A, experiment:a00-35abe797-d129d3): `_rs_v3_run` ALREADY
carried the apply logic (branch create/push, post renames, worktree re-points)
but the `--apply` tail never called it with `dry=False` — it printed
"planning-only this round". This kid wired it in and made it provable.

Changes (cli.py, branch-reshuffle region only):
1. `--apply` tail now calls `_rs_v3_run(repo, root, kinds, False, has_origin)`
   AFTER the v2 renames (rc-honest: a failed git run returns 1 and names the
   failed command; no --force; no live tree).
2. `_reshuffle_worktrees` was FILTERED through `_reshuffle_canonical`, which
   drops v3 post-source branches (`season<N>/posts/<p>` — kind `post`, not a
   legacy alias), so a worktree on one could never be re-pointed. Broadened to
   return EVERY tracked worktree; each caller matches via its OWN rename map
   (v2 keys on alias jobs, v3 matches the old post source), so both callers
   stay correct.
3. `git branch --unset-upstream <new>` on a branch that ALREADY has no
   upstream is a HARD git error (rc 128 "has no upstream information"); guarded
   it on `_post_rename_upstream(repo, new)` — only run it when the renamed
   branch carries one.
4. `_rs_town_set` now returns a `declared` flag: True for the town-* path and
   a ladder with an explicit `towns:` list, False only for the degenerate
   `["core"]` floor (a graph with NO town config). `_rs_v3_run` is INERT under
   `--apply` on an undeclared set (prints a notice, mutates nothing) — the v2
   migration is the whole apply surface for a town-less graph. This is what
   keeps the v2 suite (a town-less fixture) green AND preserves the
   delete-old B2 upstream gate: v3 posts end LOCAL with NO upstream by
   contract, which the v2 gate would read as "unpointed" and refuse.

Proof — new `test_v3_apply_creates_trunk_pairs_renames_posts_locally_and_
repoints` (test_branch_reshuffle_v3.py): builds a town-node fixture with two
linked worktrees ON the v3 post sources and the default checkout moved off
master, runs `--dry-run` then `--apply --kinds main,posts,towns`, and asserts:
  * refs/heads after == before | {6 trunk-pair creates} | {2 renamed post
    mains} MINUS {2 old post sources} (for-each-ref), and each new trunk
    points at its planned source tip (rev-parse);
  * both linked worktree HEADs follow the renamed post main;
  * each renamed local post branch has NO upstream (`@ {u}` fails).

The "v2 + v3 suite green" requirement holds: the full v2 + v3 files pass
(46 passed in test_branch_reshuffle.py + test_branch_reshuffle_v3.py). The v2
fixtures are town-less, so the v3 apply is inert there and the pre-existing
v2 apply/delete-old assertions stay true unchanged.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py extensions/agi/tests/test_branch_reshuffle_v3.py -q
46 passed

$ python3 -m pytest extensions/agi/tests/test_branch_reshuffle_v3.py -q -k v3_apply
1 passed, 15 deselected

$ python3 -m pytest extensions/agi/tests/test_cli.py extensions/agi/tests/test_commands.py extensions/agi/tests/test_branches.py -q
122 passed
```

--apply was NOT run against the live tree (live invariant: no live push, no
live ref change).

## Agent Notes
Implemented the v3 APPLY in the branch-reshuffle --apply tail: call _rs_v3_run(dry=False) after the v2 renames; broadened _reshuffle_worktrees so v3 post-source worktrees are reachable; guarded --unset-upstream (git rc128 on no-upstream); gated v3 apply inert on a graph with NO declared town set (keeps v2 suite + delete-old B2 gate true). Fixture proof: --apply --kinds main,posts,towns yields exactly the planned refs, worktrees follow renamed post mains, renamed posts have no upstream. v2+v3 suite 46 passed. Live apply NOT run (forbidden by scope).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (L4.334): accepted lean_proved:85. (1) WHAT THE BRIEF SAID: close kid A gap (1) -- implement the v3 --apply for kinds main/towns/posts from the --apply tail, with a fixture asserting the planned refs, worktree HEAD follow, and no upstream on the renamed local posts. (2) WHAT THE MACHINE ACTUALLY DOES: cli.py:3607 now calls `_rs_v3_run(repo, root, kinds, False, has_origin)` in the --apply tail after the v2 renames; cli.py:2551 _reshuffle_worktrees no longer pre-filters by _reshuffle_canonical so a worktree on a v3 post source is reachable; cli.py:3196 guards `git branch --unset-upstream` on _post_rename_upstream so a branch with no upstream is not a hard git error. The parent re-ran the broad touched set (test_branch_reshuffle{,v3}.py, test_branches{,v3}.py, test_branch_spelling_grep.py, test_towns.py, test_no_literal_town.py, test_cli.py): 176 passed in 44.97s, and read the new test test_v3_apply_creates_trunk_pairs_renames_posts_locally_and_repoints -- it builds two linked worktrees ON the v3 post sources and asserts the exact for-each-ref set, every new trunk tip via rev-parse, both worktree HEADs following, and `@{u}` FAILING on each renamed post. (3) THE NEAR MISS: a test that only asserts the six new trunk names EXIST would satisfy "apply happened" and lose the exact-set claim (the old post sources must be GONE); this test asserts equality against before|new-minus-old. Likewise an --unset-upstream run unconditionally would pass on a branch that had an upstream and crash rc128 on one that did not; the guard keeps the LOCAL-no-upstream contract true on both. (4) DEVIATION DECLARED AND ACCEPTED: the kid made v3 --apply INERT on a graph with NO declared town set (no town:* node and no ladder towns: list), because a town-less fixture would otherwise guess a tree and the v2 suite plus the delete-old B2 upstream gate depend on v2-only apply. The live tree declares towns: in ladder.md so the live apply surface is unchanged; this is a defensible narrowing, recorded here rather than silently. (5) NOT DONE: region B (loops prune/rename/HOLD) and region C (crons grid_sync mirror) untouched; real-tree proof (b) re-run by the parent but loop lines absent. That is why 85 and not proved.
<!-- THOUGHT:END -->
