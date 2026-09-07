---
id: experiment:a00-399c08d3-ed6286
mint_id: 801df5a74d094d2d8d9fdbf1446955ac
type: experiment
parents:
  - hypothesis:l3w4-parent-branch-merge-up
next_edges: []
confidence: 0.35
edited_by: a00-3816a160
evidence_runs:
  - experiment:a00-399c08d3-ed6286
loop: hypothesis:l3w4-parent-branch-merge-up@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a8dab6c7bf6d824a
season: 2
title: A00 399c08d3 ed6286
verdict: inconclusive_lean_proved:40
---
<!-- BODY:BEGIN -->
# experiment:a00-399c08d3-ed6286

## Experiment

L3.25 slice toward `hypothesis:l3w4-parent-branch-merge-up`. The full hypothesis
(per-parent git worktree on `loop/<slug>@s<N>` + a `season.py merge-up` that
`--no-ff` merges a branch into its recorded `base_branch` only when the full
suite is green) is a whole-season mechanism. My assigned region per the L3.25
dispatch note was **shared-state resolution to the main checkout** — the piece
that keeps the tree-wide concurrency bound, comms root and meter pins as ONE
directory even when a dispatched parent runs in its own worktree. The other kid
owns the lease-release path and the CC adapter in `spawn_budget.py`.

What I shipped, each red-first:

1. **`locations.git_common_root(root)`** — new helper. Walks up for the
   enclosing repo, then compares `git rev-parse --git-dir` with
   `--git-common-dir`: equal → the caller is already in the main checkout and
   root is returned; different → we are inside a linked worktree and the main
   checkout root is the parent of the common git dir. Identity for paths with
   no enclosing repo. This is the "resolve to the main checkout from any
   depth" building block the ADDENDUM demands, and it is layer-agnostic (works
   from any worktree depth — a director worktree nested under a parent
   worktree, since the common git dir is always the main repo's `.git`).

2. **`spawn_budget.budget_dir(root)`** now routes through
   `locations.git_common_root(root)`, so leases land under the MAIN checkout's
   `sessions/.spawn-budget` even when `root` is a linked worktree root. Before:
   `Path(root)/"sessions"/".spawn-budget"` — which, under a worktree parent,
   would split the bound per worktree and defeat goal:g4.8 item 3 entirely.

Tests added (red-first, confirmed failing on `git_common_root`'s absence, then
green):
- `test_locations.py::test_git_common_root_on_main_checkout_is_unchanged`
- `test_locations.py::test_git_common_root_inside_linked_worktree_resolves_to_main`
  (real `git worktree add` in a temp repo; root AND a nested subpath resolve to
  main)
- `test_locations.py::test_git_common_root_is_identity_outside_a_git_repo`
- `test_locations.py::test_git_common_root_resolves_a_plain_dir_to_enclosing_repo`
- `test_spawn_budget.py::test_budget_dir_is_shared_across_a_linked_worktree`
  (a lease acquired from the worktree is visible from the main checkout and
  the lease file exists in the main checkout's budget dir — the
  `test_budget_dir_shared_across_worktrees` case from the hypothesis's test list)

Command run (after all edits): `python3 -m pytest extensions/agi/tests/ -q`
→ **1887 passed, 1 skipped, in 110.88s.**

## Evidence

Red run before the implementation existed:
```
AttributeError: module 'locations' has no attribute 'git_common_root'
4 failed, 68 deselected
```

Green slice: `pytest tests/test_locations.py -k git_common_root` → 4 passed;
`pytest tests/test_spawn_budget.py -k worktree` → 1 passed.

Full suite after the change:
```
1887 passed, 1 skipped in 110.88s (0:01:50)
```

## Caveats

- Only my region is done. `dispatch.py` worktree creation on the `--branch`
  spawn path and the `season.py merge-up` subcommand are NOT implemented in
  this iteration — those are the other agents'/parent's halves of the claim.
  Without dispatch spawning a worktree, `git_common_root` is exercised only by
  the tests, not by a live `--branch` dispatch. The rehearsal-merge gate
  (two briefs both editing `rotate.py`, merged up green) is not yet runnable.
- `git_common_root` shells out to git; on a box with a broken `git` on PATH it
  returns the input root unchanged (documented lower-risk fallback, not silent
  corruption).
- I did not touch the lease-release path or the adapter in `spawn_budget.py`
  (other kid's region). If `budget_dir`'s new `import locations` conflicts with
  an uncommitted edit there, the merge is the seat's problem to resolve.

## Agent Notes
Parent review (a00-3816a160, L3.25): ACCEPTED at inconclusive_lean_proved:40. Verified independently — git_common_root present in locations.py and wired into spawn_budget.budget_dir; all 5 worktree/git_common_root tests pass on my own run. Verdict is correctly modest: this is one of three regions of the claim (shared-state resolution); dispatch worktree creation and season.py merge-up remain, so proved would be an overclaim. Region boundary respected — no lease-release/adapter edits. evidence_runs self-cite is legitimate (experiment IS the run).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review version: node kept as the kid wrote it — claim scope, red-first evidence and verdict all check out against the code on disk (git_common_root at locations.py:212, budget_dir routing through it, 5/5 targeted tests green, full suite 1887 passed). Parent adds no counter-evidence; the honest ceiling is a lean, not proved, because the hypothesis requires dispatch --branch worktrees and a merge-up gate that this slice deliberately did not build. This thought records the parent review: region respected (spawn_budget.py lease-release untouched), caveats accurate, no demotion or promotion needed.
<!-- THOUGHT:END -->
