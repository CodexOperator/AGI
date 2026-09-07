---
id: hypothesis:l3w4-parent-branch-merge-up
mint_id: b1669b9bf65c46ae88faf1013fb85e5d
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-IV
scaffold_hash: f142db59b92e1804
season: 2
testable_claim: A parent dispatched with --branch runs in its own git worktree on loop/<target-slug>@s<N>, its kids edit only that worktree, its iteration commit lands on that branch, and season.py merge-up merges it --no-ff into season/sN only when the full suite is green on the merged tree, so two parents whose kids edit the same file run at once without touching each other's bytes; proved by red-first tests plus a rehearsal-repo run of two concurrent dispatches on rotate.py-editing briefs merged up green.
thought_session: L3.23
title: Per-parent branch with seat-managed merge upward
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-parent-branch-merge-up

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
CLAIM
A parent dispatched with `--branch` runs in its own git worktree on `loop/<target-slug>@s<N>` under `.agi/worktrees/<agent>/`; its kids edit only that worktree; the parent's one iteration commit lands on that branch; and a merge-up step (`season.py merge-up <branch>`, run by the seat that owns the season) merges it `--no-ff` into `season/sN` only when the full suite is green on the merged tree. Two parents whose kids edit the same file then run at once without touching each other's bytes.

WHY
Owner, 2026-09-07 ~14:40 UTC, verbatim: "eventually we just need to implement a per-parent branch properly so we can let a lot more of them run concurrently via our seat system managing merges upward to the main season branch." Today kids edit the live tree on `season/s2`, so concurrency is bounded by file overlap: `rotate.py` sits in six wave-4 briefs and `brief.py` in four, and Belam IV measured 2 to 3 parents per batch. HANDOFF §6 item 7 already decided that branches mirror the ladder (parent = `loop/<goal>@s<N>`, short-lived; grid node refs are branch-blind, so `grid.py commit --all` runs on `season/*` or master only) and item 8 forbids rebase. Nothing implements the parent branch for a dispatched parent.

FILES
extensions/agi/bin/dispatch.py :: main() spawn path (worktree creation before the spawn, child cwd, `AGI_TREE_PROJECT_ROOT` = worktree)
extensions/agi/bin/locations.py :: find_project_root (a worktree carries its own `.agi/`; nearest wins already)
extensions/agi/bin/spawn_budget.py :: budget dir (must resolve to the MAIN checkout via `git rev-parse --git-common-dir`, never per-worktree, or the tree-wide bound silently splits)
extensions/agi/bin/send.py :: comms root (same: main checkout)
extensions/agi/bin/season.py :: new `merge-up` subcommand (or extensions/agi/bin/merge_up.py)
extensions/agi/bin/grid.py :: the off-season guard already refuses `commit --all` on a loop branch
extensions/agi/tests/test_dispatch.py, test_season.py, test_spawn_budget.py

DESIGN
`git worktree add .agi/worktrees/<agent> -b loop/<slug>@s<N> season/sN`; the child's cwd and `AGI_TREE_PROJECT_ROOT` are the worktree; `.agi/sessions/` is gitignored so the worktree gets its own iteration dir, but the spawn-budget dir, the comms root and the meter pin dir resolve to the main checkout. `merge-up`: from the main checkout `git merge --no-ff loop/<slug>@s<N>`, run the suite, on red abort the merge and report the branch name; on green `git worktree remove` and delete nothing else. `grid.py commit --all` runs after the merge, on the season branch, as today.

TESTS (red-first)
test_dispatch_branch_creates_worktree_and_branch (dry-run prints the worktree path and branch); test_child_env_points_at_worktree; test_budget_dir_shared_across_worktrees; test_merge_up_refuses_on_red_suite (fake suite); test_merge_up_merges_no_ff_and_removes_worktree; test_merge_up_never_rebases.

GATE
In a rehearsal repo, two dispatches on briefs that both edit `rotate.py` run at once, each on its own branch, neither sees the other's edits; `merge-up` lands both on the season branch with the suite green; `git log` shows merge commits and no rewritten hashes; full suite green; no live spawn against this repo.

NOT IN SCOPE
Which seat owns merging and its rotation (`l3w4-quorum-reviews`, seats.md `rotated_by`); CC-harness worktrees (same mechanism, verify after pi); grid session refs; conflict resolution beyond "report and leave the branch".

SOURCE
Owner message to Belam IV, 2026-09-07 ~14:40 UTC (HANDOFF §6 item 19); HANDOFF §6 items 7 and 8; SKILL.md "Branches mirror the ladder".
