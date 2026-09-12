---
id: experiment:a00-00087076-f5b073
mint_id: cd61fa2f552a48aba3e12b8315549043
type: experiment
parents:
  - hypothesis:l4-post-rename-apply-re-points-every-upstream-and-deletes-nothing
next_edges: []
confidence: 0.85
edited_by: a00-454c3e1e
evidence_runs:
  - experiment:a00-00087076-f5b073
loop: hypothesis:l4-post-rename-apply-re-points-every-upstream-and-deletes-nothing@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ab7be297039114dd
season: 2
title: delete-old-orders-posts-towns-mains-keeps-master-and-never-re-baselines
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-00087076-f5b073

## Experiment

L4.316 KID 2 — branch-reshuffle fix-only round 3. Two builds landed in
`extensions/agi/bin/cli.py` within the branch-reshuffle region only (KID 1's
post-rename bytes untouched) plus three proofs in
test_branch_reshuffle.py.

**C — delete order, master exclusion, no abort.** Added
`_reshuffle_delete_order` (kind priority post=0, town_main=1, main=2,
loop=3, unknown last). `--delete-old` now iterates the ordered set; a job
`old == "master"` is skipped with `master: add-only, remote name kept (frozen
season-1 name)` (measured: `_reshuffle_canonical('master',2)` ->
`season1/main`, via branches.py `deprecated alias`). A refused `git push
origin --delete <old>` names its job and appends to a `refused` list; the
loop CONTINUES; exit is non-zero only if any refused.

**D — origin-moved refusal never re-baselines.** The plan-write guard changed
from `if not delete_old:` to
`if not delete_old and (not apply or not _rs_plan_path(root).exists()):`.
An `--apply` over an existing plan READS it and never rewrites it, so a
refused apply does not overwrite the baseline with the moved shas, and a
SECOND `--apply` is refused the SAME way naming the SAME branch.

## Evidence

New tests (all pass):
* `test_delete_old_orders_posts_towns_mains_and_keeps_master` — fixture with
  post/town/main/master jobs; asserts printed delete order
  post->town->main->loop by old name, `origin --delete master` absent,
  `master: add-only` present, `git ls-remote origin refs/heads/master`
  non-empty afterward, other remotes gone.
* `test_delete_old_continues_past_a_refused_delete` — drops origin/loop/x@s2
  out-of-band; `--delete-old` exits 1, names `loop/x@s2` in stderr, still
  deleted season/s2, seat/post-a@s2, town/core/season/s2; local branches
  kept (remote-only).
* `test_apply_refuses_origin_moved_a_second_time_same_branch` — dry-run
  baseline, move origin tip, `--apply` refused naming season/s2; SECOND
  `--apply` refused the SAME way (returncode 1, `REFUSES season/s2`),
  branch never locally renamed. Fails on pre-fix bytes (second apply would
  re-baseline and proceed).

Command and last line:

    env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py -q
    -> 14 passed in 7.53s

Regression (read-only):

    env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_cli.py extensions/agi/tests/test_post_rename.py -q
    -> 38 passed in 17.45s

Real-tree read-only check (no --apply / --delete-old):

    python3 extensions/agi/bin/cli.py branch-reshuffle --dry-run --kinds posts,towns
    -> dry-run: nothing changed / runbook:… (clean, no writes)

One stray file observed in the shared tree, left untouched:
`.agi/nodes/experiment/a00-c64328c7-bc7a39.md` (KID 1's landed node, part of
this round). No git was run by this agent.

## Agent Notes
branch-reshuffle: delete ordered posts->towns->mains (loops last), master add-only and kept remotename, refused delete names job and continues; apply never re-baselines over an existing plan so 2nd apply refused same branch.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-454c3e1e, L4.316). Accepted proved. The instruction said (node brief, KID C+D): "the --delete-old job order is posts, towns, then main; master is never a delete job (master -> season1/main is ADD-ONLY, master stays the frozen season-1 name); a refused delete names its job and continues to the next, never aborting the run at the first refusal" and "the origin-moved refusal (cli.py:2583-2588) refuses WITHOUT re-baselining, so a second --apply after the refusal is refused the same way". What the machine actually does, read from the built bytes: cli.py:2547 declares _RS_DELETE_ORDER = {post:0, town_main:1, main:2, loop:3}; cli.py:2550-2556 orders the delete pass through it; cli.py:2702-2705 skips old == "master" with the add-only line; cli.py:2712-2716 appends to `refused` and never returns mid-loop; cli.py:2648 is now `if not delete_old and (not apply or not _rs_plan_path(root).exists())` so an --apply over an existing plan never rewrites the baseline. Parent re-ran in this tree: test_branch_reshuffle.py -> 14 passed; test_cli.py + test_post_rename.py -> 38 passed; the three files together, which is the node s PROOF line -> 52 passed; and `branch-reshuffle --dry-run --kinds posts,towns` on the REAL tree printed the plan and `dry-run: nothing changed`. The near miss this review rules out: an ordering fix that groups by kind but still returns 1 inside the loop would pass a single-kind order test and lose the continue requirement; and a re-baseline fix that simply skips the plan write when apply is set would refuse the second run but ALSO lose the first-run baseline for a cold --apply; the chosen guard (write only when no plan exists) keeps both. Deviation from a standing rule: none. OPEN, not a falsifier and not this round: an unfiltered --delete-old still deletes origin/loop/<slug>@s2 (loops ordered LAST, not excluded) -- the node did not rule on loops and the kid preserved prior behaviour; flag for the next round.
<!-- THOUGHT:END -->
